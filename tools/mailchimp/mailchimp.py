"""Mailchimp Marketing API wrapper for Stolen Goat.

Auth: API key from .env (MAILCHIMP_API_KEY).
Data centre derived from key suffix (e.g., us1).
"""

import hashlib
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv("C:/ClaudeProjects/pablo/.env")

API_KEY = os.environ["MAILCHIMP_API_KEY"]
DC = API_KEY.split("-")[-1]
BASE_URL = f"https://{DC}.api.mailchimp.com/3.0"
AUTH = ("x", API_KEY)
HEADERS = {"User-Agent": "Pablo/1.0"}

# SG Mailing List
SG_LIST_ID = "6b5b431c5b"


def subscriber_hash(email: str) -> str:
	"""MD5 hash of lowercase email — Mailchimp's subscriber identifier."""
	return hashlib.md5(email.lower().strip().encode()).hexdigest()


def _get(path: str, params: dict | None = None) -> dict:
	"""GET request to Mailchimp API."""
	r = requests.get(
		f"{BASE_URL}{path}",
		params=params,
		auth=AUTH,
		headers=HEADERS,
		timeout=30,
	)
	r.raise_for_status()
	return r.json()


def _post(path: str, data: dict) -> dict:
	"""POST request to Mailchimp API."""
	r = requests.post(
		f"{BASE_URL}{path}",
		json=data,
		auth=AUTH,
		headers=HEADERS,
		timeout=30,
	)
	r.raise_for_status()
	return r.json()


def _put(path: str, data: dict) -> dict:
	"""PUT request to Mailchimp API."""
	r = requests.put(
		f"{BASE_URL}{path}",
		json=data,
		auth=AUTH,
		headers=HEADERS,
		timeout=60,
	)
	r.raise_for_status()
	return r.json()


def _delete(path: str) -> None:
	"""DELETE request to Mailchimp API."""
	r = requests.delete(
		f"{BASE_URL}{path}",
		auth=AUTH,
		headers=HEADERS,
		timeout=30,
	)
	r.raise_for_status()


# --- Lists / Members ---

def get_list_members(list_id: str = SG_LIST_ID, count: int = 1000, offset: int = 0,
                     status: str = "subscribed") -> dict:
	"""Fetch members of a list (paginated)."""
	return _get(f"/lists/{list_id}/members", {
		"count": count,
		"offset": offset,
		"status": status,
		"fields": "members.email_address,members.tags,members.merge_fields,members.status,total_items",
	})


def get_all_members(list_id: str = SG_LIST_ID, status: str = "subscribed") -> list[dict]:
	"""Fetch all members of a list, handling pagination."""
	members = []
	offset = 0
	count = 1000
	while True:
		data = get_list_members(list_id, count=count, offset=offset, status=status)
		batch = data.get("members", [])
		members.extend(batch)
		if len(batch) < count:
			break
		offset += count
	return members


def get_member(email: str, list_id: str = SG_LIST_ID) -> dict:
	"""Fetch a single member by email."""
	return _get(f"/lists/{list_id}/members/{subscriber_hash(email)}")


def update_member(email: str, data: dict, list_id: str = SG_LIST_ID) -> dict:
	"""Update a member (merge fields, etc). Uses PUT for upsert."""
	return _put(f"/lists/{list_id}/members/{subscriber_hash(email)}", data)


# --- Tags ---

def set_tags(email: str, tags: list[dict], list_id: str = SG_LIST_ID) -> dict:
	"""Add or remove tags on a subscriber.

	tags: [{"name": "vip", "status": "active"}, {"name": "dormant", "status": "inactive"}]
	"""
	return _post(
		f"/lists/{list_id}/members/{subscriber_hash(email)}/tags",
		{"tags": tags},
	)


# --- Merge Fields ---

def get_merge_fields(list_id: str = SG_LIST_ID) -> list[dict]:
	"""List all merge fields on an audience."""
	return _get(f"/lists/{list_id}/merge-fields")["merge_fields"]


def create_merge_field(name: str, tag: str, field_type: str = "text",
                       list_id: str = SG_LIST_ID) -> dict:
	"""Create a new merge field on an audience."""
	return _post(f"/lists/{list_id}/merge-fields", {
		"name": name,
		"tag": tag,
		"type": field_type,
	})


# --- Batch Operations ---

def submit_batch(operations: list[dict]) -> dict:
	"""Submit a batch of operations. Each op is:
	{"method": "POST", "path": "/lists/.../members/.../tags", "body": "..."}

	Max 500 operations per batch.
	"""
	return _post("/batches", {"operations": operations})


def get_batch_status(batch_id: str) -> dict:
	"""Check status of a batch operation."""
	return _get(f"/batches/{batch_id}")


def wait_for_batch(batch_id: str, poll_interval: int = 5, timeout: int = 300) -> dict:
	"""Poll until a batch completes or times out."""
	start = time.time()
	while time.time() - start < timeout:
		status = get_batch_status(batch_id)
		if status["status"] == "finished":
			return status
		time.sleep(poll_interval)
	raise TimeoutError(f"Batch {batch_id} did not complete within {timeout}s")
