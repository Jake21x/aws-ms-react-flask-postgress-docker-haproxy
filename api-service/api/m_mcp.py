from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostMCP(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['sku_generated_id'] 
                json_dict[i]['sku_generated_id'] = server_generated_id() if gid in ('.','') else gid

                data.append((
                    json_dict[i]['tbluserid'],
                    json_dict[i]['tblskuid'],
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['availability'],
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['date_created'],
                    json_dict[i]['date_updated'],
                    json_dict[i]['sku_generated_id'],
                    ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_osa (tbluserid,tblskuid,tblstoreid,availability,mobile_generated_id,date_created,date_updated,sku_generated_id) values {}
                ON CONFLICT (tbluserid,tblstoreid,sku_generated_id,date_created) DO NOTHING;
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