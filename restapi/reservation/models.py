from typing import Union

from django.db import models
from django.core.exceptions import ValidationError


class Room(models.Model):
    number = models.AutoField('room number', primary_key=True)

    def __str__(self):
        return f'Room {self.number}'


class Reserve(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations', verbose_name='related room')
    customer_fullname = models.CharField(max_length=500, verbose_name='customer fullname')
    from_dt = models.DateTimeField()
    to_dt = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    def clean(self):
        reserve_is_valid(self, raise_with=ValidationError)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.customer_fullname} -> room:{self.room} ({self.from_dt} to {self.to_dt})'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(to_dt__gt=models.F('from_dt')),
                name="to_dt > from_dt"
            )
        ]


def reserve_is_valid(reserve: Reserve, raise_with: Union[Exception, None] = None) -> bool:
    """
    It checks if the given reserve is valid or not

    :param reserve: Reserve - The reserve object to be checked
    :type reserve: Reserve Model
    :param raise_with: The exception to raise if the reserve is invalid. If None, no exception will be raised
    :type raise_with: Union[Exception, None]
    :return: A boolean value that the reservation is valid or not.
    """
    conflict = Reserve.objects.filter(from_dt__lte=reserve.to_dt, to_dt__gte=reserve.from_dt, room=reserve.room)
    if conflict.exists():
        if raise_with is not None:
            raise raise_with('This room has been reserved on the given datetime!')
        return False
    return True
