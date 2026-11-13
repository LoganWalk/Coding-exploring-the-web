import csv
import re
from flask import Flask, request, jsonify, render_template
import client_generator as sg
from Client import Client
from datetime import datetime, timedelta
import calendar_manager as cm
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# --- HTML Web Page Rendering Interfaces ---
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/revenue-page', methods=['GET'])
def revenue_page():
    return render_template('revenue.html')

@app.route('/calendar-page', methods=['GET'])
def calendar_page():
    return render_template('calendar.html')
@app.route('/client-page', methods=['GET'])
def client_page():
    return render_template('client.html')

# --- Existing API Data Route Functions ---
@app.route('/api/clients/all', methods=['GET'])
def api_all():
    clients = sg.get_client_dictionaries()

    print("ALL CLIENTS:", len(clients))

    # Attach each client's payment status, built from the permanent
    # job history: how many jobs they've had, and what they still owe.
    payment = {}

    for job in cm.load_job_history():
        entry = payment.setdefault(
            job.get('client_id', ''),
            {"job_count": 0, "unpaid_count": 0, "unpaid_total": 0.0}
        )

        entry["job_count"] += 1

        if not job.get('paid'):
            entry["unpaid_count"] += 1

            try:
                entry["unpaid_total"] += float(job.get('amount', 0))
            except (ValueError, TypeError):
                pass

    for client in clients:
        entry = payment.get(
            client.get('client_id', ''),
            {"job_count": 0, "unpaid_count": 0, "unpaid_total": 0.0}
        )

        client["job_count"] = entry["job_count"]
        client["unpaid_count"] = entry["unpaid_count"]
        client["unpaid_total"] = round(entry["unpaid_total"], 2)

    return jsonify(clients)
# =========================================================
# CALENDAR API
# =========================================================

@app.route('/api/calendar/recommendations', methods=['GET'])
def calendar_recommendations():

    recommendations = cm.get_recommendations()

    return jsonify(recommendations)


@app.route('/api/calendar/schedule', methods=['GET'])
def get_calendar_schedule():

    week_data = cm.get_current_week()

    return jsonify({
        "week": cm.get_week_key(),
        "savedAt": week_data.get("savedAt"),
        "schedule": week_data.get("week", {})
    })


@app.route('/api/calendar/save', methods=['POST'])
def save_calendar_schedule():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No schedule data received."
        }), 400

    week_key = cm.get_week_key()

    schedule = cm.load_schedule()

    schedule[week_key] = data

    cm.save_schedule(schedule)

    return jsonify({
        "status": "success",
        "message": "Schedule saved successfully.",
        "week": week_key,
        "schedule": data
    })


@app.route('/api/calendar/complete', methods=['POST'])
def complete_calendar_job():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No client data received."
        }), 400

    client_id = data.get("client_id")

    if not client_id:
        return jsonify({
            "status": "error",
            "message": "Missing client ID."
        }), 400

    result = cm.complete_client(client_id)

    if not result["success"]:

        print("COMPLETE ERROR:", result)
        return jsonify(result), 404

    return jsonify(result)

@app.route('/api/revenue', methods=['GET'])
def api_revenue():
    client_dictionaries = sg.get_client_dictionaries()

    total_roster_value = 0.0
    weekly_revenue = 0.0
    bi_weekly_revenue = 0.0
    residential_revenue = 0.0
    commercial_revenue = 0.0

    for client in client_dictionaries:
        try:
            price = float(client.get('quote_price', 0))
        except (ValueError, TypeError):
            price = 0.0

        total_roster_value += price

        # Frequency breakdown
        freq = str(client.get('frequency', '')).strip().lower()

        if freq == "weekly":
            weekly_revenue += price

        elif freq == "bi-weekly":
            bi_weekly_revenue += price

        # Client type breakdown
        client_type = str(client.get('type', '')).strip().lower()

        if client_type == "residential":
            residential_revenue += price

        elif client_type == "commerical":
            # Matches the spelling currently used in clients.csv
            commercial_revenue += price

    # Estimate monthly gross based on recurring frequency
    estimated_monthly_gross = (
        weekly_revenue * 4
    ) + (
        bi_weekly_revenue * 2
    )

    return jsonify({
        "summary": {
            "total_combined_quote_value": round(total_roster_value, 2),
            "estimated_monthly_gross_revenue": round(
                estimated_monthly_gross, 2
            )
        },

        "breakdown_by_frequency": {
            "weekly_single_rotation_value": round(
                weekly_revenue, 2
            ),
            "bi_weekly_single_rotation_value": round(
                bi_weekly_revenue, 2
            )
        },

        "breakdown_by_client_type": {
            "residential_value": round(
                residential_revenue, 2
            ),
            "commercial_value": round(
                commercial_revenue, 2
            )
        }
    })
