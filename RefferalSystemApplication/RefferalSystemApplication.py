# -*- coding: utf-8 -*-
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
    querry = f"""SELECT id_tg, tg_username, tg_full_name FROM user WHERE refery_id_tg = {id_tg} ORDER BY tg_username DESC"""
    cursor.execute(querry)
    record = cursor.fetchall()
    try:
        result = 1
        referal = {"referal": []}
        referal_text = ""
        referral_count=0
        for rec in record:
            referal["referal"].append({"id_tg": rec[0], "tg_username": rec[1], "tg_full_name": rec[2]})
            referral_count+=1
            referal_text += str(referral_count) + ". "+str(rec[1]) + " | " + "sssdssd" + "\n"
            
    except:
        result = 0
        
    
    cursor.close()
    
    connection.commit()
    connection.close()

    res = {"result":result, "referal":referal, "referral_count": referral_count, "referal_text": referal_text}
    return json.dumps(res)

s = '{"db_setting": {"db_user":"chermisha2","db_password":"Ck2ABSXRPJT$GPVJ", "db_host":"FVH1.spaceweb.ru", "db_database":"chermisha2"}, "bot_params": {"id_tg":756885569}}'
print(handle(s))