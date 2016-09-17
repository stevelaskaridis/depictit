import os
import sys
import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import *

@api_view(['GET', 'POST'])
def webhook(request):
    log(request.data)
    if request.method == 'GET':
        if request.query_params['hub.mode'] == "subscribe" and request.query_params['hub.challenge']:
            if not request.GET.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
                return Response("Verification token mismatch", status=403)
        return Response(int(str(request.query_params['hub.challenge']).replace('"', '')), status=200)
    elif request.method == 'POST':
        return Response({"message": "OK!"}, status=200)

#     # endpoint for processing incoming messaging events
#
#     # data = request.get_json()
#     data = request.body
#     log(
#         data)  # you may not want to log every incoming message in production, but it's good for testing
#
#     if data["object"] == "page":
#
#         for entry in data["entry"]:
#             for messaging_event in entry["messaging"]:
#
#                 if messaging_event.get("message"):  # someone sent us a message
#
#                     sender_id = messaging_event["sender"][
#                         "id"]  # the facebook ID of the person sending you the message
#                     #    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
#                     message_text = messaging_event["message"]["text"]  # the message's text
#                     if message_text == "Start game":
#                         send_message(sender_id, "Choose the number of the players")
#                     if message_text == "Hi":
#                         send_message(sender_id, "Hi")
#                     if message_text.isdigit():
#                         send_message(sender_id, "Starting game with " + message_text + " players")
#
#                 if messaging_event.get("delivery"):  # delivery confirmation
#                     pass
#
#                 if messaging_event.get("optin"):  # optin confirmation
#                     pass
#
#                 if messaging_event.get(
#                         "postback"):  # user clicked/tapped "postback" button in earlier message
#                     pass
#
#     return "ok", 200
#
#
def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers,
                      data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

@api_view(['POST'])
def copy_to_env(request):
    from shutil import copyfile
    import os.path

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    copyfile(os.path.join(PROJECT_ROOT, '../to_be_revoked/GoogleAPI.json'), os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    return Response("OK", status=200)


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
