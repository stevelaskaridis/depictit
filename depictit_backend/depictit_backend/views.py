from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import *

@api_view(['POST'])
def webhook(request):
    return Response({"message": "OK!"})

def _create_game(owner_id, no_players):
  # Search for player with specific owner_id
  player = Player.objects.filter(session_id=owner_id)
  if not player:
    player = Player(session_id=owner_id)
    player.save()
  else:
    player = player[0]
  # Search for game with specific owner_id
  game = Game.objects.filter(owner_id=owner_id)
  if not game:
    game = Game(owner=player, turn=0, no_players=no_players)
    game.save()
    for i in xrange(no_players):
      sb = Scoreboard(game=game, team_number=i, team_score=0)
      sb.save()
  else:
    game = game[0]

  return game
