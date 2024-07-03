from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.BinaryField(null=False)

    class Meta:
        db_table = 'image'


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2000)
    shortDescription = models.CharField(max_length=400, db_column='short_description', null=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id')
    date = models.DateField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, db_column='image_id')

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.title
