from django.urls import path

from core.views import CompanyInfo

urlpatterns = [
    path('details/', CompanyInfo.as_view(), name="company_info_view"),
]