from django.db import models

# Create your models here.
class Username(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    sex = models.CharField(max_length= 10)
    age = models.IntegerField()
    education = models.CharField(max_length=20)
    research = models.CharField(max_length=100)

class Duration(models.Model):
    did = models.AutoField(primary_key=True)
    time = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    consumingtime = models.IntegerField()
    username = models.ForeignKey('Username', on_delete=models.CASCADE, default='')

class Rectangle(models.Model):
    rid = models.AutoField(primary_key=True)
    time = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()
    username = models.ForeignKey('Username', on_delete=models.CASCADE, default='')
    duration = models.ForeignKey('Duration', on_delete=models.CASCADE, default='')

#     def __str__(self):
#         return "{" + "name: {0}, x1: {1}, y1: {2}, x2: {3}, y2: {4}".format(self.name, self.x1, self.y1, self.x2, self.y2) + "}"