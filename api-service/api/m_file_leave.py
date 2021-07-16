from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostFileLeave(Resource):
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
                    json_dict[i]['tbluserid'],
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['longitude'],
                    json_dict[i]['latitude'],
                    json_dict[i]['leave_category'],
                    json_dict[i]['date_of_leave_from'],
                    json_dict[i]['date_of_leave_to'],
                    json_dict[i]['reason'],
                    json_dict[i]['confirm_by'],
                    json_dict[i]['confirmation'],
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['date_created'],
                    ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_file_leave (tbluserid, tblstoreid, longitude, latitude, leave_category, date_of_leave_from, date_of_leave_to, reason, confirm_by, confirmation, mobile_generated_id, date_created) values {}
                ON CONFLICT (tbluserid,mobile_generated_id) DO NOTHING;
                """.format(args_str) , data , commit=True) 
        
            return {'status' : 'success', 'message' : 'success'}

        except psycopg2.ProgrammingError as exc:
            return {'status' : 'failed', 'message' : str(exc)}
            
        except BaseException as e:
            return {'status' : 'failed', 'message' : str(e)}
        except Exception as e:
            x = str(e)
            x.replace('\n', '')
            return {'status' : 'failed', 'message' : str(x)}
        finally:
            print("completed")