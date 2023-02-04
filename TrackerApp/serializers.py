from rest_framework import serializers
from .models import *


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = '__all__'


class ModeOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeOfBusiness
        fields = ["businessMode", "id"]


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", 'is_superuser',"id"]


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionData
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ["id",
                  "companyName",
                  "companyRepresentative",
                  "status",
                  "locationName",
                  "phoneNumber",
                  "primaryBusinessMode"]
