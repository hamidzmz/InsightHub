import json
import random
import string
import sys
import time
from urllib import request, error


BASE_URL = "http://localhost:8000/api"


def rnd_suffix(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def http_request(method: str, path: str, token: str | None = None, body: dict | None = None, expect_status: int | None = 200):
    url = f"{BASE_URL}{path}"
    headers = {}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=15) as resp:
            payload = resp.read().decode("utf-8")
            if expect_status is not None and resp.status != expect_status:
                print(f"Unexpected status {resp.status} for {method} {path}", file=sys.stderr)
                print(payload, file=sys.stderr)
                sys.exit(1)
            return json.loads(payload) if payload else None
    except error.HTTPError as e:
        payload = e.read().decode("utf-8")
        if expect_status is not None and e.code != expect_status:
            print(f"HTTPError {e.code} for {method} {path}", file=sys.stderr)
            print(payload, file=sys.stderr)
            sys.exit(1)
        try:
            return json.loads(payload)
        except Exception:
            return {"raw": payload}


def http_get(path: str, token: str | None = None, expect_status: int | None = 200):
    return http_request("GET", path, token, None, expect_status)


def http_post(path: str, body: dict, token: str | None = None, expect_status: int | None = 200):
    return http_request("POST", path, token, body, expect_status)


def http_put(path: str, body: dict, token: str | None = None, expect_status: int | None = 200):
    return http_request("PUT", path, token, body, expect_status)


def http_patch(path: str, body: dict, token: str | None = None, expect_status: int | None = 200):
    return http_request("PATCH", path, token, body, expect_status)


def http_delete(path: str, token: str | None = None, expect_status: int | None = 204):
    return http_request("DELETE", path, token, None, expect_status)


def choose_params(input_schema: dict) -> dict:
    params: dict = {}
    for key, typ in (input_schema or {}).items():
        if typ == "string":
            if "email" in key:
                params[key] = "user@example.com"
            elif "source" in key:
                params[key] = "/tmp"
            elif "destination" in key:
                params[key] = "/backup"
            elif "table" in key:
                params[key] = "logs"
            else:
                params[key] = "sample"
        elif typ == "integer":
            params[key] = 1
        elif typ == "boolean":
            params[key] = True
        elif typ == "float":
            params[key] = 1.0
    return params


