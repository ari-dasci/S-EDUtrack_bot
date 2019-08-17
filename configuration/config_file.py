from pymongo import MongoClient

# DB CONNECTION
server_DB = "mongodb+srv://user:Password@cluster0-mpfq1.mongodb.net/test?retryWrites=true&w=majority"
name_DB = "__EDUTRACK"
client = MongoClient(server_DB, connectTimeoutMS=30000)
db = client.get_database(name_DB)

# BOT DATA
token_bot = "812280671:AAFmBZPmb7KqE41W5AaRPlnokPiNS4UX94Y"
teacher_data = {
  "_id":"706831578",
  "telegram_name": "Jovas Pruebas",
  "username": "user_test_0",
}

# GLOBAL VARIABLES
is_config_files_set = False
meeting = {"active": False, "planet": "", "number": ''}
uploaded_students = set()
verified_students = set()
uploaded_activities = set()
qualifying_activities = set()