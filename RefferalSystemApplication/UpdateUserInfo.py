# -*- coding: cp1251 -*-
import mysql.connector
import json

def handle (params):
    data = json.loads(params)
    
    db_user = data["db_setting"]["db_user"]
    db_password = data["db_setting"]["db_password"]
    db_host = data["db_setting"]["db_host"]
    db_database = data["db_setting"]["db_database"]
    
    id_tg = data["bot_params"]["id_tg"]
    tg_username = data["bot_params"]["tg_username"]
    tg_full_name = data["bot_params"]["tg_full_name"]
    
    try: phone_number = data["bot_params"]["phone_number"] 
    except: phone_number = None
    try: id_doterra = data["bot_params"]["id_doterra"] 
    except: id_doterra = None
    try: referral_link = data["bot_params"]["referral_link"] 
    except: referral_link = None
    try: link_generation_time_par = str(data["bot_params"]["link_generation_time"]) 
    except: link_generation_time_par = (None)
    try: full_name = data["bot_params"]["full_name"]
    except: full_name = None
    try: email = data["bot_params"]["email"]
    except: email = None
    try: city = data["bot_params"]["city"]
    except: city = None

    
    #parse DATETIME
    if link_generation_time_par != None:
        link_generation_time_param_massive = link_generation_time_par.split()
        link_generation_date_massiv = link_generation_time_param_massive[0].split(".")
        link_generation_date = link_generation_date_massiv[2]+"-"+link_generation_date_massiv[1]+"-"+link_generation_date_massiv[0]
        link_generation_time_time = link_generation_time_param_massive[1]+":00"
        link_generation_time = link_generation_date+" "+link_generation_time_time
    else: 
        link_generation_time = None
    
    connection = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_database)
    
    cursor = connection.cursor()
    querry = f"""SELECT id_tg FROM user WHERE id_tg = {id_tg}"""
    cursor.execute(querry)
    
    record = cursor.fetchall()
  
    
    if (record): #There are in Data base?
        result = 1
        if (link_generation_time != None):
            querry = f"""UPDATE user SET tg_username = "{tg_username}", tg_full_name = "{tg_full_name}", phone_number = "{phone_number}", id_doterra = {id_doterra}, referral_link = "{referral_link}", full_name = "{full_name}", email = "{email}", link_generation_time = "{link_generation_time}", city = "{city}" WHERE id_tg = {id_tg}"""
        else:
            querry = f"""UPDATE user SET tg_username = "{tg_username}", tg_full_name = "{tg_full_name}", phone_number = "{phone_number}", full_name = "{full_name}", email = "{email}", city = "{city}" WHERE id_tg = {id_tg}"""
        cursor.execute(querry);
     
    else:
        result = 0

        
            
    cursor.close()
    
    connection.commit()
    connection.close()

    res = {"res":result}
    return json.dumps(res)


#s = '{"db_setting": {"db_user":"chermisha2","db_password":"Ck2ABSXRPJT$GPVJ", "db_host":"FVH1.spaceweb.ru", "db_database":"chermisha2"}, "bot_params": {"id_tg":12314, "tg_username":"#{tg_username}", "tg_full_name":"#{tg_full_name}"}}'
#print(handle(s))