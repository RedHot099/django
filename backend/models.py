from django.db import models
from django.contrib.auth.models import User


class Zaplecze(models.Model):
    #basic
    domain = models.CharField(max_length=64, blank=True, null=True, unique=True)
    email = models.CharField(max_length=64, blank=True, null=True)

    #Admin
    url = models.CharField(max_length=64, blank=True, null=True)
    login = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)

    #WP Create
    ftp_user = models.CharField(max_length=64, blank=True, null=True)
    ftp_pass = models.CharField(max_length=64, blank=True, null=True)
    db_user = models.CharField(max_length=64, blank=True, null=True)
    db_pass = models.CharField(max_length=64, blank=True, null=True)

    #WP API stuff
    lang = models.CharField(max_length=4, blank=True, null=True)
    topic = models.CharField(max_length=128, blank=True, null=True)
    wp_user = models.CharField(max_length=32, blank=True, null=True)
    wp_password = models.CharField(max_length=64, blank=True, null=True)
    wp_api_key = models.CharField(max_length=128, blank=True, null=True)
    wp_post_count = models.IntegerField(default=0, null=True, blank=True)



class Link(models.Model):
    task_id = models.IntegerField(default=0)
    ul_id = models.CharField(max_length=32, default="client0")
    user = models.CharField(max_length=64)
    domain = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    keyword = models.CharField(max_length=128)
    url = models.CharField(max_length=128, blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    done = models.BooleanField()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_api_key = models.CharField(max_length=64, default="", blank=True, null=True)
    semstorm_api_key = models.CharField(max_length=64, default="", blank=True, null=True)
    tokens_used = models.IntegerField(default=0)
    cursor_followed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username