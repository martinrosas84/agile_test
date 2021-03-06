import requests
import json
from concurrent import futures
from model.cache import DbConnection

class Tokenizer:

    API_KEY = "23567b218376f79d9415"
    AUTH_URL = "http://interview.agileengine.com/auth"
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self):
        self.token = ""

    def get_auth_token(self):
        response = requests.post(self.AUTH_URL, data=json.dumps({"apiKey": self.API_KEY}), headers=self.HEADERS)
        resp_dict = response.json()
        self.token = "Bearer {}".format( resp_dict['token'])
        return self.token

class Loader:

    def __init__(self):
        self.tokenizer = Tokenizer()
        self.auth_token = self.tokenizer.get_auth_token()
        db = DbConnection()
        db.delete_all()
        db.close()

    def get_page(self, page_number=1):
        '''
        Load one page of images
        params: @page_number: the number of the paginated page
        '''
        url = "http://interview.agileengine.com/images?page={}".format(page_number)
        response = requests.get(url, headers={'Authorization': self.auth_token})
        return response.json()

    def get_pictures(self, page_number):
        '''
        Get all pictures from one page and call to save_image_data
        params: @page_number: the number of the paginated page
        '''
        resp_dict = self.get_page(page_number=page_number)
        with futures.ThreadPoolExecutor(40) as executor:
            executor.map(self.save_image_data, resp_dict['pictures'])
        
    def save_image_data(self, image_data):
        '''
        Save information of the image from the API 
        params: @image_data: The images's information as a dict
        '''
        url = "http://interview.agileengine.com/images/{}".format(image_data['id'])
        response = response = requests.get(url, headers={'Authorization': self.auth_token})
        resp_dict = response.json()
        db = DbConnection()
        db.save_image_data(resp_dict)
        db.close()

    def load_images(self):
        '''
        Entry point: get the first page in order to get the total amount of pictures
        '''
        resp_dict = self.get_page()
        total_count = int(resp_dict['pageCount'])
        with futures.ThreadPoolExecutor(40) as executor:
            executor.map(self.get_pictures, list(range(1, total_count + 1)))
    