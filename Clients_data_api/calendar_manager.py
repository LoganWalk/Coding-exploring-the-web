from datetime import datetime, timedelta
import csv
import hashlib
import json
import os
import uuid

CLIENT_FILE = "clients.csv"
SCHEDULE_FILE = "weekly_schedule.json"
COMPLETED_JOBS_FILE = "completed_jobs.json"

# Permanent record of every completed job, ever — never
# cleared by "Finish Week". Revenue math (This Month, Total)
# reads from here, not from COMPLETED_JOBS_FILE, so resetting
# the current week's completed-jobs list never loses revenue
# history.
JOB_HISTORY_FILE = "job_history.json"


# =========================================================
# DATE HELPERS
# =========================================================

def parse_date(date_string):
    try:
        return datetime.strptime(
            str(date_string).strip(),
            "%m%d%y"
        )

    except (ValueError, TypeError):
        return None
def format_display_date(date_string):
    date = parse_date(date_string)

    if date is None:
        return ""

    return date.strftime("%m/%d/%y")


def get_monday(date=None):
    if date is None:
        date = datetime.today()

    return date - timedelta(days=date.weekday())


def get_week_range(date=None):
    monday = get_monday(date)
    friday = monday + timedelta(days=4)

    return monday, friday


def get_week_key(date=None):
    monday = get_monday(date)

    return monday.strftime("%Y-%m-%d")


# =========================================================
# CLIENT DATA
# =========================================================

