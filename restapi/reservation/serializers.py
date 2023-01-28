from datetime import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as RestValidationError

from reservation.models import Reserve
from project.exceptions import Conflict


class RoomReserveSerializer(serializers.ModelSerializer):
    room_num = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reserve
        exclude = ('created_at',)
        extra_kwargs = {'room': {'read_only': True}}

    def create(self, validated_data):
        room = self.context.get('room')

        try:
            instance = Reserve.objects.create(**self.validated_data, room=room)
        except ValidationError as e:
            raise Conflict({'detail': e.messages})

        return instance

    def save(self, **kwargs):
        self.context.setdefault('room', kwargs.get('room'))
        self.validated_data.pop('room_num', None)
        return super().save()


class EmptyRoomsSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=0, help_text='count of empty rooms.')
    rooms_number = serializers.ListField(
        child=serializers.IntegerField(), help_text='list of empty room\'s unique Id'
    )


class EmptyRoomsQuerySerializer(serializers.Serializer):
    start_dt = serializers.IntegerField(
        min_value=0, help_text='Time you want to check empty rooms(datetime in timestamp)'
    )
    end_dt = serializers.IntegerField(
        min_value=0, required=False,
        help_text='End of datetime range that you want to check empty rooms\n'
                  '<mark><b>Set it only when you want to get the list in a time frame</b></mark>'
    )

    def validate_start_dt(self, start_dt):
        try:
            return dt.fromtimestamp(start_dt)
        except ValueError:
            raise RestValidationError('Invalid timestamp!')

    def validate_end_dt(self, end_dt):
        try:
            return dt.fromtimestamp(end_dt) if end_dt else None
        except ValueError:
            raise RestValidationError('Invalid timestamp!')

    def validate(self, attrs):
        start, end = attrs.get('start_dt'), attrs.get('end_dt')
        if end and (end <= start):
            raise RestValidationError('End datetime must be greater than start!')
        return attrs
