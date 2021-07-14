from utils import DEV_PASSPORT,DEV_ROOTPASSPORT
from flask_jwt_extended import create_access_token
import hashlib
import datetime

def LoginAuth(conn,args): 
  
    _device_id = args['device_id']

    _imei = ""
    try:
        _imei = args['IMEI']
    except Exception as e:
        print('no _imei')

    _commit = ""
    try:
        _commit = args['commit']
    except Exception as e:
        print('no _commit')

    _device_info = args['device_info']
    _appversion = args['appversion']

    _user = args['username']
    _userPassword = args['password']

    _ux = args['username']
    _px = args['password']

    isUserdev = DEV_PASSPORT in _user
    isPwddev = DEV_PASSPORT in _userPassword

    isRoot = DEV_ROOTPASSPORT in _user

    if (isUserdev):
        _user = _user.replace(DEV_PASSPORT, "")

    if (isRoot):
        _user = _user.replace(DEV_ROOTPASSPORT, "")

    if (isPwddev):
        _userPassword = _userPassword.replace(DEV_PASSPORT, "")
    
    m = hashlib.md5(_userPassword.encode()).hexdigest()
    print('LoginAuth',_user, _userPassword, _device_id, _appversion, _device_info, _imei, _commit)
   
    user_info = """SELECT 
                    active,
                    username,
                    firstname,
                    middle_initial,
                    lastname,
                    employeeid,
                    roleid,userid,
                    (select userrole from users_role where roleid = users.roleid) 
                    FROM users WHERE 
                    username =  \'{u}\' AND 
                    password = \'{p}\';""".format(u=_user, p=m)

    print('user_info',user_info)
    data = conn.execute(user_info,result=True)
    print('LoginAuth >  data ',data)
    x = len(list(data))

    status = ""
    expires = datetime.timedelta(days=7)

    if(x == 1):  # first cursor 1 means user is exsiting
        active = data[0][0] 


        
        if active != 'Yes':
            return {'status': 'failed', 'message': 'Login is blocked! Your account is inactive, Please contact the administrator!'}
        else:
            
            access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m, fresh=True, expires_delta=expires)

            return {
            "tblsingleroleid": data[0][6],
            "tbluserid": data[0][7],
            "username": data[0][1],
            "firstname": data[0][2],
            "middle_initial": "na",
            "lastname": data[0][4],
            "employee_id": data[0][5],
            "user_role": data[0][8], 
            "image_path":'.',
            "access_token":access_token,
            "status": "success",
            "message": "success",
            "assigned_stores":[],
    }
    
    else:
        return {'status': 'failed', 'message': 'Wrong credentials'}
    
    return {'status': 'failed','message': m}