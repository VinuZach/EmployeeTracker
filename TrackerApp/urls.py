from django.urls import path
from .views import *
from .ApiCalls import *

urlpatterns = [
    path('login', loginPage),
    path('dashboard', dashboard),
    path('newCollectionEntry', addNewCollectionData),
    path('newAccountCreation', newAccountCreation),
    path('EmployeeLocation', employeeLocation),
    path('addNewRemarks/<int:companyId>/', addNewRemarks),
    path('userSignOut', userSignOut),
]

urlpatterns += [
    path("getAllLocationList", getLocationList_api),
    path("getAllModeOfBusiness", getModeOfBusiness),
    path("verifyUserAccount", verifyUserAccount),
    path("uploadCollectionDetails", uploadCollectionDetails),
    path("retrieveCompanyList", retrieveCompanyList),
    path("retrieveCollectionData", retrieveCollectionData),
    path("getEmployeeLocationList", getEmployeeLocationList),
    path("changeCompanyStatus", changeCompanyStatus),
    path("getPreviousCollectionDetails", getPreviousCollectionDetails),
    path("addNewRemark", addNewRemark),
]
