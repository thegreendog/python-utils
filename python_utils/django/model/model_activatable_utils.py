"""Activatable models utils"""
import uuid

from activatable_model.models import BaseActivatableModel
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.utils import timezone
from python_utils.django.model.manager.activatable import \
    DateBaseActivatableManager
from python_utils.django.model.model_utils import BaseModel, DateBaseModel


class DateBaseActivatableModel(BaseActivatableModel, DateBaseModel):
    """Mixin base activatable and date model"""
    class Meta:
        abstract = True

    objects = DateBaseActivatableManager()


class CustomBaseActivatableModel(BaseActivatableModel, BaseModel):
    """Mixin base activatable, date and UUID id model"""
    class Meta:
        abstract = True

    objects = DateBaseActivatableManager()
