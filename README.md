# Logging
## Formatters
### GELF formatter
Log formatters to be used with GELF systems

# Django
## Middlewares
### HealthCheck Middleware
Exposes /healthz and /readyz endpoints for liveness and readiness probes

## Models
### DateBaseModel
Abstract model with created_at and modified_at fields

### BaseModel
Default abstract model intented to be a defult one

# Django Rest Framework
## Mixins
### LoggingMixin
Mixin to log some REST methods and their contents

### DestroyActivatableModelMixin
Mixin to change delete action to pass a force parameter to deleting instance, for using in combination with [django-activatable-model](https://github.com/ambitioninc/django-activatable-model)

## Viewsets
### ActivatableModelViewSet
Changes DRF's ModelViewSet to use DestroyActivatableModelMixin instead of DestroyModelMixin