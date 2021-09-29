from django.db import models


class AboutAuthorView(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
