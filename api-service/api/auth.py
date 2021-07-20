from utils import DEV_PASSPORT,DEV_ROOTPASSPORT,excludeLogin
from flask_jwt_extended import create_access_token
import hashlib
import datetime
from flask_restful import Resource,reqparse
from database import Database  


class ApiAuth(Resource):
    def post(self):   

        conn = Database() 

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('device_id', type=str)
        parser.add_argument('appversion', type=str)
        parser.add_argument('device_info', type=str)
        parser.add_argument('IMEI', type=str) 
        args = parser.parse_args()  
        return LoginAuth(conn,args) 

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

    _user = str(args['username']).lower()
    _userPassword = args['password']

    _ux = str(args['username']).lower()
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
                    (select userrole from users_role where roleid = users.roleid),
                    agencyid,
                    (select name from agency where agencyid = users.agencyid) as agency_name
                    FROM users WHERE 
                    lower(username) =  \'{u}\' AND 
                    password = \'{p}\';""".format(u=_user, p=m)

    print('user_info',user_info)
    cursor = conn.execute(user_info,result=True)
    data  = [dict(((cursor.description[i][0]), value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    print('LoginAuth >  data ',data)
    x = len(list(data))

    status = ""
    expires = datetime.timedelta(days=7)
    defaultError = {'status': 'failed', 'message': 'Wrong credentials'}

    if(x == 1):  # first cursor 1 means user is exsiting
        active = data[0]['active'] 
        
        if active != 'Yes':
            return {'status': 'failed', 'message': 'Login is blocked! Your account is inactive, Please contact the administrator!'}
     
        access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m, fresh=True, expires_delta=expires)
        
        stores = []

        x1 = data[0]['roleid']

        if(x1 == 8): 
            stores = conn.execute("""
                select 
                stores.storeid as tblstoreid,
                name as store_name,
                geofence,
                longitude,
                latitude,
                null as address,
                to_char(stores.date_updated, 'yyyy-mm-dd HH24:MI:SS') AS date_updated
                from stores
                where agencyid='{a}' active = 'Yes' and priority = '1'
                """.format(a=data[0]['agencyid']),result=True)
        else:
            stores = conn.execute("""
                    select 
                    stores.storeid as tblstoreid,
                    name as store_name,
                    geofence,
                    longitude,
                    latitude,
                    null as address,
                    to_char(stores.date_updated, 'yyyy-mm-dd HH24:MI:SS') AS date_updated
                    from stores,users,users_schedules
                    where 
                    users_schedules.storeid = stores.storeid AND 
                    users_schedules.userid = users.userid AND 
                    users.username = '{u}' AND
                    stores.active = 'Yes' and stores.priority = '1'
                """.format(u=data[0]['username']),result=True)
        
        assigned_stores = [dict(((stores.description[i][0]), value) for i, value in enumerate(row)) for row in stores.fetchall()]
        print('assigned_stores',assigned_stores) 
        
        _sucess_r = [{
            "tblsingleroleid": data[0]['roleid'],
            "tbluserid": data[0]['userid'],
            "username": data[0]['username'],
            "firstname": data[0]['firstname'],
            "middle_initial": "na",
            "lastname": data[0]["lastname"],
            "employee_id": data[0]['employeeid'],
            "user_role": data[0]['userrole'], 
            "agencyid":data[0]['agencyid'],
            "agency_name":data[0]['agency_name'],
            "image_path":'.',
            "access_token":access_token,
            "status": "success",
            "message": "success",
            "assigned_stores":assigned_stores,
        }]

        return execute_device_lock(_sucess_r, conn, _ux, _px, _device_id, _device_info, _appversion, _imei)  
    
    else:
        return defaultError
    
    return defaultError


def execute_device_lock(_sucess_r, conn, _ux, _px, _device_id, _device_info, _appversion, _imei):
    lock_mgs = 'You are not authorize!,\nThis device is locked to other user please contact the administrator!'
    user_details = str(_sucess_r[0]['firstname']) + ' ' + str(_sucess_r[0]['lastname']) + ' ('+str(_sucess_r[0]['user_role'])+')'
    status = 'Logged-in Successfully'
    print('user_details', status)
    ExcludeUser = excludeLogin 
    try:

        isUserdev = DEV_PASSPORT in _ux
        isPwddev = DEV_PASSPORT in _px
        isRoot = DEV_ROOTPASSPORT in _ux
        print(isUserdev, isPwddev, 'Check Passport')

        if isRoot:
            print("Passport Passed!\nDev use passport for this user root!")
            # status = 'Dev. admin logged-in as '+user_details +' successfully '
            # login_log(status,_sucess_r[0]['tbluserid'],_device_id,_appversion,_device_info,_imei)
            return _sucess_r

        elif isUserdev and isPwddev:
            print("Passport Passed!\nDev use passport for this user gms!")
            # status = 'GMS admin logged-in as '+user_details +' successfully '
            # login_log(status,_sucess_r[0]['tbluserid'],_device_id,_appversion,_device_info,_imei)
            return _sucess_r

        elif (_sucess_r[0]['tbluserid'] in ExcludeUser):
            print("This user is excluded from device lock")
            # login_log(status,_sucess_r[0]['tbluserid'],_device_id,_appversion,_device_info,_imei)
            return _sucess_r
        
        elif _sucess_r is not None:

            device_auth = []
            user_auth = []
    
            user_devices = conn.execute("select * from devices where userid = '{}'".format(_sucess_r[0]['tbluserid']),result=True)
            user_auth = [dict(((user_devices.description[i][0]), value) for i, value in enumerate(row)) for row in user_devices.fetchall()]

            device_ids = conn.execute("select * from devices where device_id = '" + str(_device_id)+"' AND device_info = '"+str(_device_info)+"'", result=True)
            device_auth = [dict(((device_ids.description[i][0]), value) for i, value in enumerate(row)) for row in device_ids.fetchall()]

            print('devices', user_auth , device_auth)
    
            date_updated = str(datetime.datetime.now())
            if len(user_auth) != 0:
                version = str(user_auth[0]['appversion'])
                if version != str(_appversion):
                    up_query = """
                        UPDATE devices SET appversion='{a}',date_updated='{b}' 
                        WHERE userid='{c}' AND device_id='{d}' AND device_info ='{e}'
                    """.format(
                            a=_appversion,
                            b= date_updated,
                            c=str(_sucess_r[0]['tbluserid']),
                            d=_device_id,
                            e=_device_info
                        ) 

                    print('updating app version..' , up_query) 
                    conn.execute(up_query,commit=True)
            else:
                print('No user auth')
                # print(chknull(_device_id),chknull(_device_info))

            
            #admin no locking 
            if str(_sucess_r[0]['tblsingleroleid']) == '4':
                    print('This user is admin!')
                    login_log(conn,status, str(_sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    return _sucess_r

            # ac/acsup/manager
            elif str(_sucess_r[0]['tblsingleroleid']) in ['5', '6', '8']:
                # print('user_auth -----')
                # print(user_auth)
                if len(user_auth) == 0 and len(device_auth) == 0:
                    register_new_device(conn,status, user_auth, str(_sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    # print('_sucess_r')
                    return _sucess_r

                elif len(user_auth) != 0 and str(user_auth[0]['device_id']) == chknull(_device_id) and str(user_auth[0]['userid']) == str(_sucess_r[0]['tbluserid']) and str(user_auth[0]['device_info']) == chknull(_device_info):
                    # print('_sucess_r')
                    login_log(conn,status, str(_sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    return _sucess_r
                else:
                    # print({'status' : 'failed', 'message' :  lock_mgs })
                    status = 'Unauthorized Device'
                    login_log(conn,status, str(_sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    return {'status': 'failed', 'message':  lock_mgs}
    
    except Exception as e:
        status = 'Login Error, '+str(e)
        login_log(conn,status, str(_sucess_r[0]['tbluserid']),_device_id, _appversion, _device_info, _imei)
        return {'status': 'failed', 'message': 'failed' + str(e)}
            

def chknull(val):
    # print('chknull',val)
    try:
        if val == '':
            return str(None)
        elif val == 'null':
            return str(None)
        else:
            return str(val)
    except Exception as e:
        return str(None)


def register_new_device(conn,status, user_auth, tbluserid, device_id, version, device_info, imei):
    print('register_new_device', user_auth, tbluserid,device_id, version, device_info, imei)
    login_log(conn,status, tbluserid, device_id, version, device_info, imei)
    if len(user_auth) == 0:

        date_updated = str(datetime.datetime.now())
         
        conn.execute("INSERT INTO devices(userid, device_id ,status,date_updated,appversion,device_info,imei) VALUES ('" +
            str(tbluserid)+"','" +
            str(device_id)+"','" +
            str('active')+"','" +
            date_updated+"','" +
            str(version)+"','" +
            str(device_info)+"','" +
            str(imei)+"')",commit=True)
         
        print('Registered new Device!..')
    else:
        print('Device is not Registered!..')


def login_log(conn,status, tbluserid, device_id, version, device_info, imei):
    print('login_log', status, tbluserid,
          device_id, version, device_info, imei)

    date_updated = str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p"))
    print('login_log > date_updated', date_updated)

    conn.execute("INSERT INTO logs_logins(tbluserid, device_id ,message,date_updated,appversion,device_info,imei) VALUES ('" +
        str(tbluserid)+"','" +
        str(device_id)+"','" +
        str(status)+"','" +
        str(date_updated)+"','" +
        str(version)+"','" +
        str(device_info)+"','" +
        str(imei)+"')",commit=True)
