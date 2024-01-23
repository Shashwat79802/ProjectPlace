from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import CustomUser
from .serializers import CustomUserSerializer

class UserView(APIView):

    serializer_class = CustomUserSerializer

    def get_user_by_email(self, email):
        try:
            return CustomUser.objects.get(email=email)     # if user exists, return user
        except CustomUser.DoesNotExist:
            return False    # else, return false

    def post(self, request):
        if self.get_user_by_email(email=request.data['email']):
            return Response(
                data={'message': 'User already exists, please login!!'},
                status=status.HTTP_409_CONFLICT     # return a Conflict error code which is 409 conflict
            )

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                        data=serializer.data,
                        status=status.HTTP_201_CREATED
                        )
        return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    def put(self, request):
        user = self.get_user_by_email(email=request.data['email'])
        if user:
            data_to_update = CustomUserSerializer(instance=user, data=request.data, partial=True)
            if data_to_update.is_valid(raise_exception=True):
                try:
                    updated_data = data_to_update.update(instance=user, validated_data=data_to_update.validated_data)
                except PermissionError:
                    return Response(
                        data={"message": "Altering user profile type/email is not allowed"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

                updated_data = CustomUserSerializer(updated_data).data
                return Response(
                        data={"message": "Data updated successfully", "data": updated_data},
                        status=status.HTTP_202_ACCEPTED
                        )
            else:
                return Response(
                        data=data_to_update.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE
                        )
        return Response(
                data={"message": "Invalid Email!!"},
                status=status.HTTP_404_NOT_FOUND
                )
