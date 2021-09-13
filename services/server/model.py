from pymongo import MongoClient

DATABASE_URL = 'mongodb://localhost:27017/'
client = MongoClient(DATABASE_URL)
db = client['dome2']
users = db['users']
tasks = db['tasks']


######## Db url and path
# MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
# MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
# DATABASE_URL = f'mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@mongo:27017'

