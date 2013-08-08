from django.db import models

# Create your models here.
class Team(models.Model):
    add_date = models.DateTimeField('date added')
    owner = models.CharField(max_length=50)
    
    def __str__(self):
        return "Owner: %s" % self.owner

class Player(models.Model):
    name = models.CharField(max_length=50)
    age = models.SmallIntegerField()
    team = models.ForeignKey(Team)

    def __str__(self):
        return "Name: %s Team: %s" % (self.name,self.team)
