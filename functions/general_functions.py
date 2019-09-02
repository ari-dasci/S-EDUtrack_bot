import arrow
import re
import os
import sys
import inspect
import pandas as pd

from unicodedata import normalize
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)
import configuration.config_file as cfg
from configuration.config_file import (
  db, client,
  meeting)
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang)
from functions import(
  teacher_functions as tea_fun,
  edutrack_functions as edu_fun,
  commands as cmd
)


def basic_setup(bot):
  """Inicializa las configuraciones básicas de EDUtrack.
  - Crea la colección de docente.
  - Crea los directorios necesarios.
  """
  print(bot)
  try:
    if not db.teachers.find_one():
      db.teachers.insert_one(cfg.teacher_data)

    #OBTENER VARIBLES GLOBALES
    cfg.teacher_list =  set(db.teachers.find().distinct('_id'))
    if (db.students_file.find_one() and db.activities.find_one()):
      cfg.is_config_files_set = True
    
    cfg.autoeva_questions_list = list(g_lang.autoevaluation_questions_text["ES"])
      
    if db.students_file.find_one():
      cfg.uploaded_students = set(db.students_file.find().distinct('_id'))
    if db.registered_students.find_one():
      cfg.registered_students = set(db.registered_students.find().distinct('_id'))
      cfg.identified_students = set(db.registered_students.find({'planet':''}).distinct('_id'))
      

    if db.activities.find_one():
      cfg.activities_sections = set(db.activities.find().distinct('section'))
      cfg.uploaded_activities = set(db.activities.find().distinct('_id'))
      cfg.qualifying_activities = set(db.activities.find({'weight':{'$gt':0}}).distinct('_id'))
      cfg.active_activities = set(db.activities.find({'active':True}).distinct('_id'))
      
      max_week = max(db.activities.find().distinct('week'))
      for i in range(1,max_week+1):
        if i < 10:
          cfg.weeks_array.append("w_0"+str(i))
        else:
          cfg.weeks_array.append("w_"+str(i))
      print(cfg.weeks_array)
      


      
      
    """
    if not db.data_arrays.find_one({'_id':bot.username}):
        db.data_arrays.insert_one({
          '_id':bot.username,
          'is_config_files_set' : cfg.is_config_files_set,
          'uploaded_students' : cfg.uploaded_students,
          'registered_students' :  cfg.registered_students,
          'upload_activities' : cfg.uploaded_activities,
          'qualifying_activities' : cfg.qualifying_activities,
          'activities_sections' : cfg.activities_sections,
          'weeks_array' : cfg.weeks_array,
          'meetings_array': cfg.meetings_array,
          'teacher_criteria' : cfg.teacher_criteria
          })
        
      
    else:
      cfg.activities_sections = db.data_arrays.find_one({'_id':bot.username})['activities_sections']
      cfg.weeks_array = db.data_arrays.find_one({'_id':bot.username})['weeks_array']
      cfg.meetings_array = db.data_arrays.find_one({'_id':bot.username})['meetings_array']
      cfg.teacher_criteria = db.data_arrays.find_one({'_id':bot.username})['teacher_criteria']
    # print("Se termino de crear los arreglos")
      """
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def send_Msg(context, chat_id, text, mode='HTML', query=""):
  """EDUtrack envía un mensaje al chat especificado.
  chat_id => ID a donde se enviará el mensaje.
  text => Texto del Mensaje.
  mode => Formato del mensaje (HTML ó Markdown).
  
  """ 
  try:
    reply_markup=""
    if not query:
      context.bot.sendMessage(
        chat_id = chat_id,
        parse_mode = mode,
        text = text)
    else:
      query.edit_message_text(
        parse_mode = mode,
        text = text,
        reply_markup = reply_markup)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def show_menu(query, menu_opt, menu_text):
  try:
    keyboard = menu_opt
    reply_markup = IKMarkup(keyboard)
    query.edit_message_text(
          parse_mode = 'HTML',
          text = menu_text,
          reply_markup = reply_markup)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def strip_accents(string):
  """Recibe un string y elimina los acentos y lo devuelve en mayúsculas."""
  # print("CHECK GFUN ENTRO A STRIP ACCENTS")
  try:
    string = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
            r"\1", normalize("NFD", string), 0, re.I)
    string = normalize('NFC', string)
    return string.upper()
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def get_user_data(update, language=""):
  """Obtiene los datos de un usuario y verifica si hay cambios en sus datos de Telegram. Devuelve un diccionario con los datos del Usuario: {id, telegram_name, username, planet, is_teacher, language}.

  """
  # print("CHECK GFUN GET USER DATA")
  try:
    chat_id = update._effective_chat.id
    user_data = update._effective_user

    user = {
      '_id': str(user_data['id']),
      'telegram_name': str(user_data.full_name),
      'username': "",
      'planet': "",
      'is_teacher': False,
      'language': language
    }
    
    if user_data['username']:
      user['username'] = str(user_data['username'])

    if user['_id'] in cfg.teacher_list:
      user['is_teacher'] = True 

    if not user['is_teacher']:
      if chat_id < 0: 
        if update.message.chat['title']:
          user['planet'] = strip_accents(str(update.message.chat['title']))
      elif db.telegram_users.find_one({'_id':user['_id'],'planet':{'$ne':''}}):
        user['planet'] = strip_accents(db.telegram_users.find_one({'_id': user['_id']})['planet'])

    if not user['language']:
      if db.telegram_users.find_one({
        '_id': user['_id'],'language':{'$ne':''}}):
          user['language'] = db.telegram_users.find_one(
          {'_id': user['_id']})['language']
      elif chat_id > 0:
        user_first_name = update._effective_user.first_name
        keyboard = g_lang.language_opt
        reply_markup = IKMarkup(keyboard)
        update.message.reply_text(
            parse_mode = 'HTML',
            text = g_lang.choice_language_text(user_first_name),
            reply_markup = reply_markup)
        return False
    if user != db.telegram_users.find_one({'_id': user['_id']}):
      db.telegram_users.save(user)
    # print("~~~~~ USUARIO NUEVO",user)
    return user
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def welcome(context, query, user):
  """EDUtrack da la bienvenida al usuario dependiendo de su perfil."""
  # print("CHECK GFUN WELCOME")
  try:
    if user['is_teacher']:
      msg = tea_lang.welcome_text(context, user['language'],start_cmd=True)
    else:
      msg = stu_lang.welcome_text(context, user['language'])
    query.edit_message_text(
      parse_mode='HTML',
      text=msg)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def is_user_registered(update, context, user):

  """ Revisa si el usuario esta o no registrado en la base de datos de estudiantes o docentes.

  Retorna True si el usuario esta registrado de lo contrario intenta registrarlo.

  """
  #  print("CHECK GFUN   ** ENTRO A IS USER REGISTER **\n")
  try:
    chat_id = update._effective_chat.id

    if user['is_teacher']:
      return True
    
    # Revisa si hay cambios, si el usuario ya esta registrado.
    #if db.registered_students.find_one({'_id': user['_id']}):
    if user['_id'] in cfg.registered_students:
      user_db = db.registered_students.find_one({'_id': user['_id']})
      user['name'] = user_db['name']
      user['email'] = user_db['email']
      difference = set(user.items()).difference(set(user_db.items()))
      
      if difference:
        for element in difference:
          user_db[element[0]] = user[element[0]]
        db.registered_students.save(user_db)
        
      if user['_id'] in cfg.identified_students:
        if not edu_fun.create_collections(user):
          return False
      return True

    else:
      # Intenta registrar al usuario por su username, si no, pide al usuario ingresar su email.
      if user['username']:
        if user['username'] != context.bot.username:
          if db.students_file.find_one({'username': user['username']}):
            student_data = db.students_file.find_one(
              {'username': user['username']})
            if not user['planet'] and student_data['planet']:
              user['planet'] = student_data['planet'] 
            
            if edu_fun.create_collections(user):
              db.registered_students.save(
                {'_id': user['_id'],
                'email': student_data['_id'],
                'name': f"{student_data['last_name']}, {student_data['first_name']}",
                'telegram_name': user['telegram_name'],
                'username': user['username'],
                'planet': user['planet'],
                'is_teacher': user['is_teacher'],
                'language' : user['language']
                })
              cfg.registered_students.add(user['_id'])
              return True
            else:
              return False
          else:
            send_Msg(context, user['_id'], 
              stu_lang.check_email_registration_text[user['language']],
              mode = "Markdown")
            for teacher in cfg.teacher_list:
              language = db.telegram_users.find_one(
                {'_id': teacher})['language']
              send_Msg(context, teacher, tea_lang.teacher_message_registration_error_text(
                context, language, user))
            return False
      else:
        send_Msg(context, chat_id,
        stu_lang.no_username_text[user['language']])


        print(
          "El usuario", user['_id'], "no tiene un username asociado a su cuenta de Telegram.")
        return False

      ###################################################
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def received_message(update, context):
  """
  Recibe cada mensaje que se envía en EDUtrack que no sea comando o status_update.

  """
  try:
    print("CHECK GFUN ** ENTRO A RECEIVED_MESSAGE **")
    upm = update.message
    user = get_user_data(update)
    if not user:
      return False
    # Se revisa si se esta subiendo archivos de configuración
    if user['is_teacher']:
      if cfg.is_config_files_set and not upm.document:
        if upm.chat_id < 0 and upm.text:
          if "== inicio de meeting" in upm.text:
            meeting['active'] = True
            meeting['planet'] = strip_accents(
              upm.chat['title'])
            meeting['number'] = "meeting_" + \
              (upm.text).split(' ')[4]
            meetings_array.append(meeting['number'])
            print("______________________ ", upm.text,
                                "del planeta", upm.chat['title'], "\n\n")
          elif "== fin de meeting" in upm.text:
            meeting['active'] = False
            meeting['planet'] = ""
            print("______________________SE FINALIZO EL MEETING ",
                                upm.text, "del planeta", upm.chat['title'], "\n\n")
        else:
          send_Msg(context, user['_id'],
          tea_lang.welcome_short_text[user['language']])
      elif upm.document:
        doc = upm.document
        if (doc.file_name == "students_format.csv" or
          doc.file_name == "activities_format.csv" or
          doc.file_name == "add_students_format.csv" or
          doc.file_name == "add_activities_format.csv" or
          doc.file_name == "replace_students_format.csv" or
          doc.file_name == "replace_activities_format.csv" or
            doc.file_name == "grades_format.csv"):

          if doc.file_name == "grades_format.csv":
            edit_grades(bot, update)
          elif (doc.file_name == "students_format.csv" or
                doc.file_name == "activities_format.csv"):
            if ((doc.file_name == "students_format.csv" and
                db.students_file.find_one()) or
                (doc.file_name == "activities_format.csv" and
                db.activities.find_one())):
              send_Msg(context, user['_id'],
              tea_lang.config_files_set_exist_DB(doc.file_name,
              user['language']))
            else:
              tea_fun.config_files_upload(update, context, user)
              print("SALIO")
          else:
            tea_fun.config_files_upload(update, context, user)
            print("SALIO")
        # REVISAR DONDE VA
      else:
        if upm.chat_id > 0:
          send_Msg(
            context, upm.chat_id,
            tea_lang.not_config_files_set_text[user['language']])
          tea_fun.config_files_set(context, user)
    else:
      if cfg.is_config_files_set:
        if is_user_registered(update, context, user):
          if upm.chat_id < 0:
            edu_fun.reg_messages(upm, context, user)
            if meeting['active']:
              add_student_vc_meetings(user)
          else:
            send_Msg(context, user['_id'],
            stu_lang.welcome_short_text[user['language']])
      else:
        if update._effective_chat.id > 0:
          send_Msg(context, upm.chat_id,
          stu_lang.not_config_files_set_text(context, user['language']))
    

  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def csv_to_mongodb(update, context, user, collection, file,add_elements=False):
  """Recibe el path de un archivo ".csv" y almacena su contenido en la base de datos.    """
  try:
    print("CHECK GFUN ** CSV TO MONGODB **")
    chat_id = update._effective_chat.id
    delete_blank_lines(file)
    df = pd.read_csv(file, sep=",")
    if 'grades' in file:
        df.fillna(0,inplace=True)
    else:
      df.fillna('',inplace=True)
    if not add_elements:
        if collection.find_one():
            collection.drop()
    else:
      elements = 'students' if 'students' in file else 'activities'
      upload_elements = set(df['_id'].tolist())
      db_elements = set(collection.find().distinct('_id'))
      duplicates = upload_elements.intersection(db_elements)
      new_elements = upload_elements.difference(db_elements)

      for element in duplicates:
        df = df.drop(df[df.loc[:, '_id'] == element].index)
      if df.empty:
        send_Msg(context, chat_id,
        tea_lang.add_elements_all_exists_text(user['language'], elements))
        return True
      else:
        if duplicates:
          duplicates_list = tea_lang.add_elements_duplicates(
          user['language'], elements)
          for element in duplicates:
            duplicates_list += "\n"+element
          send_Msg(context, chat_id, duplicates_list)
    collection.insert(df.to_dict('records'))
    
    if 'students' in file:
      cfg.uploaded_students = set(df['_id'].tolist())
    else:
      cfg.uploaded_activities = set(df['_id'].tolist())
      cfg.qualifying_activities = set(db.activities.find({'weight':{'$gt':0}}).distinct('_id'))
    return True
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


