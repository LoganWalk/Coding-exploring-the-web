
import csv
from flask import Flask, request, jsonify, render_template
import client_generator as sg
from datetime import datetime, timedelta
import calendar_manager as cm

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

    schedule = cm.get_current_week()

    return jsonify({
        "week": cm.get_week_key(),
        "schedule": schedule
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
        freq = str(client.get('frequency', '')).lower()
        if freq == "bi-weekly":
            bi_weekly_revenue += price
        elif freq == "weekly":
            weekly_revenue += price
            
    estimated_monthly_gross = (weekly_revenue * 4) + (bi_weekly_revenue * 2)
    return jsonify({
        "summary": {
            "total_combined_quote_value": round(total_roster_value, 2),
            "estimated_monthly_gross_revenue": round(estimated_monthly_gross, 2)
        },
        "breakdown_by_frequency": {
            "weekly_single_rotation_value": round(weekly_revenue, 2),
            "bi_weekly_single_rotation_value": round(bi_weekly_revenue, 2)
        },
        "breakdown_by_client_type": {
            "residential_value": round(residential_revenue, 2),
            "commercial_value": round(commercial_revenue, 2)
        }
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
                writer.writerow(["First Name","Last Name","Additional Name","Street Address","City","State","Zip","Reoccuring","Frequency","Type of Service","Additional Services","Type","Quote Price","Last Service Date","Next Service"])
                for c in client_list:
                    writer.writerow([
                        c.get_first_name(), c.get_last_name(), c.get_additional_name(),
                        c.get_street_address(), c.get_city(), c.get_state(), c.get_zip(),
                        c.get_reoccuring(), c.get_frequency(), c.get_type_of_service(),
                        c.get_additional_service(), c.get_type(), c.get_quote_price(),
                        c.get_last_service_date(), c.get_next_service()
                    ])
            return jsonify({"status": "success", "message": f"Successfully updated schedule for {first} {last}!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "not_found", "message": "Client matching records not found"}), 404;
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
                "Next Service"
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
                    client.get_next_service()
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
                "Next Service"
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
                    c.get_next_service()
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
                "Next Service"
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
                    c.get_next_service()
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
