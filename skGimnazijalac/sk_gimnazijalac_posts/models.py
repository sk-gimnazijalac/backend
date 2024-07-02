from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2000)
    shortDescription = models.CharField(max_length=400, db_column='short_description', null=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id')
    date = models.DateField()
    src = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.title
