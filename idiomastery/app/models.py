from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self, post):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post['firstname'])<3:
            errors['firstname'] = "First Name should be at least 3 characters"
        if len(post['lastname'])<3:
            errors['lastname'] = "Last Name should be at least 3 characters"
        if not EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid email address!"
        if len(post['password'])<8:
            errors['password'] = "Password should be at least 8 characters"

        return errors
    
    def login_validator(self, post):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid email address!"
        if len(post['password'])<8:
            errors['password'] = "Password should be at least 8 characters"

        return errors

class IdiomManager(models.Manager):
    def idiom_validator(self, post):
        errors={}
        if len(post['phrase'])<3:
            errors['phrase'] = "Idioms should be at least 3 characters"
        if len(post['meaning'])<5:
            errors['meaning'] = "Meanings should be at least 5 characters"
        if len(post['example'])<10:
            errors['example'] = "Examples should be at least 10 characters"
        if len(post['origin'])<10:
            errors['origin'] = "The origin/history should be at least 10 characters"

        return errors

class User(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Idiom(models.Model):
    phrase=models.CharField(max_length=255)
    meaning=models.TextField()
    origin=models.TextField()
    example=models.CharField(max_length=255)
    score=models.IntegerField
    user= models.ForeignKey(User, related_name="idioms", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now=True)

class Translation(models.Model):
    score=models.IntegerField
    idiom=models.ForeignKey(Idiom, related_name="translations", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name=models.CharField(max_length=255)
    idioms=models.ManyToManyField(Idiom, related_name="tags")
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now=True)