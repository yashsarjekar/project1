from users.services.model_services. \
    user_model_services import UserModelService
from users.models import (
    User,
    Permission
)


class UserService:
    def __init__(self) -> None:
        self.__user_model_service = UserModelService()

    def get_all_records(self):
        records = self.__user_model_service. \
            get_all_records()
        return records

    def authenticate_user_login(self, email) -> User:
        user = self.__user_model_service. \
            authenticate_user_login(
                email=email
            )
        return user

    def get_user_using_id(self, id):
        user = self.__user_model_service.get_user_using_id(
            id=id
        )
        return user

    def get_all_permission(self):
        return self.__user_model_service.get_all_permission()

    def get_all_roles(self):
        return self.__user_model_service.get_all_roles()

    def get_role(self, id):
        return self.__user_model_service.get_role(
            id=id
        )

    def delete_role(self, id):
        return self.__user_model_service.delete_role(id=id)

    def get_user_details(self, id):
        return self.__user_model_service.get_user_details(
            id=id
        )
