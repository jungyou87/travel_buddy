from __future__ import unicode_literals

from django.db import models
import bcrypt
import datetime

# Create your models here.
class UserManager(models.Manager):
    def register_validation(self, form_data):
        errors=[]
        if len(form_data['name']) < 3:
            errors.append("name too short")
        if len(form_data['username']) < 3:
            errors.append("username too short")
        if len(form_data['password']) < 8:
            errors.append("password too short")
        if form_data['password'] != form_data['confirm_pw']:
            errors.append("passwords not maching")
        if User.objects.filter(username = form_data['username']):
            errors.append("username taken")
        return errors

    def register(self, form_data):
        password = str(form_data['password'])
        enc_pw = bcrypt.hashpw(password, bcrypt.gensalt())


        user = User.objects.create(
            name = form_data['name'],
            username = form_data['username'],
            password = enc_pw
        )

        return user

    def login_validation(self, form_data):
        errors = []
        if len(form_data['username']) < 3:
            errors.append("username too short")
        if len(form_data['password']) < 8:
            errors.append("password too short")

        user = User.objects.filter(username = form_data['username']).first()

        if not user:
            errors.append("no username found")
            return errors

        elif user:
            password_str = str(form_data['password'])
            user_password = str(user.password)

            encryptedPW = bcrypt.hashpw(password_str, user_password)

            if encryptedPW != user_password:
                errors.append("wrong password")
            return errors

    def login(self, form_data):
        user = User.objects.get(username = form_data['username'])

        return user


class User(models.Model):
    name = models.CharField(blank=True, max_length=100)
    username = models.CharField(blank=True, max_length=100)
    password = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class TripManager(models.Manager):
    def add_trip_validation(self, form_data):
        errors=[]
        if len(form_data['destination']) == 0:
            errors.append("destination too short")
        if len(form_data['plan']) == 0:
            errors.append("description too short")
            # Need to modify Today does not work ()
        if form_data['startdate'] < datetime.date.today:
            errors.append("startdate to be in future")
        if form_data['enddate'] <= form_data['startdate']:
            errors.append("enddate to be later than startdate")
        return errors

    def add_trip(self, form_data, user):
        trip = Trip.objects.create(
            destination = form_data['destination'],
            plan = form_data['plan'],
            startdate = form_data['startdate'],
            enddate = form_data['enddate'],
            creator = user
        )
        return trip

class Trip(models.Model):
    destination = models.CharField(blank=True, max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    plan = models.TextField(blank=True)
    creator = models.ForeignKey(User, related_name='creates')
    buddy = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
