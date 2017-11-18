import time
import random
import json
import asyncio
from aiohttp import ClientSession
from sastoken import get_auth_token

sas = get_auth_token("gregseon4e059a98c11c","test5scaling","RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")

async def delfromqueue(msgid,lockid,session):
    global sas
    headers = {'Authorization':sas["token"],'Content-Type': 'application/atom+xml;type=entry;charset=utf-8'}
    URL = "https://gregseon4e059a98c11c.servicebus.windows.net/test5scaling/messages/" + str(msgid) + "/" + str(lockid)
    async with session.delete(URL, headers=headers) as response:
        if response.status != 200:
            asyncio.sleep(5)
            await delfromqueue(msgid,lockid,session)


async def tblwrite(msg,session, id):
    uri = "https://gregseon4e059a98c11c.table.core.windows.net/" + "Test" +\
           "?sv=2017-04-17&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-11-30T08:49:46Z&st=2017-11-18T00:49:46Z&spr=https&sig=XL0n1GIAFRslWdTOZY8ivSqK7hQqW7SZXpLHCWrUSmw%3D"
    data = json.dumps({"PartitionKey":"Transactions","RowKey":id,"message":msg})
    headers = {'Content-Type':'application/json;odata=nometadata','Content-Length':str(len(data)),'Prefer':'return-no-content'}
    async with session.post(uri,headers=headers,data=data) as response:
        if response.status != 204:
             asyncio.sleep(5)
             await tblwrite(msg,session, id)
        return await response.status


async def getmsg(session, id):
    ''' send message async '''
    global sas
    headers = {'Authorization':sas["token"],'Content-Type': 'application/atom+xml;type=entry;charset=utf-8'}
    URL = "https://gregseon4e059a98c11c.servicebus.windows.net/test5scaling/messages/head"
    async with session.post(URL, headers=headers) as response:
        if response.status != 201:
            await getmsg(session, id) # add another read if https breaks downs for this read. Message should still be in queue and unlocked for another competing consumer.
        msg = json.dumps([x async for x in response.content][0])
        msginfo = json.loads(response.headers.get("BrokerProperties"))
        status = await tblwrite(msg, session, id)
        if status == 204:
            await delfromqueue(msginfo["MessageId"],msginfo["LockToken"],session)
        return await response.read() 

async def boundgetmsg(sem, session, id):
    ''' async semaphore '''
    async with sem:
        await getmsg(session, id)

async def run(r):
    ''' kicks off the asynchronous genration of the post requests '''
    sem = asyncio.Semaphore(1000)
    tasks = []
    async with ClientSession() as session:
        for id in range(r):
            task = asyncio.ensure_future(boundgetmsg(sem, session, id))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses       

N = 100
LOOP = asyncio.get_event_loop()
FUTURE = asyncio.ensure_future(run(N))
LOOP.run_until_complete(FUTURE)
print(N)
