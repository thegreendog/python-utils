"""General models and utils"""
import uuid

from django.db import models
from python_utils.django.model.manager.general import DateBaseManager


class DateBaseModel(models.Model):
    """Base model to automatically log the created and modified date"""

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    objects = DateBaseManager()


class BaseModel(DateBaseModel):
    """Mixin base model of all of our actual and future base models usin id as an uuid field"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
