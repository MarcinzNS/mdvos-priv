from django.urls import path
from main.views import login_system, profile, add_device
from main.views import index, categories, devices, error, os, favourite, like_devices, adminek
from main.services import admin_functions

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index.home, name="home"),
    path('sign-in', login_system.loginUser, name="login"),
    path('sign-out', login_system.logoutUser, name="logout"),
    path('sign-up', login_system.registration, name="registration"),
    path('categories', categories.categories, name="categories"),
    path('add-device', add_device.add_device, name="add_device"),
    path('devices', devices.devices, name="devices"),
    path('devices/<int:page>', devices.devices, name="devices"),
    path('devices/<int:how_many_item_on_page>/<int:page>', devices.devices, name="devices"),
    path('devices/<str:category>', devices.devices, name="devices"),
    path('devices/<str:category>/<int:page>', devices.devices, name="devices"),
    path('devices/<str:category>/<int:how_many_item_on_page>/<int:page>', devices.devices, name="devices"),
    path('one-device/<int:id>', devices.one_device, name="one_device"),


    path('profile/followed/', devices.followed_list, name='followed_list'),
    path('profile/followed/<int:page>', devices.followed_list, name="followed_list"),
    path('profile/followed/<int:how_many_item_on_page>/<int:page>', devices.followed_list, name="followed_list"),
    path('profile/followed/<str:category>', devices.followed_list, name="followed_list"),
    path('profile/followed/<str:category>/<int:page>', devices.followed_list, name="followed_list"),
    path('profile/followed/<str:category>/<int:how_many_item_on_page>/<int:page>', devices.followed_list, name="followed_list"),


    path('profile', profile.profile, name="profile"),
    path('error404', error.error404, name="error404"),
    path('error503', error.error503, name="error503"),
    path('adminek', adminek.adminek, name="adminek"),
    path('remove-device/<int:device_id>/', admin_functions.remove_device, name="remove_device"),
    path('edit-device-info/<int:device_id>/', admin_functions.edit_device_info, name="edit_device_info"),
    path('edit-device-photo/<int:device_id>/', admin_functions.edit_device_photo, name="edit_device_photo"),
    path('os', os.os, name="os"),
    path('add_MainComment/<int:device_id>/', devices.add_MainComment, name='add_MainComment'),
    path('add_UnderComment/<int:device_id>/<int:main_comment_id>/', devices.add_UnderComment, name='add_UnderComment'),
    path('fav/<int:id>/', favourite.favourite_add, name="fav"),
    path('profile/favourites/', favourite.favourites_list, name='favourites_list'),
    
    path('device/<int:device_id>/like/', like_devices.add_like, name='add_like'),
    path('device/<int:device_id>/dislike/', like_devices.add_dislike, name='add_dislike'),
    path('device/<int:device_id>/like/remove/', like_devices.remove_like, name='remove_like'),
    path('device/<int:device_id>/dislike/remove/', like_devices.remove_dislike, name='remove_dislike'),
    path('password/', auth_views.PasswordChangeView.as_view(), name= "change-password"),
]
# template_name="change-password.html"
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
