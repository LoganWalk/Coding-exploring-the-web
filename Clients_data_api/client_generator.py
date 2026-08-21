import csv
from Client import Client


def load_clients():
    clients = []

    with open(
        "clients.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as data_file:

        reader = csv.DictReader(data_file)

        for row in reader:

            try:

                customer = Client(
                    row["First Name"].strip(),
                    row["Last Name"].strip(),
                    row["Additional Name"].strip(),
                    row["Street Address"].strip(),
                    row["City"].strip(),
                    row["State"].strip(),
                    row["Zip"].strip(),
                    row["Reoccuring"].strip(),
                    row["Frequency"].strip(),
                    row["Type of Service"].strip(),
                    row["Additional Services"].strip(),
                    row["Type"].strip(),
                    float(row["Quote Price"]),
                    row["Last Service Date"].strip(),
                    row["Next Service"].strip(),

                    # NEW
                    row["Client ID"].strip()
                )

                clients.append(customer)

            except (KeyError, ValueError) as error:

                print(
                    f"Skipping invalid client record: {error}"
                )

                continue

    return clients


def client_to_dictionary(list_of_clients):

    client_dictionary_list = []

    for client in list_of_clients:

        client_dictionary = {

            # -----------------------------------------
            # CLIENT ID
            # -----------------------------------------

            "client_id":
                client.get_client_id(),


            # -----------------------------------------
            # CLIENT INFORMATION
            # -----------------------------------------

            "first_name":
                client.get_first_name(),

            "last_name":
                client.get_last_name(),

            "additional_name":
                client.get_additional_name(),

            "street_address":
                client.get_street_address(),

            "zip":
                client.get_zip(),

            "city":
                client.get_city(),

            "state":
                client.get_state(),


            # -----------------------------------------
            # SERVICE INFORMATION
            # -----------------------------------------

            "reoccuring":
                client.get_reoccuring(),

            "frequency":
                client.get_frequency(),

            "type_of_service":
                client.get_type_of_service(),

            "additional_service":
                client.get_additional_service(),

            "type":
                client.get_type(),


            # -----------------------------------------
            # PRICE / DATES
            # -----------------------------------------

            "quote_price":
                client.get_quote_price(),

            "last_service_date":
                client.get_last_service_date(),

            "next_service":
                client.get_new_service_date()
        }

        client_dictionary_list.append(
            client_dictionary
        )

    return client_dictionary_list


def get_client_dictionaries():

    client_list = load_clients()

    return client_to_dictionary(
        client_list
    )
