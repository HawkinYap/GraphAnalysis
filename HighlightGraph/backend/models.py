from django.db import models

# Create your models here.
class Rectangle(models.Model):
    name = models.CharField(max_length= 50)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()

    def __str__(self):
        return "{" + "name: {0}, x1: {1}, y1: {2}, x2: {3}, y2: {4}".format(self.name, self.x1, self.y1, self.x2, self.y2) + "}"