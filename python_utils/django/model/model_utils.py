"""Model utils"""
import uuid

from activatable_model.models import (ActivatableManager, ActivatableQuerySet,
                                      BaseActivatableModel)
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.utils import timezone
from manager_utils import ManagerUtilsManager, ManagerUtilsQuerySet


class DateBaseQuerySet(ManagerUtilsQuerySet):
    """Provides bulk modified updates method for date base models"""

    @transaction.atomic
    def update(self, *args, **kwargs):
        if 'modified_date' not in kwargs:
            kwargs['modified_date'] = timezone.now()
        res = super().update(*args, **kwargs)
        return res


class DateBaseManager(ManagerUtilsManager):
    """Date base manager"""

    def get_queryset(self):
        return DateBaseQuerySet(self.model)


class DateBaseModel(models.Model):
    """Base model to automatically log the created and modified date"""

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    objects = DateBaseManager


class BaseModel(DateBaseModel):
    """Mixin base model of all of our actual and future base models usin id as an uuid field"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseDateActivatableQuerySet(ActivatableQuerySet, DateBaseQuerySet):
    """Provides bulk modified updates method for date based and activatable models"""
    pass


class BaseDateActivatableManager(ActivatableManager):
    """Custom manager activatable and date based"""

    def get_queryset(self):
        return BaseDateActivatableQuerySet(self.model)


class BaseDateActivatableModel(BaseActivatableModel, DateBaseModel):
    """Mixin base activatable and date model"""
    class Meta:
        abstract = True

    objects = BaseDateActivatableManager()


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 2.2's postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)
