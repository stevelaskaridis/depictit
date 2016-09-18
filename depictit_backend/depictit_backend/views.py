import os
import sys
import json
import requests
import random
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from models import *
from django.conf import settings
from messenger_utils import send_message, send_generic_template_message
from google_vision_api import GoogleVisionApi

@api_view(['GET', 'POST'])
def webhook(request):
    log(request.data)
    if request.method == 'GET':
        if request.query_params['hub.mode'] == "subscribe" and request.query_params['hub.challenge']:
            if not request.GET.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
                return Response("Verification token mismatch", status=403)
        return Response(int(str(request.query_params['hub.challenge']).replace('"', '')), status=200)
    elif request.method == 'POST':
        text = request.data['entry'][0]['messaging'][0]['message']['text']
        timestamp = request.data['entry'][0]['time']
        sender_id = request.data['entry'][0]['messaging'][0]['sender']['id']

        if str(text).lower() == 'new game':
            send_message(sender_id, 'How many teams?')
        elif text.isdigit() and int(text) > 1:
            no_players = int(text)
            _create_game(sender_id, no_players)
            selection = random.randint(0, 9)
            gv = GoogleVisionApi()
            send_generic_template_message(sender_id,
                                          'Selection #{selection}'.format(selection=selection+1), "https://fierce-tor-62927.herokuapp.com/static/{selection}.jpg".format(selection=selection),
                                          "Don't use the words: " + ", ".join(gv.get_photo_desc_from_cloud_storage("gs://hack_zurich_bucket/{selection}.jpg".format(selection=selection))), [])
        return Response({"message": "OK!"}, status=200)


# def send_message(recipient_id, message_text):
#     log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
#
#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "text": message_text
#         }
#     })
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers,
#                       data=data)
#     if r.status_code != 200:
#         log(r.status_code)
#         log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

@api_view(['POST'])
def gen_gc(request):
    export_filename = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    secure_cred = json.dumps({
      "type": os.environ["type"],
      "project_id": os.environ["project_id"],
      "private_key_id": os.environ["private_key_id"],
      "private_key": os.environ["private_key"].replace('\\n', os.linesep),
      "client_email": os.environ["client_email"],
      "client_id": os.environ["client_id"],
      "auth_uri": os.environ["auth_uri"],
      "token_uri": os.environ["token_uri"],
      "auth_provider_x509_cert_url": os.environ["auth_provider_x509_cert_url"],
      "client_x509_cert_url": os.environ["client_x509_cert_url"],
    })
    with open(export_filename, 'w') as f:
      f.write(secure_cred)
    return Response("OK!", status=200)

# class FileUploadView(APIView):
#     parser_classes = (FileUploadParser,)
#
#     def put(self, request, filename, format=None):
#         from django.core.files.storage import default_storage
#         from django.core.files.base import ContentFile
#         file_obj = request.FILES['file']
#
#         path = default_storage.save('tmp/'+filename, ContentFile(file_obj.read()))
#         from shutil import copyfile
#         copyfile(os.path.join(settings.MEDIA_ROOT, path), os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
#         return Response(status=204)


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

