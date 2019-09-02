"""Funciones de los comandos establecidos en el bot EDUtrack"""
import re
import sys
import inspect
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)
import configuration.config_file as cfg
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang
)
from configuration.config_file import (
  client, db,
  is_config_files_set)
from functions import (
  general_functions as g_fun,
  teacher_functions as tea_fun,
  student_functions as stu_fun,
  edutrack_functions as edu_fun
)

def start(update, context):
  """ Inicializa el bot y revisa si se encuentra configurado.
  Si es la primera vez que entra en usuario solicita que se seleccione el lenguaje. Si ya se ingresado antes EDUtrack da la bienvenida al usuario.
  
  """
  try:
    print("CHECK CMD *** START ***")
    chat_id = update._effective_chat.id
    if chat_id > 0:
      user = g_fun.get_user_data(update)
      if not user:
        return False
      elif user['is_teacher']:
          g_fun.send_Msg(context, user['_id'],
          tea_lang.welcome_text(context, user['language']))

      else:
        if not user['_id'] in cfg.registered_students:
          if not g_fun.is_user_registered(update, context, user):
            return False
        g_fun.send_Msg(context, user['_id'],
        stu_lang.welcome_text(context, user['language']))
  except:
    g_fun.print_except(inspect.stack()[0][3])


def menu(update, context):
  try:
    chat_id = update._effective_chat.id
    if chat_id > 0:
      user = g_fun.get_user_data(update) 
      if user['is_teacher']:
        if cfg.is_config_files_set:
          tea_fun.menu(update, context, user)
        else:
          g.fun.send_Msg(context, chat_id,
          tea_lang.not_config_files_set_text[user['language']])
          tea_fun.config_files_set(context, user)
      else:
        if cfg.is_config_files_set:
          if g_fun.is_user_registered(update, context, user):
            stu_fun.menu(update, context, user)
        else:
          g_fun.send_Msg(context, chat_id,
          stu_lang.not_config_files_set_text (context, user['language']))  
    else:
      g_fun.send_Msg(context, chat_id,
      g_lang.wrong_command_group[user['language']])
  except:
    g_fun.print_except(inspect.stack()[0][3]) 


def press_button(update, context):
  """Recibe la respuesta al presionar un boton del menú."""
  try:
    print("CHECK CMD *** PRESS BUTTON ***")
    query = update.callback_query
    print("CHECK CMD QUERY DATA:",query.data,"\n")
    selections = (query.data).split('-')
    choice = selections[-1]
    valid_languages = ["ES","EN"]
    
    if choice in valid_languages:
      user = g_fun.get_user_data(update, language=choice)
    else:  
      user = g_fun.get_user_data(update)
    if not user:
        return False
    if cfg.is_config_files_set:
      if g_fun.is_user_registered(update,context, user):      
        print(selections)
        if len(selections) > 1:
          if selections[0] == 's_menu':
            if selections[1] == "stu_back":
              g_fun.show_menu(query, 
              stu_lang.menu_opt[user['language']],
              stu_lang.menu_text[user['language']])
              #stu_fun.menu(update, context, user)
            elif selections[1] == "grade":
              stu_fun.my_grade(update, context, user, query)
            elif selections[1] == "opn":
              stu_fun.opinion(query, selections)
            elif selections[1]== "eva":
                stu_fun.evaluate(query, selections)
          elif selections[0] == 't_menu':
            if selections[1] == 'tea_back':
              g_fun.show_menu(query, 
              tea_lang.menu_opt[user['language']],
              tea_lang.menu_text[user['language']])
            elif selections[1] == "academic":
              if len(selections) == 2:
                g_fun.show_menu(query, 
                tea_lang.menu_academic_opt[user['language']], tea_lang.menu_academic_text[user['language']]
                )
              elif selections[2] == "act":
                if len(selections) == 3:
                  g_fun.show_menu(query,
                  tea_lang.menu_academic_act_opt[user['language']], tea_lang.menu_academic_act_text[user['language']]
                  )
                elif selections[3] == "view":
                  if len(selections) == 4:
                    g_fun.show_menu(query,
                    tea_lang.menu_academic_act_view_opt[user['language']], tea_lang.menu_academic_act_view_text[user['language']]
                    )
                  else:
                    # Envía la selección, all o qualifying para ver la lista
                    tea_fun.view_activities(update, context, user, selections[4], query)
                elif selections[3] == "grade":
                  if len(selections) == 4:
                    g_fun.show_menu(query,
                    tea_lang.menu_academic_act_grade_opt[user['language']], tea_lang.menu_academic_act_grade_text[user['language']]
                  )
                  elif selections[4] == "upload":
                    g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_act_grade_upload_text[user['language']], query=query)
                    tea_fun.config_files_send_document(context, user,'grades')
                  elif selections[4] == "cmd":
                    g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_act_grade_cmd_text[user['language']],mode = 'Markdown', query=query)
                elif selections[3] == "add":
                  tea_lang.add_activity
                  
                elif selections[3] == "modify":
                  print("MODIFY ACTIVITIES")
                  g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_act_modify_text([user['language']]))
                  
                elif selections[3] == "delete":
                  print("DELETE ACTIVITIES")
                  
              elif selections[2] == "grades":
                if len(selections) == 3:
                  g_fun.show_menu(query,
                  tea_lang.menu_academic_grades_opt[user['language']], tea_lang.menu_academic_grades_text[user['language']]
                  )
                elif selections[3] == "view":
                  print("GRADES VIEW")
                elif selections[3] == "arf":
                  print("GRADES ARF")
              elif selections[2] == "stu":
                if len(selections) == 3:
                  g_fun.show_menu(query,
                  tea_lang.menu_academic_stu_opt[user['language']], tea_lang.menu_academic_stu_text[user['language']]
                  )
                elif selections[3] == "view":
                  if len(selections) == 4:
                    g_fun.show_menu(query,
                    tea_lang.menu_academic_stu_view_opt[user['language']], tea_lang.menu_academic_stu_view_text[user['language']]
                    ) 
                  elif selections[4] == "file":
                    print('VIEW STUDENTS FILE')
                  elif selections[4] == "reg":
                    print('VIEW REGISTERED STUDENTS')
                elif selections[3] == "add":
                  print('ADD STUDENT')
                  g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_stu_add_text[user['language']])
                elif selections[3] == "modify":
                  print('MODIFY STUDENT')
                  g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_stu_modify_text[user['language']])
                elif selections[3] == "delete":
                  print('DELETE STUDENT')
                  g_fun.send_Msg(context, user['_id'], tea_lang.menu_academic_stu_delete_text[user['language']])
              elif selections[2] == "vc":
                if len(selections) == 3:
                  g_fun.show_menu(query,
                  tea_lang.menu_academic_vc_opt[user['language']], tea_lang.menu_academic_vc_text[user['language']]
                  )
                elif selections[3] == "members":
                  #if len(selections) == 4:
                    print('VC MEMBERS LLENAR CON MIEMBROS')
                    g_fun.show_menu(query,
                    tea_lang.menu_academic_vc_members_opt[user['language']], tea_lang.menu_academic_vc_members_text[user['language']]
                    )
                elif selections[3] == "planet":
                  #if len(selections) == 4:
                  print('VC PLANET LLENAR CON los planetas')
                  g_fun.show_menu(query,
                  tea_lang.menu_academic_vc_members_opt[user['language']], tea_lang.menu_academic_vc_members_text[user['language']]
                  )
                elif selections[3] == "subject":
                #if len(selections) == 4:
                  print('VC SUBJECT ')

          elif category == "welcome":
            g_fun.welcome(context, query, user)    
        else:
          if choice == "suggestion":
            suggestion(query)
          elif choice == "change_language":
            change_language(query)
          elif choice == "actions":
            cmd.actions(update, context)
    else:
      if user['is_teacher']:
        tea_fun.config_files_set(context, user)
      else:
        query.edit_message_text(
          parse_mode = "HTML",
          text = stu_lang.not_config_files_set_text (context, user['language'])
      )
  except:
    g_fun.print_except(inspect.stack()[0][3])


