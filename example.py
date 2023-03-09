import requests

url = "http://localhost/rw/rapid/symbol/data/RAPID/T_ROB1/Module1/offX?action=set"
username = "Default User"
password = "robotics"
data = {"value": "666"}

response = requests.post(url, auth=requests.auth.HTTPDigestAuth(username, password), data=data)

print(response.text)