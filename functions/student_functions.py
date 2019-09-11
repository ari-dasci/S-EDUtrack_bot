import inspect 
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup)

import configuration.config_file as cfg
from configuration.config_file import (
  db, client)
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
        keyboard = stu_lang.menu[user['language']]["opt"]
        reply_markup = IKMarkup(keyboard)
        update.message.reply_text(
              parse_mode = 'HTML',
              text = stu_lang.menu[user['language']]['text'],
              reply_markup = reply_markup)
      else:
        pass  
    else:
      g_fun.send_Msg(context, chat_id, stu_lang.not_config_files_set_text (context, user['language']))
  except:
    g_fun.print_except(inspect.stack()[0][3])


def my_grade(update, context, user, query):
  try:
    #print("CHECK STUFUN *** ENTRO A STUDENT VIEW GRADE **")
    actual_week = g_fun.get_week(action="text")
    email = db.registered_students.find_one({'_id': user['_id']})['email']
    activities_list = ""
    grades = db.grades.find_one({'_id':email})["activities"]
    week = g_fun.get_week()

    if cfg.active_activities:
      for activity in cfg.active_activities:
        grade = grades[activity]
        activities_list += f"{activity} = {grade}\n"
    
      student_arf = db.arf.find_one({'_id':user['_id']},{'_id':0})['weeks'][actual_week]
      linguistic_arf = student_arf['linguistic_arf']
      pot_recovery_score  = round(student_arf['pot_recovery_score'],3)
      actual_score = round(db.grades.find_one({'_id':email})['total_score'],3)
      g_fun.send_Msg(context, user['_id'],
        stu_lang.my_grade(user['language'], "grades", week, linguistic_arf, actual_score,pot_recovery_score, activities_list))
    else: g_fun.send_Msg(context, user['_id'],
        stu_lang.my_grade(user['language'], "no_active",week))

  except:
    g_fun.print_except(inspect.stack()[0][3])


def opn_tea_practice(context, query, user, selections):
  try:
    #print("CHECK *** OPN TEACHER PRACTICE ***")
    actual_week = g_fun.get_week("text")
    num_week = g_fun.get_week()
    criterion = value = ""
    category = selections[3]
    if len(selections) > 4:
      criterion = selections[4]
      if len(selections) > 5:
        value = selections[5]

    if not value: 
      if not criterion:
        if category == 'teacher':
          criteria = {criterion for criterion in cfg.teacher_criteria if "T_" in criterion}
        else:
          criteria = {criterion for criterion in cfg.teacher_criteria if "C_" in criterion}
        
        db_criteria = db.eva_teacher.find_one({'_id':user['_id'],},{'_id':0})
        for criterion in db_criteria:
          if db_criteria[criterion][actual_week]:
            criteria.discard(criterion)

        keyboard = []
        for criterion in criteria:
          keyboard.append([IKButton(criterion[2:],
                          callback_data=f's_menu-opn-tp-{category}-{criterion}' )])
        keyboard.append([IKButton(g_lang.back_text[user['language']],
                        callback_data=f's_menu-opn-tp' )])              
        
        if len(keyboard) == 1:
          g_fun.show_menu(query, keyboard,
            stu_lang.opn_tea_practice(user['language'],"no_criteria",week=num_week))

        else:
          g_fun.show_menu(query, keyboard,
                      stu_lang.opn_tea_practice_menu[user['language']]["text"])
      else:
        
        g_fun.show_menu(query, g_lang.scale_7(user['language'],query.data),
          stu_lang.opn_tea_practice(user['language'], "criterion",criterion, num_week))
    else:
      db.eva_teacher.update_one({'_id':user['_id']},{
        '$set':{f"{criterion}.{actual_week}" : value}
      })
      #g_fun.show_menu(query,stu_lang.opn_tea_practice_menu[user['language']]['opt'],stu_lang.opn_tea_practice(user['language'],'text_after_save'))
      
      opn_collaboration(context, query, user, selections[:-3])
  except:
    g_fun.print_except(inspect.stack()[0][3])


