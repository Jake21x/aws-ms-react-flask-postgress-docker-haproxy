from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostLogsMobile(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        print(len(json_dict))
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['mgenerated_id'] 
                # print('gid',str(gid))  
                json_dict[i]['mgenerated_id'] = server_generated_id() if gid in ('.','',None) else gid
                # print('mgenerated_id',json_dict[i]['mgenerated_id'])
                data.append((
                    json_dict[i]['tbluserid'],
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['mgenerated_id'],
                    json_dict[i]['module'],
                    json_dict[i]['event'],
                    json_dict[i]['current_longitude'],
                    json_dict[i]['current_latitude'],
                    json_dict[i]['end_longitude'],
                    json_dict[i]['end_latitude'],
                    json_dict[i]['gps_accuracy'],
                    json_dict[i]['gps_provider'],
                    json_dict[i]['battery'],
                    json_dict[i]['netinfo'],
                    json_dict[i]['device_id'],
                    json_dict[i]['datetime_log'], )) 

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into logs_mobile (tbluserid,tblstoreid,mgenerated_id,module, event, current_longitude, current_latitude, end_longitude, end_latitude, gps_accuracy, gps_provider, battery,netinfo,device_id, date_created) values {}
                ON CONFLICT (tbluserid,mgenerated_id,date_created) DO NOTHING;
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

 