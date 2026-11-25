
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Project folders
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CLIENTS_DIR = BASE_DIR / "clients"
SCRATCH_DIR = BASE_DIR / "scratch"

# Create folders if they do not exist
for folder in [DATA_DIR, OUTPUT_DIR, CLIENTS_DIR, SCRATCH_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# LinkedIn search configuration
SEARCH_KEYWORDS = [
    "Java Developer C2C",
    "Java Developer Bench",
    "Java Developer W2",
    "Java Developer Full-Time",
    "Java Developer Hotlist"
]

LOCATION = "United States"
POST_AGE_HOURS = 24

# CSV file locations
RECRUITERS_CSV = DATA_DIR / "recruiters.csv"
EMAIL_HISTORY_CSV = DATA_DIR / "email_sent_history.csv"

# Follow-up configuration
FOLLOWUP_DAYS = 7

print("C2C configuration loaded successfully.")
