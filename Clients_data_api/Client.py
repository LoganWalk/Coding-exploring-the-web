class Client():

    def __init__(
        self,
        first_name,
        last_name,
        additional_name,
        street_address,
        city,
        state,
        zip,
        reoccuring,
        frequency,
        type_of_service,
        additional_service,
        type,
        quote_price,
        last_service_date,
        next_service,
        client_id
    ):

        self.__first_name = first_name
        self.__last_name = last_name
        self.__additional_name = additional_name
        self.__street_address = street_address
        self.__city = city
        self.__state = state
        self.__zip = zip
        self.__reoccuring = reoccuring
        self.__frequency = frequency
        self.__type_of_service = type_of_service
        self.__additional_service = additional_service
        self.__type = type
        self.__quote_price = quote_price
        self.__last_service_date = last_service_date
        self.__next_service = next_service
        self.__client_id = client_id


    # -----------------------------------------------------
    # CLIENT ID
    # -----------------------------------------------------

    def get_client_id(self):
        return self.__client_id

    def set_client_id(self, new_client_id: str):
        self.__client_id = new_client_id


    # -----------------------------------------------------
    # STATE
    # -----------------------------------------------------

    def get_state(self):
        return self.__state

    def set_state(self, new_state: str):
        self.__state = new_state


    # -----------------------------------------------------
    # FIRST NAME
    # -----------------------------------------------------

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, new_name: str):
        self.__first_name = new_name


    # -----------------------------------------------------
    # LAST NAME
    # -----------------------------------------------------

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, new_last_name: str):
        self.__last_name = new_last_name


    # -----------------------------------------------------
    # ADDITIONAL NAME
    # -----------------------------------------------------

    def get_additional_name(self):
        return self.__additional_name

    def set_additional_name(self, new_additional_name: str):
        self.__additional_name = new_additional_name


    # -----------------------------------------------------
    # STREET ADDRESS
    # -----------------------------------------------------

    def get_street_address(self):
        return self.__street_address

    def set_street_address(self, new_street_address: str):
        self.__street_address = new_street_address


    # -----------------------------------------------------
    # CITY
    # -----------------------------------------------------

    def get_city(self):
        return self.__city

    def set_city(self, new_city: str):
        self.__city = new_city


    # -----------------------------------------------------
    # ZIP
    # -----------------------------------------------------

    def get_zip(self):
        return self.__zip

    def set_zip(self, new_zip: str):
        self.__zip = new_zip


    # -----------------------------------------------------
    # REOCCURING
    # -----------------------------------------------------

    def get_reoccuring(self):
        return self.__reoccuring

    def set_reoccuring(self, new_reoccuring: str):
        self.__reoccuring = new_reoccuring


    # -----------------------------------------------------
    # FREQUENCY
    # -----------------------------------------------------

    def get_frequency(self):
        return self.__frequency

    def set_frequency(self, new_frequency: str):
        self.__frequency = new_frequency


    # -----------------------------------------------------
    # TYPE OF SERVICE
    # -----------------------------------------------------

    def get_type_of_service(self):
        return self.__type_of_service

    def set_type_of_service(self, new_type_of_service: str):
        self.__type_of_service = new_type_of_service


    # -----------------------------------------------------
    # ADDITIONAL SERVICE
    # -----------------------------------------------------

    def get_additional_service(self):
        return self.__additional_service

    def set_additional_service(self, new_additional_service: str):
        self.__additional_service = new_additional_service


    # -----------------------------------------------------
    # TYPE
    # -----------------------------------------------------

    def get_type(self):
        return self.__type

    def set_type(self, new_type: str):
        self.__type = new_type


    # -----------------------------------------------------
    # QUOTE PRICE
    # -----------------------------------------------------

    def get_quote_price(self):
        return self.__quote_price

    def set_quote_price(self, new_quote_price: float):
        self.__quote_price = new_quote_price


    # -----------------------------------------------------
    # LAST SERVICE DATE
    # -----------------------------------------------------

    def get_last_service_date(self):
        return self.__last_service_date

    def set_last_service_date(self, new_last_service_date: str):
        self.__last_service_date = new_last_service_date


    # -----------------------------------------------------
    # NEXT SERVICE DATE
    # -----------------------------------------------------

    def get_next_service(self):
        return self.__next_service

    def set_next_service(self, new_next_service: str):
        self.__next_service = new_next_service


    # -----------------------------------------------------
    # UPDATE SERVICE DATE
    # -----------------------------------------------------

    def get_new_service_date(self):

        from datetime import date, datetime, timedelta

        today = date.today()

        try:
            next_service = datetime.strptime(
                self.__next_service.strip(),
                "%m%d%y"
            ).date()

        except (ValueError, TypeError):
            return self.__next_service


        # Only advance the schedule when the
        # service is due.

        if next_service <= today:

            self.__last_service_date = self.__next_service


            if self.__frequency == "weekly":

                next_service += timedelta(
                    weeks=1
                )


            elif self.__frequency == "bi-weekly":

                next_service += timedelta(
                    weeks=2
                )


            self.__next_service = (
                next_service.strftime("%m%d%y")
            )


        return self.__next_service


    # -----------------------------------------------------
    # PRINT DATA
    # -----------------------------------------------------

    def print_data(self):

        print(
            f"{self.__first_name} "
            f"{self.__last_name} "
            f"{self.__additional_name}"
        )

        print(
            f"Client ID: {self.__client_id}"
        )

        print(
            f"Street Address: {self.__street_address}, "
            f"City: {self.__city}, "
            f"State: {self.__state}, "
            f"Zip: {self.__zip}"
        )

        print(
            f"Type of Service: {self.__type_of_service}, "
            f"Additional Service: {self.__additional_service}, "
            f"Type: {self.__type}, "
            f"Quote Price: ${self.__quote_price}"
        )

        print(
            f"Reoccuring: {self.__reoccuring}, "
            f"Frequency: {self.__frequency}, "
            f"Last Service Date: {self.__last_service_date}, "
            f"Next Service Date: {self.get_new_service_date()}"
        )

        print(
            "===================================================================================================="
        )