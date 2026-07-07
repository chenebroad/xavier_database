import requests
import json

BASE_URL = "https://xavier-db-dev-134042435125.us-central1.run.app"

# -------------------------
# Helpers
# -------------------------
def post_with_debug(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    try:
        res = requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        raise Exception({
            "error_type": "RequestException",
            "error_msg": str(e),
            "method": "POST",
            "endpoint": endpoint,
            "payload": payload
        })

    if res.status_code != 200:
        try:
            err_obj = res.json()
        except json.JSONDecodeError:
            err_obj = {"error_msg": res.text}
        raise Exception({
            "error_type": err_obj.get("error_type", f"HTTP {res.status_code}"),
            "error_msg":  err_obj.get("error_msg", res.text),
            "method":     "POST",
            "endpoint":   endpoint,
            "payload":    payload
        })

    return res.json()


def delete_with_debug(endpoint, row_id):
    url = f"{BASE_URL}/{endpoint}/{row_id}"
    try:
        res = requests.delete(url)
    except requests.exceptions.RequestException as e:
        raise Exception({
            "error_type": "RequestException",
            "error_msg": str(e),
            "method": "DELETE",
            "endpoint": endpoint,
            "id": row_id
        })

    if res.status_code != 200:
        try:
            err_obj = res.json()
        except json.JSONDecodeError:
            err_obj = {"error_msg": res.text}
        raise Exception({
            "error_type": err_obj.get("error_type", f"HTTP {res.status_code}"),
            "error_msg":  err_obj.get("error_msg", res.text),
            "method":     "DELETE",
            "endpoint":   endpoint,
            "id":         row_id
        })

    return res.json()


# -------------------------
# Query / update
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
        except Exception:
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


def run_sql_query(sql):
    res = requests.post(f"{BASE_URL}/sql", json={"sql": sql})
    if res.status_code != 200:
        try:
            err = res.json()
        except Exception:
            err = res.text
        raise Exception(err)
    return res.json()


# -------------------------
# Create
# -------------------------
def create_project(payload):          return post_with_debug("projects", payload)
def create_sample(payload):           return post_with_debug("samples", payload)
def create_subject(payload):          return post_with_debug("subjects", payload)
def create_sample_source(payload):    return post_with_debug("sample_sources", payload)
def create_cohort(payload):           return post_with_debug("cohorts", payload)
def create_cohort_member(payload):    return post_with_debug("cohort_members", payload)
def create_experiment(payload):       return post_with_debug("experiments", payload)
def create_pool(payload):             return post_with_debug("pools", payload)
def create_pool_member(payload):      return post_with_debug("pool_members", payload)
def create_run(payload):              return post_with_debug("sequencing", payload)
def create_flowcell_library(payload): return post_with_debug("flowcell_libraries", payload)
def create_file(payload):             return post_with_debug("files", payload)

# -------------------------
# Delete
# -------------------------
def delete_project(row_id):          return delete_with_debug("projects", row_id)
def delete_sample(row_id):           return delete_with_debug("samples", row_id)
def delete_subject(row_id):          return delete_with_debug("subjects", row_id)
def delete_cohort(row_id):           return delete_with_debug("cohorts", row_id)
def delete_experiment(row_id):       return delete_with_debug("experiments", row_id)
def delete_pool(row_id):             return delete_with_debug("pools", row_id)
def delete_run(row_id):              return delete_with_debug("sequencing", row_id)
def delete_flowcell_library(row_id): return delete_with_debug("flowcell_libraries", row_id)
def delete_file(row_id):             return delete_with_debug("files", row_id)
