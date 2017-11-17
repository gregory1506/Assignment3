import time
import random
import json
import asyncio
from aiohttp import ClientSession
from sastoken import get_auth_token

sas = get_auth_token("gregseon4e059a98c11c","test4scaling","RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")



async def sendmsg(data,session):
    ''' send message async '''
    global sas
    headers = {'Authorization':sas["token"],'Content-Type':'Content-Type: application/vnd.microsoft.servicebus.json'}
    URL = "https://gregseon4e059a98c11c.servicebus.windows.net/test4scaling/messages"
    async with session.post(URL, data=data, headers=headers) as response:
        assert response.status == 201
        return await response.read() 

async def boundsendmsg(sem, data, session):
    ''' async semaphore '''
    async with sem:
        await sendmsg(data, session)

async def run(r):
    ''' kicks off the asynchronous genration of the post requests '''
    sem = asyncio.Semaphore(1000)
    tasks = []
    products = ["Financial Trap", "Insurance", "Bitcoin", "Timeshares", "Food", "Clothes"]
    async with ClientSession() as session:
        for _ in range(r):
            tmp = []
            for x in range(10):
                userid = "A" + str(random.randint(1,1000))
                sellerid = "S" + str(random.randint(1,1000))
                data = {"TransactionID":int(time.time()),"UserId":userid,'SellerID':sellerid,'ProductName':random.choice(products),"SalePrice":random.randint(1000,1000000),\
                    'TransactionDate':time.strftime("%Y-%m-%d")}
                tmp.append(data)
            task = asyncio.ensure_future(boundsendmsg(sem,json.dumps(tmp), session))
            tasks.append(task)
            asyncio.sleep(0.1)

        await asyncio.gather(*tasks)
N = 200
LOOP = asyncio.get_event_loop()
FUTURE = asyncio.ensure_future(run(N))
LOOP.run_until_complete(FUTURE)
print(N)
