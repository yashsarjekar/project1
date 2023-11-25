from users.models import (
    User,
    Permission,
    Role
)

class UserModelService:
    def __init__(self) -> None:
        pass

    def get_all_records(self):
        records = User.objects.all()
        return records
    
    def authenticate_user_login(self, email):
        user = User.objects.filter(email=email).first()
        return user
    
    def get_user_using_id(self, id):
        user = User.objects.filter(id=id)
        return user
    
    def get_all_permission(self):
        return Permission.objects.all()
    
    def get_all_roles(self):
        return Role.objects.all()
    
    def get_role(self, id):
        return Role.objects.get(id=id)
    
    def delete_role(self, id):
        return Role.objects.filter(id=id).delete()
    
    def get_user_details(self, id):
        return User.objects.get(id=id)