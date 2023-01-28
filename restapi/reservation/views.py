from logging import getLogger

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from reservation.models import Room
from reservation.serializers import RoomReserveSerializer, EmptyRoomsSerializer, EmptyRoomsQuerySerializer

logger = getLogger(__name__)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description="Reservation of a certain room for a customer in a certain period of time.",
        responses={
            400: 'Bad Request',
            409: 'Conflict',
        },
        security=[],
    )
)
class RoomReserveView(CreateAPIView):
    serializer_class = RoomReserveSerializer

    def perform_create(self, serializer):
        room = self.get_object()
        serializer.save(room=room)

    def get_object(self):
        room_num = self.request.data.get('room_num')
        return get_object_or_404(Room.objects.all(), number=room_num)


class EmptyRoomsView(APIView):
    response_serializer_class = EmptyRoomsSerializer
    query_serializer_class = EmptyRoomsQuerySerializer

    @swagger_auto_schema(
        operation_description="Return list of empty rooms in a certain time or specific time range.",
        responses={
            200: response_serializer_class,
            400: 'Bad Request',
        },
        security=[], query_serializer=query_serializer_class)
    def get(self, request, *args, **kwargs):
        serializer = self.query_serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        empty_rooms = self.get_empty_rooms(serializer.validated_data)
        res_serializer = self.response_serializer_class(data={
            'count': empty_rooms.count(),
            'rooms_number': empty_rooms.values_list('number', flat=True),
        })
        res_serializer.is_valid()
        return Response(data=res_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_empty_rooms(validated_data: dict) -> QuerySet:
        """
        "Get all rooms that don't have any reservations that overlap with the given start and end dates."

        The function takes a validated_data dictionary as an argument. This is the data that has been validated by the
        serializer. The function then extracts the start and end dates from the validated_data dictionary

        :param validated_data: The validated data from the serializer
        :type validated_data: dict
        :return: A QuerySet of Room objects that are not reserved during the time period specified.
        """
        start = validated_data.get('start_dt')
        end = validated_data.get('end_dt', start)
        return Room.objects.exclude(reservations__from_dt__lte=end, reservations__to_dt__gte=start)
