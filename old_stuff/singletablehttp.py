import requests
import json
import datetime
# from azure.storage.table import TableService, Entity
# table_service = TableService(account_name='gregseon4e059a98c11c',\
#     account_key='yE7Kuy0xVxUDR+wHGoWPjSpOhFO9WLd9b+t3+RI9C8tuBNbuLwEtWSQGERiO7LJRE1cFTGB0/TT4+CYGhtMfww==')
# if not table_service.exists('Test'):
#     table_service.create_table('Test')
# new_entity = Entity()
# new_entity.PartitionKey = "hello"
# new_entity.RowKey = "hello"
# new_entity.Sellerid = "hello"
# new_entity.ProductName = "hello"
# new_entity.SalePrice = "hello"
# new_entity.TransactionDate = "hello"
# table_service.insert_or_replace_entity('Test',new_entity)

tbendpoint = "https://gregseon4e059a98c11c.table.core.windows.net/"
tblname = "Test"
sas = "?sv=2017-04-17&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-11-30T08:49:46Z&st=2017-11-18T00:49:46Z&spr=https&sig=XL0n1GIAFRslWdTOZY8ivSqK7hQqW7SZXpLHCWrUSmw%3D"
data = json.dumps({"PartitionKey":"Hello","RowKey":"12444","Tomatoes":"yes"})
# headers = {'Authorization': "sv=2017-04-17&tn=Test&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-11-30T08:30:31Z&st=2017-11-18T00:30:31Z&sip=190.213.155.82&spr=https&sig=7PbNgkMzWeEGJ%2B3KDJCD4txfv6NgkrsiVO9h3C41hxM%3D",\
            # 'Content-Type':'application/json;odata=nometadata','Content-Length':str(len(data))}
headers = {'Content-Type':'application/json;odata=nometadata','Content-Length':str(len(data)),'Prefer':'return-no-content'}
uri = tbendpoint + tblname + sas
r = requests.post(uri,headers=headers,data=data)
print(r)


