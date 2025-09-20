import json
import sys
import time
from urllib import request, error


BASE_URL = "http://localhost:8000/api"


def http_post(path, body, token=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, data=data, headers=headers, method="POST")
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get(path, token=None):
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, headers=headers, method="GET")
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def choose_params(input_schema):
    params = {}
    for key, typ in (input_schema or {}).items():
        if typ == "string":
            if "email" in key:
                params[key] = "test@example.com"
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
    try:
        login = http_post(
            "/auth/login/",
            {"username": "admin", "password": "admin123"},
        )
        access = login.get("access_token")
        refresh = login.get("refresh_token")
        if not access or not refresh:
            print("Login failed: missing tokens", file=sys.stderr)
            sys.exit(1)

        tasks = http_get("/tasks/", token=access)
        results = tasks.get("results", [])
        if not results:
            print("No tasks available", file=sys.stderr)
            sys.exit(1)
        task = results[0]
        task_id = task["id"]
        params = choose_params(task.get("input_schema", {}))

        schedule = http_post(
            "/schedules/",
            {
                "task_definition": task_id,
                "cron_expression": "*/5 * * * *",
                "parameters": params,
                "is_active": True,
            },
            token=access,
        )
        schedule_id = schedule.get("id")
        if not schedule_id:
            print("Schedule creation failed", file=sys.stderr)
            print(json.dumps(schedule, indent=2))
            sys.exit(1)

        _ = http_get(f"/schedules/{schedule_id}/", token=access)

        toggle = http_post(f"/schedules/{schedule_id}/toggle_active/", {}, token=access)
        if "is_active" not in toggle:
            print("Toggle failed", file=sys.stderr)
            sys.exit(1)

        search = http_post(
            "/schedules/search/",
            {"filters": {"is_active": True}, "ordering": ["-created_at"], "page_size": 5},
            token=access,
        )
        if "results" not in search:
            print("Search failed", file=sys.stderr)
            sys.exit(1)

        logs = http_get(f"/schedules/{schedule_id}/logs/", token=access)
        if not isinstance(logs, dict):
            print("Logs fetch failed", file=sys.stderr)
            sys.exit(1)

        refreshed = http_post("/auth/refresh/", {"refresh": refresh})
        if not refreshed.get("access"):
            print("Token refresh failed", file=sys.stderr)
            sys.exit(1)

        print("E2E test completed successfully")
    except error.HTTPError as e:
        print("HTTPError:", e.code, e.reason, file=sys.stderr)
        try:
            print(e.read().decode("utf-8"), file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


