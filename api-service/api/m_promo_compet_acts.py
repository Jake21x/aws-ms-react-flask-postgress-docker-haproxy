from flask_restful import Resource,request
from utils import server_generated_id,UPLOAD_FOLDER
from database import Database  
from itertools import chain 
import psycopg2 
import os,base64

class ApiPostPromoCompetActs(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            pdata = []
            cdata = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['mobile_generated_id'] 
                use_id = server_generated_id() if gid in ('.','') else gid

                if json_dict[i]['image_path'] !=".":
                    with open(os.path.join(UPLOAD_FOLDER, use_id + ".jpg"), "wb") as fh:
                        json_dict[i]['image_path'] = str('uploads/' + use_id + ".jpg")
                        fh.write(base64.b64decode(json_dict[i]['image_path']))
                else:
                    print('no photo') 
                 
                item = (
                        json_dict[i]['tbluserid'],
                        json_dict[i]['tblstoreid'],
                        json_dict[i]['tblskuid'],
                        json_dict[i]['tblcatid'],
                        json_dict[i]['competitor'],
                        json_dict[i]['activity_name'],
                        json_dict[i]['mechanics'],
                        json_dict[i]['sku_name'],
                        json_dict[i]['notes'],
                        json_dict[i]['scheme'],
                        json_dict[i]['price'],
                        json_dict[i]['placement'],
                        json_dict[i]['duration_type'],
                        json_dict[i]['date_from'],
                        json_dict[i]['date_to'],
                        json_dict[i]['has_effect_on_offtake'],
                        json_dict[i]['image_path'],
                        json_dict[i]['type'],
                        use_id,
                        json_dict[i]['sku_price'],
                        json_dict[i]['date_created'],
                        json_dict[i]['date_updated'],
                        json_dict[i]['brand'],
                    )

                pdata.append(item)
                cdata.append(item)

            # args_str = ','.join(['%s'] * len(data)) 
            # query = conn.mogrify("""
            #     insert into m_planograms (tbluserid,tblstoreid, type, tblcategoryid,tblrefid, followed, notes, image_path, mobile_generated_id, date_created, date_updated) values {}
            #     ON CONFLICT (tbluserid,mobile_generated_id) DO NOTHING;
            #     """.format(args_str) , data , commit=True) 
        
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