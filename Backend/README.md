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

TODO: create migrations with mock data

### ENV

You may use the following env files:

TODO: add more files

`dev.db.env` &mdash; dev database settings
`dev.env` &mdash; dev settings
`docker.dev.env` &mdash; dev settings for docker, overrides `dev.env`
(in .gitignore) `local.docker.env` &mdash; for setting in specific machine, overrides `docker.dev.env`

### Linting

Precommit hooks with gitlab CI: <https://blog.mounirmesselmeni.de/pre-commit-your-django-projects>

Ruff

```bash
ruff check --fix
ruff check --watch
ruff format
```

### Testing

To create fixture data for local development you may run (take into consideration that it will clear the current database state):

```bash
manage.py make_dev_data_migrations
```

[Guide](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing).

[Usage of fixtures and mocks](https://dev.to/ifihan/testing-in-django-26e5)

[Django test classes (official doc)](https://docs.djangoproject.com/en/5.2/topics/testing/tools/#provided-test-case-classes)

[REST framework test classes (official doc)](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases)

Usage of `pytest-django`: <https://tamerlan.dev/how-to-test-drf-apis/>

A lot about fixtures with django unittest and pytest: <https://realpython.com/django-pytest-fixtures/>

Dump and load data:

```bash
# Dump
python manage.py dumpdata auth.Group --pk 1 --indent 4 > group.json
# Load
python manage.py loaddata group.json
```

Example of serializers testing: <https://apidog.com/articles/how-to-test-django-rest-framework/>

Questions:

- How to make fixtures?
- Will fixtures affect database?


Django uses `unittest` for testing.

Run tests

```bash
python3 manage.py test
python3 manage.py test --verbosity 2 # 0, 1 (default), 2 or 3
python3 manage.py test --parallel auto

# Run the specified module
python3 manage.py test catalog.tests.test_models
# Run the specified class
python3 manage.py test catalog.tests.test_models.YourTestClass
# Run the specified method
python3 manage.py test catalog.tests.test_models.YourTestClass.test_one_plus_one_equals_two

# With pytest
pytest
```

If you use `addopts = --reuse-db` in `pytest.ini`, you have to run `pytest --create-db` to force re-creation of the test database after changing its schema.

pytest isntallation:

```bash
pip install pytest
pip install pytest-django
```

pytest doc for django: <https://pytest-django.readthedocs.io/_/downloads/en/stable/pdf/>

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
