
class Producer:
   
  async def producer(self):
    yield "started producer"
    for i in range(0, 100):
      for connection in self.connections:
        
        await connection.asend(i)
        

class Consumer:
    
  async def consumer(self):
    yield "started consumer"
    while True:
      for connection in self.producers:
        item = yield 0
        print("item", item)



async def do():
  producers = []
  consumers = []
  for i in range(0, 10):
    producers.append(Producer())
  for i in range(0, 10):
    consumers.append(Consumer())
  
  prodawait = []
  consumeawait = []
  for b in consumers:
    cons = b.consumer()
    await cons.__anext__()
    consumeawait.append(cons)
  for a in producers:
    prod = a.producer()
    prodawait.append(prod)
    await prod.__anext__()

    
  for producer in producers:
    producer.connections = consumeawait
  for consumer in consumers:
    consumer.producers = prodawait
  

  while True:
    for consumer in consumeawait:
      
      for item in prodawait:
        await item.__anext__()
      await consumer.__anext__()

import asyncio
asyncio.run(do())