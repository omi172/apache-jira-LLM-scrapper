import json
from utils import sanitize_text
from config import OUTPUT_DIR
import os
from config import CHECKPOINT_DIR

def transform_issue(issue, project):
    fields = issue.get("fields") or {}

    comments = (fields.get("comment") or {}).get("comments", [])
    status = (fields.get("status") or {}).get("name")
    priority = (fields.get("priority") or {}).get("name")
    reporter = (fields.get("reporter") or {}).get("displayName")
    assignee = (fields.get("assignee") or {}).get("displayName")

    return {
        "issue_id": issue.get("key"),
        "project": project,
        "title": sanitize_text(fields.get("summary")),
        "status": status,
        "priority": priority,
        "reporter": reporter,
        "assignee": assignee,
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "labels": fields.get("labels", []),
        "description": sanitize_text(fields.get("description")),
        "comments": [sanitize_text(c.get("body")) for c in comments if c and isinstance(c, dict)],
        "tasks": {
            "summarization": f"{fields.get('summary')} - {sanitize_text(fields.get('description'))[:100]}...",
            "classification": "bug" if "bug" in fields.get("labels", []) else "task",
            "qna": {
                "question": f"What is the issue {issue.get('key')} about?",
                "answer": sanitize_text(fields.get("summary"))
            }
        }
    }


def write_jsonl(project, issues):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/{project}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        for issue in issues:
            json.dump(issue, f)
            f.write("\n")
