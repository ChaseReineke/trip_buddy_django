from django.db import models
from django.db.models.deletion import CASCADE
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First name must be 3 characters or more!"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last name must be 3 characters or more!"
        if len(post_data['email']) < 8:
            errors['email'] = "Email must be 8 characters or more!"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be 8 characters or more!"
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm'] = "Passwords don't match!"
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['email']) < 8:
            errors['email'] = "Email must be 8 characters or more!"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be 8 characters or more!"
        return errors
    
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors['destination'] = "A trip destination must be 3 characters or more!"
        if len(postData['plan']) < 3:
            errors['plan'] = "A plan must be 3 characters or more!"
        today = date.today()
        if postData['start_date'] < str(today) or postData['end_date'] < postData['start_date']:
            errors['start_date'] = "Please choose a valid start date!"
        if postData['end_date'] < postData['start_date'] or postData['end_date'] < str(today):
            errors['end_date'] = "Please choose a valid end date!"
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    traveler = models.ForeignKey(User, related_name="trips", on_delete=models.CASCADE)
    joiner = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)