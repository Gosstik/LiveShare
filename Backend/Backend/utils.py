import datetime as dt
from enum import Enum
from enum import EnumMeta

from django.core.exceptions import ObjectDoesNotExist

# TODO: remove drf_yasg
from drf_yasg.inspectors import FieldInspector
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.inspectors import swagger_settings
from drf_yasg import openapi

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiResponse

import Backend.utils as utils
from Backend.exceptions import BadRequest400
from Backend.exceptions import NotFound404

################################################################################

### Date

DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%:z"


def parse_datetime(datetime_str):
    return dt.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")


def parse_date(date_str):
    return dt.datetime.strptime(date_str, "%Y-%m-%d")


def parse_default_datetime(datetime_str):
    return dt.datetime.strptime(datetime_str, DEFAULT_DATETIME_FORMAT)

# from datetime import datetime
# d = "2015-04-30T23:59:59+00:00"
# if ":" == d[-3:-2]:
#     d = d[:-3]+d[-2:]
# print(datetime.strptime(d, "%Y-%m-%dT%H:%M:%S%z"))

################################################################################

### Enum utils

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item) # pylint: disable=no-value-for-parameter
        except ValueError:
            return False
        return True

    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value


class EnumWithContains(Enum, metaclass=MetaEnum):
    pass


class SortType(utils.EnumWithContains):
    ASC = "asc"
    DESC = "desc"


SORT_TYPES = [(val.value, val.name) for val in SortType]


################################################################################

### Bad Request

class BadRequestSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()


def basic_bad_request_body(code="error_code", detail="error_detail"):
    return {
        "code": code,
        "detail": detail,
    }


def basic_bad_request(code="error_code", detail="error_detail"):
    # TODO: remove default args
    # TODO: add BadRequestSerializer
    return Response(
        basic_bad_request_body(code, detail),
        status.HTTP_400_BAD_REQUEST,
    )


def true_or_400(condition: bool, code="error_code", detail="error_detail"):
    if condition:
        return
    raise BadRequest400(code=code, detail=detail)


################################################################################

### Other

def get_object_or_404(get_query, error_detail):
    try:
        return get_query()
    except ObjectDoesNotExist:
        # TODO: replace it with rest_framework ApiException
        raise NotFound404(detail=error_detail)


def validate_data(
    response_data,
    serializer_class: serializers.Serializer.__class__,
    raise_exception=True,
    verbose_code=None,
    partial=False,
):
    serializer = serializer_class(data=response_data, partial=partial)
    is_valid = serializer.is_valid(raise_exception=raise_exception)
    if not is_valid:
        error = ValidationError(code=verbose_code, detail=serializer.errors)
        print(f"ERROR: {error}")
    return serializer.validated_data
    # return serializer.data


def validate_and_get_response(
    response_data,
    serializer_class: serializers.Serializer.__class__,
    status_code=status.HTTP_200_OK,
    raise_exception=True,
    verbose_code=None,
    partial=False,
):
    validated_data = validate_data(
        response_data,
        serializer_class,
        raise_exception=raise_exception,
        verbose_code=verbose_code,
        partial=partial,
    )
    return Response(validated_data, status=status_code)


# TODO: unused remove ???
class NoSchemaTitleInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        # remove the `title` attribute of all Schema objects
        if isinstance(result, openapi.Schema.OR_REF):
            # traverse any references and alter the Schema object in place
            schema = openapi.resolve_ref(result, self.components)
            schema.pop("title", None)

            # no ``return schema`` here, because it would mean we always generate
            # an inline `object` instead of a definition reference

        # return back the same object that we got - i.e. a reference if we got a reference
        return result


# TODO: unused remove ???
class NoTitleAutoSchema(SwaggerAutoSchema):
    field_inspectors = [
        NoSchemaTitleInspector
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS


# TODO: unused remove ???
def set_default_help_text_from_model(serializer):
    for field_name, field in serializer.fields.items():
        # Get model field
        model_field = None
        try:
            model_field = serializer.Meta.model._meta.get_field(field_name)
        except:
            print(
                f"Exception: field {field_name} is not found in model {serializer.Meta.model.__name__}"
            )
            continue

        # Get help_text from model
        if not hasattr(model_field, "help_text") or not model_field.help_text:
            continue
        model_help_text = model_field.help_text

        # Extract field from serializer in case it is redefined there
        if field_name in vars(serializer)["fields"]:
            field = vars(serializer)["fields"][field_name]

        # Check that field does not already have help_text
        if field.help_text is not None:
            continue

        setattr(field, "help_text", model_help_text)


def single_example(value, name="Basic Example", **kwargs):
    return [
        OpenApiExample(
            name,
            **kwargs,
            value=value,
        ),
    ]


class StrictFieldsMixin(serializers.Serializer):
    """
    Serializer mixin to forbid additional properties in deserialization
    and ensure all fields are included in serialization
    """

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected a dictionary of items")

        unknown_fields = set(data.keys()) - set(self.fields.keys())
        if unknown_fields:
            raise serializers.ValidationError(
                {
                    key: f"Additional properties are not allowed, class={self.__class__.__name__}"
                    for key in unknown_fields
                }
            )

        return super().to_internal_value(data)

    def to_representation(self, instance):
        # Get all fields including method fields
        representation = super().to_representation(instance)
        # Ensure all declared fields are included
        for field_name in self.fields.keys():
            if field_name not in representation:
                representation[field_name] = self.fields[field_name].get_attribute(instance)
        return representation


class SerializerErrorsSerializer(StrictFieldsMixin):
    serializer_errors = serializers.DictField(child=serializers.CharField())
    detail = serializers.CharField(required=False)


def get_serializer_errors_response(serializer: serializers.Serializer, detail=None):
    response_data = {"serializer_errors": serializer.errors}
    if detail is not None:
        response_data["detail"] = detail
    return validate_and_get_response(
        response_data,
        SerializerErrorsSerializer,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def deserialize_or_400(
    data,
    serializer_class: serializers.Serializer.__class__,
    detail: str = None,
    partial: bool = False,
):
    serializer = serializer_class(data=data, partial=partial)
    if not serializer.is_valid():
        return get_serializer_errors_response(
            serializer, detail=detail
        )
    return serializer.validated_data


def get_user_display_name(email: str, first_name=None, last_name=None):
    if first_name and last_name:
        return f"{first_name} {last_name}"
    if first_name:
        return first_name
    return email
