from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, permissions
from . import serializers
from accounts.models import User
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import requests
import json
from core.tasks import send_message




sandbox = 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'http://116.203.154.145:8000/verify/'


@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(View):
    def post(self, request):
        amount = request.POST.get('amount')
        chat_id = request.POST.get('chat_id')
        user = User.objects.get(chat_id = chat_id)
        setting = models.SettingModel.objects.first()
        description_text = f'{str(chat_id)} - ربات شماره مجازی - {str(amount)} تومان'
        data = {
            "MerchantID": setting.zarin_key,
            "Amount": int(amount),
            "Description": description_text,
            "Phone": '09123456789',
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            print(response.status_code)
            if response.status_code == 200:
                response_data = response.json()
                
                if response_data['Status'] == 100:
                    models.UserPaymentModel.objects.create(
                        user = user ,
                        amount = amount ,
                        key = str(response_data['Authority']),
                        )
                    return JsonResponse({'status': True, 'url':ZP_API_STARTPAY + str(response_data['Authority']), 'authority': response_data['Authority']})
                else:
                    models.UserPaymentModel.objects.create(
                        user = user ,
                        amount = amount ,
                        key = str(response_data['Authority']),
                        )
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])})
                
            return JsonResponse({'status': False, 'code': 'unexpected error'})
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})
            







def verify(request):

    authority = request.GET.get('Authority')
    payment_data = models.UserPaymentModel.objects.get(key=authority)
    setting = models.SettingModel.objects.first()

    if authority:
        data = {
            "MerchantID": setting.zarin_key,
            "Amount": int(payment_data.amount),
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)        
        if response.status_code == 200:
            response_data = response.json()
            
            if response_data['Status'] == 100:
                payment_data.status = True
                payment_data.save()

                # ذخیره موجودی قبلی
                user = payment_data.user
                previous_wallet_balance = user.wallet
                
                user.wallet += payment_data.amount
                user.save()

                # ارسال موجودی قبلی به تسک
                send_message.delay(
                    status='ok',
                    chat_id=user.chat_id,
                    amount=payment_data.amount,
                    previous_balance=previous_wallet_balance,  # موجودی قبلی
                    date=payment_data.creation
                )
                return render(request, 'core/success.html')
            
            else:
                payment_data.status = False
                payment_data.save()
                return render(request, 'core/unsuccess.html')
        return render(request,  'core/unsuccess.html')
    return render(request,  'core/unsuccess.html')








class UserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)})

# Create your views here.
class SettingAPIView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        setting = models.SettingModel.objects.first()
        serializer = serializers.SettingSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.http import JsonResponse
from rest_framework.views import APIView
from . import models  # مطمئن شوید مدل‌ها را به درستی وارد کرده‌اید



class UserOrderAPIView(APIView):

    def post(self, request):
        chat_id = request.data.get('chat_id')
        country_id = request.data.get('country_id')
        number = request.data.get('number')
        price = request.data.get('price')
        request_id = request.data.get('request_id')

        # یافتن کاربر بر اساس chat_id
        try:
            user = models.User.objects.get(chat_id=chat_id)
        except models.User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        country = None
        if country_id:
            # یافتن کشور بر اساس country_id در صورتی که مقدار داشته باشد
            try:
                country = models.NumbersModel.objects.get(id=country_id)
            except models.NumbersModel.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Country not found'}, status=404)

        try:
            price = int(price)  # تبدیل قیمت به عدد صحیح
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid price'}, status=400)

        # بررسی یونیک بودن request_id
        if models.UserOrdersModel.objects.filter(request_id=request_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Order already exists'}, status=400)

        if user.wallet < price:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)

        user.wallet -= price
        user.save()

        # ایجاد سفارش
        models.UserOrdersModel.objects.create(
            user=user, 
            request_id=request_id, 
            country=country,  # در صورت None بودن، به عنوان خالی ذخیره می‌شود
            price=price, 
            number=number
        )
        return JsonResponse({'status': 'ok'})





class UpdatePhoneUserAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request) :
        chat_id = request.data.get('chat_id')
        phone = request.data.get('phone')
        user = User.objects.filter(chat_id= chat_id)
        if user.exists :
            user = user.first()
            user.phone = phone
            user.save()
            return Response({'status': 'ok',}, status=status.HTTP_200_OK) 
        return Response({'status': 'ok',}, status=status.HTTP_404_NOT_FOUND) 



class InventoryTransferAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]


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
