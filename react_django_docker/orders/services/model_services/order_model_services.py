from orders.models import Order, OrderItem


class OrderModelService:
    def __init__(self) -> None:
        pass

    def get_all_records(self):
        records = Order.objects.all().order_by('-created_at')
        return records