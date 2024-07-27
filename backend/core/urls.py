from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('api/user_update/' , views.UserUpdateAPIView.as_view() , name='user_update'),
    path('api/setting/', views.SettingAPIView.as_view() , name='setting'),
    path('api/transfer/' , views.InventoryTransferAPIView.as_view() , name='transfer'),
    path('api/update_phone/' , views.UpdatePhoneUserAPIView.as_view() , name = 'update_phone'),

    path('api/request/', views.PaymentView.as_view(), name='request'),

    # path('api/plans/' , views.PlansAPIView.as_view() ,name='plans') ,

    # path('api/add_sub/' , views.AddSubUserAPIView.as_view() , name='add_su') ,
    # path('api/rm_sub/' , views.RemoveSubUserAPIView.as_view() , name='remove_sub') ,
    # path('api/update_sub/' , views.UserSubUpdate.as_view() , name='update_sub')

]