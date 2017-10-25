# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime



# Create your models here.

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors['name'] = "Name must be at least 2 characters"

        if len(postData['alias']) < 2:
            errors['alias'] = "alias name must be at least 2 characters"

        if len(postData['password']) < 8:
            errors['password'] = "password must be at least 8 characters"

        if not my_re.match(postData['email']):
            errors['email'] = "Please enter a valid email format"

        if postData['password'] != postData['confirm']:
            errors['password'] = "passwords must match"

        try:
            current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
            print current_date
            user_bday = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
            print user_bday
            if user_bday > current_date:
                errors['birthday'] = "You need to be alive for at least one day to use this website"
        except:
            errors['birthday'] = "Please input a birthday"
        return errors

    def validateLogin(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        hash2 = postData['password'].encode()
        if not my_re.match(postData['email']):
            errors['email'] = "Please enter a valid email format"

        if not bcrypt.checkpw(hash2, postData['hash1'].encode()):
            errors['password'] = 'email and password do not match'

        return errors

class QuoteManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 3:
            errors['quoted_by'] = "quoted_by name must be at least 3 characters"

        if len(postData['message']) < 10:
            errors['message'] = "Quote must be at least 10 characters"

        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.name, self.email, self.birthday)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.name, self.email, self.birthday)

class Quote(models.Model):
    quoted_by = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)

    posted_by = models.ForeignKey(User, related_name='quotes')
    favorited_by = models.ManyToManyField(User, related_name='favorites')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

    def __repr__(self):
        return "User: \n{}\n{}\n{}\n".format(self.id, self.quoted_by, self.message)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n".format(self.id, self.quoted_by, self.message)
        
