from rest_framework import serializers
from .models import SettingModel  , InventoryTransferModel , UserPaymentModel
from accounts.models import User







class SettingSerializer(serializers.ModelSerializer):
    channels = serializers.SerializerMethodField()

    def get_channels(self, obj):
        channels = [obj.channel_1, obj.channel_2, obj.channel_3, obj.channel_4, obj.channel_5]
        channels = [channel for channel in channels if channel]
        return channels

    class Meta:
        model = SettingModel
        fields = '__all__'





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


# class UserPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPlanModel
#         fields = '__all__'




# class UserSerializer(serializers.ModelSerializer):
#     sub = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = '__all__'

#     def get_sub(self, obj):
#         user_subs = obj.plans.filter(is_active = True).first()
#         serializer = UserPlanSerializer(user_subs)
#         return serializer.data
