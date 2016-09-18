from django.db import models
from django.db.models import Max

class Player(models.Model):
    session_id = models.CharField(max_length=50)

class Game(models.Model):
    owner = models.OneToOneField(Player, unique=True, primary_key=True)
    turn = models.IntegerField(default=0)
    no_players = models.IntegerField(default=2)

    def increment_turn(self):
      self.turn = self.turn+1 % self.no_players
      self.save()

    def evaluate_winner(self):
      return Scoreboard.objects.all().filter(game=self).aggregate(Max('team_score')).team_number


class Scoreboard(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team_number = models.IntegerField()
    team_score = models.IntegerField()


