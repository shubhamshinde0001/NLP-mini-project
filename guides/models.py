from django.db import models

class FirstAidGuide(models.Model):
    title = models.CharField(max_length=255)
    steps = models.JSONField()  # Stores list of steps
    youtube_url = models.URLField()
    category = models.CharField(max_length=100, default="General Pet Guide")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
