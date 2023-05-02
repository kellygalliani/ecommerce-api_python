from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'password', 
            'first_name', 
            'last_name', 
            'is_superuser', 
            'is_seller', 
            'cart', 
            'address'
        ]
        depth = 1
        read_only_fields = [
            "id", "is_superuser"
        ]
        extra_kwargs = {
            'username': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all())],
            },
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password: instance.set_password(password)
        
        instance.save()

        return instance