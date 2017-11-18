import requests
import json
headers = {'Authorization':'SharedAccessSignature sr=https%3A%2F%2Fgregseon4e059a98c11c.servicebus.windows.net%2Ftest4scaling&sig=yFfu901g1/W10N5l4LyCZjGAIriLZhoxrjZFbQRoN04%3D&se=1512602004&skn=RootManageSharedAccessKey',
        'Content-Type':'application/json'}
data = "this is a message"
for _ in range(100):
    r = requests.post("https://gregseon4e059a98c11c.servicebus.windows.net/test4scaling/messages/head",headers=headers)
    print(r.content)