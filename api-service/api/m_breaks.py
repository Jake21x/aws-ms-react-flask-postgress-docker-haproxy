from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostBreaks(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['mobile_generated_id'] 
                json_dict[i]['mobile_generated_id'] = server_generated_id() if gid in ('.','') else gid

                data.append((
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['tbluserid'], 
                    json_dict[i]['tblstoreid'], 
                    json_dict[i]['break_name'], 
                    json_dict[i]['break_designated_time'],
                    json_dict[i]['break_consume_time'], 
                    json_dict[i]['break_status'],
                    json_dict[i]['date'], 
                    json_dict[i]['time'],
                    json_dict[i]['date_created'],
                    json_dict[i]['date_updated'],
                    json_dict[i]['over_break_minutes'], 
                    ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_breaks (mobile_generated_id, tbluserid, tblstoreid, break_name, break_designated_time,break_consume_time,break_status,date,time,date_created,date_updated,over_break_minutes) values {}
                ON CONFLICT (tbluserid,mobile_generated_id) DO NOTHING;
                """.format(args_str) , data , commit=True) 
        
            return {'status' : 'success', 'message' : 'success'}

        except psycopg2.ProgrammingError as exc:
            conn.rollback()
            return {'status' : 'failed', 'message' : str(exc)}
            
        except BaseException as e:
            if conn is not None:
                conn.rollback()
            return {'status' : 'failed', 'message' : str(e)}
        except Exception as e:
            x = str(e)
            x.replace('\n', '')
            
            return {'status' : 'failed', 'message' : str(x)}
        finally:
            print("completed")