from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=50)
    age = models.SmallIntegerField()
    team = models.ForeignKey(Team)

class Team(models.Model):
    add_date = models.DateTimeField('date added')
    owner = models.CharField(max_length=50)
