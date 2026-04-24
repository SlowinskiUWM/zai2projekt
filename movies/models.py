from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