def delete_blank_lines(file):
  """Recibe el path de un archivo ".csv" y elimina las líneas en blanco."""
  print("CHECK GFUN DELETE BLANK LINES")
  try:
    df = pd.read_csv(file, sep=",")
    df.dropna(subset=['_id'], inplace=True)
    df.to_csv(file, sep=',', index=False)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def remove_file(file):
  """Recibe el path de un archivo y sí existe lo elimina así como su versión html.

  """
  try:
    print("CHECK GFUN REMOVE FILES")
    if os.path.isfile(file):
      os.remove(file)
    file = file[:-4] + ".html"
    if os.path.isfile(file):
      os.remove(file)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def get_week():
  today = arrow.utcnow()
  start_date = arrow.get(cfg.start_date, 'DD-MM-YYYY')
  day = start_date.format('dddd')
  if day != 'Monday':
    for i in range(7):
      monday_week = start_date.shift(days=-i)
      day = start_date.shift(days=-i).format('dddd') 
      if day =='Monday':
        break
  diferencia = (today - monday_week)
  actual_num_week = int(diferencia.days / 7)+1
  if actual_num_week > 15:
    actual_num_week = 15
  return actual_num_week


def mongo_to_csv_html(elements, file):
  """ Recibe un Cursor MongoDB y el path de un archivo. Guarda el cursor en la dirección del path con las extensiones '.csv' y '.html'.
  
  """
  try:
    df = pd.DataFrame(list(elements))
    df.to_csv(file, index=False)
    file = file[:-4]
    df.index = range(1,df.shape[0]+1)
    with open(file+'.html',"w") as html_file:
      html_file.write(df.to_html(justify='center'))
    return True
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


