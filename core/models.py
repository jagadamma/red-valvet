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
    linkedin_profile = fields.StringField()
    facebook_profile = fields.StringField()
    twitter_profile = fields.StringField()
    youtube_profile = fields.StringField()
    career_page_link = fields.StringField()
    created_on = fields.DateTimeField(default=datetime.utcnow)
    logo_url = fields.StringField()
    background_color = fields.StringField()
    text_color = fields.StringField()