def opn_collaboration(context, query, user, selections):
  try:
    #print("CHECK *** OPN COLLABORATION ***")
    actual_week = g_fun.get_week("text")
    num_week = g_fun.get_week()
    classmate =value = ""
    
    if len(selections) > 3:
      classmate = selections[3]
      if len(selections) > 4:
          value = selections[4]

    if not value:
      if not classmate:
        classmates = db.eva_collaboration.find_one({'_id':user['planet']},{'_id':0})['members'][user['_id']]['classmates']

        keyboard = []
        for classmate in classmates:
          if not classmates[classmate]['weeks'][actual_week]:
            name = db.registered_students.find_one({'_id':classmate})['name']
            keyboard.append([IKButton(name, callback_data =  f"s_menu-opn-coll-{classmate}")])
          keyboard.append([IKButton(g_lang.back_text[user['language']],
            callback_data=f's_menu-opn' )])
        if len(keyboard)==1:
          g_fun.show_menu(query, keyboard,
          stu_lang.opn_collaboration(user['language'],"no_classmates",week=num_week))
        else:
          g_fun.show_menu(query, keyboard,
            stu_lang.opn_collaboration(user['language'],"text"))
      else:
        g_fun.show_menu(query, g_lang.scale_7(user['language'],query.data),
          stu_lang.opn_collaboration(user['language'], "scale", classmate, num_week))
    else:
      db.eva_collaboration.update_one({'_id':user['planet']},{
        '$set':{f"members.{user['_id']}.classmates.{classmate}.weeks.{actual_week}" : value}
      })
      #g_fun.show_menu(query, stu_lang.menu_opinion[user['language']]['opt'], stu_lang.opn_collaboration(user['language'],'text_after_save'))
      opn_collaboration(context, query, user, selections[:-2])
  except:
    g_fun.print_except(inspect.stack()[0][3])

def opn_rsrcs(context, query, user, selections):
  try:
    #print("CHECK *** OPN RESOURCES ***")
    actual_week = g_fun.get_week("text")
    num_week = g_fun.get_week()
    if cfg.resources['week'] < num_week:
      g_fun.get_resources()
    section = resource = value = ""
    
    if len(selections) > 3:
      section = selections[3]
      if len(selections) > 4:
        resource = selections[4]
        if len(selections) > 5:
          value = selections[5]
    student_resources = db.eva_resources.find_one({'_id':user['_id']},{'_id':0})
    #sections_resources = list(db.activities.distinct("section",{'week':{'$lte':num_week}}))
    #sections_resources.sort()
    #revised_resources = db.activities.find({'week':{'$lte':num_week}})
    keyboard = []
    if not value:
      if not resource:
        if not section:
          
            sections = sorted(cfg.resources)
            sections.remove('week')
            for section in sections:
              for resource in cfg.resources[section]:
                if not student_resources[section][resource]:
                  keyboard.append([IKButton(section,
                    callback_data=f"s_menu-opn-rsrcs-{section}")])
                  break
            keyboard.append([IKButton(g_lang.back_text[user['language']],
              callback_data=f's_menu-opn' )])
            
            if len(keyboard)==1:
              g_fun.show_menu(query, keyboard,
                stu_lang.opn_resources(user['language'],"no_section"))
            else:
              g_fun.show_menu(query, keyboard,
                stu_lang.opn_resources(user['language'],"text_section"))
        else:
          for resource in cfg.resources[section]:
            if not student_resources[section][resource]:
              resource_name = db.activities.find_one({'_id':resource})['name']
              keyboard.append([IKButton(resource_name,
                    callback_data=f"s_menu-opn-rsrcs-{section}-{resource}")])
          keyboard.append([IKButton(g_lang.back_text[user['language']],
              callback_data=f's_menu-opn' )])
          g_fun.show_menu(query, keyboard,
            stu_lang.opn_resources(user['language'],"text_rsrc"))
      else:
        resource_name = db.activities.find_one({'_id':resource})['name']
        g_fun.show_menu(query, g_lang.scale_7(user['language'],query.data),
          stu_lang.opn_resources(user['language'], "scale", resource_name))

    else:
      db.eva_resources.update_one({'_id':user['_id']},{
        '$set':{
          f"{section}.{resource}":value
        }
      })

      opn_rsrcs(context, query, user, selections[:-3])
  except:
    g_fun.print_except(inspect.stack()[0][3])