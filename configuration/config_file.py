from pymongo import MongoClient

# DB CONNECTION
server_DB = "mongodb+srv://user:Password@cluster0-mpfq1.mongodb.net/test?retryWrites=true&w=majority"
name_DB = "__EDUTRACK"
client = MongoClient(server_DB, connectTimeoutMS=30000)
db = client.get_database(name_DB)

# BOT DATA
token_bot = "812280671:AAHjmwHoa5G0xZsznBFkuR2xi1kQcXVHWpc"
teacher_data = {
  "_id":"706831578",
  "telegram_name": "Jovas Pruebas",
  "user_name": "user_test_0",
}