from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserLocation(models.Model):
    lat = models.FloatField('Latitude', blank=False)
    lng = models.FloatField('Longitude', blank=False)
    totalDistance = models.FloatField('totalDistance', blank=False, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Location(models.Model):
    locationName = models.CharField(max_length=100, blank=False)


class ModeOfBusiness(models.Model):
    businessMode = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.businessMode


class Feasibility(models.IntegerChoices):
    HIGH = 1,
    MEDIUM = 2,
    LOW = 3


class Status(models.IntegerChoices):
    CLOSE = 0
    ACTIVE = 1
    DROP = 2


class CompanyDetails(models.Model):
    companyName = models.CharField(max_length=200, blank=False, unique=False)
    companyRepresentative = models.CharField(max_length=100, blank=False)
    modeOfBusiness = models.ManyToManyField(ModeOfBusiness)
    status = models.IntegerField(choices=Status.choices, default=Feasibility.LOW)


class PhoneNumber(models.Model):
    phoneNumber = models.CharField(max_length=20)
    companyId = models.ForeignKey(CompanyDetails, related_name="companyId", on_delete=models.CASCADE)

    def __str__(self):
        return self.phoneNumber


def __str__(self):
    return "companyName : " + self.companyName + " \n companyRepresentative " + str(self.companyRepresentative)


class Enquiry(models.Model):
    enquiryName = models.CharField(max_length=100, blank=False, unique=True)


class CollectionData(models.Model):
    previousCollectionID = models.PositiveIntegerField(primary_key=False, blank=True, null=False, default=0)
    companyId = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    feasibility = models.IntegerField(choices=Feasibility.choices, default=Feasibility.LOW)
    followUpDate = models.DateField(auto_now=False)
    remark = models.CharField(max_length=100, blank=False)
    reference = models.CharField(max_length=100, blank=True)
    enquiry = models.ManyToManyField(Enquiry, default="", blank=True)
    imageFileData = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return "remark : " + self.remark + " \n followUpDate " + str(self.followUpDate)
