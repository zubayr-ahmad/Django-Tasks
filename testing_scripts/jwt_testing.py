import requests

# Get JWT tokens
response = requests.post(
    'http://127.0.0.1:8000/accounts/jwt/login/',
    data={'username': 'zubair', 'password': 'zubair'}
)
tokens = response.json()
access_token = tokens['access']

# Test protected endpoint
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://127.0.0.1:8000/library/books/', headers=headers)
print(response.json())

# Test without token
response = requests.get('http://127.0.0.1:8000/library/books/')
print(response.status_code)  # Should be 401