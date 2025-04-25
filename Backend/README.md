# Live Share Backend

### Database

postgresql

Generate docs.

Diagram with `DrawSQL`: <https://drawsql.app/teams/gostik/diagrams/liveshare>

### Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

./manage.py makemigrations
./manage.py migrate

./manage.py createsuperuser
./manage.py runserver
```


### Guides

Main django docs: <https://docs.djangoproject.com/en/5.2/>

About viewsets:

- <https://www.django-rest-framework.org/api-guide/viewsets/>
- mixins, attributes and funcs of GenericAPIView: <https://www.django-rest-framework.org/api-guide/generic-views/>
- ViewSets vs APIView: <https://medium.com/@p0zn/django-apiview-vs-viewsets-which-one-to-choose-c8945e538af4>
- Implementation of PUT and PATCH (update mixin) in DRF: <https://github.com/encode/django-rest-framework/blob/085b7e166ba80aa973645e5249b441f2dbdc0c96/rest_framework/mixins.py#L80>
- Important about serializers: <https://www.django-rest-framework.org/api-guide/serializers/>
- datetime ISO format: <https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python>
- parsing datetime from strings: <https://stackoverflow.com/questions/41129921/validate-an-iso-8601-datetime-string-in-python>
- Guide how to change request and response serializer in viewset: <https://stribny.name/posts/drf-different-request-response-serializers/>
- Model field types: <https://docs.djangoproject.com/en/5.1/ref/models/fields/#model-field-types>
- Overriding model methods (e.g. self or create): <https://docs.djangoproject.com/en/5.2/topics/db/models/#overriding-model-methods>

Django ORM:

- Accessing ForeignKey models and making queries: <https://docs.djangoproject.com/en/5.1/topics/db/examples/many_to_one/>
- Aggregation: <https://docs.djangoproject.com/en/5.2/topics/db/aggregation/#order-of-annotate-and-filter-clauses>
- Field lookups (gte, gt, startswith): <https://docs.djangoproject.com/en/5.2/ref/models/querysets/#field-lookups>

- DRF guide with link to full guide: <https://www.django-rest-framework.org/tutorial/quickstart/>

LifeHack for Z suffix:

```python
from datetime import datetime

def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return False
    return True
```

### TODO

- Swagger tags: <https://stackoverflow.com/questions/62572389/django-drf-yasg-how-to-add-description-to-tags>

```python
class ClientView(APIView):
    @swagger_auto_schema(tags=['my custom tag'])
    def get(self, request, client_id=None):
        pass
```

- Поиск постов по названию
- Переименовать ручки под V1
