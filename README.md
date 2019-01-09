# Python
## Generic
### Datetime utils
* Functions to seriale/deserialize dates in ISO_8601 format
* Functions to print relative time passed since a datetime

### Enum
Enum that accepts a second description argument

## Logs
### GELF formatter
Log formatters to be used with GELF systems


# Django
## Logs
### DjangoRequestGELFFormatter
Django specific Request formatter that uses GELF format

## Middlewares
### HealthCheck Middleware
Exposes /healthz and /readyz endpoints for liveness and readiness probes

## Models
### DateBaseModel
Abstract model with created_at and modified_at fields

### BaseModel
Default abstract model intented to be a default one

# Django Filters
## Backends (for Rest Framework)
### BaseFilterBackend
Base custom filter backend just with new filter mappings added

### UUIDInFilterBackend
Custom filter backend with new filter mappings added and a default `id__in` field

# Django Rest Framework
## Mixins
### LoggingMixin
Mixin to log some REST methods and their contents

### DestroyActivatableModelMixin
Mixin to change delete action to pass a force parameter to deleting instance, for using in combination with [django-activatable-model](https://github.com/ambitioninc/django-activatable-model)

## Viewsets
### ActivatableModelViewSet
Changes DRF's ModelViewSet to use DestroyActivatableModelMixin instead of DestroyModelMixin and ListActivatableModelMixin instead of ListModelMixin

## Serializers
### BaseModelSerializer
Default base serializer with all fields and read only fields _id_, _created_at_ and _modified_at_
### BaseActivatableModelSerializer
Adds to the default serializer an _is_active_ field

# Eve
## Utils
### Datetime utils
Utils for serializing datetimes in ISO_8601 format. Overwrites `eve.io.mongo.mongo.Mongo` to change datetime serializer and json encoder class. This class can be passed to Eve constructor as `data` argument: `app = Eve(data=MyMongo)`

# Gunicorn
## Logs
### GunicornRequestGELFFormatter
Gunicorn specific Request formatter that uses GELF format

### GunicornLogger
Specific logger class for Gunicorn that logs some extra fields
