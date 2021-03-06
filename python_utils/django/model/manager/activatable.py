"""Activatable manager utils"""
from activatable_model.models import ActivatableManager, ActivatableQuerySet
from manager_utils import ManagerUtilsManager, ManagerUtilsQuerySet
from python_utils.django.model.manager.general import DateBaseQuerySet


class DateBaseActivatableQuerySet(ActivatableQuerySet, DateBaseQuerySet):
    """Provides bulk modified updates method for date based and activatable models"""
    pass


class DateBaseActivatableManager(ActivatableManager):
    """Custom manager activatable and date based"""

    def get_queryset(self):
        return DateBaseActivatableQuerySet(self.model)
