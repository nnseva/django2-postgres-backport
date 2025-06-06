[![Tests with postgres9.6](https://github.com/nnseva/django2-postgres-backport/actions/workflows/test-postgres9.yml/badge.svg)](https://github.com/nnseva/django2-postgres-backport/actions/workflows/test-postgres9.yml)
[![Tests with postgres12](https://github.com/nnseva/django2-postgres-backport/actions/workflows/test-postgres12.yml/badge.svg)](https://github.com/nnseva/django2-postgres-backport/actions/workflows/test-postgres12.yml)
[![Tests with postgres14](https://github.com/nnseva/django2-postgres-backport/actions/workflows/test-postgres14.yml/badge.svg)](https://github.com/nnseva/django2-postgres-backport/actions/workflows/test-postgres14.yml)

# Django2-Postgres-Backport

The collection of backports for the Django v2.x using modern PostgreSQL features

# Installation

Latest version from the GIT repository:

    pip install "git+git://github.com/nnseva/django2-postgres-backport.git"

Stable version from the PyPi repository:

    pip install django2-postgres-backport

## Using modern versions of the psycopg package

The modern versions of the `psycopg` package allow using modern PostgreSQL database versions.
The patch makes the Django v2.x code compatible with the modern `psycopg` package versions.

### Using

Use the following code in `settings.py` to patch the Django v2.x code:

```python
from django2_postgres import psycopg_patch

psycopg_patch.fix()
```

### Safe transfer to the modern Django versions

The patch code is version-dependent and just does nothing for the modern Django versions.

## Fix reversed coordinates in GeoJSON generated by the GEOSGeometry

The old Django versions have a contributed OGR library version which is not fully compatible
with the modern OSes. The main sympthom of such incompatibility is wrong Django-provided
generation of GeoJSON data for geometry fields (reversed order of coordinates).

### Using

Use the following code in `settings.py` to patch the Django code (v2.x-3.0):

```python
from django2_postgres import geos_patch

geos_patch.fix_geojson()
```

### Safe transfer to the modern Django versions

The patch code determines the issue presence and just does nothing for the modern Django versions.

## Add/Remove Index Concurrently

Introduce running Add and Remove PostgreSQL indexes [concurrently](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY)
as it is [available in the Django version >= 3](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/operations/#concurrent-index-operations)

### Index declaration

Use the modern syntax in your model to declare indexes, for example:

```python
class MyModel(models.Model):
    field1 = models.CharField(max_length=10)
    field2 = models.charField(max_length=10)
    class Meta:
        indexes = [
            models.Index(fields=['field1', 'field2'], name='my_index'),
        ]
```

### Automatic creation of a migration

Create a migration as usual, for example:

```sh
python manage.py makemigrations mypackage
```

### Manual updating of the migration file

Modify a migration to use the CREATE INDEX CONCURRENTLY manually.

- import the backport
- mark the migration as non-atomic
- replace the `AddIndex` by the `AddIndexConcurrently`
- replace the `RemoveIndex` by the `RemoveIndexConcurrently`

For example:

```python
# Generated by Django 2.2.5 on 2025-05-26 13:51

from django.db import migrations, models
# -- import the backport
from django2_postgres import operations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]
# -- The concurrent index creation can be only in non-atomic migration
    atomic = False

    operations = [
# -- We remove the originally generated operation ...
#        migrations.AddIndex(
#            model_name='mymodel',
#            index=models.Index(fields=['field1', 'field2'], name='my_index'),
#        ),
# -- And replace it by a modified one
        operations.AddIndexConcurrently(
            model_name='mymodel',
            index=models.Index(fields=['field1', 'field2'], name='my_index'),
        ),
    ]

```

### Side effects

Using concurrent index creation has its own side effects described in the
[Django documentation](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/operations/#concurrent-index-operations), and
in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY),
please read it carefully.

The backport doesn't add any additional side effects.

### Safe transfer to the modern Django versions

The modern Django versions (>=3.0) have
[originally provided](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/operations/#concurrent-index-operations)
versions of these functions.

The backport files are version-dependent and provide original Django operations instead of backported, when the version of the Django is upgraded.
Therefore, you can use all your old migrations without any changes when transfer your code to the new Django version.
