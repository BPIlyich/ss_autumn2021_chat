from django.urls import path

from .views import ChatLoginFormView, RoomTemplateView

urlpatterns = [
    path('login/', ChatLoginFormView.as_view(), name='login'),
    path('<str:room_name>/', RoomTemplateView.as_view(), name='room'),
]
