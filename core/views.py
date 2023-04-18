from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Company
from core.serializers import CompanySerializer
from core.reponses import responses_200,responses_201,responses_400,responses_404

class CompanyInfo(APIView):

    def get(self, request, *args, **kwargs):
        recruiter_id = request.query_params.get('recruiter_id', None)
        if not recruiter_id:
            return Response({"status": "failure", "status_code": "400", "error_code": "TA8001"})
        company = Company.objects.get(id=recruiter_id)
        serializer = CompanySerializer(company)
        return Response({"status": "success", "status_code": "200", "data": serializer.data})
    
    def put(self, request, *args, **kwargs):
        data = request.data
        company = Company.objects.get(id=data.get('id'))
        serializer = CompanySerializer(company, data=data)
        if serializer.is_valid():
            serializer.save()
            #return Response(data=serializer.data, status=HTTP_201_CREATED)
            responses_201["Data"]=serializer.data
            return Response(responses_201)
        #return Response(data="Invalid Data", status=HTTP_400_BAD_REQUEST)
        responses_400["Error message"]="Data is not valid"
        return Response(responses_400)



