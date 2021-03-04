from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

# Create your models here.
class Favourite(models.Model):
    image_id= models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_original=models.URLField(blank=True,null=True)
    url_m = models.URLField(blank=True,null=True)

    class Meta:
        unique_together = ('user', 'image_id')