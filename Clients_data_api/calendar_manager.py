from datetime import datetime, timedelta
import csv
import json
import os

CLIENT_FILE = "clients.csv"
SCHEDULE_FILE = "weekly_schedule.json"


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

    return (
        f"{client.get('First Name', '').strip().lower()}|"
        f"{client.get('Last Name', '').strip().lower()}|"
        f"{client.get('Street Address', '').strip().lower()}"
    )


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
# EMPTY WEEK
# =========================================================

def create_empty_week():

    return {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": []
    }


# =========================================================
# CURRENT WEEK
# =========================================================

def get_current_week():

    week_key = get_week_key()

    schedule = load_schedule()

    if week_key not in schedule:

        schedule[week_key] = create_empty_week()

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

    current_week = schedule.get(
        current_week_key,
        {}
    )

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


# =========================================================
# COMPLETE A CLIENT
# =========================================================

def complete_client(client_id):

    schedule = load_schedule()

    week_key = get_week_key()

    if week_key not in schedule:

        return {
            "success": False,
            "message": "Current week does not exist."
        }

    found_client = None

    # -----------------------------------------------------
    # Find scheduled client
    # -----------------------------------------------------

    for day in schedule[week_key]:

        day_clients = schedule[week_key][day]

        if not isinstance(day_clients, list):
            continue

        for scheduled_client in day_clients:

            if scheduled_client.get(
                "client_id"
            ) == client_id:

                scheduled_client["completed"] = True

                found_client = scheduled_client

                break

        if found_client:
            break

    if not found_client:

        return {
            "success": False,
            "message": "Scheduled client not found."
        }

    # -----------------------------------------------------
    # Find actual client record
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Determine if recurring
    # -----------------------------------------------------

    recurring = (
        actual_client.get(
            "Reoccuring",
            ""
        ).strip().lower() == "yes"
    )

    frequency = (
        actual_client.get(
            "Frequency",
            ""
        ).strip().lower()
    )

    # -----------------------------------------------------
    # RECURRING CLIENT
    # -----------------------------------------------------

    if recurring:

        current_service_date = parse_date(
            actual_client.get(
                "Next Service",
                ""
            )
        )

        if current_service_date:

            actual_client["Last Service Date"] = (
                actual_client["Next Service"]
            )

            if "weekly" == frequency:

                next_date = (
                    current_service_date
                    + timedelta(weeks=1)
                )

                actual_client["Next Service"] = (
                    next_date.strftime("%m%d%y")
                )

            elif "bi-weekly" == frequency:

                next_date = (
                    current_service_date
                    + timedelta(weeks=2)
                )

                actual_client["Next Service"] = (
                    next_date.strftime("%m%d%y")
                )

    # -----------------------------------------------------
    # ONE-TIME CLIENT
    # -----------------------------------------------------

    else:

        # Nothing is changed in clients.csv.
        #
        # The completed one-time job stays in the
        # historical weekly schedule but will not be
        # recommended again.
        pass

    # -----------------------------------------------------
    # Save everything
    # -----------------------------------------------------

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