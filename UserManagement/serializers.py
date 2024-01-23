from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'is_buyer', 'is_seller', 'new_password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_buyer=validated_data['is_buyer'],
            is_seller=validated_data['is_seller']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    def update(self, instance, validated_data):
        if (
            instance.email == validated_data['email'] 
            and instance.is_buyer == validated_data['is_buyer']
            and instance.is_seller == validated_data['is_seller']
        ):
            instance.first_name = validated_data['first_name']
            instance.last_name = validated_data['last_name']

            password = validated_data.get('password', None)
            new_password = validated_data.get('new_password', None)

            if new_password:
                if password:
                    if instance.check_password(password):
                        instance.set_password(new_password)
                    else:
                        raise serializers.ValidationError('Incorrect password')
                else:
                    raise serializers.ValidationError('Password is required to change password')

            instance.save()
            return instance
        else:
            raise PermissionError('Altering user profile type/email is not allowed')
