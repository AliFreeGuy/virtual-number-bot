from rest_framework import serializers
from .models import SettingModel  , InventoryTransferModel
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



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'




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