@app.route('/api/completed-jobs', methods=['GET'])
def api_completed_jobs():
    return jsonify(cm.load_completed_jobs())


@app.route('/api/finish-week', methods=['POST'])
def finish_week():
    """
    Clears the CURRENT completed-jobs list (what the Completed
    Jobs panel shows) so the next week starts fresh. This does
    NOT touch job_history.json, which permanently records every
    completed job for revenue math (This Month, Total) — so
    finishing a week never loses revenue history.
    """
    try:
        cm.save_completed_jobs([])
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return jsonify({
        "status": "success",
        "message": "Week finished. Completed jobs list has been reset."
    })


@app.route('/api/revenue/actual', methods=['GET'])
def api_actual_revenue():
    # Revenue math reads from the permanent job history, not the
    # current-week completed-jobs list, so "Finish Week" resetting
    # that list never loses revenue totals.
    completed_jobs = cm.load_job_history()

    today = datetime.today()

    today_revenue = 0.0
    week_revenue = 0.0
    month_revenue = 0.0
    total_revenue = 0.0

    paid_total = 0.0
    unpaid_total = 0.0
    unpaid_jobs = []

    for job in completed_jobs:
        try:
            amount = float(job.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0.0

        total_revenue += amount

        # Paid / unpaid split (job_history.json is the source of truth)
        if job.get('paid'):
            paid_total += amount
        else:
            unpaid_total += amount
            unpaid_jobs.append({
                "job_id": job.get('job_id', ''),
                "client_id": job.get('client_id', ''),
                "first_name": job.get('first_name', ''),
                "last_name": job.get('last_name', ''),
                "city": job.get('city', ''),
                "type_of_service": job.get('type_of_service', ''),
                "amount": amount,
                "date_completed": job.get('date_completed', '')
            })

        try:
            completed_date = datetime.strptime(
                job.get('date_completed', ''),
                '%m%d%y'
            )
        except ValueError:
            continue

        if completed_date.date() == today.date():
            today_revenue += amount

        if (
            completed_date.isocalendar().week
            == today.isocalendar().week
            and completed_date.year == today.year
        ):
            week_revenue += amount

        if (
            completed_date.month == today.month
            and completed_date.year == today.year
        ):
            month_revenue += amount

    return jsonify({
        "today_revenue": round(today_revenue, 2),
        "week_revenue": round(week_revenue, 2),
        "month_revenue": round(month_revenue, 2),
        "total_revenue": round(total_revenue, 2),
        "paid_total": round(paid_total, 2),
        "unpaid_total": round(unpaid_total, 2),
        "unpaid_jobs": unpaid_jobs
    })


@app.route('/api/jobs/paid', methods=['POST'])
def api_set_job_paid():
    data = request.get_json() or {}

    job_id = str(data.get('job_id', '')).strip()

    if not job_id:
        return jsonify({
            "status": "error",
            "message": "No job_id received."
        }), 400

    paid = bool(data.get('paid', True))

    if not cm.set_job_paid(job_id, paid):
        return jsonify({
            "status": "error",
            "message": "Job not found."
        }), 404

    return jsonify({
        "status": "success",
        "message": "Marked as paid." if paid else "Marked as unpaid.",
        "job_id": job_id,
        "paid": paid
    })



# --- Interactive "Mark As Mowed" Live CSV Updater ---
@app.route('/api/client/mowed', methods=['POST'])
def mark_client_mowed():
    data = request.get_json()
    first = data.get('first_name')
    last = data.get('last_name')
    client_list = sg.load_clients() 
    updated = False
    
    for client in client_list:
        if client.get_first_name().strip().lower() == first.strip().lower() and client.get_last_name().strip().lower() == last.strip().lower():
            client.get_new_service_date() 
            updated = True
            break
            
    if updated:
        try:
            with open("clients.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["First Name","Last Name","Additional Name","Street Address","City","State","Zip","Reoccuring","Frequency","Type of Service","Additional Services","Type","Quote Price","Last Service Date","Next Service","Client ID"])
                for c in client_list:
                    writer.writerow([
                        c.get_first_name(), c.get_last_name(), c.get_additional_name(),
                        c.get_street_address(), c.get_city(), c.get_state(), c.get_zip(),
                        c.get_reoccuring(), c.get_frequency(), c.get_type_of_service(),
                        c.get_additional_service(), c.get_type(), c.get_quote_price(),
                        c.get_last_service_date(), c.get_next_service(), c.get_client_id()
                    ])
            return jsonify({"status": "success", "message": f"Successfully updated schedule for {first} {last}!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "not_found", "message": "Client matching records not found"}), 404;
def _generate_next_client_id(client_list):
    """
    Finds the highest existing CL-NNN number and returns the
    next one (e.g. CL-041 -> CL-042). Falls back to
    len(client_list) + 1 if no client IDs match that pattern.
    """

    max_num = 0

    for client in client_list:
        match = re.match(
            r"^CL-(\d+)$",
            str(client.get_client_id()).strip()
        )

        if match:
            max_num = max(max_num, int(match.group(1)))

    if max_num == 0:
        max_num = len(client_list)

    return f"CL-{max_num + 1:03d}"


@app.route('/api/client/add', methods=['POST'])
def add_client():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No client data received."
        }), 400

    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()

    if not first_name or not last_name:
        return jsonify({
            "status": "error",
            "message": "First and last name are required."
        }), 400

    try:
        quote_price = float(data.get('quote_price', 0))
    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "message": "Quote price must be a number."
        }), 400

    client_list = sg.load_clients()

    new_client_id = _generate_next_client_id(client_list)

    new_client = Client(
        first_name,
        last_name,
        data.get('additional_name', '').strip() or 'none',
        data.get('street_address', '').strip(),
        data.get('city', '').strip(),
        data.get('state', '').strip(),
        data.get('zip', '').strip(),
        data.get('reoccuring', '').strip() or 'yes',
        data.get('frequency', '').strip(),
        data.get('type_of_service', '').strip(),
        data.get('additional_service', '').strip() or 'none',
        data.get('type', '').strip() or 'Residential',
        quote_price,
        data.get('last_service_date', '').strip(),
        data.get('next_service', '').strip(),
        new_client_id
    )

    client_list.append(new_client)

    try:

        with open(
            "clients.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "First Name",
                "Last Name",
                "Additional Name",
                "Street Address",
                "City",
                "State",
                "Zip",
                "Reoccuring",
                "Frequency",
                "Type of Service",
                "Additional Services",
                "Type",
                "Quote Price",
                "Last Service Date",
                "Next Service",
                "Client ID"
            ])

            for c in client_list:

                writer.writerow([
                    c.get_first_name(),
                    c.get_last_name(),
                    c.get_additional_name(),
                    c.get_street_address(),
                    c.get_city(),
                    c.get_state(),
                    c.get_zip(),
                    c.get_reoccuring(),
                    c.get_frequency(),
                    c.get_type_of_service(),
                    c.get_additional_service(),
                    c.get_type(),
                    c.get_quote_price(),
                    c.get_last_service_date(),
                    c.get_next_service(),
                    c.get_client_id()
                ])

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return jsonify({
        "status": "success",
        "message": f"Added {first_name} {last_name} successfully.",
        "client_id": new_client_id
    })


