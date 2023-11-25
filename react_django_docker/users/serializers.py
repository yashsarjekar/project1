from rest_framework import serializers
from users.models import User
from users.models import Permission, Role

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','email','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return PermissionSerializer(value).data

    def to_internal_value(self, data):
        return data

class RoleSerializer(serializers.ModelSerializer):
    permission = PermissionRelatedField(many=True)
    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        permission = validated_data.pop('permission', None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permission.add(*permission)
        instance.save()
        return instance