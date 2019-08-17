import sys
import inspect
import pandas as pd
from urllib.request import urlopen
import configuration.config_file as cfg
from configuration.config_file import (
  db, client)
from functions import (
  general_functions as g_fun
)
from dictionaries import (
  teacher_dict_lang as tea_lang
)

##### CONFIG FILES SET FUNCTIONS
def config_files_set(context, user):
  """Envía los archivos de configuración de estudiantes y actividades para que el docente configure la asignatura.

  """
  try:

    print("CHECK TEA FUN *** CONFIG FILES SET ***")
    if not db.students_file.find_one() and not db.activities.find_one():
      g_fun.send_Msg(context, user['_id'], tea_lang.download_config_files_text[user['language']] )
      files = ["files/guides/students_format.csv",
      "files/guides/activities_format.csv"]
      for file in files:
        context.bot.send_document(chat_id=user['_id'], document=open(file, 'rb'))
    else:
      if not db.students_file.find_one():
        g_fun.send_Msg(context, user['_id'], tea_lang.config_file_set_text ('students', user['language']))
        context.bot.send_document(
          chat_id=user['_id'],
          document=open("files/guides/students_format.csv", 'rb'))
      elif not db.activities.find_one():
        g_fun.send_Msg(context, user['_id'], tea_lang.config_file_set_text ('activities', user['language']))
        context.bot.send_document(
          chat_id=user['_id'],
          document=open("files/guides/activities_format.csv", 'rb'))
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")
  

def upload_config_files(update, context, user):
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
    temp = urlopen(f_path)   # Se abre un temporal
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
        ##### REVISAR SI NO SE TRABA CUANDO NO ES ADD ELEMENTS por que no esta declarado antes.
        if add_elements:
          #g_fun.send_Msg(context, user['_id'], tea_lang.add_elements_ready_text(user['language'], elements))
          if create_grades(update, context, user, add_elements= True):
            g_fun.send_Msg(context, user['_id'], tea_lang.add_elements_ready_text(user['language'],elements))

        else:
          #g_fun.send_Msg(context, user['_id'], tea_lang.config_files_ready_both_text[user['language']] )
          if create_grades(update, context, user):
            g_fun.send_Msg(context, user['_id'], tea_lang.grades_section_ready_text[user['language']])
      else:
        g_fun.send_Msg(context, user['_id'], tea_lang.config_files_ready_one_text[user['language']])
        config_files_set(context, user)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


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
      ## ADD STUDENTS
      if "activities" in doc.file_name:
        activities_in_grades = (db.grades.find().distinct('activities'))

        activities_ids = []
        for i in range(len(activities_in_grades)):
          activities_ids.append(list(activities_in_grades[i].keys())[0])
        activities_in_grades = set(activities_ids)
        new_activities = list(cfg.qualifying_activities.difference(activities_in_grades))
        activities_list = [{ activity : 0} for activity in new_activities ]
        #activities_list = [dict.fromkeys(new_activities,0)]
        db.grades.update_many({},{'$push':{'activities':{'$each':activities_list,}}})
        return True
        
      elif "students" in doc.file_name:
        students_in_grades = set(db.grades.find().distinct('_id'))
      new_students = list(cfg.uploaded_students.difference(students_in_grades))
      new_elements = list(db.students_file.find({'_id':{'$in':new_students}},{'_id':1}))


    else:
      if db.grades.find_one():
        db.grades.drop()
      new_elements = students

    activities_list = [{ activity : 0} for activity in activities ]
    for student in new_elements:
      student.update({'total_score':0,'max_actual_score':0})
    db.grades.insert_many(new_elements)

    if not add_elements:
      db.grades.update_many({},{'$push':{'activities':{'$each':activities_list,'$position':-1}}})
    return True


    ''' for activity in activities:
      #print(activity['_id'])
      activities_list.append(activity['_id'])
    activities_new_students = activities_list[:]

    if db.grades.find_one({}):
      activities = db.grades.find_one({})
      for activity in activities:
        if not (activity == "_id" or
          activity == "total_score" or
          activity == "max_actual_score"):
          activities_list.remove(activity)

    if add_elements:
      message_id = bot.sendMessage(
        parse_mode='HTML',
        chat_id=user['_id'],
        text="Espera un momento ahora estoy creando el apartado de <b>calificaciones</b>.")['message_id']
    else:
      num_activities = len(activities_list)
      time = (num_activities/8)*num_elements
      if time>60:
        time = str(int(time//60))+" min "+str(int(time%60))+" seg"
      else:
        time = str(int(time))+" seg"
      message_id = bot.sendMessage(
            parse_mode='HTML',
            chat_id=user['_id'],
            text="Espera un momento ahora estoy creando el apartado de <b>calificaciones</b>. Tiempo estimado: "+time+".")['message_id']
      print("   Creando calificaciones en la base de datos")

    count = 1.0
    for student in students:
      #print(student['_id'])
      email = student['_id']
      if not db.grades.find_one({'_id': email}):
        print("entro para el susuario:",email)
        db.grades.insert({'_id': email,
                'total_score': float(0),
                'max_actual_score':float(0)})
        for activity in activities_new_students:
          db.grades.update({'_id': email},
          {'$set': {
            activity: float(0)
          }})
      else:
        if activities_list:
          for activity in activities_list:
            if not db.grades.find_one({'_id': email, activity:{'$exists':True}}):
              #print("********",activity)
              db.grades.update({'_id': email},
                      {'$set': {
                        activity: float(0)
                      }})
            else:
              print(
                "La actividad", activity, "ya existe en calificaciones de la base de datos.")

      count += 1
    if first_time:
      g_fun.send_Msg(context, user['_id'], tea_lang.grades_section_ready_text[user['language']])
    else:
      if count != 1.0:
        bot.editMessageText(
          chat_id = update.message.chat_id,
          message_id = message_id,
          parse_mode = 'HTML',
          text="Se actualizo el apartado de calificaciones en la base de datos.")
        print("   Se actualizo grades en la base de datos.")

    cgf.is_config_files_set = True '''

  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")






if __name__ == "__main__":
    pass