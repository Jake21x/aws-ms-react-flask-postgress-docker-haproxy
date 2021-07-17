
from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiGetVideoAccessUser(Resource):
    def get(self):

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