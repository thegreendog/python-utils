# Python utils

General purpose utilities

## Generate python dist

Generate egg in dist folder: `python setup.py sdist`

## Python

### Generic

#### Datetime utils

- Functions to seriale/deserialize dates in ISO_8601 format
- Functions to print relative time passed since a datetime

#### Enum

Enum that accepts a second description argument

### Logs

#### GELF formatter

Log formatters to be used with GELF systems

## Django

### Logs

#### DjangoRequestGELFFormatter

Django specific Request formatter that uses GELF format

### Middlewares

#### HealthCheckMiddleware

Exposes /healthz and /readyz endpoints for liveness and readiness probes. Those paths can be overrided

#### NeverCacheMiddleware

Adds `Cache-Control: max-age=0, no-cache, no-store, must-revalidate` header to response if no previous Cache-control header is present

### Models

#### DateBaseModel

Abstract model with created_at and modified_at fields

#### BaseModel

Default abstract model intented to be a default one

#### BaseDateActivatableModel

Abstract model activatable with created_at and modified_at fields

#### CustomBaseActivatableModel

Abstract model activatable with created_at, modified_at and UUID id fields

#### ChoiceArrayField

A model field that allows to store an array of chosen values

### Admin

#### IsActiveListFilter

Filter that allows to list only active model instances in admin by default

## Django Filters

### Backends (for Rest Framework)

#### BaseFilterBackend

Base custom filter backend just with new filter mappings added

#### UUIDInFilterBackend

Custom filter backend with new filter mappings added and a default `id__in` field

## Django Rest Framework

### Mixins

#### LoggingMixin

Mixin to log some REST methods and their contents

#### DestroyActivatableModelMixin

Mixin to change delete action to pass a force parameter to deleting instance, for using in combination with [django-activatable-model](https://github.com/ambitioninc/django-activatable-model)

#### ActionViewMixin

Mixin to get a base POST class based view which performs an action (use it in conjunction with Rest Framework's generics.GenericAPIView)

#### OpenViewMixin

Mixin to set a view with AllowAny permissions

#### ProxyDjangoViewMixin

Proxy view to be used against Django backends

#### ProxyEveViewMixin

Proxy view to be used against EVE backends

#### ProxyGetViewMixin

Proxy view to be used in combination with ProxyDjangoViewMixin or ProxyEveViewMixin that makes a get request against desired backend

#### GetUserObjectMixin

Overrides `get_object` to filter against the user in the request. Defines also a default common queryset and lookup_field for this use case. Useful for using in combination with `UpdateAPIView`, `DestroyAPIView` and `RetrieveAPIView`

#### GetUserQuerysetMixin

Overrides `get_queryset` to add a filtering against the user in the request. Useful for using in combination with viewsets for example

### Viewsets

#### ActivatableModelViewSet

Changes DRF's ModelViewSet to use DestroyActivatableModelMixin instead of DestroyModelMixin and ListActivatableModelMixin instead of ListModelMixin

### Errors

#### as_serializer_validation_error

Method that raises a ValidationError as if it was raised in a serializer validation (intended for being used in views)

### Generics

#### PutAPIView

It's an `UpdateAPIView` but only with `put` method defined

#### PatchAPIView

It's an `UpdateAPIView` but only with `patch` method defined

### Pagination

#### PageNumberPaginationWithPageSize

Django Rest Framework's PageNumberPagination with `page_size_query_param` defined

### Serializers

#### BaseModelSerializer

Default base serializer with all fields and read only fields _id_, _created_at_ and _modified_at_

#### BaseActivatableModelSerializer

Adds to the default serializer an _is_active_ field

### Settings

#### NoMetaData

Return no metadata in OPTION method requests.

## DRF-YASG

### Response autoschemas

#### ErrorResponseAutoSchema

Generates a default error response schema for common django-rest-framework errors. Set it in `DEFAULT_AUTO_SCHEMA_CLASS` parameter of drf-yasg's `SWAGGER_SETTINGS` settings

## Eve

### Utils

#### Datetime utils

Utils for serializing datetimes in ISO_8601 format. Overwrites `eve.io.mongo.mongo.Mongo` to change datetime serializer and json encoder class. This class can be passed to Eve constructor as `data` argument: `app = Eve(data=MyMongo)`

## Gunicorn

### Logs

#### GunicornRequestGELFFormatter

Gunicorn specific Request formatter that uses GELF format

#### GunicornLogger

Specific logger class for Gunicorn that logs some extra fields
