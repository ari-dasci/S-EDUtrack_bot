import sys
import os
import re
import inspect
import pandas as pd
from urllib.request import urlopen
from telegram import (
  #InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)
import configuration.config_file as cfg
from configuration.config_file import (
  db, client)
from functions import (
  general_functions as g_fun,
  teacher_functions as tea_fun
)
from dictionaries import (
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang,
  general_dict_lang as g_lang
)

def check_teacher(update, context):
  try:
    user = g_fun.get_user_data(update)
    chat_id = update._effective_chat.id
    if chat_id > 0:
      if user['is_teacher']:
        if cfg.is_config_files_set:
          return True
        else:
          g.fun.send_Msg(context, chat_id,
          tea_lang.not_config_files_set_text[user['language']])
          tea_fun.config_files_set(context, user)  
          return False
      else:
          g_fun.send_Msg(context, chat_id,
          g_lang.invalid_user[user['language']])
          return False
  except:
    g_fun.print_except(inspect.stack()[0][3])

##### CONFIG FILES SET FUNCTIONS
def config_files_set(context, user):
  """Envía los archivos de configuración de estudiantes y actividades para que el docente configure la asignatura.

  """
  try:

    print("CHECK TEA FUN *** CONFIG FILES SET ***")
    if not db.students_file.find_one() and not db.activities.find_one():
      g_fun.send_Msg(context, user['_id'], 
      tea_lang.download_config_files_text[user['language']] )
      config_files_send_document(context, user,'students')
      config_files_send_document(context, user,'activities')
    else:
      if not db.students_file.find_one():
        g_fun.send_Msg(context, user['_id'],
        tea_lang.config_file_set_text ('students', user['language']))
        config_files_send_document(context, user,'students')
      elif not db.activities.find_one():
        g_fun.send_Msg(context, user['_id'],
        tea_lang.config_file_set_text ('activities', user['language']))
        config_files_send_document(context, user,'activities')
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def config_files_upload(update, context, user):
  """EDUtrack recibe un documento de configuración:
  students_format, replace_students_format, activities_format o replace_activities_format y lo descarga para subirlo a la base de datos.

  """
  try:
    print("CHECK TEA FUN ** UPLOAD CONFIG FILES **")
    chat_id = update._effective_chat.id
    doc = update.message.document
    # print("CHECK   Se recibió el archivo:", doc)
    msg = ""
    if 'students' in doc.file_name:  
      collection = db.students_file
      elements = 'students'
      g_fun.remove_file("files/download/students_full.csv")
      g_fun.remove_file("files/downlad/students.csv")    
    else:
      collection = db.activities
      elements = 'activities'
      g_fun.remove_file("files/download/all_activities.csv")
      g_fun.remove_file("files/download/qualifying_activities.csv")
    # Se obtiene el id del archivo
    
    input_file = context.bot.get_file(doc.file_id)
    f_path = input_file['file_path']  # Se obtiene la ruta de descarga
    f_save_name = "files/config/"+doc.file_name  # Ruta donde se guardara el archivo
    temp = urlopen(f_path)  # Se abre un temporal
    temp2 = urlopen(f_path)
    file_headers = temp2.readline().decode('UTF-8')
    file_headers = set(file_headers[:-2].split(','))
    #Revisa si los encabezados son los correctos
    if 'student' in doc.file_name:
      if file_headers != set(cfg.students_headers_file):
        g_fun.send_Msg(context, user['_id'],
        tea_lang.error_file_headers_text(user['language'], cfg.students_headers_file))
        students_format(context, user)
        return False
      
    elif 'activities' in doc.file_name:
      print(file_headers, set(cfg.activities_headers_file))
      if file_headers != set(cfg.activities_headers_file):
        g_fun.send_Msg(context, user['_id'],
        tea_lang.error_file_headers_text(user['language'], cfg.activities_headers_file))
        activities_format(context, user)
        return False
    
    with open(f_save_name, "wb") as file: 
      file.write(temp.read())
    
    add_elements = False 
    if 'add' in doc.file_name:
      add_elements = True
      upload_data = g_fun.csv_to_mongodb (update, context, user, collection, f_save_name, add_elements=True)
    else:
      upload_data = g_fun.csv_to_mongodb (update, context, user, collection, f_save_name)

    if upload_data:
      if db.students_file.find_one() and db.activities.find_one():
        cfg.is_config_files_set = True
        if add_elements:
          if create_grades(update, context, user, add_elements= True):
            g_fun.send_Msg(context, user['_id'], tea_lang.add_elements_ready_text(user['language'],elements))

        else:
          if create_grades(update, context, user):
            g_fun.send_Msg(context, user['_id'],
            tea_lang.welcome_text(context, user['language']))
      else:
        g_fun.send_Msg(context, user['_id'], tea_lang.config_files_ready_one_text[user['language']])
        config_files_set(context, user)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def config_files_send_document(context, user, elements):
  context.bot.sendDocument(
    chat_id=user['_id'],
    document=open(
      tea_lang.config_files_send_document(user['language'], elements) , 'rb'))


def create_grades(update, context, user, add_elements=False):
  """Crea el apartado de calificaciones en la base de datos a partir deel archivo de estudiantes y actividades subidos por el docente.
  

  """
  print("CHECK TEA FUN\n** CREATE GRADES **")
  try:
    students = list(db.students_file.find({},{'_id':1}))
    activities = list(db.activities.find({'weight':{'$gt':0}}).distinct('_id'))
    activities_list = []

    if add_elements:
      doc = update.message.document
      if "activities" in doc.file_name:
        student_grades = list(db.grades.find())
        activities_in_grades = db.grades.find().distinct('activities')[0]
        new_activities = cfg.qualifying_activities.difference(set(list(activities_in_grades)))
        for student in student_grades:
          student['activities'].update(dict.fromkeys(list(new_activities),0))  
        db.grades.drop()
        db.grades.insert_many(student_grades)
        return True
        
      elif "students" in doc.file_name:
        students_in_grades = set(db.grades.find().distinct('_id'))
      new_students = list(cfg.uploaded_students.difference(students_in_grades))
      new_elements = list(db.students_file.find({'_id':{'$in':new_students}},{'_id':1}))


    else:
      if db.grades.find_one():
        db.grades.drop()
      new_elements = students

    activities_list = dict.fromkeys(activities,0)
    
    for student in new_elements:
      student.update({'total_score':0,'max_actual_score':0,'activities':activities_list})

    db.grades.insert_many(new_elements)
    return True

  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


### TEACHER MENU FUNCTIONS

def menu(update, context, user):
  try:
    chat_id = update._effective_chat.id
    if cfg.is_config_files_set:
        keyboard = tea_lang.menu_opt[user['language']]
        reply_markup = IKMarkup(keyboard)
        update.message.reply_text(
              parse_mode = 'HTML',
              text = tea_lang.menu_text[user['language']],
              reply_markup = reply_markup)  
    else:
      g_fun.send_Msg(context, chat_id,
      stu_lang.not_config_files_set_text (context, user['language']))
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def view_activities(update, context, user, option, query=""):
  if option == 'all':
    file = 'files/download/all_activities.csv'
    activities = db.activities.find()
  else:
    file = 'files/download/qualifying_activities.csv'
    activities = db.activities.find({'weight':{'$gt':0}})

  if g_fun.mongo_to_csv_html('activities',file):
    g_fun.send_Msg(context, user['_id'], 
    g_lang.files_ready_for_download[user['language']],query=query)
  else:
    g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_act_view_not_file[user['language']])

  context.bot.sendDocument(chat_id=user['_id'], document=open(file, 'rb'))
  context.bot.sendDocument(chat_id=user['_id'], document=open(file[:-4]+'.html', 'rb'))


