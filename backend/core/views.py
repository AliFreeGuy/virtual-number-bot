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
    


















class InventoryTransferAPIView(APIView):

    def post(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        amount = request.data.get('amount')

        # Check if all required parameters are provided
        if not sender_id or not receiver_id or amount is None:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
        except ValueError:
            return Response({"error": "Amount must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"error": "Amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch sender and receiver users
        try:
            sender_user = User.objects.get(chat_id=sender_id)
            receiver_user = User.objects.get(chat_id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "User(s) not found"}, status=status.HTTP_404_NOT_FOUND)

        if sender_user.wallet < amount:
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the transfer
        sender_user.wallet -= amount
        receiver_user.wallet += amount
        sender_user.save()
        receiver_user.save()

        transfer = models.InventoryTransferModel(sender=sender_user, receiver=receiver_user, amount=amount)
        transfer.save()

        return Response({
            'status': 'ok',
            'tracking_code': transfer.tracking_code
        }, status=status.HTTP_200_OK)