def check_email(update, context):
  try:
    print("CHECK CMD *** CHECK EMAIL ***")
    chat_id = update._effective_chat.id
    if chat_id > 0:
      if cfg.is_config_files_set:
        user = g_fun.get_user_data(update)
        if not user:
          return False
        if len(context.args) ==1:
          email = context.args[0].lower()
          print(email.lower())
          if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', email.lower()):
            if db.registered_students.find_one({'email':email}):
              g_fun.send_Msg(context, user['_id'], stu_lang.check_email_already_registered_text(email, user['language']))
              return True
            else:
              if db.students_file.find_one({'_id':email}):
                student = db.students_file.find_one({'_id':email})
                print(user,"\n",student)

                if edu_fun.create_collections(user):
                  db.registered_students.save({
                    '_id' : user['_id'],
                    'email':email,
                    'name' : f"{student['last_name']}, {student['first_name']}",
                    'telegram_name' : user['telegram_name'],
                    'username' : user['username'],
                    'planet' : user['planet'],
                    'is_teacher' : user['is_teacher'],
                    'language' : user['language']
                  })
                  cfg.registered_students.add(user['_id'])
                  g_fun.send_Msg(context, user['_id'], stu_lang.check_email_successfully_registered_text[user['language']])
                  return True
                else:
                  return False
              else:
                g_fun.send_Msg(context, user['_id'], stu_lang.check_email_not_found_text(email, user['language']))
          else:
            g_fun.send_Msg(context, user['_id'],
            g_lang.email_syntax_error_text(user['language'], email))
        elif len(context.args) < 1:
          g_fun.send_Msg(context, user['_id'], stu_lang.check_email_no_args_text[user['language']])
        else:
          g_fun.send_Msg(context, user['_id'], stu_lang.check_email_many_args_text(' '.join(context.args), user['language']))
      else:
        g_fun.send_Msg(context, chat_id,
        stu_lang.not_config_files_set_text (context, user['language']))
    else:
      g_fun.send_Msg(context, chat_id,
      g_lang.wrong_command_group[user['language']])
  except:
    g_fun.print_except(inspect.stack()[0][3])


def change_language(update, context):
  try:
    chat_id = update._effective_chat.id
    user = g_fun.get_user_data(update)
    if not user:
        return False
    if chat_id > 0:
      if db.telegram_users.find_one({'_id':user['_id']}):
        user = db.telegram_users.find_one({'_id':user['_id']})
        current_lang = user['language']
        new_lang = "EN" if current_lang == "ES" else "ES"
        db.telegram_users.update_one({'_id':user['_id']},
          {'$set':{
            'language':new_lang}})
        g_fun.send_Msg(context, chat_id,
        g_lang.cmd_change_language_text[user['language']])
    else:
      g_fun.send_Msg(context, chat_id,
      g_lang.wrong_command_group[user['language']])
  except:
    g_fun.print_except(inspect.stack()[0][3])


def grade_students(update, context):
  try:
    user = g_fun.get_user_data(update)
    if tea_fun.check_teacher(update, context):
      tea_fun.grade_students(update, context, user, context.args)
  except:
    g_fun.print_except(inspect.stack()[0][3])






if __name__ == '__main__':
    pass