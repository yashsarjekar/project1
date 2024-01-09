class OrderRecord:

    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        total_price: float = None,
        order_items: list = None,
        created_at=None,
        updated_at=None
    ) -> None:
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__total_price = total_price
        self.__order_items = order_items
        self.__created_at = created_at
        self.__updated_at = updated_at

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_total_price(self):
        return self.__total_price

    def get_order_items(self):
        return self.__order_items

    def get_created_at(self):
        return self.__created_at

    def get_updated_at(self):
        return self.__updated_at
