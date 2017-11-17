import time
import random
import json
import asyncio
from aiohttp import ClientSession
from sastoken import get_auth_token

sas = get_auth_token("gregseon4e059a98c11c","test4scaling","RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")



async def getmsg(session):
    ''' send message async '''
    global sas
    headers = {'Authorization':sas["token"],'Content-Type': 'application/atom+xml;type=entry;charset=utf-8'}
    URL = "https://gregseon4e059a98c11c.servicebus.windows.net/test4scaling/messages/head"
    async with session.post(URL, headers=headers) as response:
        assert response.status == 201
        print([x async for x in response.content][0])
        msg = json.loads(response.headers.get("BrokerProperties"))
        print(msg["LockToken"])
        print(msg["MessageId"])
        return await response.read() 

async def boundgetmsg(sem, session):
    ''' async semaphore '''
    async with sem:
        await getmsg(session)

async def run(r):
    ''' kicks off the asynchronous genration of the post requests '''
    sem = asyncio.Semaphore(1000)
    tasks = []
    async with ClientSession() as session:
        for _ in range(r):
            task = asyncio.ensure_future(boundgetmsg(sem, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses       

N = 20
LOOP = asyncio.get_event_loop()
FUTURE = asyncio.ensure_future(run(N))
LOOP.run_until_complete(FUTURE)
print(N)
