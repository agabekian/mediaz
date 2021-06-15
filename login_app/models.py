from django.db import models
from django import forms
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email address doesn't look like an email"
        if len(post_data['fname']) <2:
            errors["name"] = "First name must contain at least 2 chars!"
        if len(post_data['lname']) <2:
            errors["name"] = "Last Name must contain at least 2 chars!"
        if len(post_data['password']) < 8:
            errors["password"] = "Password must be at least 8 chars long!"
        if post_data['confirm_pw']!= post_data['password']:
            errors["confirm_pw"] = "Passwords don't match"
        return errors
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['password']) < 8:
            errors["password"] = "Password must be at least 8 chars long!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email address doesn't look like an email"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager() #added
