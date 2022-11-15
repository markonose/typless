import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:example@localhost:27017')
db = client.documents
