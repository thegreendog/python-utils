"""General manager utils"""
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils import timezone


class DateBaseQuerySet(QuerySet):
    """Provides bulk modified updates method for date base models"""

    def update(self, *args, **kwargs):
        if 'modified_date' not in kwargs:
            kwargs['modified_date'] = timezone.now()
        res = super().update(*args, **kwargs)
        return res


class DateBaseManager(Manager):
    """Date base manager"""

    def get_queryset(self):
        return DateBaseQuerySet(self.model)
