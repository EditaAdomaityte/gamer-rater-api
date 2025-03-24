from django.db import models
from django.contrib.auth.models import User

class Game(models. Model):
    title=models.CharField(max_length=155)
    description=models.CharField(max_length=300)
    designer=models.CharField(max_length=155)
    year_released=models.CharField(max_length=10)
    number_of_players=models.CharField(max_length=155)
    play_time=models.CharField(max_length=155)
    recommended_age=models.CharField(max_length=155)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    categories= models.ManyToManyField("Category", through='GameCategory', related_name='games')