@app.route('/api/client/edit', methods=['POST'])
def edit_client():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No client data received."
        }), 400

    old_first_name = data.get("old_first_name")
    old_last_name = data.get("old_last_name")

    if not old_first_name or not old_last_name:
        return jsonify({
            "status": "error",
            "message": "Missing original client name."
        }), 400

    client_list = sg.load_clients()

    found_client = None

    # Find the original client
    for client in client_list:

        if (
            client.get_first_name().strip().lower()
            == old_first_name.strip().lower()
            and
            client.get_last_name().strip().lower()
            == old_last_name.strip().lower()
        ):

            found_client = client
            break

    if found_client is None:

        return jsonify({
            "status": "not_found",
            "message": "Original client could not be found."
        }), 404


    # =====================================================
    # UPDATE THE CLIENT
    # =====================================================

    found_client.set_first_name(data.get("first_name", "").strip())
    found_client.set_last_name(data.get("last_name", "").strip())
    found_client.set_additional_name(data.get("additional_name", "").strip())
    found_client.set_street_address(data.get("street_address", "").strip())
    found_client.set_city(data.get("city", "").strip())
    found_client.set_state(data.get("state", "").strip())
    found_client.set_zip(data.get("zip", "").strip())
    found_client.set_reoccuring(data.get("reoccuring", "").strip())
    found_client.set_frequency(data.get("frequency", "").strip())
    found_client.set_type_of_service(data.get("type_of_service", "").strip())
    found_client.set_additional_service(data.get("additional_service", "").strip())
    found_client.set_type(data.get("type", "").strip())

    try:
        found_client.set_quote_price(
            float(data.get("quote_price", 0))
        )
    except (ValueError, TypeError):

        return jsonify({
            "status": "error",
            "message": "Quote price must be a number."
        }), 400

    found_client.set_last_service_date(
        data.get("last_service_date", "").strip()
    )

    found_client.set_next_service(
        data.get("next_service", "").strip()
    )


    # =====================================================
    # SAVE EVERYTHING BACK TO CSV
    # =====================================================

    try:

        with open(
            "clients.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "First Name",
                "Last Name",
                "Additional Name",
                "Street Address",
                "City",
                "State",
                "Zip",
                "Reoccuring",
                "Frequency",
                "Type of Service",
                "Additional Services",
                "Type",
                "Quote Price",
                "Last Service Date",
                "Next Service",
                "Client ID"
            ])

            for client in client_list:

                writer.writerow([
                    client.get_first_name(),
                    client.get_last_name(),
                    client.get_additional_name(),
                    client.get_street_address(),
                    client.get_city(),
                    client.get_state(),
                    client.get_zip(),
                    client.get_reoccuring(),
                    client.get_frequency(),
                    client.get_type_of_service(),
                    client.get_additional_service(),
                    client.get_type(),
                    client.get_quote_price(),
                    client.get_last_service_date(),
                    client.get_next_service(),
                    client.get_client_id()
                ])


        return jsonify({
            "status": "success",
            "message": "Client updated successfully."
        })


    except Exception as e:

        print("ERROR SAVING CLIENT:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@app.route('/api/client/remove', methods=['POST'])
def remove_client():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No client data received."
        }), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not first_name or not last_name:
        return jsonify({
            "status": "error",
            "message": "Missing client name."
        }), 400

    client_list = sg.load_clients()

    found_client = None

    for client in client_list:

        if (
            client.get_first_name().strip().lower()
            == first_name.strip().lower()
            and
            client.get_last_name().strip().lower()
            == last_name.strip().lower()
        ):
            found_client = client
            break

    # IMPORTANT:
    # This must be AFTER the loop.
    if found_client is None:
        return jsonify({
            "status": "not_found",
            "message": "Client not found."
        }), 404

    client_list.remove(found_client)

    try:

        with open(
            "clients.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "First Name",
                "Last Name",
                "Additional Name",
                "Street Address",
                "City",
                "State",
                "Zip",
                "Reoccuring",
                "Frequency",
                "Type of Service",
                "Additional Services",
                "Type",
                "Quote Price",
                "Last Service Date",
                "Next Service",
                "Client ID"
            ])

            for c in client_list:

                writer.writerow([
                    c.get_first_name(),
                    c.get_last_name(),
                    c.get_additional_name(),
                    c.get_street_address(),
                    c.get_city(),
                    c.get_state(),
                    c.get_zip(),
                    c.get_reoccuring(),
                    c.get_frequency(),
                    c.get_type_of_service(),
                    c.get_additional_service(),
                    c.get_type(),
                    c.get_quote_price(),
                    c.get_last_service_date(),
                    c.get_next_service(),
                    c.get_client_id()
                ])

        return jsonify({
            "status": "success",
            "message":
                f"Removed {first_name} {last_name} successfully."
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@app.route('/api/client/update', methods=['POST'])
def update_client():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No client data received."
        }), 400

    original_first_name = data.get('original_first_name')
    original_last_name = data.get('original_last_name')

    if not original_first_name or not original_last_name:
        return jsonify({
            "status": "error",
            "message": "Missing original client name."
        }), 400

    client_list = sg.load_clients()

    found_client = None

    for client in client_list:

        if (
            client.get_first_name().strip().lower()
            == original_first_name.strip().lower()
            and
            client.get_last_name().strip().lower()
            == original_last_name.strip().lower()
        ):
            found_client = client
            break

    if found_client is None:
        return jsonify({
            "status": "not_found",
            "message": "Client not found."
        }), 404

    try:

        # Update the values on the existing client object.
        found_client.first_name = data.get(
            'first_name',
            found_client.get_first_name()
        )

        found_client.last_name = data.get(
            'last_name',
            found_client.get_last_name()
        )

        found_client.additional_name = data.get(
            'additional_name',
            found_client.get_additional_name()
        )

        found_client.street_address = data.get(
            'street_address',
            found_client.get_street_address()
        )

        found_client.city = data.get(
            'city',
            found_client.get_city()
        )

        found_client.state = data.get(
            'state',
            found_client.get_state()
        )

        found_client.zip = data.get(
            'zip',
            found_client.get_zip()
        )

        found_client.reoccuring = data.get(
            'reoccuring',
            found_client.get_reoccuring()
        )

        found_client.frequency = data.get(
            'frequency',
            found_client.get_frequency()
        )

        found_client.type_of_service = data.get(
            'type_of_service',
            found_client.get_type_of_service()
        )

        found_client.additional_service = data.get(
            'additional_service',
            found_client.get_additional_service()
        )

        found_client.type = data.get(
            'type',
            found_client.get_type()
        )

        found_client.quote_price = data.get(
            'quote_price',
            found_client.get_quote_price()
        )

        found_client.last_service_date = data.get(
            'last_service_date',
            found_client.get_last_service_date()
        )

        found_client.next_service = data.get(
            'next_service',
            found_client.get_next_service()
        )

        # Rewrite CSV
        with open(
            "clients.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "First Name",
                "Last Name",
                "Additional Name",
                "Street Address",
                "City",
                "State",
                "Zip",
                "Reoccuring",
                "Frequency",
                "Type of Service",
                "Additional Services",
                "Type",
                "Quote Price",
                "Last Service Date",
                "Next Service",
                "Client ID"
            ])

            for c in client_list:

                writer.writerow([
                    c.get_first_name(),
                    c.get_last_name(),
                    c.get_additional_name(),
                    c.get_street_address(),
                    c.get_city(),
                    c.get_state(),
                    c.get_zip(),
                    c.get_reoccuring(),
                    c.get_frequency(),
                    c.get_type_of_service(),
                    c.get_additional_service(),
                    c.get_type(),
                    c.get_quote_price(),
                    c.get_last_service_date(),
                    c.get_next_service(),
                    c.get_client_id()
                ])

        return jsonify({
            "status": "success",
            "message": "Client updated successfully."
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

