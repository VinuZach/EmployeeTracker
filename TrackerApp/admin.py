from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PhoneNumber)
admin.site.register(Location)
admin.site.register(ModeOfBusiness)
admin.site.register(CollectionData)
admin.site.register(CompanyDetails)
admin.site.register(Enquiry)
admin.site.register(UserLocation)