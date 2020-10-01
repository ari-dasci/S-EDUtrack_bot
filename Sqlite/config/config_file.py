subject_data = {
  "_id": "FS1920",
  "name": "Fundamentos del Software",
  "start_date": "22/09/2020",
  "course_weeks": "15",
  "max_final_grade": "10",
  "max_activity_grade": "10",
  "min_grade_to_pass": "5",
  "min_ideal_grade": "8",
  "activate_evaluations:": "0",
  "active_planet_registry": "1",
}

teacher_data = {
  "email": "edutrack.ugr@gmail.com",
  "telegram_name": "Soporte EDUtrack",
  "username": "Soporte_EDUtrack",
  "telegram_id": "970331050",
  "is_teacher": 1,
  "language": "es",
}

####################################
standby_teachers = False
config_files_set = False
active_activities = False
active_meetings = {}
monday_start_week = ""
admins_list = {}
registered_stu = {}
evaluation_scheme = {}
resources = {"week": 0}

teacher_criteria = [
  "T_VOCALIZACION",
  "T_DOMINIO_TEMA",
  "T_CERCANIA",
  "T_ATENCION_AUDIENCIA",
  "T_CLARIDAD_EXPRESIONES",
  "C_CALIDAD_TRANSPARENCIAS",
  "C_CALIDAD_EJEMPLOS",
  "C_CONTENIDOS_NIVEL",
]

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

tables = {
  "activities": f"""
        _id TEXT NOT NULL PRIMARY KEY,
        name TEXT,
        section TEXT,
        week INTEGER DEFAULT 0,
        weight REAL DEFAULT 0,
        visible INTEGER DEFAULT 0,
        category TEXT
        """,
  "actual_grades": f"""
        email TEXT NOT NULL PRIMARY KEY,
        SUBJECT REAL DEFAULT 0,
        FOREIGN KEY(email) REFERENCES students_file(email)
        """,
  "eva_collaboration": f"""
        _id INTEGER NOT NULL,
        planet TEXT NOT NULL,
        classmate_id INTEGER NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id),
        FOREIGN KEY(planet) REFERENCES planets(_id),
        FOREIGN KEY(classmate_id) REFERENCES telegram_users(_id)
        """,
  "eva_teacher": f"""
        _id INTEGER NOT NULL PRIMARY KEY,
        value TEXT,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "eva_autoevaluation": f"""
        _id INTEGER NOT NULL PRIMARY KEY,
        question INTEGER NOT NULL,
        value TEXT,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)""",
  "evaluation_scheme": f"""
        _id TEXT NOT NULL PRIMARY KEY,
        category_score REAL NOT NULL DEFAULT 0.0,
        subject_score REAL NOT NULL DEFAULT 0.0,
        active INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(_id) REFERENCES activities(_id)
        """,
  "grades": f"""
        email TEXT NOT NULL PRIMARY KEY,
        _PERFORMANCE_SCORE REAL DEFAULT 0,
        _MAX_ACTUAL_SCORE REAL DEFAULT 0,
        _MAX_POSSIBLE_GRADE REAL DEFAULT 10,
        FOREIGN KEY(email) REFERENCES students_file(email)
        """,
  "linguistic_risk_factor": f"""
        email TEXT NOT NULL PRIMARY KEY,
        FOREIGN KEY(email) REFERENCES students_file(email)
        """,
  "meetings_attendance": f"""
        _id INTEGER NOT NULL,
        meeting INTEGER NOT NULL,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "opn_collaboration": f"""
        _id INTEGER NOT NULL,
        planet TEXT NOT NULL,
        classmate_id INTEGER NOT NULL,
        week TEXT NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "opn_resources": f"""
        _id TEXT NOT NULL,
        section TEXT,
        resource TEXT NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY(_id) REFERENCES activities(_id)
        """,
  "opn_teacher_meetings": f"""
        _id INTEGER NOT NULL,
        meeting INTEGER NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "opn_teacher_practice": f"""
        _id INTEGER NOT NULL,
        week INTEGER NOT NULL,
        criterion TEXT NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "planets": """
        _id TEXT NOT NULL PRIMARY KEY,
        chat_id INTEGER DEFAULT '',
        num_members	INTEGER NOT NULL DEFAULT 0,
        active INTEGER NOT NULL DEFAULT 0
        """,
  "planet_admins": """
        _id TEXT NOT NULL PRIMARY KEY,
        admins TEXT,
        FOREIGN KEY(_id) REFERENCES planets(_id)
        """,
  "planet_users": """
        _id	INTEGER NOT NULL PRIMARY KEY,
        planet TEXT,
        registered INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id),
        FOREIGN KEY(planet) REFERENCES planets(_id)
        """,
  "registered_students": """
        _id	INTEGER NOT NULL PRIMARY KEY,
        full_name	TEXT NOT NULL,
        email	TEXT NOT NULL,
        username TEXT NOT NULL,
        planet TEXT,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id),
        FOREIGN KEY(email) REFERENCES students_file(email)
        FOREIGN KEY(username) REFERENCES telegram_users(username)
        FOREIGN KEY("planet") REFERENCES "planets"("_id")
        """,
  "risk_factor": f"""
        email TEXT NOT NULL PRIMARY KEY,
        FOREIGN KEY(email) REFERENCES students_file(email)
        """,
  "students_file": """
        email	TEXT NOT NULL PRIMARY KEY,
        first_name	TEXT,
        last_name	TEXT,
        username	TEXT,
        planet	TEXT,
        FOREIGN KEY(username) REFERENCES telegram_users(username)
        FOREIGN KEY("planet") REFERENCES "planets"("_id")
        """,
  "student_messages": f"""
        _id	INTEGER NOT NULL ,
        planet TEXT,
        meeting INTEGER DEFAULT -1,
        TEXT INTEGER DEFAULT 0,
        IMAGE INTEGER DEFAULT 0,
        VIDEO INTEGER DEFAULT 0,
        VOICE INTEGER DEFAULT 0,
        STICKER INTEGER DEFAULT 0,
        GIF INTEGER DEFAULT 0,
        DOCUMENT INTEGER DEFAULT 0,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "suggestions": f"""
        _id TEXT NOT NULL,
        email TEXT NOT NULL,
        date TEXT NOT NULL,
        suggestion TEXT NOT NULL,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        """,
  "subject_data": f"""
        _id	TEXT NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        course_weeks INTEGER NOT NULL,
        max_final_grade	REAL NOT NULL DEFAULT 10,
        max_activity_grade REAL NOT NULL DEFAULT 10,
        min_grade_to_pass	REAL NOT NULL DEFAULT 5,
        min_ideal_grade	REAL NOT NULL DEFAULT 10,
        activate_evaluations INTEGER DEFAULT 0,
        active_planet_registry INTEGER NOT NULL DEFAULT 1
        """,
  "teachers": """
        email	TEXT NOT NULL PRIMARY KEY,
        telegram_name	TEXT NOT NULL,
        username TEXT NOT NULL,
        telegram_id	INTEGER,
        FOREIGN KEY(telegram_id) REFERENCES telegram_users(_id)
        """,
  "teacher_messages": f"""
        _id	INTEGER NOT NULL,
        planet TEXT,
        meeting INTEGER DEFAULT -1,
        TEXT INTEGER DEFAULT 0,
        IMAGE INTEGER DEFAULT 0,
        VIDEO INTEGER DEFAULT 0,
        VOICE INTEGER DEFAULT 0,
        STICKER INTEGER DEFAULT 0,
        GIF INTEGER DEFAULT 0,
        DOCUMENT INTEGER DEFAULT 0,
        FOREIGN KEY(_id) REFERENCES telegram_users(_id)
        FOREIGN KEY("planet") REFERENCES "planets"("_id")
        """,
  "telegram_users": """
        _id INTEGER NOT NULL PRIMARY KEY,
        telegram_name	TEXT NOT NULL,
        username	TEXT NOT NULL,
        is_teacher	INTEGER NOT NULL DEFAULT 0,
        language	TEXT DEFAULT 'en'
        """,
}


