from flask import Flask
from flask_restful import Resource, reqparse, request , Api
from flask import request
from flask_httpauth import HTTPBasicAuth 
import jwt,json,os,datetime,time,random,base64 
from flask_jwt_extended import JWTManager
from functools import wraps
from itertools import chain 
from database import Database  
from api.upload_agency import UploadAgency
from api.upload_skus import UploadSKUs
from api.upload_category import UploadCategory
from api.upload_category_refs import UploadCategoryRefs
from api.upload_area import UploadArea
from api.upload_chain import UploadChain
from api.upload_stores import UploadStores
from api.upload_users import UploadUsers
from api.upload_users_schedules import UploadUsersSchedules
from api.auth import LoginAuth
from api.skus import ApiGetSKUs
from api.latestupdates import ApiLatestUpdates
from api.appversion import ApiAppVersion
from api.stores import ApiGetAllStores,ApiGetStoreSKUs,ApiGetAssignUsersInStore
from api.category import ApiGetCategory

app = Flask(__name__)
jwt = JWTManager()
api = Api(app)
jwt.init_app(app)
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'mykey'

USER_DATA = {"admin":"admin"}

conn = Database()

# dbconfig = {
#     'dbname':'sales_track_v2', 
#     'user':'postgres',
#     'host':'db.pcrwpfgzubsfyfbrczlj.supabase.co', 
#     'password':'jmgtechplays21x', 
#     'connect_timeout':'3',
#     'options':'-c statement_timeout=5000000'            
#     } 

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class Login(Resource): 
    @auth.login_required
    def get(self):
        token = jwt.encode({
            'user':request.authorization.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),

        }, app.config['SECRET_KEY'])

        return json.dumps({
            'token':token.decode('UTF-8')

        }, indent=3)



def verify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token', None)
        if token is None:
            return {"Message":"Your are missing Token"}
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return {"Message":"Token is Missing or invalid" + str(e)}
    return decorator


class HelloWorld(Resource):
    @verify_token
    def get(self):
        return json.dumps({"Messagesssssss ":"ok "})
class UPFILE(Resource):
    @verify_token
    def post(self):

        json_dict = request.get_json(force=True, silent=True)
        x = len(json_dict) 
        photo_name = []
        for i in chain(range(0, x)): 
            use_id = server_generated_id() 
            if json_dict[i]['photo'] !=".":
                with open(os.path.join(UPLOAD_FOLDER, use_id + ".jpg"), "wb") as fh:
                    photo_name.append(str('uploads/' + use_id + ".jpg"), )
                    fh.write(base64.b64decode(json_dict[i]['photo']))
            else:
                print('no photo')

        list = os.listdir(UPLOAD_FOLDER)
        number_files = len(list) 

        print('json_dict > ',json_dict , number_files)
        return json.dumps({"FILE ":"ok "})


class STATUS(Resource):
    def get(self):    
        data = conn.execute('select version()') 
        print('result',data) 
        return {"result ":data}

class ApiUploadCategoryRefs(Resource):
    def post(self):
        template = request.files['file']  
        return UploadCategoryRefs(conn,template) 

class ApiUploadCategory(Resource):
    def post(self):
        template = request.files['file']  
        return UploadCategory(conn,template) 

class ApiUploadSKUs(Resource):
    def post(self):
        template = request.files['file']  
        return UploadSKUs(conn,template) 
class ApiUploadStores(Resource):
    def post(self):
        template = request.files['file']  
        return UploadStores(conn,template) 
class ApiUploadUsers(Resource):
    def post(self):
        template = request.files['file']  
        return UploadUsers(conn,template) 

class ApiUploadUsersSchedules(Resource):
    def post(self):   
        template = request.files['file']  
        return UploadUsersSchedules(conn,template) 

class ApiUploadAgency(Resource):
    def post(self):   
        template = request.files['file']  
        return UploadAgency(conn,template) 

class ApiUploadArea(Resource):
    def post(self):   
        template = request.files['file']  
        return UploadArea(conn,template) 

class ApiUploadChain(Resource):
    def post(self):   
        template = request.files['file']  
        return UploadChain(conn,template)

class ApiAuth(Resource):
    def post(self):      
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('device_id', type=str)
        parser.add_argument('appversion', type=str)
        parser.add_argument('device_info', type=str)
        parser.add_argument('IMEI', type=str) 
        args = parser.parse_args()  
        return LoginAuth(conn,args) 
 

api.add_resource(Login, '/api/login')
api.add_resource(HelloWorld, '/api/verify')
api.add_resource(UPFILE, '/api/upload')
api.add_resource(STATUS, '/api/status')

api.add_resource(ApiAuth, '/api/gmsi/mobiletracker/login_api') 

api.add_resource(ApiLatestUpdates, '/api/get/latest_store_sku_category_ref/<string:userid>')
api.add_resource(ApiGetSKUs, '/api/get/sku')
api.add_resource(ApiAppVersion, '/api/get/latest/app-version')
api.add_resource(ApiGetAllStores, '/api/get/store_sku_50')
api.add_resource(ApiGetCategory, '/api/get/category_api')
api.add_resource(ApiGetStoreSKUs, '/api/get/store_api/<string:storeid>')
api.add_resource(ApiGetAssignUsersInStore, '/api/get/assigned_user_in_store_api/<string:storeid>')

api.add_resource(ApiUploadCategoryRefs, '/api/upload/template/category_reference')
api.add_resource(ApiUploadCategory, '/api/upload/template/category')
api.add_resource(ApiUploadSKUs, '/api/upload/template/skus')
api.add_resource(ApiUploadUsers, '/api/upload/template/users')
api.add_resource(ApiUploadArea, '/api/upload/template/area')
api.add_resource(ApiUploadChain, '/api/upload/template/chain')
api.add_resource(ApiUploadAgency, '/api/upload/template/agency')
api.add_resource(ApiUploadStores, '/api/upload/template/stores')
api.add_resource(ApiUploadUsersSchedules, '/api/upload/template/users_schedules') 

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True,host="0.0.0.0",port=port)