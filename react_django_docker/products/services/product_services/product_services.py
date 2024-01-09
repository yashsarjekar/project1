from products.services.model_services.product_model_services import ProductModelService

class ProductService:
    def __init__(self) -> None:
        self.__product_model_service = ProductModelService()

    def get_all_records(self):
        records = self.__product_model_service. \
            get_all_records()
        return records