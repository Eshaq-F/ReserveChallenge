from django.contrib import admin
from reservation.models import Reserve, Room


# Register your models here.

class ReserveAdmin(admin.ModelAdmin):
    list_display = ('customer_fullname', 'room', 'created_at',)
    search_fields = ('customer_fullname',)
    readonly_fields = ('created_at',)


admin.site.register(Reserve, ReserveAdmin)
admin.site.register(Room)
