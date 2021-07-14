from flask import Flask
from flask_restful import Resource, Api ,request
from flask import request
from flask_httpauth import HTTPBasicAuth 
import jwt,json,os,datetime,time,random,base64 
from functools import wraps
from itertools import chain 
from database import Database
from utils import server_generated_id
import xlrd

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT_UPLOAD = os.path.dirname(os.path.abspath('api-service'))
UPLOAD_FOLDER = 'uploads' 

app = Flask(__name__)
api = Api(app)
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

class UploadUsers(Resource):
    def post(self):
        data = conn.execute('select version()') 
        print('result',data) 
        return {"result ":data}

class UploadUsersSchedules(Resource):
    def post(self):   
        data = conn.execute('select version()') 
        print('result',data) 
        return {"result ":data}

class UploadArea(Resource):
    def post(self): 
        data = conn.execute('select version()') 
        print('result',data) 
        return {"result ":data}

class UploadChain(Resource):
    def post(self):   
        template = request.files['file']
        
        if template.filename != '':
            filename = server_generated_id('chain_',2)+'.'+ template.filename.split(".")[-1]
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            template.save(file_path)

            book = xlrd.open_workbook(file_path)
            sheet = book.sheet_by_index(0)

            col1 = []
            for r in range(1, sheet.nrows):
               col1.append(str(sheet.cell(r, 0).value).replace('.0', ''))
 
            print('template', template.filename)
            print('template', col1)
             
        print('template',template)
        # data = conn.execute('select version()') 
        # print('result',data) 
        return {"result ": 'OK'}


api.add_resource(Login, '/login')
api.add_resource(HelloWorld, '/verify')
api.add_resource(UPFILE, '/upload')
api.add_resource(STATUS, '/status')
api.add_resource(UploadUsers, '/api/upload/template/users')
api.add_resource(UploadArea, '/api/upload/template/area')
api.add_resource(UploadChain, '/api/upload/template/chain')
api.add_resource(UploadUsersSchedules, '/api/upload/template/usersschedules')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host="0.0.0.0",port=port)