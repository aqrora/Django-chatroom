from django.test import TestCase
from django.urls import reverse
import json
from .lib import verify_jwt_token
from .models import User, Message

# TODO rewrite tests
# Create your tests here.
# class MyViewTestCase(TestCase):
    
    # def test_view_returns_200(self):
    #     url = reverse('chat:chat_room')
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('messages', response.context)
    #     self.assertIn('current_user', response.context)


    # def test_login_view(self):
    #     url = reverse('chat:login')
    #     payload = {
    #         "username": "testuser" 
    #     } # payload isn't working, TODO fix
    #     response = self.client.post(url, data = json.dumps(payload), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     json_response = json.loads(response.content)
    #     print(json_response)
    #     token = json_response.get('token', None)
    #     self.assertIsNotNone(token)


    #     self.assertEqual(type(verify_jwt_token(token)), User)



