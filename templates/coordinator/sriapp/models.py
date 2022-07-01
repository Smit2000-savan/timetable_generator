from django.db import models

# Create your models here.

class Course(models.Model):
    cid = models.CharField(max_length=5)
    cname = models.CharField(max_length=75)
    branch = models.CharField(max_length=10)

class Batch(models.Model):
    bid = models.CharField(max_length=10)
    bname = models.CharField(max_length=10)

class Prof(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    pswrd = models.CharField(max_length=50)

class Available(models.Model):
    batch = models.CharField(max_length=10)
    slot1 = models.CharField(max_length=100)
    slot2 = models.CharField(max_length=100)
    slot3 = models.CharField(max_length=100)
    slot4 = models.CharField(max_length=100)
    slot5 = models.CharField(max_length=100)
    slot6 = models.CharField(max_length=100)
    slot7 = models.CharField(max_length=100)
    slot8 = models.CharField(max_length=100)