def grade_students(update, context, user, args):
  """ Califica la actividad indicada a los estudiantes indicados """
  print("\n** ENTRO A GRADE STUDENTS **",args)

  if len(args) == 0:
    g_fun.send_Msg(context, user['_id'],
    tea_lang.grade_students_no_arguments[user['language']])
    g_fun.send_Msg(context, user['_id'],
    tea_lang.menu_academic_act_eval_cmd_text[user['language']],mode='Markdown')
  else:
      if cfg.qualifying_activities:
        activity_id = args[0].upper()
        print("   ID_ACTIVIDAD", activity_id)
        if activity_id in cfg.qualifying_activities:
        #db.grades.find_one({'activities.'+activity_id: {"$exists":"true"}}):
          students = " ".join(args[1:]).split(';')
          if students[-1] == '':
            students.remove('')

          if students and students != ['']:
            modified_students = ""
            unregistered_students = ""
            grade_error = ""
            ungraded_students = ""
            email_syntax_error = ""

            for student in students:
              datos = (student.strip(' ')).split(' ')
              email = datos[0]
              
              if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower()):
                print("   CORREO", email)
                if email in cfg.uploaded_students:
                  #if db.grades.find_one({'_id': email }):
              
                  if len(datos) == 2:
                    grade = float(datos[1])
                    print("   GRADE", grade)
                    if grade >= 0 and grade <= 10:
                        db.grades.update_one(
                          {'_id': email},
                          {"$set": {
                            'activities.'+activity_id: float(grade)
                          }})
                        if not activity_id in cfg.active_activities:
                          db.activities.update_one({'_id':activity_id},{
                            '$set':{
                              'active':True}})
                          cfg.active_activities.add(activity_id)
                        
                        #NO BORRARAR ESTE
                        #risk_factor_one(email)
                        modified_students += "\n"+email

                    else:
                      grade_error += "\n"+email
                      #g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_grading_error(user['language'], grade, email))
                  elif len(datos) == 1:
                    ungraded_students += "\n"+email
                    #g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_no_grade(user['language'],email))
                  else:
                    g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_no_semicolon(user['language'], email))
                    break
                else:
                  unregistered_students += "\n"+email 
                  #g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_unregistered_email(user['language'], email))
              else:
                email_syntax_error += "\n"+email
                #g_fun.send_Msg(context, user['_id'], g_lang.email_syntax_error_text(user['language'], email))
              
            if modified_students:
              g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_successful_students(user['language'], activity_id, modified_students) )
            if unregistered_students:
              g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_unregistered_email(user['language'], unregistered_students))
            if grade_error:
              g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_grading_error(user['language'], grade_error))
            if ungraded_students:
              g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_no_grade(user['language'], ungraded_students))
            if email_syntax_error:
              g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_email_syntaxis_error(user['language'], email_syntax_error ))


          else:
            g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_no_students[user['language']])
        else:
          g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_unregistered_activity(user['language'], activity_id))

      else:
        g_fun.send_Msg(context, user['_id'], tea_lang.grade_students_no_activities_qualifying[user['language']])






if __name__ == "__main__":
    pass