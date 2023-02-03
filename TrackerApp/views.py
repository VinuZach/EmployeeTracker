from django.contrib.auth import login, authenticate, logout
from django.db import connection
from django.db.models import Count, Max
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .ApiCalls import *


# Create your views here.
def loginPage(request):
    errorMessage = ""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            errorMessage = "Invalid User Details"
    else:
        if not request.user.is_anonymous:
            return redirect('/dashboard')

    return render(request, 'LoginPage.html', {"errorMessage": errorMessage})


def userSignOut(request):
    logout(request)
    return redirect('/login')


def addNewRemarks(request, **kwargs):
    print(kwargs.get("companyId"))
    companyId = kwargs.get("companyId")

    if request.method == "POST":
        followUpDate = request.POST.get("newDate")
        remark = request.POST.get("newRemark")
        print(followUpDate)
        print(remark)
        addNewRemarkToDataBase(companyId, followUpDate, remark,Feasibility.HIGH)

    collectionDetails = CollectionData.objects.filter(companyId=companyId)
    return render(request, 'NewRemarkPage.html', {"collectionDetails": collectionDetails})


def employeeLocation(request):
    userDetailsList = User.objects.all()
    return render(request, 'EmployeeLocationPage.html', {"userDetailsList": userDetailsList})


def newAccountCreation(request):
    responseMessage = ""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username).first()
        if user is None:
            User.objects.create_user(username=username,
                                     password=password, is_superuser=False)
            responseMessage = "User created successfully"
        else:
            responseMessage = "User Already Exists"

    return render(request, 'NewAccount.html', {"errorMessage": responseMessage})


def addNewCollectionData(request):
    if request.method == 'POST':
        selectedCompanyId = request.POST.get("company_id")
        print("selected " + str(selectedCompanyId))
        feasibility = request.POST.get("feasibility")
        followUpDate = request.POST.get("followUpDate")
        remark = request.POST.get("remarks")
        reference = request.POST.get("reference")
        enquiryList = request.POST.getlist("enquiry")
        previousCollectionId = 0
        print(enquiryList)
        if selectedCompanyId is None or len(selectedCompanyId) == 0:
            phoneNumber = request.POST.get("comp_phone")
            companyName = request.POST.get("companyName")
            companyRepresentative = request.POST.get("comp_repret")
            mode_of_business_List = request.POST.getlist("mode_of_business")
            insertedCompany = CompanyDetails(companyName=companyName, companyRepresentative=companyRepresentative,
                                             status=Status.ACTIVE.value)
            insertedCompany.save()
            for businessItem in mode_of_business_List:
                item = ModeOfBusiness.objects.get(businessMode=businessItem)
                insertedCompany.modeOfBusiness.add(item.id)
                print(insertedCompany)
            contactNum = PhoneNumber(phoneNumber=phoneNumber, companyId=insertedCompany)
            contactNum.save()
        else:
            insertedCompany = CompanyDetails.objects.get(id=selectedCompanyId)
            previousCollectionId = CollectionData.objects.filter(companyId=selectedCompanyId).aggregate(
                Max('previousCollectionID'))['previousCollectionID__max'] + 1
            print(previousCollectionId)
        newCollectionData = CollectionData(previousCollectionID=previousCollectionId, companyId=insertedCompany,
                                           feasibility=feasibility,
                                           followUpDate=followUpDate, remark=remark, reference=reference,
                                           imageFileData=None)
        newCollectionData.save()
        for enquiry in enquiryList:
            newCollectionData.enquiry.add(enquiry)

    company = PhoneNumber.objects.select_related('companyId')
    feasibilityValues = [Feasibility.LOW, Feasibility.MEDIUM, Feasibility.HIGH]
    modeOfBusiness = ModeOfBusiness.objects.all()
    enquiry = Enquiry.objects.all()
    return render(request, 'CollectionEntryData.html',
                  {"companyList": company, "feasibilityValues": feasibilityValues, "modeOfBusiness": modeOfBusiness,
                   "enquiryList": enquiry})


@login_required
def dashboard(request):
    responseMessage = ""
    if request.method == 'POST':
        dataType = request.POST.get("dialog_dataType")
        newData = request.POST.get("newData")
        if dataType == 'location':
            isExistingLocation = Location.objects.filter(locationName=newData).first()
            if isExistingLocation is None:
                Location(locationName=newData).save()
                responseMessage = "New Location Added"
            else:
                responseMessage = "Location already Exists"
        else:
            isBusinessModeExists = ModeOfBusiness.objects.filter(businessMode=newData).first()
            if isBusinessModeExists is None:
                ModeOfBusiness(businessMode=newData).save()
                responseMessage = "New business mode Added"
            else:
                responseMessage = "business mode already Exists"
    feasibility = Feasibility.choices

    return render(request, 'Dashboard.html',
                  {"responseMessage": responseMessage, "feasibility": feasibility})


class LatestCollectionData:
    def __init__(self, feasibility, remark, companyName, previousCollectionId, companyId, status):
        self.feasibility = feasibility
        self.remark = remark
        self.companyName = companyName
        self.previousCollectionId = previousCollectionId
        self.companyId = companyId
        self.status = status


def retrieveAsClass(queryListData):
    collectionDataList = list()
    for item in queryListData:
        collectionItem = LatestCollectionData(item[0], item[1], item[2], item[3], item[4], item[6])
        collectionDataList.append(collectionItem)
    return collectionDataList
