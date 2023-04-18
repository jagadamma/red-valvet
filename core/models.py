from django.db import models
from mongoengine import Document, fields
from datetime import datetime

class Company(Document):
    id = fields.IntField(primary_key=True)
    name = fields.StringField()
    website = fields.StringField()
    type = fields.StringField()
    industry = fields.StringField()
    speciality = fields.StringField()
    employee_count = fields.IntField()
    founded_in = fields.IntField()
    description = fields.StringField()
    company_culture = fields.StringField()
    company_life = fields.StringField()
    company_values = fields.StringField()
    diversity_policy = fields.StringField()
    company_benefits = fields.StringField()
    company_work_life = fields.StringField()
    linkedin_profile = fields.StringField()
    facebook_profile = fields.StringField()
    twitter_profile = fields.StringField()
    youtube_profile = fields.StringField()
    career_page_link = fields.StringField()
    created_on = fields.DateTimeField(default=datetime.utcnow)

