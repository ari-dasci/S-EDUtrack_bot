standby_teachers = False
config_files_set = False
monday_start_week = ""

subject_data = {
  "name": "Fundamentos del Software",
  "_id": "FS1920",
  "start_date": "09/07/2020",
  "num_weeks": "15",
  "max_final_grade": "10",
  "min_grade_to_pass": "5",
  "min_ideal_grade": "7.5",
}

teacher_data = {
  "_id": "970331050",
  "telegram_name": "Profesor Edutrack",
  "username": "Profesor_Edutrack",
  "email": "escribeleaqui@gmail.com",
  "is_teacher": 1,
  "language": "es",
}

activities_headers_file = [
  "_id",
  "name",
  "section",
  "week",
  "weight",
  "visible",
  "category",
]

students_headers_file = ["email", "first_name", "last_name", "username", "planet"]

list_config_files = [
  "students_format.csv",
  "add_students_format.csv",
  "replace_students_format.csv",
  "activities_format.csv",
  # "add_activities.csv",
  "replace_activities_format.csv",
]

tables = [
  {
    "name": "telegram_users",
    "fields": """
              _id INTEGER NOT NULL PRIMARY KEY,
              telegram_name	TEXT NOT NULL,
              username	TEXT NOT NULL UNIQUE,
              is_teacher	INTEGER NOT NULL DEFAULT 0,
              language	TEXT DEFAULT 'en'
              """,
  },
  {
    "name": "teachers",
    "fields": """
              _id	INTEGER NOT NULL PRIMARY KEY,
              telegram_name	TEXT NOT NULL,
              username TEXT NOT NULL UNIQUE,
              email	TEXT,
              FOREIGN KEY(_id) REFERENCES telegram_users(_id)
              """,
  },
  {
    "name": "planets",
    "fields": """
              _id TEXT NOT NULL PRIMARY KEY,
              num_members	INTEGER NOT NULL DEFAULT 0
              """,
  },
  {
    "name": "planet_admins",
    "fields": """
              _id	INTEGER NOT NULL PRIMARY KEY,
              planet	TEXT NOT NULL,
              FOREIGN KEY(_id) REFERENCES telegram_users(_id),
              FOREIGN KEY(planet) REFERENCES planets(_id)
              """,
  },
  {
    "name": "planet_users",
    "fields": """
              _id	INTEGER NOT NULL PRIMARY KEY,
              planet	TEXT,
              FOREIGN KEY(_id) REFERENCES telegram_users(_id),
              FOREIGN KEY(planet) REFERENCES planets(_id)
              """,
  },
  {
    "name": "students_file",
    "fields": """
              email	TEXT NOT NULL PRIMARY KEY,
              first_name	TEXT,
              last_name	TEXT,
              username	TEXT,
              planet	TEXT,
              FOREIGN KEY(username) REFERENCES telegram_users(username)
              FOREIGN KEY("planet") REFERENCES "planets"("_id")
              """,
  },
  {
    "name": "registered_students",
    "fields": """
              _id	INTEGER NOT NULL PRIMARY KEY,
              full_name	TEXT NOT NULL,
              email	TEXT NOT NULL UNIQUE,
              username TEXT NOT NULL UNIQUE,
              planet TEXT,
              FOREIGN KEY(_id) REFERENCES telegram_users(_id),
              FOREIGN KEY(email) REFERENCES students_file(email)
              FOREIGN KEY(username) REFERENCES telegram_users(username)
              FOREIGN KEY("planet") REFERENCES "planets"("_id")
              """,
  },
  {
    "name": "academic_risk_factor",
    "fields": """
              _id INTEGER NOT NULL PRIMARY KEY,
              FOREIGN KEY(_id) REFERENCES telegram_users(_id)
              """,
  },
  {
    "name": "subject_data",
    "fields": f"""
              _id	TEXT NOT NULL PRIMARY KEY,
              name	TEXT NOT NULL,
              start_date	TEXT NOT NULL,
              course_weeks	INTEGER NOT NULL,
              ideal_grading	REAL NOT NULL DEFAULT 10,
              max_final_score	REAL NOT NULL DEFAULT 10,
              min_score_to_pass	REAL NOT NULL DEFAULT 5,
              active_planet_registry	INTEGER NOT NULL DEFAULT 1,
              db_is_loaded	INTEGER NOT NULL DEFAULT 1
              """,
  },
  {
    "name": "activities",
    "fields": f"""
              _id TEXT NOT NULL PRIMARY KEY,
              name TEXT,
              section TEXT,
              week INTEGER DEFAULT 0,
              weight REAL DEFAULT 0,
              visible INTEGER DEFAULT 0,
              category TEXT,
              active INTEGER DEFAULT 0
              """
    "",
  },
]

