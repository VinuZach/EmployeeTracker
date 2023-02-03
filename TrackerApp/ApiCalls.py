from builtins import print

from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.utils import json
from django.db import connection
from .serializers import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from rest_framework import status


@api_view(['GET'])
def getLocationList_api(request):
    locationList = Location.objects.all()
    return JsonResponse({"locationList": LocationSerializer(locationList, many=True).data}, safe=True)


@api_view(['GET'])
def getEmployeeLocationList(request):
    print(request.GET.get("userId"))
    userLocation = UserLocation.objects.filter(author=request.GET.get("userId"))
    totalDistance = userLocation.aggregate(Max('totalDistance'))
    return JsonResponse(
        {"employeeLocationList": UserLocationSerializer(userLocation, many=True).data,
         "totalDistance": totalDistance["totalDistance__max"]},
        safe=False)


@api_view(['GET'])
def changeCompanyStatus(request):
    newStatus = request.GET.get("newStatus")
    companyDetails = CompanyDetails.objects.filter(id=request.GET.get("companyId")).first()
    companyDetails.status = newStatus
    companyDetails.save()

    return JsonResponse({"responseMessage": "status changed"}, safe=False)


@api_view(['GET'])
def getModeOfBusiness(request):
    modeOfBusinessList = ModeOfBusiness.objects.all()
    return JsonResponse({"modeOfBusiness": ModeOfBusinessSerializer(modeOfBusinessList, many=True).data}, safe=False)


@api_view(['POST'])
def uploadCollectionDetails(request):
    print(request.POST)
    return JsonResponse({"Response": "ff"})


@api_view(['GET'])
def retrieveCompanyList(request):
    companyList = CompanyDetails.objects.all()
    return JsonResponse(data=CompanySerializer(companyList,many=True).data, safe=False)


@api_view(['GET'])
def retrievePhoneNumbers(request):
    phoneNumberList = PhoneNumber.objects.all()
    return JsonResponse(data={"companyList": PhoneNumberSerializer(phoneNumberList).data}, safe=False)


# @api_view(['GET'])
# def retrieveOptionList(request):
#     modeOfBusinessList = ModeOfBusiness.objects.all()
#     locationList = Location.objects.all()
#     enquiryList = Enquiry.objects.all()
#     return  JsonResponse


@api_view(['GET'])
def getPreviousCollectionDetails(request):
    companyId = request.GET.get("companyId")
    collectionDetails = CollectionData.objects.filter(companyId=companyId)
    return JsonResponse(data={"collectionDetails": CollectionSerializer(collectionDetails, many=True).data}, safe=False)


@api_view(['GET'])
def retrieveCollectionData(request):
    startDate = request.GET.get("startDate")
    endDate = request.GET.get("endDate")
    feasibility = request.GET.get("selectedFeasibility")
    startDateQuery = ""
    endDateQuery = ""
    feasibilityQuery = ""
    if len(startDate) > 0:
        startDateQuery = "and data.followUpDate>='" + startDate + "'"
    if len(endDate) > 0:
        endDateQuery = "and data.followUpDate<='" + endDate + "'"

    if len(feasibility) > 0:
        if int(feasibility) > 0:
            feasibilityQuery = "and feasibility==" + feasibility

    collectionData = CollectionData.objects.count()
    if collectionData > 0:
        with connection.cursor() as cursor:
            cursor.execute(
                "select feasibility,remark,companyName,max(previousCollectionID) as latestDataId,company.id as "
                "companyId,companyRepresentative,status from "
                "TrackerApp_companydetails company left join TrackerApp_collectiondata "
                "data on data.companyId_id=company.id  where data.id>0 "
                + startDateQuery
                + endDateQuery
                + feasibilityQuery
                + " group by company.id"
            )

            row = cursor.fetchall()
            data = retrieveAsClass(row)
            json_string = json.dumps([ob.__dict__ for ob in data])
    return HttpResponse(json_string)


class LatestCollectionData:
    def __init__(self, feasibility, remark, companyName, previousCollectionId, companyId, companyRepresentative,
                 status1):
        self.feasibility = feasibility
        self.remark = remark
        self.companyName = companyName
        self.previousCollectionId = previousCollectionId
        self.companyId = companyId
        self.companyRepresentative = companyRepresentative
        self.status1 = status1


def retrieveAsClass(queryListData):
    collectionDataList = list()
    for item in queryListData:
        collectionItem = LatestCollectionData(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
        collectionDataList.append(collectionItem)
    return collectionDataList


@api_view(['POST'])
def addNewRemark(request):
    followUpDate = request.data.get("newFollowUpDate")
    remark = request.data.get("newRemark")
    companyId = request.data.get("companyId")
    feasibility = request.data.get("feasibility")
    addNewRemarkToDataBase(companyId, followUpDate, remark, feasibility)
    responseMessage = {"message": "New Remark Added"}
    return JsonResponse(responseMessage, safe=False)


@api_view(['POST'])
def verifyUserAccount(request):
    userName = request.POST.get("userName")
    password = request.POST.get("password")
    user = authenticate(username=userName, password=password)
    if user is None:
        responseMessage = {"errorResponse": "Invalid User Account"}
        statusMessage = 299
    else:
        phoneNumberList = PhoneNumber.objects.all()
        companyList = CompanyDetails.objects.all()
        print(companyList.count())
        responseMessage = UserSerializer(user).data
        responseMessage["companyCount"] = companyList.count()
        responseMessage["phoneNumberListCount"] = phoneNumberList.count()
        statusMessage = status.HTTP_200_OK
    return JsonResponse(responseMessage, safe=False, status=statusMessage)


def addNewRemarkToDataBase(companyId, followUpDate, remark, feasibility):
    print(companyId)
    print(followUpDate)
    print(remark)
    print(feasibility)
    collectionDetails = CollectionData.objects.filter(companyId=companyId)
    previousValue = collectionDetails.aggregate(Max('previousCollectionID'))
    newCollectionData = CollectionData(previousCollectionID=previousValue["previousCollectionID__max"],
                                       companyId=collectionDetails.first().companyId,
                                       feasibility=feasibility,
                                       followUpDate=followUpDate, remark=remark,
                                       imageFileData=None)
    newCollectionData.save()
