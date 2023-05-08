from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 
            'street', 
            'number', 
            'po', 
            'city', 
            'country', 
            'state', 
            'complement'
        ]
        read_only_fields = [
            "id"
        ]

    def update(self, instance: Address, validated_data: dict) -> Address:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
