from django.db import models

from api.content.models import ProfileBrand


class ChatToken(models.Model):
    token = models.CharField(max_length=300, null=False, blank=False)
    expiration_date = models.DateTimeField()
    profile_brand = models.ForeignKey(ProfileBrand, on_delete=models.CASCADE)
