import time
import random
import json
import asyncio
from aiohttp import ClientSession
from sastoken import get_auth_token
from config import queuename

#generate token for https comms
sas = get_auth_token("gregseon4e059a98c11c",queuename,"RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")

async def sendmsg(data,session):
    ''' send message async '''
    try:
        global sas
        headers = {'Authorization':sas["token"],'Content-Type':'Content-Type: application/vnd.microsoft.servicebus.json'}
        URL = "https://gregseon4e059a98c11c.servicebus.windows.net/"+queuename+"/messages"
        async with session.post(URL, data=data, headers=headers) as response:
            if response.status != 201:
                asyncio.sleep(5) # sort of like a circuit breaker pattern. Wait 5 seconds and retry
                await sendmsg(data, session)
            return await response.read()
    except asyncio.TimeoutError:
        pass 

async def boundsendmsg(sem, data, session):
    ''' async semaphore. A semaphore manages an internal counter which is decremented by each 
        acquire() call and incremented by each release() call. The counter can never go below zero;
        when acquire() finds that it is zero, it blocks, waiting until some other coroutine calls release(). '''
    async with sem:
        await sendmsg(data, session)

async def run(r):
    ''' kicks off the asynchronous genration of the post requests '''
    sem = asyncio.Semaphore(1000)
    tasks = []
    products = ["Financial Trap", "Insurance", "Bitcoin", "Timeshares", "Food", "Clothes"]
    async with ClientSession() as session:
        for _ in range(r):
            userid = "A" + str(random.randint(1,1000))
            sellerid = "S" + str(random.randint(1,1000))
            failure = "no"
            if _ % 50000 == 0: # introducing a failure on every 50000 entry
                failure = "yes"
            data = {"TransactionID":int(time.time()),"UserId":userid,'SellerID':sellerid,'ProductName':random.choice(products),"SalePrice":random.randint(1000,1000000),\
                    'TransactionDate':time.strftime("%Y-%m-%d"),'failure':failure}
            task = asyncio.ensure_future(boundsendmsg(sem,json.dumps(data), session))
            tasks.append(task)
            
        await asyncio.gather(*tasks)
N = 100000
LOOP = asyncio.get_event_loop()
FUTURE = asyncio.ensure_future(run(N))
LOOP.run_until_complete(FUTURE)
print(N)
