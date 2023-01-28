from django.urls import path
from reservation.views import RoomReserveView, EmptyRoomsView

app_name = 'reservation'

urlpatterns = [
    path('room-reserve/', RoomReserveView.as_view(), name='room_reserve'),
    path('empty-rooms/', EmptyRoomsView.as_view(), name='empty_rooms'),
]
