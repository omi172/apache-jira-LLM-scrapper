import os
import json
from config import CHECKPOINT_DIR

def save_checkpoint(project, start_at):
    path = f"{CHECKPOINT_DIR}/{project}.json"
    with open(path, "w") as f:
        json.dump({"startAt": start_at}, f)

def load_checkpoint(project):
    path = f"{CHECKPOINT_DIR}/{project}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f).get("startAt", 0)
    return 0

def sanitize_text(text):
    return text.replace("\n", " ").strip() if text else ""