triggers = [
  """
    CREATE TRIGGER IF NOT EXISTS set_user_planet
    AFTER INSERT ON registered_students
    BEGIN
      INSERT OR IGNORE INTO planet_users (_id, planet)
        VALUES ( new._id, new.planet);
      UPDATE planet_users SET registered = 1 WHERE _id = new._id;
      INSERT OR IGNORE INTO planets (_id) VALUES(new.planet);
      UPDATE planets SET num_members = num_members + 1 WHERE _id = new.planet;
      INSERT OR IGNORE INTO student_messages (_id, planet)
        VALUES(new._id, new.planet);
    END;
    """,
  """
    CREATE TRIGGER update_user_planet
      AFTER UPDATE OF planet ON registered_students
      BEGIN
          UPDATE planet_users SET planet = new.planet WHERE _id = new._id;
          INSERT OR IGNORE INTO planets (_id) VALUES(new.planet);
          UPDATE planets SET num_members = num_members + 1 WHERE _id = new.planet;
          UPDATE planets SET num_members = num_members - 1 WHERE _id = old.planet;
      END;
      """,
  """
    CREATE TRIGGER update_is_teacher
      AFTER INSERT ON teachers
      BEGIN
          UPDATE telegram_users SET is_teacher = 1 WHERE _id = new._id;
      END;
  """,
  """
    CREATE TRIGGER insert_planet_admins
      AFTER INSERT ON planets
      BEGIN
          INSERT OR IGNORE INTO planet_admins (_id) VALUES (new._id);
      END;
  """,
]
