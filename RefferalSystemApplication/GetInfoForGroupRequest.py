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
    
    #we receive the data of the person who submitted the application
    querry = f"""SELECT id_tg, phone_number, tg_username, tg_full_name, full_name, city, email FROM user WHERE id_tg = {id_tg}"""
    cursor.execute(querry)
    record = cursor.fetchall()
    request_param = {"user_request_param":[],"refery_request_param":[],"refery_doterra_request_param":[]}
    for rec in record:
        request_param["user_request_param"].append({"id_tg":rec[0], "phone_number":rec[1], "tg_username":rec[2], "tg_full_name":rec[3],"full_name":rec[4], "city":rec[5],"email":rec[6]}) 
    
    #we get the data of his referee
    querry2 = f"""SELECT refery_id_tg FROM user WHERE id_tg = "{id_tg}" """
    cursor.execute(querry2)
    refery_id_tg = cursor.fetchone()
    is_refery_have_id_doterra = None
    if (refery_id_tg[0] !=None):
        querry3 = f"""SELECT id_tg, phone_number, tg_username, tg_full_name, full_name, city, email, id_doterra FROM user WHERE id_tg = "{refery_id_tg[0]}" """
        cursor.execute(querry3)
        record3 = cursor.fetchall()
        for rec in record3:
            request_param["refery_request_param"].append({"id_tg":rec[0], "phone_number":rec[1], "tg_username":rec[2], "tg_full_name":rec[3],"full_name":rec[4], "city":rec[5],"email":rec[6], "id_doterra":rec[7]}) 
            is_refery_have_id_doterra = True if (rec[7]!=None) else False
    else: 
        request_param["refery_request_param"].clear()
        request_param["refery_request_param"].append(" ---- (user doesn't have refery)")
    
    #we get the referee's data with the doterra id
    if (is_refery_have_id_doterra == False):
        querry6 = f"""SELECT id_tg FROM user """
        cursor.execute(querry6)
        all_record = cursor.fetchall()
        is_refery_have_id_doterra2=None
        id_tg_if_not_found = refery_id_tg
        for rec in all_record: #We are looking for a referee with doterra id
            id_tg_ref = refery_id_tg
            querry4 = f"""SELECT refery_id_tg FROM user WHERE id_tg = "{id_tg_ref[0]}" """
            cursor.execute(querry4)
            refery_id_tg = cursor.fetchone()
            if (refery_id_tg[0] !=None):
                querry5 = f"""SELECT id_tg, phone_number, tg_username, tg_full_name, full_name, city, email, id_doterra FROM user WHERE id_tg = "{refery_id_tg[0]}" """
                cursor.execute(querry5)
                record4 = cursor.fetchall()
                for rec in record4:
                    if (rec[7]!=None):
                        is_refery_have_id_doterra2=True
                        request_param["refery_doterra_request_param"].append({"id_tg":rec[0], "phone_number":rec[1], "tg_username":rec[2], "tg_full_name":rec[3],"full_name":rec[4], "city":rec[5],"email":rec[6], "id_doterra":rec[7]}) 
                if (is_refery_have_id_doterra2==True):
                    break
            else:
                break
        #if you do not find a referee with doterra id, then we take a second-level referee (referee from the referee)
        if (is_refery_have_id_doterra2!=True):
            querry6 = f"""SELECT refery_id_tg FROM user WHERE id_tg = "{id_tg_if_not_found[0]}" """
            cursor.execute(querry6)
            record_refery_id_tg = cursor.fetchone()
            querry7 = f"""SELECT id_tg, phone_number, tg_username, tg_full_name, full_name, city, email, id_doterra FROM user WHERE id_tg = "{record_refery_id_tg[0]}" """
            cursor.execute(querry7)
            record5 = cursor.fetchall()
            for rec in record5:
                request_param["refery_doterra_request_param"].append({"id_tg":rec[0], "phone_number":rec[1], "tg_username":rec[2], "tg_full_name":rec[3],"full_name":rec[4], "city":rec[5],"email":rec[6], "id_doterra":rec[7]}) 
        
        if (len(request_param["refery_doterra_request_param"]) == 0):
            request_param["refery_doterra_request_param"].clear()
            request_param["refery_doterra_request_param"].append(" ---- (refery1 doesn't have refery)")
        
        
    else: 
        if (is_refery_have_id_doterra==True):
            request_param["refery_doterra_request_param"].clear()
            request_param["refery_doterra_request_param"].append(" ---- (refery1 has id doterra)")
        else:
            request_param["refery_doterra_request_param"].clear()
            request_param["refery_doterra_request_param"].append(" ---- (user doesn't have refery)")
    cursor.close()
    
    connection.commit()
    connection.close()

    res = {"request_param": request_param, "refery_request_param": request_param["refery_request_param"]}
    return json.dumps(res)



#s = '{"db_setting": {"db_user":"chermisha2","db_password":"Ck2ABSXRPJT$GPVJ", "db_host":"FVH1.spaceweb.ru", "db_database":"chermisha2"}, "bot_params": {"id_tg":756885569}}'
#print(handle(s))