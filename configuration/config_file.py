from pymongo import MongoClient

# DB CONNECTION
server_DB = "mongodb+srv://user:Password@cluster0-mpfq1.mongodb.net/test?retryWrites=true&w=majority"
#name_DB = "__EDUTRACK"
name_DB = "A"
client = MongoClient(server_DB, connectTimeoutMS=30000)
db = client.get_database(name_DB)

# EDUtrack DATA
token_bot = "812280671:AAFmBZPmb7KqE41W5AaRPlnokPiNS4UX94Y"
teacher_data = {
  "_id":"706831578",
  "telegram_name": "Jovas Pruebas",
  "username": "user_test_0",
}
subject_name = "Fundamentos del Software"
subject_id = "FS1819C"
start_date = '01-08-2019'
course_weeks = '15'

# GLOBAL VARIABLES
is_config_files_set = False

uploaded_students = set()
registered_students = set()
identified_students = set()

uploaded_activities = set()
qualifying_activities = set()
activities_sections = set()
activities_for_section = {}
active_activities = set()

created_planets = set()
teacher_list = set()
meeting = {"active": False, "planet": "", "number": ''}
meetings_array = []
weeks_array = []

activities_headers_file = ['_id','name','section','week','weight']
students_headers_file =  ['_id','first_name','last_name','username','planet']
messages_type = {'TEXT': 0, 'IMAGE': 0, 'VIDEO': 0, 'VOICE': 0,
        'STICKER': 0, 'GIF': 0, 'DOCUMENT': 0, '_TOTAL':0}
teacher_criteria = [
  'D_Vocalizacion',
  'D_Dominio del tema',
  'D_Cercanía',
  'D_Atención a la audiencia',
  'D_Claridad en las expresiones',
  'C_Calidad de las transparencias',
  'C_Calidad de los ejemplos',
  'C_Contenidos adaptados al nivel'
  ]

autoeva_questions_list = []