import mysql.connector
import json

def handle (params):
    data = json.loads(params)
    
    db_user = data["db_setting"]["db_user"]
    db_password = data["db_setting"]["db_password"]
    db_host = data["db_setting"]["db_host"]
    db_database = data["db_setting"]["db_database"]
    
    id_tg = data["bot_params"]["id_tg"]
    tg_username = "@"+data["bot_params"]["tg_username"]
    tg_full_name = data["bot_params"]["tg_full_name"]
    
    time_of_entry_param = str(data["bot_params"]["time_of_entry"])
    
    #parse DATETIME
    time_of_entry_param_massive = time_of_entry_param.split()
    date_of_entry_massiv = time_of_entry_param_massive[0].split(".")
    date_of_entry = date_of_entry_massiv[2]+"-"+date_of_entry_massiv[1]+"-"+date_of_entry_massiv[0]
    time_of_entry_time = time_of_entry_param_massive[1]+":00"
    time_of_entry = date_of_entry+" "+time_of_entry_time
    
    connection = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_database)
    
    cursor = connection.cursor()
    querry = f"""SELECT id_tg FROM user WHERE id_tg = {id_tg}"""
    cursor.execute(querry)
    
    record = cursor.fetchall()
    if (record): #There are in Data base?
        result = 1 
        try:
            querry8 = f"""SELECT id_tg FROM user WHERE id_tg = {id_tg} AND time_of_entry IS NULL """
            cursor.execute(querry8)
            record3 = cursor.fetchone()
            if(record3):
                querry6 = f"""UPDATE user SET tg_username = "{tg_username}", tg_full_name = "{tg_full_name}", time_of_entry = "{time_of_entry}", is_in_the_group = 1 WHERE id_tg = {id_tg} AND time_of_entry IS NULL"""
                cursor.execute(querry6);
            else:
                querry9 = f"""SELECT id_tg FROM user WHERE id_tg = {id_tg} AND time_of_entry IS NOT NULL """
                cursor.execute(querry9)
                record4 = cursor.fetchone()
                if (record4):
                    querry7 = f"""UPDATE user SET tg_username = "{tg_username}", tg_full_name = "{tg_full_name}", is_in_the_group = 1 WHERE id_tg = {id_tg} AND time_of_entry IS NOT NULL"""
                    cursor.execute(querry7)
        except:
            cursor.close()
            connection.commit()
            connection.close()
            res = {"res":"Error"}
            return json.dumps(res)
            
    else:
        result = 0
        querry2 = f"""INSERT INTO user (id_tg, tg_username, tg_full_name, time_of_entry, is_in_the_group) VALUES ({id_tg}, "{tg_username}", "{tg_full_name}", "{time_of_entry}", 1)"""
        cursor.execute(querry2);

            
    cursor.close()
    
    connection.commit()
    connection.close()

    res = {"res":result}
    return json.dumps(res)

#s = '{"db_setting": {"db_user":"chermisha2","db_password":"Ck2ABSXRPJT$GPVJ", "db_host":"FVH1.spaceweb.ru", "db_database":"chermisha2"}, "bot_params": {"id_tg":12314, "tg_username":"#{tg_username}", "tg_full_name":"#{tg_full_name}", "refery_link":"https://t.me/+vONuEALlBwdiYTMy", "time_of_entry":"23.02.2042 23:42"}}'
#print(handle(s))