def print_except(funcion):
  print(f"\n**********\n\
      ERROR IN FUNCTION {funcion}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def risk_factor_one(email):
  print("   ** ENTRO A RISK FACTOR ONE **", email)
  try:
    student_id = db.registered_students.find_one({'email':email})
    print(student_id)
    actual_num_week = get_week()

    if actual_num_week < 10:
      actual_week = "week_0"+str(actual_num_week)
    else:
      actual_week = "week_"+str(actual_num_week)
    obtained_weight = 0
    max_actual_score = 0
    active_activities = db.activities.find({'active':True})
    for activity in active_activities:
      obtained_grade = float(db.grades.find_one({'_id':student_id})[activity['_id']])
      weight = float(db.activities.find_one({'_id': activity['_id']})['weight'])
      max_actual_score += weight
      obtained_weight += (obtained_grade/10*weight)
    #print("   CONTROL MAX SCORE",max_actual_score,"-- STUDENT SCORE",obtained_weight)
    IC = 1-(obtained_weight/max_actual_score) if max_actual_score != 0 else 0
    recovery_factor = (1-max_actual_score)+obtained_weight
    #print("   CONTROL IC =",IC,"RECOVERY FACTOR",recovery_factor)

    db.grades.update_one({'_id':student_id},{
      '$set' : {
        'total_score' : obtained_weight*10,
        'max_actual_score' : max_actual_score*10
      }
    })

    #print("\nObtained_grade:",obtained_weight,"Max_actual_score:",max_actual_score,"\nIC:",IC,"recovery_factor:",recovery_factor,"Semana actual:",actual_num_week)
    #print("   CONTROL Semana Actual",actual_num_week)


    gamma_IC = actual_num_week/15*recovery_factor
    gamma_FR = 1-gamma_IC
    #print("gamma_IC",gamma_IC,"gamm_FR",gamma_FR)
    IC2 = (1-IC) * gamma_IC
    FR2 = recovery_factor * gamma_FR
    #print("\n\nIC",IC,"IC_real",IC2,"\nFR",recovery_factor,"FR_real",FR2)


    risk_factor = IC2+FR2
    #risk_factor = recovery_factor
    #print("\nRISK_FACTOR", risk_factor)
    if risk_factor < 0.5:
      risk_factor_linguistic = "irrecuperable"
    elif risk_factor < 0.6:
      risk_factor_linguistic = "muy crítico"
    elif risk_factor < 0.7:
      risk_factor_linguistic = "crítico"
    elif risk_factor < 0.8:
      risk_factor_linguistic = "moderado"
    elif risk_factor < 0.9:
      risk_factor_linguistic = "bajo"
    else:
      risk_factor_linguistic = "ninguno"
    #print("RISK_FACTOR", risk_factor_linguistic)
    #print("_______________________________________________________________________________\n")
    # Calificación Potencial de Recuperación
    recovery_factor = round(recovery_factor*10, 1)
    if not db.risk_factor.find_one({'_id': student_id}):
      db.risk_factor.insert_one(
        {'_id': student_id,
        'risk_factor': round(risk_factor, 4),
        'risk_factor_linguistic': risk_factor_linguistic,
        'recovery_factor': recovery_factor
      })
      # print("   Se registro el risk_factor del estudiante:",email)
      db.weekly_srf.insert_one({
        '_id':student_id,
        actual_week:{
          'risk_factor': round(risk_factor, 4),
          'risk_factor_linguistic': risk_factor_linguistic,
          'recovery_factor': recovery_factor
      }})
    else:
      db.risk_factor.update_one(
        {'_id': student_id},{
          '$set':{
            'risk_factor': round(risk_factor, 4),
            'risk_factor_linguistic': risk_factor_linguistic,
            'recovery_factor': recovery_factor
      }})
      db.weekly_srf.update_one({'_id':student_id},{
        '$set':{
          actual_week:{
            'risk_factor': round(risk_factor, 4),
            'risk_factor_linguistic': risk_factor_linguistic,
            'recovery_factor': recovery_factor
          }}},True)
    #print("~~~~ RISK FACTOR: ",round(risk_factor, 4),"\n~~~~ LINGUISTIC: ",risk_factor_linguistic,"\n~~~~ RECOVERY FACTOR",recovery_factor)
    #print("CONTROL FINALIZO RISK FACTOR ONE")
    return True


  except:
    print("****\n*** ERROR RISK FACTOR ONE\n****")
    return False













if __name__ == "__main__":
  pass

