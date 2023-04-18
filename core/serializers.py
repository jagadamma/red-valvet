from rest_framework import serializers

from core.models import Company

class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    website = serializers.CharField()
    type = serializers.CharField()
    industry = serializers.CharField()
    speciality = serializers.CharField()
    employee_count = serializers.IntegerField()
    founded_in = serializers.CharField()
    description = serializers.CharField()
    company_culture = serializers.CharField()
    company_life = serializers.CharField()
    company_values = serializers.CharField()
    diversity_policy = serializers.CharField()
    company_benefits = serializers.CharField()
    company_work_life = serializers.CharField()
    linkedin_profile = serializers.CharField()
    facebook_profile = serializers.CharField()
    twitter_profile = serializers.CharField(allow_null=True, allow_blank=True)
    youtube_profile = serializers.CharField(allow_null=True, allow_blank=True)
    career_page_link = serializers.CharField(allow_null=True, allow_blank=True)
    
    def create(self, validated_data):
        return Company.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.website = validated_data.get('website', instance.name)
        instance.type = validated_data.get('type', instance.name)
        instance.industry = validated_data.get('industry', instance.name)
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.employee_count = validated_data.get('employee_count', instance.employee_count)
        instance.founded_in = validated_data.get('founded_in', instance.founded_in)
        instance.description = validated_data.get('description', instance.description)
        instance.company_culture = validated_data.get('company_culture', instance.company_culture)
        instance.company_life = validated_data.get('company_life', instance.company_life)
        instance.company_values = validated_data.get('company_values', instance.company_values)
        instance.diversity_policy = validated_data.get('diversity_policy', instance.diversity_policy)
        instance.company_benefits = validated_data.get('company_benefits', instance.company_benefits)
        instance.company_work_life = validated_data.get('company_work_life', instance.company_work_life)
        instance.linkedin_profile = validated_data.get('linkedin_profile', instance.linkedin_profile)
        instance.facebook_profile = validated_data.get('facebook_profile', instance.facebook_profile)
        instance.twitter_profile = validated_data.get('twitter_profile', instance.twitter_profile)
        instance.youtube_profile = validated_data.get('youtube_profile', instance.youtube_profile)
        instance.career_page_link = validated_data.get('career_page_link', instance.career_page_link)

        return instance.save()
