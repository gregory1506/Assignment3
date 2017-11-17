import requests
import json
headers = {'Content-Type':'application/json','Content-Length':'0'}
data = '{"PartitionKey":"Hello","RowKey":12334,"Tomatoes":"yes"}'
tableuri = "https://gregseon4e059a98c11c.table.core.windows.net/Transactions?sv=2017-04-17&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-12-01T03:27:52Z&st=2017-11-17T19:27:52Z&spr=https&sig=XY5q47DIJodmH0e8VKg9kwp8JIXRuFRHr4ZTG9M2eUY%3D"
r = requests.post(tableuri,headers=headers)
print(r)