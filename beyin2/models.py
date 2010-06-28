from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


voteChoices = (
            ( 'U', '+1'),
            ( 'D', '-1'),
            ( 'N', ' 0'),
)


class Idea(models.Model):
    title = models.CharField(max_length = 128)
    description = models.TextField()
    dateSubmitted = models.DateTimeField("date submitted",default=datetime.now())
    submitter = models.ForeignKey(User)
    status = models.ForeignKey("Status")
    category = models.ForeignKey("Category")



class Status(models.Model):
    name = models.CharField(max_length = 128)


class Category(models.Model):
    name = models.CharField(max_length = 128)


class Vote(models.Model):
    idea = models.ForeignKey("Idea")
    vote = models.CharField(max_length= 1, choices=voteChoices)


class ScreenShot(models.Model):
    idea = models.ForeignKey("Idea")
    image = models.ImageField(upload_to="beyin2/")



