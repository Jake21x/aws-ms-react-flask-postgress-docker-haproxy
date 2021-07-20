from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostOSA(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = [] 
            data_store_sku = [] 

            for i in chain(range(0, x)):
                userid = json_dict[i]['tbluserid']
                storeid =  json_dict[i]['tblstoreid']
                mobile =  json_dict[i]['tblstoreid']
                
                gid = json_dict[i]['mobile_generated_id'] 
                mobile_id = server_generated_id() if gid in ('.','') else gid
                created = json_dict[i]['date_created'] 
                updated = json_dict[i]['date_updated'] 
                
                for j in chain(range(0, len(json_dict[i]['sku']))):
                    tblskuid = json_dict[i]['sku'][j]['tblskuid'] 
                    availability = json_dict[i]['sku'][j]['availability'] 
                    sku_id = mobile_id + tblskuid
                    data.append((userid,storeid,mobile_id,tblskuid,availability,sku_id ,created,updated ))
                    
                    sku_status = ""
                    if availability == '1':
                        sku_status = 'Yes'
                    else:
                        sku_status = 'No'
                    
                    data_store_sku.append((storeid,tblskuid,sku_status , updated ))

            print(data) 
            args_str = ','.join(['%s'] * len(data)) 
            conn.mogrify("""
                insert into m_osa (tbluserid,tblstoreid,mobile_generated_id,tblskuid,availability,sku_generated_id,date_created,date_updated) values {}
                ON CONFLICT (tbluserid,tblstoreid,tblskuid,date_created) DO NOTHING;
                """.format(args_str) , data , commit=True)


            args_str_up = ','.join(['%s'] * len(data_store_sku)) 
            conn.mogrify("""
                insert into stores_skus (storeid,skuid,carry,date_updated) values {}
                ON CONFLICT (storeid,skuid) DO UPDATE 
                SET (carry,date_updated) = 
                    (
                        EXCLUDED.carry,
                        EXCLUDED.date_updated
                    );
                """.format(args_str_up) , data_store_sku , commit=True) 


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