from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostFacings(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['mobile_generated_id'] 
                use_id = server_generated_id() if gid in ('.','') else gid

                data.append(
                    (
                    json_dict[i]['tbluserid'],
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['tblrefid'],
                    json_dict[i]['tblcategoryid'],
                    json_dict[i]['no_of_facings'],
                    json_dict[i]['category_space'],
                    json_dict[i]['mnc_space'],
                    json_dict[i]['percent_share'],
                    json_dict[i]['target'],
                    json_dict[i]['complied'],
                    json_dict[i]['actual_cm_space'],
                    json_dict[i]['date_created'],
                    json_dict[i]['date_updated'],
                    use_id, )
                    )

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_facings (tbluserid,tblstoreid,tblrefid,tblcategoryid, no_of_facings, category_space, mnc_space, percent_share, target, complied, actual_cm_space, date_created, date_updated,mobile_generated_id) values {}
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