import requests

headers = {'Authorization':'SharedAccessSignature sr=https%3A%2F%2Fgregseon4e059a98c11c.servicebus.windows.net%2Ftest4scaling&sig=yFfu901g1/W10N5l4LyCZjGAIriLZhoxrjZFbQRoN04%3D&se=1512602004&skn=RootManageSharedAccessKey',
        'Content-Type':'application/json'}
r = requests.get("https://management.core.windows.net/d494b561-b40d-4b16-a8d1-d4a6bdcf54b2/services/servicebus/NameSpaces/gregseon4e059a98c11c/Queues/test4scaling/Metrics")
print(r)