import requests
import json

BASE_URL = "https://xavier-db-dev-134042435125.us-central1.run.app"

# -------------------------
# Helper for POST requests
# -------------------------
def post_with_debug(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    try:
        res = requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"REQUEST ERROR [{endpoint}]:", str(e))
        raise Exception({
            "error_type": "RequestException",
            "error_msg": str(e),
            "method": "POST",
            "endpoint": endpoint,
            "payload": payload
        })

    if res.status_code != 200:
        # Try to parse JSON response for structured error
        try:
            err_obj = res.json()
        except json.JSONDecodeError:
            err_obj = {"error_msg": res.text}

        print(f"API ERROR [{endpoint}] POST payload:", payload)
        print("RESPONSE:", res.text)

        raise Exception({
            "error_type": err_obj.get("error_type", f"HTTP {res.status_code}"),
            "error_msg": err_obj.get("error_msg", res.text),
            "method": "POST",
            "endpoint": endpoint,
            "payload": payload
        })

    return res.json()

# -------------------------
# API FUNCTIONS
# -------------------------
def query_data(table, limit=100):
    res = requests.get(
        f"{BASE_URL}/query",
        params={"table": table, "limit": limit},
        timeout=5
    )

    if res.status_code != 200:
        try:
            err = res.json()
        except:
            err = res.text
        raise Exception(err)

    return res.json()

def run_quick_query(query_type, **params):
    res = requests.get(
        f"{BASE_URL}/quick_query",
        params={"query_type": query_type, **params}
    )

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()

def update_row(table, row_id, payload):
    res = requests.patch(
        f"{BASE_URL}/{table}/{row_id}",
        json=payload
    )

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()


def create_project(payload):
    return post_with_debug("projects", payload)

def create_sample(payload):
    return post_with_debug("samples", payload)

def create_experiment(payload):
    return post_with_debug("experiments", payload)

def create_run(payload):
    return post_with_debug("sequencing", payload)

def create_seqexp(payload):
    return post_with_debug("seqexp", payload)

def create_file(payload):
    return post_with_debug("files", payload)