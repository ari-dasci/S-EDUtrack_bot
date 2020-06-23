import collections

subject_data = {
  "name": "Fundamentos del Software",
  "_id": "FS1920",
  "start_date": "07/09/2020",
  "max_final_grade": "10",
  "min_grade_to_pass": "5",
  "min_ideal_grade": "7.5",
}

teacher_data = {
  "id_telegram": "970331050",
  "telegram_name": "Profesor Edutrack",
  "username": "Profesor_Edutrack",
  "email": "escribeleaqui@gmail.com",
  "is_teacher": 1,
  "language": "es",
}

config_files_set = False

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
    "name": "planets",
    "fields": """
              _id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
              name	TEXT NOT NULL,
              num_members	INTEGER NOT NULL DEFAULT 0
              """,
  },
  {
    "name": "planet_admins",
    "fields": """
              id_telegram	INTEGER NOT NULL PRIMARY KEY,
              id_planet	INTEGER NOT NULL,
              FOREIGN KEY(id_telegram) REFERENCES telegram_users(_id)
              """,
  },
  {
    "name": "teachers",
    "fields": """
              id_telegram	INTEGER NOT NULL PRIMARY KEY,
              telegram_name	TEXT NOT NULL,
              username TEXT NOT NULL UNIQUE,
              email	TEXT,
              FOREIGN KEY(id_telegram) REFERENCES telegram_users(_id)
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
              FOREIGN KEY("planet") REFERENCES "planets"("name")
              """,
  },
  {
    "name": "registered_students",
    "fields": """
              id_telegram	INTEGER NOT NULL PRIMARY KEY,
              full_name	TEXT NOT NULL,
              email_students_file	TEXT NOT NULL UNIQUE,
              FOREIGN KEY(id_telegram) REFERENCES telegram_users(_id),
              FOREIGN KEY(email_students_file) REFERENCES students_file(email)
              """,
  },
  {
    "name": "academic_risk_factor",
    "fields": """
              id_telegram INTEGER NOT NULL PRIMARY KEY
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
              week INTEGER,
              weight REAL,
              visible INTEGER,
              category TEXT
              """
    "",
  },
]

# {
#     "name": "grades",
#     "fields": """
#               student_email	TEXT NOT NULL UNIQUE PRIMARY KEY,
#               FOREIGN KEY(student_email) REFERENCES students_file(email)
#               """,
#   },
