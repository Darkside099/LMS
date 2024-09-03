from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.userlist, name="user_list"),
    path("register/", views.register, name="register"),
    path("user_info/<str:user_id>/", views.user_info, name="user_info"),
    path("catalog/<str:category>/", views.catalog, name="catalog"),
    path("services/<str:user_id>/", views.services, name="services"),
    path("checkout/<int:item_id>", views.checkout, name="checkout"),
    path("item_info/<int:item_id>", views.item_info, name="item_info"),
]
