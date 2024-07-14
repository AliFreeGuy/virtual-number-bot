from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from . import serializers
from accounts.models import User
from django.http import JsonResponse
from . import models






class UserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try :
            chat_id = request.data.get('chat_id')
            if not chat_id:
                return Response({"detail": "chat_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(chat_id=chat_id).first()
            
            if user:
                serializer = serializers.UserSerializer(user, data=request.data, partial=True)
            else:
                serializer = serializers.UserSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return JsonResponse({'error' : str(e)})



# Create your views here.
class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication ,]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        setting = models.SettingModel.objects.first()
        serializer = serializers.SettingSerializer(setting)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
