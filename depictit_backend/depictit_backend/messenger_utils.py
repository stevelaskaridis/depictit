import requests
import os

# Must be set as an environment variable
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
ENDPOINT = "https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN


def send_message(recipient_user_id, message):
    r = requests.post(ENDPOINT,
                      data={
                          "recipient": {
                              "id": recipient_user_id
                          },
                          "message": {
                              "text": message
                          }
                      })
    return r


def send_generic_template_message(recipient_user_id, title, image_url, subtitle, buttons):
    # buttons = [
    #     {
    #         "type": "web_url",
    #         "url": "https://example.com",
    #         "title": "View Info"
    #     },
    #     {
    #         "type": "postback",
    #         "title": "Start Chatting",
    #         "payload": "DEVELOPER_DEFINED_PAYLOAD"
    #     }
    # ]

    r = requests.post(ENDPOINT, data={
        "recipient": {
            "id": recipient_user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": title,
                            "image_url": image_url,
                            "subtitle": subtitle,
                            "buttons": buttons
                        }
                    ]
                }
            }
        }
    })

    return r
