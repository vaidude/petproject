from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)

admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(Notification)
admin.site.register(Shelter)
admin.site.register(Feedback)
admin.site.register(Pet)
admin.site.register(Doctor)
admin.site.register(VetAppointment)
admin.site.register(Vaccinations)
admin.site.register(Adopt)
admin.site.register(ShelterBooking)
admin.site.register(UserPet)