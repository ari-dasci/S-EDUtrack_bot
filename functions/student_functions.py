from telegram import (
  #InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)

import configuration.config_file as cfg
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang
)
from functions import(
  general_functions as g_fun
)


def menu(update, context, user):
  try:
    chat_id = update._effective_chat.id
    if cfg.is_config_files_set:
      if user['_id'] in cfg.registered_students:
        keyboard = stu_lang.menu_opt[user['language']]
        reply_markup = IKMarkup(keyboard)
        update.message.reply_text(
              parse_mode = 'HTML',
              text = stu_lang.menu_text[user['language']],
              reply_markup = reply_markup)
      else:
        pass  
    else:
      g_fun.send_Msg(context, chat_id, stu_lang.not_config_files_set_text (context, user['language']))
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")


def my_grade(update, context, user, query):
  print("\n** ENTRO A STUDENT VIEW GRADE **")
  actual_num_week = g_fun.get_week()
  email = db.registered_students.find_one({'_id': user['_id']})['email']
  print("El usuario", user['_id'], "con el e-mail", email, "ha solicitado su calificación")

  if db.activities.find_one({'active':True}):
    activities_list = "<b>SEMANA "+str(actual_num_week-5)+"</b>:\nTu factor de riesgo es <b>Moderado</b>.\n\nA continuación te muestro cada actividad y su calificación que se han evaluado hasta este momento:\n"
    active_activities = db.activities.find({'active':True})
    for activity in active_activities:
      activity_id = activity['_id']
      grade = db.grades.find_one({'_id':email})[activity_id]
      activities_list += "\n"+activity_id+" = "+str(round(grade,1))
    risk_factor_one(email)
    total_score = round(db.grades.find_one({'_id': email})['total_score'],2)
    #print("CONTROL TOTAL SCORE",total_score)
    max_actual_score = round(db.grades.find_one({'_id': email})['max_actual_score'],2)
    #print("CONTROL MAX ACTUAL SCORE",max_actual_score)
    risk_factor = str(round(db.risk_factor.find_one(
      {'_id': email})['risk_factor'],2))
    risk_factor_linguistic = (db.risk_factor.find_one(
      {'_id': email})['risk_factor_linguistic']).upper()
    recovery_factor = str(db.risk_factor.find_one(
      {'_id': email})['recovery_factor'])