from users.models import User

class UserModelService:
    def __init__(self) -> None:
        pass

    def get_all_records(self):
        records = User.objects.all().values()
        return records