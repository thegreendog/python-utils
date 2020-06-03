"""Admin model utils"""
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class IsActiveListFilter(SimpleListFilter):
    """Activatable model admin filter"""
    title = _('Active')
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('all', _('All')),
            (None, _('Active')),
            ('deleted', _('Deleted')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        query_parameters = {}
        if self.value() == 'deleted':
            query_parameters[self.parameter_name] = False
        else:
            query_parameters[self.parameter_name] = True
        return queryset.filter(**query_parameters)
