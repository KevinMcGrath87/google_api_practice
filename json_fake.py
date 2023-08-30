
import requests
import json

api_url = "https://jsonplaceholder.typicode.com/todos/10"
response = requests.get(api_url)
print(response.json())

todo = {"userId": 1, "title": "Wash car", "completed": True}

# must send the body in this case as json parameter and not serialize....I think...
response = requests.put(api_url, json=todo)
print(response.status_code)
print(response.json())


