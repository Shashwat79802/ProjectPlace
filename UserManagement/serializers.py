from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
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


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid email/password combination!!")

            if not user.is_active:
                raise serializers.ValidationError("The user is deactivated!!")
        else:
            raise serializers.ValidationError("Email/Password not provided!!")

        return data

