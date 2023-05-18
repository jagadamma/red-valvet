import jsonschema
from jsonschema import Draft7Validator, FormatChecker

import boto3
import os
from botocore.exceptions import ClientError

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from core.schema import SCHEMA1
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
        serializer_data = serializer.data
        serializer_data.update({"logo_url": company.logo_url}) # Adding logo_url separately as it is not part of PUT call in serializer
        return Response({"status": "success", "status_code": "200", "data": serializer_data})
    
    def put(self, request, *args, **kwargs):
        '''
        Updates the data for the company. We are assuming the company already has some by default data inserted by the operations team.
        Hence, there name should already exist in db at this point of time.
        '''
        data = request.data
        company = Company.objects.get(id=data.get('id'))
        serializer = CompanySerializer(company, data=data)
        if serializer.is_valid():
            myschema = SCHEMA1
            v=Draft7Validator(schema=myschema,format_checker=FormatChecker())
            if len(list(v.iter_errors(data)))!=0:
                validation_errors = list(v.iter_errors(data))
                errors=[]
                for error in validation_errors:
                    errors.append({
                        'field': error.path[0] if error.path else '','message': error.message
                    })  
                #return Response({"status": "failure","status_code": "400", "error_code": "TA8001", "error_message": errors})
                responses_400["Error Message"]=errors
                return Response(responses_400)
            else:
                serializer.save()
                #return Response(data=serializer.data, status=HTTP_201_CREATED)
                responses_201["data"]=serializer.data
                responses_201["message"]="Profile Updated successfully"
                return Response(responses_201)
        #return Response(data="Invalid Data", status=HTTP_400_BAD_REQUEST)
        responses_400["error_message"]=serializer.errors
        return Response(responses_400)
    
class CompanyLogo(APIView):

    def put(self, request, *args, **kwargs):
        data = request.data
        id = data.get('id')

        if 'file' not in request.FILES:
            return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":"File Not Found"}}, status=404)
            
        # Get the file from the request
        file = request.FILES['file']

        file_name = file.name

        s3_key = id+'-'+file_name
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
        
        response_data = {"status": "passed" ,"message":"Logo Uploaded Successfully"}
        response_data["logo_url"] = s3_url

        return Response({"status": "success", "status_code": "200", "data": response_data})
    




