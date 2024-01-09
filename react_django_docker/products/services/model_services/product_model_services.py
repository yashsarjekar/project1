from products.models import Products


class ProductModelService:
    def __init__(self) -> None:
        pass

    def get_all_records(self):
        records = Products.objects.all()
        return records