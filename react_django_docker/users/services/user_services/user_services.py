from users.services.model_services.\
user_model_services import UserModelService

class UserService:
    def __init__(self) -> None:
        self.__user_model_service =  UserModelService()

    def get_all_records(self):
        records = self.__user_model_service.\
        get_all_records()
        return records