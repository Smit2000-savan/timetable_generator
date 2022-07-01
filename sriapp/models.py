from django.db import models

# Create your models here.

class Course(models.Model):
    cid = models.CharField(max_length=5)
    cname = models.CharField(max_length=75)
    branch = models.CharField(max_length=10)
    type = models.CharField(max_length=100)

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

class Slots(models.Model):
    cid = models.CharField(max_length=5)
    type = models.CharField(max_length=100)
    bname = models.CharField(max_length=10)
    slt = models.CharField(max_length=100)
    prof = models.CharField(max_length=100)

class C_pref(models.Model):
    slt = models.CharField(max_length=100)
    mn8 = models.IntegerField(default=0)
    mn10 = models.IntegerField(default=0)
    mn12 = models.IntegerField(default=0)
    tu8 = models.IntegerField(default=0)
    tu10 = models.IntegerField(default=0)
    tu12 = models.IntegerField(default=0)
    wd8 = models.IntegerField(default=0)
    wd10 = models.IntegerField(default=0)
    wd12 = models.IntegerField(default=0)
    th8 = models.IntegerField(default=0)
    th10 = models.IntegerField(default=0)
    th12 = models.IntegerField(default=0)
    fr8 = models.IntegerField(default=0)
    fr10 = models.IntegerField(default=0)
    fr12 = models.IntegerField(default=0)

class Time_to_slot(models.Model):
    time = models.CharField(max_length=50)
    slt = models.CharField(max_length=100)

class P_pref(models.Model):
    prof = models.CharField(max_length=100)
    cnt = models.IntegerField(default=0)
