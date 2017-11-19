import time
import random
import json
import asyncio
from aiohttp import ClientSession
from sastoken import get_auth_token
from config import queuename, tablename

#generate token for https comms
sas = get_auth_token("gregseon4e059a98c11c",queuename,"RootManageSharedAccessKey","d8PrqA7to95t0wUFywAfhNDcbUwvh2sIpiHqvUdbPSQ=")

async def tblwrite(msg,session):
    ''' Write message to table '''
    uri = "https://gregseon4e059a98c11c.table.core.windows.net/" + tablename + "?sv=2017-04-17&ss=bfqt&srt=sco&sp=rwdlacup&se=2017-11-30T08:49:46Z&st=2017-11-18T00:49:46Z&spr=https&sig=XL0n1GIAFRslWdTOZY8ivSqK7hQqW7SZXpLHCWrUSmw%3D"
    tid = str(msg["TransactionID"])
    suid = str(msg["UserId"]) + str(msg["SellerID"]) 
    data = json.dumps({"PartitionKey":tid,"RowKey": suid, "message":str(msg)})
    headers = {'Content-Type':'application/json;odata=nometadata','Content-Length':str(len(data)),'Prefer':'return-no-content'}
    async with session.post(uri,headers=headers,data=data) as response:
        if response.status == 409 or response.status == 204:
            pass  # this means it was either duplicate key pairs or inserted fine
        else:
            asyncio.sleep(5) # circuit breaker like approach that accepts that the message failed to be sent immediately and waits before resending same message.
            await tblwrite(msg,session)
        return response.status


async def getmsg(session):
    ''' send message async '''
    global sas
    headers = {'Authorization':sas["token"], 'Content-Type': \
              'application/atom+xml;type=entry;charset=utf-8'}
    URL = "https://gregseon4e059a98c11c.servicebus.windows.net/"+queuename+"/messages/head"
    async with session.delete(URL, headers=headers) as response:
        if response.status not in (200,204):
            # add another read if https breaks downs for this read.
            # Message should still be in queue and unlocked for another competing consumer.
            await getmsg(session)
        elif response.status == 204: # means queue empty and nothing to write to table. return now
            return None
        else: # means message recieved
            msg = json.loads([x async for x in response.content][0].decode())
            await tblwrite(msg, session)
        return await response.read()

async def boundgetmsg(sem, session):
    ''' async semaphore '''
    async with sem:
        await getmsg(session)

async def run(r):
    ''' kicks off the asynchronous generation of the post requests '''
    sem = asyncio.Semaphore(1000)
    tasks = []
    async with ClientSession() as session:
        for _ in range(r):
            task = asyncio.ensure_future(boundgetmsg(sem, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses       

def readqueue(num_messages):
    N = num_messages
    LOOP = asyncio.get_event_loop()
    FUTURE = asyncio.ensure_future(run(N))
    LOOP.run_until_complete(FUTURE)
    return


