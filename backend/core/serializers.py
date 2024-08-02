from rest_framework import serializers
from .models import SettingModel  , InventoryTransferModel , UserPaymentModel  , NumbersModel
from accounts.models import User







class SettingSerializer(serializers.ModelSerializer):
    channels = serializers.SerializerMethodField()
    numbers = serializers.SerializerMethodField()

    def get_channels(self, obj):
        channels = [obj.channel_1, obj.channel_2, obj.channel_3, obj.channel_4, obj.channel_5]
        channels = [channel for channel in channels if channel]
        return channels

    def get_numbers(self, obj):
        interest_rate = obj.interest_rates / 100  # تبدیل درصد به عدد اعشاری
        numbers = NumbersModel.objects.all()
        for number in numbers:
            number.price += number.price * interest_rate  # محاسبه قیمت جدید با درصد تنظیمات
        serializer = NumbersSerializer(numbers, many=True)
        return serializer.data

    class Meta:
        model = SettingModel
        fields = '__all__'




class NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumbersModel
        fields = ['id','weight', 'name', 'default_price', 'price', 'status', 'range', 'emoji']





class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentModel
        fields = '__all__'



class InventoryTransferSerializer(serializers.ModelSerializer):
    sender_chat_id = serializers.SerializerMethodField()
    receiver_chat_id = serializers.SerializerMethodField()

    class Meta:
        model = InventoryTransferModel
        fields = ['id', 'creation_date', 'amount', 'sender_chat_id', 'receiver_chat_id']  # اضافه کردن فیلدهای مورد نیاز

    def get_sender_chat_id(self, obj):
        return obj.sender.chat_id

    def get_receiver_chat_id(self, obj):
        return obj.receiver.chat_id

class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()
    transfers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_payments(self, obj):
        payments = UserPaymentModel.objects.filter(user=obj)
        return UserPaymentSerializer(payments, many=True).data

    def get_transfers(self, obj):
        sent_transfers = InventoryTransferModel.objects.filter(sender=obj)
        received_transfers = InventoryTransferModel.objects.filter(receiver=obj)
        all_transfers = sent_transfers.union(received_transfers).order_by('-creation_date')
        return InventoryTransferSerializer(all_transfers, many=True).data