def main():
    # Admin login for later RBAC checks
    admin_login = http_post("/auth/login/", {"username": "admin", "password": "admin123"})
    admin_access = admin_login.get("access_token")
    if not admin_access:
        print("Admin login failed", file=sys.stderr)
        sys.exit(1)

    # Register regular user
    uname = f"user_{int(time.time())}_{rnd_suffix()}"
    reg = http_post(
        "/auth/register/",
        {
            "username": uname,
            "email": f"{uname}@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
        },
        expect_status=201,
    )
    assert reg.get("user", {}).get("username") == uname

    # Login regular user
    login = http_post(
        "/auth/login/", {"username": uname, "password": "securepassword123"}
    )
    access = login.get("access_token")
    refresh = login.get("refresh_token")
    assert access and refresh

    # Profile
    profile = http_get("/auth/profile/", token=access)
    assert profile.get("username") == uname

    # Refresh token
    refreshed = http_post("/auth/refresh/", {"refresh": refresh})
    assert refreshed.get("access")

    # Tasks list and available
    tasks = http_get("/tasks/", token=access)
    assert "results" in tasks and tasks["results"]
    first_task = tasks["results"][0]
    task_id = first_task["id"]
    available = http_get("/tasks/available/", token=access)
    assert "results" in available

    # Create up to 5 active schedules
    input_schema = first_task.get("input_schema", {})
    valid_params = choose_params(input_schema)
    created_ids = []
    for _ in range(5):
        sc = http_post(
            "/schedules/",
            {
                "task_definition": task_id,
                "cron_expression": "*/5 * * * *",
                "parameters": valid_params,
                "is_active": True,
            },
            token=access,
            expect_status=201,
        )
        created_ids.append(sc["id"])

    # 6th active schedule should fail
    sixth = http_post(
        "/schedules/",
        {
            "task_definition": task_id,
            "cron_expression": "*/5 * * * *",
            "parameters": valid_params,
            "is_active": True,
        },
        token=access,
        expect_status=400,
    )
    assert "Regular users cannot have more than 5 active jobs" in json.dumps(sixth)

    # Invalid cron expression
    bad_cron = http_post(
        "/schedules/",
        {
            "task_definition": task_id,
            "cron_expression": "invalid cron",
            "parameters": valid_params,
            "is_active": True,
        },
        token=access,
        expect_status=400,
    )
    assert "Invalid cron expression" in json.dumps(bad_cron)

    # Invalid parameter types + unknown keys
    wrong_params = {k: ("not_a_number" if t == "integer" else 123) for k, t in input_schema.items()}
    wrong_params["unknown_param"] = "x"
    bad_params = http_post(
        "/schedules/",
        {
            "task_definition": task_id,
            "cron_expression": "*/5 * * * *",
            "parameters": wrong_params,
            "is_active": True,
        },
        token=access,
        expect_status=400,
    )
    bad_params_text = json.dumps(bad_params)
    assert (
        "not a valid parameter" in bad_params_text
        or "must be" in bad_params_text
        or "Validation failed" in bad_params_text
    )

    # Pagination defaults and limits (regular user)
    listed = http_get("/schedules/", token=access)
    assert "results" in listed and len(listed["results"]) <= 10
    listed7 = http_get("/schedules/?page_size=7", token=access)
    assert len(listed7["results"]) <= 7
    listed_oversize = http_get("/schedules/?page_size=999", token=access)
    assert len(listed_oversize["results"]) <= 10

    # Dynamic search with body-provided pagination and ordering
    searched = http_post(
        "/schedules/search/",
        {"filters": {"is_active": True}, "ordering": ["-created_at"], "page_size": 5},
        token=access,
    )
    assert "results" in searched and len(searched["results"]) <= 5

    # Toggle one schedule to inactive and then create one more active (should succeed)
    toggled = http_post(f"/schedules/{created_ids[0]}/toggle_active/", {}, token=access)
    assert toggled.get("is_active") is False
    sc_ok = http_post(
        "/schedules/",
        {
            "task_definition": task_id,
            "cron_expression": "*/10 * * * *",
            "parameters": valid_params,
            "is_active": True,
        },
        token=access,
        expect_status=201,
    )
    new_id = sc_ok["id"]

    # Update schedule (PUT) with valid changes
    upd = http_put(
        f"/schedules/{new_id}/",
        {"cron_expression": "0 0 * * *", "parameters": valid_params, "is_active": True},
        token=access,
    )
    assert upd["cron_expression"] == "0 0 * * *"
    assert "next_run_time" in upd

    # Logs endpoint (shape check)
    logs = http_get(f"/schedules/{new_id}/logs/", token=access)
    assert "results" in logs

    # RBAC: admin sees other users' schedules
    admin_list = http_get("/schedules/", token=admin_access)
    assert any(item.get("user_username") == uname for item in admin_list.get("results", [])) or admin_list.get("count", 0) > len(admin_list.get("results", []))
    # Regular user cannot access other user's schedule detail
    other_uname = f"user2_{int(time.time())}_{rnd_suffix()}"
    http_post(
        "/auth/register/",
        {
            "username": other_uname,
            "email": f"{other_uname}@example.com",
            "first_name": "Other",
            "last_name": "User",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
        },
        expect_status=201,
    )
    other_login = http_post(
        "/auth/login/", {"username": other_uname, "password": "securepassword123"}
    )
    other_access = other_login.get("access_token")
    http_get(f"/schedules/{created_ids[1]}/", token=other_access, expect_status=404)

    # Delete a schedule
    http_delete(f"/schedules/{new_id}/", token=access)

    # Swagger/Redoc reachable
    # schema/docs/redoc reachable
    request.urlopen(f"{BASE_URL}/schema/", timeout=10).read()
    request.urlopen(f"{BASE_URL}/docs/", timeout=10).read()
    request.urlopen(f"{BASE_URL}/redoc/", timeout=10).read()
    
    # Admin pagination behavior
    admin_large = http_get("/schedules/?page_size=150", token=admin_access)
    assert len(admin_large.get("results", [])) <= 100
    admin_search = http_post(
        "/schedules/search/",
        {"filters": {}, "ordering": ["-created_at"], "page_size": 99},
        token=admin_access,
    )
    assert len(admin_search.get("results", [])) <= 99
    
    # Invalid login should fail
    http_post("/auth/login/", {"username": "nosuch", "password": "wrong"}, expect_status=400)

    print("Full E2E suite completed successfully")


if __name__ == "__main__":
    main()


