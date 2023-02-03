from rest_framework import serializers
from .models import *


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["locationName", "id"]


class ModeOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeOfBusiness
        fields = ["businessMode", "id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", 'is_superuser']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ["id", "companyName", "companyRepresentative", "status"]


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionData
        fields = '__all__'
