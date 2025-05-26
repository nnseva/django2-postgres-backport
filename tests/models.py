from django.db import models
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    field1 = models.CharField(max_length=10)
    field2 = models.CharField(max_length=10)
    class Meta:
        pass
# -- to generate the third migration we removed the index
# -- to generate the second migration we added an index
#        indexes = [
#            models.Index(fields=['field1', 'field2'], name='my_index'),
#        ]
