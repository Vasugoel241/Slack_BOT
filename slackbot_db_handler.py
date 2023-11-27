import time
from config import Config
from config import setuplogger, logger

setuplogger()

class SlackbotDB:

    def get_jobcount(job_name):
        try:
            connection = Config.connect_to_database()
            cursor = connection.cursor()        
        

            check_query = "SELECT COUNT(jobname) FROM JOB_STATUS WHERE jobname = %s"
            values = (job_name,)
            cursor.execute(check_query,values)

            row = cursor.fetchone()
            
            connection.commit()
            cursor.close()
            connection.close()

            return row[0]
        except Exception as e:
            logger.exception(f"DB Get error: {e}")

    def add_jobname(job_name):
        try:
            connection = Config.connect_to_database()
            cursor = connection.cursor()        
            
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S",t)

            insert_query = "INSERT INTO JOB_STATUS (jobname, action, start_time) VALUES (%s, %s, %s)"
            values = (job_name,'pending',current_time)
            cursor.execute(insert_query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            logger.exception(f"DB Insertion error: {e}")

    def update_job_status(job_name):
        try:
            connection = Config.connect_to_database()
            cursor = connection.cursor()        
            
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S",t)

            update_query = "UPDATE JOB_STATUS SET action = %s, approver_name = NULL, approver_id = NULL, start_time = %s, action_time = NULL WHERE jobname = %s" 
            values = ('pending',current_time,job_name)
            cursor.execute(update_query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            logger.exception(f"DB Update error: {e}")

    def update_action(job_name,action, approver_name, approver_id):
        try:
            connection = Config.connect_to_database()
            cursor = connection.cursor()    
            
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S",t)
            
            update_query = "UPDATE JOB_STATUS SET action = %s, approver_name = %s, approver_id = %s, action_time = %s WHERE jobname = %s"
            values = (action,approver_name,approver_id,current_time,job_name)
            cursor.execute(update_query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            logger.exception(f"DB Update error: {e}")


    def get_action(job_name):
        try:
            connection = Config.connect_to_database()
            cursor = connection.cursor()    
            
            select_query = "SELECT action FROM JOB_STATUS WHERE jobname = %s"
            cursor.execute(select_query,(job_name,))

            row = cursor.fetchone()
            
            connection.commit()
            cursor.close()
            connection.close()

            return row
        except Exception as e:
            logger.exception("Error while getting")