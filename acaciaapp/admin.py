from django.contrib import admin
from .models import Room, RoomBooking, Reservation, EventBooking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'price', 'available')
    list_editable = ('available',)  # only fields that exist in the model

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'room', 'check_in', 'check_out', 'email', 'phone')
    list_editable = ()  # you can choose fields, but only existing ones

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reserved_name', 'people', 'date', 'time', 'user')

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "event_name", "date", "attendees", "email", "is_canceled", "created_at")
    list_filter = ("date", "is_canceled")
    search_fields = ("customer_name", "email", "phone", "event_name")
