from django.urls import path

from core.views import CompanyInfo, CompanyLogo

urlpatterns = [
    path('details/', CompanyInfo.as_view(), name="company_info_view"),
    path('logo/', CompanyLogo.as_view(), name="company_logo_view") 
]