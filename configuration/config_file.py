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
start_date = '02-09-2019'
course_weeks = '15'
ideal_grading = '8'
max_final_score = '10'
min_score_to_pass= "5"


# GLOBAL VARIABLES
is_config_files_set = False
monday_start_week = ""

uploaded_students = set()
registered_students = set()
identified_students = set()

uploaded_activities = set()
qualifying_activities = set()
active_activities = set()
resources = {'week':0}

created_planets = set()
planet_users ={}
plenet_meetings = {}
teacher_list = set()
active_meetings = {}
weeks_array = []

activities_headers_file = ['_id','name','section','week','weight']
students_headers_file =  ['_id','first_name','last_name','username','planet']
messages_type = {'TEXT': 0, 'IMAGE': 0, 'VIDEO': 0, 'VOICE': 0,
        'STICKER': 0, 'GIF': 0, 'DOCUMENT': 0, '_TOTAL':0}
teacher_criteria = [
  'T_Vocalización',
  'T_Dominio del tema',
  'T_Cercanía',
  'T_Atención a la audiencia',
  'T_Claridad en las expresiones',
  'C_Calidad de las transparencias',
  'C_Calidad de los ejemplos',
  'C_Contenidos adaptados al nivel'
  ]

autoeva_questions_list = []

ADD_ACT_NAME, ADD_ACT_SECTION, ADD_ACT_WEEK, ADD_ACT_WEIGHT, ADD_ACT_SAVE = range(5)

ADD_STU_NAME = range(1)