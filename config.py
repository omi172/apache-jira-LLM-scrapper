PROJECTS = ["HADOOP", "SPARK", "KAFKA"]
BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"
FIELDS = "summary,description,comment,created,updated,status,priority,assignee,reporter,labels"
PAGE_SIZE = 10
MAX_RETRIES = 5
TIMEOUT = 10
CHECKPOINT_DIR = "checkpoints"
OUTPUT_DIR = "output"
