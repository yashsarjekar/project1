from orders.services.model_services.order_model_services import OrderModelService
from orders.objects.order_record import OrderRecord
class OrderService:
    def __init__(self) -> None:
        self.__order_model_service = OrderModelService()

    def get_all_records(self):
        records = self.__order_model_service. \
            get_all_records()
        orders = []
        print(records)
        for record in records:
            order_items = record.order_items.all()
            total_price = 0
            order_item_list = []
            for order_item in order_items:
                total_price += order_item.price
                order_item_dict = {
                    "product_title": order_item.product_title,
                    "price": order_item.price,
                    "quantity": order_item.quantity,
                    "created_at": order_item.created_at,
                    "updated_at": order_item.updated_at
                }
                order_item_list.append(order_item_dict)

            orders.append(OrderRecord(
                first_name=record.first_name,
                last_name=record.last_name,
                email=record.email,
                total_price=total_price,
                order_items=order_item_list,
                created_at=record.created_at,
                updated_at=record.updated_at
            ))

        return orders