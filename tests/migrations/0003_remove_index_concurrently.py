# Generated by Django 2.2.5 on 2025-05-26 13:58

from django.db import migrations
# -- import the backport
from django2_postgres import operations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_index_concurrently'),
    ]
# -- The concurrent index creation can be only in non-atomic migration
    atomic = False

    operations = [
# -- We remove the originally generated operation ...
#        migrations.RemoveIndex(
#            model_name='mymodel',
#            name='my_index',
#        ),
# -- And replace it by a modified one
        operations.RemoveIndexConcurrently(
            model_name='mymodel',
            name='my_index',
        ),
    ]
