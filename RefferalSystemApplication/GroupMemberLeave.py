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
    
    connection = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_database)
    
    cursor = connection.cursor()
    querry = f"""SELECT id_tg FROM user WHERE id_tg = {id_tg}"""
    cursor.execute(querry)
    
    record = cursor.fetchall()
  
    
    if (record): #There are in Data base?
        result = 1
        querry = f"""UPDATE user SET is_in_the_group = 0 WHERE id_tg = {id_tg} AND is_in_the_group = 1"""
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