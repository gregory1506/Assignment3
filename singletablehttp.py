import requests
import json
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
data = json.dumps({"PartitionKey":"Hello","RowKey":"12334","Tomatoes":"yes"})
headers = {'Authorization': "?sv=2017-04-17&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-11-30T08:24:02Z&st=2017-11-18T00:24:02Z&sip=0.0.0.0&spr=https&sig=BhtbROIi5eRVHsqGlk8ZxFG7RKc8PKdVvHqDyBym%2FW4%3D",\
            'Content-Type':'application/json','Content-Length':str(len(data))}
tableuri = "https://gregseon4e059a98c11c.table.core.windows.net/"
r = requests.post(tableuri,headers=headers)
print(r)