def get_all_clients():

    clients = []

    with open(
        CLIENT_FILE,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for client in reader:
            clients.append(client)

    return clients


def save_all_clients(clients):

    if not clients:
        return

    fieldnames = list(clients[0].keys())

    with open(
        CLIENT_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(clients)


# =========================================================
# CLIENT ID
# =========================================================

def get_client_id(client):

    return client.get("Client ID", "").strip()



# =========================================================
# SCHEDULE FILE
# =========================================================

def load_schedule():

    if not os.path.exists(SCHEDULE_FILE):
        return {}

    try:

        with open(
            SCHEDULE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {}


def save_schedule(schedule):

    with open(
        SCHEDULE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            schedule,
            file,
            indent=4
        )
# =========================================================
# COMPLETED JOBS
# =========================================================

def _normalize_jobs(jobs):
    """
    Makes sure every job record has the fields paid/unpaid
    tracking needs: job_id, paid and paid_date.

    Older records (saved before this existed) get a stable
    job_id built from their own contents, so the copy in
    completed_jobs.json and the copy in job_history.json end
    up with the SAME id and can be updated together.

    Returns True if anything was changed.
    """

    changed = False
    seen = {}

    for job in jobs:

        if not isinstance(job, dict):
            continue

        if not job.get("job_id"):

            key = (
                f"{job.get('client_id', '')}|"
                f"{job.get('date_completed', '')}|"
                f"{job.get('amount', '')}"
            )

            occurrence = seen.get(key, 0)
            seen[key] = occurrence + 1

            digest = hashlib.sha1(
                f"{key}|{occurrence}".encode("utf-8")
            ).hexdigest()[:10]

            job["job_id"] = f"legacy-{digest}"
            changed = True

        if "paid" not in job:
            job["paid"] = False
            changed = True

        if "paid_date" not in job:
            job["paid_date"] = ""
            changed = True

    return changed


def load_completed_jobs():
    if not os.path.exists(COMPLETED_JOBS_FILE):
        return []

    try:
        with open(
            COMPLETED_JOBS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            jobs = json.load(file)

    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(jobs, list):
        return []

    if _normalize_jobs(jobs):
        try:
            save_completed_jobs(jobs)
        except OSError:
            pass

    return jobs


def save_completed_jobs(completed_jobs):
    with open(
        COMPLETED_JOBS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            completed_jobs,
            file,
            indent=4
        )


# =========================================================
# JOB HISTORY (permanent — never cleared by Finish Week)
# =========================================================

def load_job_history():
    if not os.path.exists(JOB_HISTORY_FILE):
        return []

    try:
        with open(
            JOB_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            jobs = json.load(file)

    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(jobs, list):
        return []

    if _normalize_jobs(jobs):
        try:
            save_job_history(jobs)
        except OSError:
            pass

    return jobs


def save_job_history(job_history):
    with open(
        JOB_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            job_history,
            file,
            indent=4
        )


def add_to_job_history(job):
    history = load_job_history()
    history.append(job)
    save_job_history(history)


# =========================================================
# PAID / UNPAID
#
# A job lives in two files (the current-week list and the
# permanent history), so marking it paid updates both.
# =========================================================

def set_job_paid(job_id, paid):

    paid = bool(paid)

    paid_date = (
        datetime.today().strftime("%m%d%y")
        if paid else ""
    )

    found = False

    for loader, saver in (
        (load_completed_jobs, save_completed_jobs),
        (load_job_history, save_job_history)
    ):

        jobs = loader()

        changed = False

        for job in jobs:

            if job.get("job_id") == job_id:
                job["paid"] = paid
                job["paid_date"] = paid_date
                changed = True
                found = True

        if changed:
            saver(jobs)

    return found


# =========================================================
# EMPTY WEEK
#
# NOTE: keys are lowercase to match the shape the front end
# actually saves (see collectAndSaveSchedule in calendar.html
# and save_calendar_schedule in app.py), which nests the day
# lists under a "week" key alongside "savedAt".
# =========================================================

def create_empty_week():

    return {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": []
    }


# =========================================================
# CURRENT WEEK
#
# Returns the FULL stored wrapper for this week:
# { "savedAt": <iso string or None>, "week": {day: [...]} }
#
# If this week has never been saved, a fresh empty wrapper
# is created (and persisted) so callers always get a
# consistent shape back.
# =========================================================

def get_current_week():

    week_key = get_week_key()

    schedule = load_schedule()

    if week_key not in schedule:

        schedule[week_key] = {
            "savedAt": None,
            "week": create_empty_week()
        }

        save_schedule(schedule)

    return schedule[week_key]


# =========================================================
# FIND CLIENT
# =========================================================

def find_client(client_id):

    clients = get_all_clients()

    for client in clients:

        if get_client_id(client) == client_id:
            return client

    return None


# =========================================================
# CLIENT INFORMATION FOR CALENDAR
# =========================================================

def client_to_calendar_data(client):

    return {
        "client_id": get_client_id(client),

        "first_name":
            client.get("First Name", ""),

        "last_name":
            client.get("Last Name", ""),

        "city":
            client.get("City", ""),

        "address":
            client.get("Street Address", ""),

        "state":
            client.get("State", ""),

        "zip":
            client.get("Zip", ""),

        "additional_service":
            client.get("Additional Services", ""),

        "type_of_service":
            client.get("Type of Service", ""),

        "type":
            client.get("Type", ""),

        "frequency":
            client.get("Frequency", ""),

        "quote_price":
            client.get("Quote Price", ""),
        "last_service":
            format_display_date(
                client.get("Last Service Date", "")
            ),
        "next_service":
            format_display_date(
                client.get("Next Service", "")
            ),

        "recurring":
            client.get("Reoccuring", "").strip().lower() == "yes"
    }


# =========================================================
# RECOMMENDATIONS
# =========================================================

def get_recommendations():

    today = datetime.today()

    monday, friday = get_week_range(today)

    clients = get_all_clients()

    schedule = load_schedule()

    recommendations = {
        "overdue": [],
        "this_week": [],
        "upcoming": []
    }

    # -----------------------------------------------------
    # Only ignore clients completed IN THE CURRENT WEEK.
    #
    # This is important.
    #
    # A client completed last week still needs to appear
    # again when their next service date arrives.
    # -----------------------------------------------------

    current_week_key = get_week_key()

    completed_this_week = set()

    # The stored wrapper is { "savedAt": ..., "week": {day: [...]} } —
    # drill into "week" before iterating the day lists, otherwise
    # this loop iterates over "savedAt" (a string) and the whole
    # "week" dict itself instead of each day's client list.
    current_week = schedule.get(
        current_week_key,
        {}
    ).get("week", {})

    for day_clients in current_week.values():

        if not isinstance(day_clients, list):
            continue

        for scheduled_client in day_clients:

            if scheduled_client.get("completed") is True:

                client_id = scheduled_client.get(
                    "client_id"
                )

                if client_id:
                    completed_this_week.add(
                        client_id
                    )

    # -----------------------------------------------------
    # Categorize clients
    # -----------------------------------------------------

    for client in clients:

        next_service = parse_date(
            client.get("Next Service", "")
        )

        if next_service is None:
            continue

        client_id = get_client_id(client)

        # Already completed this week's occurrence
        if client_id in completed_this_week:
            continue

        client_data = client_to_calendar_data(
            client
        )

        # -------------------------------------------------
        # OVERDUE
        # -------------------------------------------------

        if next_service < monday:

            client_data["status"] = "overdue"

            recommendations["overdue"].append(
                client_data
            )

        # -------------------------------------------------
        # THIS WEEK
        # -------------------------------------------------

        elif monday <= next_service <= friday:

            client_data["status"] = "this_week"

            recommendations["this_week"].append(
                client_data
            )

        # -------------------------------------------------
        # UPCOMING
        # -------------------------------------------------

        else:

            client_data["status"] = "upcoming"

            recommendations["upcoming"].append(
                client_data
            )

    return recommendations


def complete_client(client_id):
    print("COMPLETE CLIENT ID:", client_id)

    schedule = load_schedule()
    week_key = get_week_key()

    if week_key not in schedule:
        return {
            "success": False,
            "message": "Current week does not exist."
        }

    week_data = schedule[week_key].get("week", {})

    found_client = None

    for day in week_data:
        day_clients = week_data[day]

        if not isinstance(day_clients, list):
            continue

        for scheduled_client in day_clients:
            if scheduled_client.get("client_id") == client_id:
                found_client = scheduled_client
                break

        if found_client:
            break

    if not found_client:
        return {
            "success": False,
            "message": "Scheduled client not found."
        }

    # Find the actual client in clients.csv
    clients = get_all_clients()
    actual_client = None

    for client in clients:
        if get_client_id(client) == client_id:
            actual_client = client
            break

    if actual_client is None:
        save_schedule(schedule)
        return {
            "success": True,
            "message": "Job completed."
        }

    # Update recurring client's dates
    recurring = actual_client.get("Reoccuring", "").strip().lower() == "yes"
    frequency = actual_client.get("Frequency", "").strip().lower()

    if recurring:
        current_service_date = parse_date(
            actual_client.get("Next Service", "")
        )

        if current_service_date:
            actual_client["Last Service Date"] = actual_client["Next Service"]

            if frequency == "weekly":
                next_date = current_service_date + timedelta(weeks=1)
                actual_client["Next Service"] = next_date.strftime("%m%d%y")

            elif frequency == "bi-weekly":
                next_date = current_service_date + timedelta(weeks=2)
                actual_client["Next Service"] = next_date.strftime("%m%d%y")
        # -----------------------------------------------------
    # RECORD COMPLETED JOB
    # -----------------------------------------------------

    try:
        amount = float(
            actual_client.get("Quote Price", 0)
        )
    except (ValueError, TypeError):
        amount = 0.0

    completed_jobs = load_completed_jobs()

    completed_job_record = {
        "client_id": client_id,
        "first_name": actual_client.get(
            "First Name",
            ""
        ),
        "last_name": actual_client.get(
            "Last Name",
            ""
        ),
        "city": actual_client.get(
            "City",
            ""
        ),
        "type_of_service": actual_client.get(
            "Type of Service",
            ""
        ),
        "type": actual_client.get(
            "Type",
            ""
        ),
        "frequency": actual_client.get(
            "Frequency",
            ""
        ),
        "amount": amount,
        "date_completed": datetime.today().strftime(
            "%m%d%y"
        ),
        "job_id": uuid.uuid4().hex[:12],
        "paid": False,
        "paid_date": ""
    }

    completed_jobs.append(completed_job_record)

    save_completed_jobs(completed_jobs)

    # Also record permanently — this list is never cleared by
    # Finish Week, so revenue totals (This Month, Total) stay
    # accurate even after the current week's list is reset.
    add_to_job_history(completed_job_record)

    save_all_clients(clients)
    save_schedule(schedule)

    return {
        "success": True,
        "message": "Job completed successfully.",
        "recurring": recurring,
        "next_service": format_display_date(
            actual_client.get("Next Service", "")
        )
    }