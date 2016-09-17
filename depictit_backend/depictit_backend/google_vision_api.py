from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


class GoogleVisionApi:
    def _login_google_vision(credentials_path=''):
        """
        Logins with Google Vision API.
        :return: the vision_service
        """
        credentials = GoogleCredentials.get_application_default()
        if not credentials and not credentials_path:
            credentials = GoogleCredentials.from_json(credentials_path)
        service = discovery.build('vision', 'v1', credentials=credentials,
                                  discoveryServiceUrl=DISCOVERY_URL)
        return service

    def _login_google_storage(credentials_path=''):
        """
        Logins with Google Vision API.
        :return: the storage_service
        """
        credentials = GoogleCredentials.get_application_default()
        if not credentials and not credentials_path:
            credentials = GoogleCredentials.from_json(credentials_path)
        service = discovery.build('storage', 'v1', credentials=credentials)
        return service

    def __init__(self):
        self.vision_service = self._login_google_vision()
        self.storage_service = self._login_google_storage()

    def get_photos(self, bucket_name='bucket'):
        """
        Get all photos from the specified bucket.
        :param bucket_name: The name of the bucket.
        :return:
        """
        fields_to_return = 'nextPageToken,items(name,size,contentType)'
        req = self.storage_service.objects().list(bucket=bucket_name, fields=fields_to_return)
        all_objects = []
        # If you have too many items to list in one request, list_next() will
        # automatically handle paging with the pageToken.
        while req:
            resp = req.execute()
            all_objects.extend(resp.get('items', []))
            req = self.storage_service.objects().list_next(req, resp)
        return all_objects


    def get_photo_desc_from_cloud_storage(self, filename):
        service_request = self.service.images().annotate(body={
         "requests": [
          {
           "features": [
            {
             "type": "LABEL_DETECTION",
             "maxResults": 5,
            }
           ],
           "image": {
            "source": {
             "gcsImageUri": filename
            }
           }
          }
         ]
        })

        response = service_request.execute()
        tags = []
        for l in response['responses']:
            for a in l['labelAnnotations']:
                tags.append(a['description'])
        return tags


    def get_photo_desc_from_base64(self, img_filename):
        with open(img_filename, 'rb') as image:
            import base64
            image_content = base64.b64encode(image.read())
            service_request = self.vision_service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
            }]
        })
        response = service_request.execute()
        tags = []
        for l in response['responses']:
            for a in l['labelAnnotations']:
                tags.append(a['description'])
        return tags

