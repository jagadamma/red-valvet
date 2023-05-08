import boto3
import os
from botocore.exceptions import ClientError

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Company
from core.serializers import CompanySerializer
from core.reponses import responses_200,responses_201,responses_400,responses_404


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY_ID = os.environ.get('AWS_SECRET_KEY_ID')
AWS_REGION = os.environ.get('AWS_REGION')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_KEY_ID,region_name=AWS_REGION)

class CompanyInfo(APIView):

    def get(self, request, *args, **kwargs):
        recruiter_id = request.query_params.get('recruiter_id', None)
        if not recruiter_id:
            return Response({"status": "failure", "status_code": "400", "error_code": "TA8001"})
        company = Company.objects.get(id=recruiter_id)
        serializer = CompanySerializer(company)
        return Response({"status": "success", "status_code": "200", "data": serializer.data})
    
    def put(self, request, *args, **kwargs):
        '''
        Updates the data for the company. We are assuming the company already has some by default data inserted by the operations team.
        Hence, there name should already exist in db at this point of time.
        '''
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
    
class CompanyLogo(APIView):

    def put(self, request, *args, **kwargs):
        data = request.data
        id = data.get('id')

        if 'file' not in request.FILES:
            return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":"File Not Found"}}, status=404)
            
        # Get the file from the request
        file = request.FILES['file']

        s3_key = id
        s3_bucket = S3_BUCKET_NAME

        # Upload file to S3
        s3_bucket = S3_BUCKET_NAME
        try:
            response = s3.upload_fileobj(file, s3_bucket, s3_key)
        except ClientError as e:
            return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":e}}, status=404)
        
        # Create S3 URL
        s3_url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"

        company = Company.objects.get(id=id)
        company.logo_url = s3_url
        company.save()

        response_data = {}
        response_data["s3_url"] = s3_url
        
        response_data = {"status": "passed" ,"message":"Logo Uploaded Successfully"}

        return Response({"status": "success", "status_code": "200", "data": response_data})
    




