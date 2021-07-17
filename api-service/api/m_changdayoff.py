from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostChangeDayoff(Resource):
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
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['current_day_off'],
                    json_dict[i]['new_day_off'],
                    json_dict[i]['confirm_by'],
                    json_dict[i]['confirmation'],
                    json_dict[i]['change_by_id'],
                    json_dict[i]['date_created'], 
                    ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_changedayoff(tbluserid,mobile_generated_id, tblstoreid, current_day_off, new_day_off, confirm_by, confirmation,change_by_id, date_created) values {}
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


class ApiGetChangedayOff(Resource):
    def get(self,userid=None):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try:  
             
            return []

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