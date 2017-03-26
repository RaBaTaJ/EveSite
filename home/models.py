from django.db import models

# Create your models here.
class HomeNotice(models.Model):
    PubDate = models.DateTimeField("Date & Time")
    TextContent = models.TextField("Content")
    Author = models.CharField("Author", max_length=50)

    def __str__(self):
        return str(self.PubDate)