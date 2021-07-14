from flask import jsonify
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
import hashlib
import json
import psycopg2
import datetime
from itertools import chain
import base64
from werkzeug.utils import secure_filename
import os
import io
import datetime
import time
from random import randint
import xlrd
from app.web import web
from itertools import groupby

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT_UPLOAD = os.path.dirname(os.path.abspath('app'))
UPLOAD_FOLDER = 'app/static/uploads'
UPLOAD_FOLDER_SIGNATURE = 'app/static/uploads/signatures'
UPLOAD_FOLDER_API = 'app/static/uploads/api_uploads'
DEV_ROOTPASSPORT = 'root.admin-'
DEV_PASSPORT = 'dev.admin-'


class AuthenticateUser(Resource):
    def post(self):
        # try:
        pixar = []
        random_id = []
        device_locker = []
        shid = []
        d = []
        d1 = []
        d2 = []
        d3 = []
        type_and_time = []
        position = None
        groupname = None
        x1 = None
        conn = None
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('device_id', type=str)
        parser.add_argument('appversion', type=str)
        parser.add_argument('device_info', type=str)
        parser.add_argument('IMEI', type=str)
        parser.add_argument('commit', type=str)

        # try:
        # except Exception as e:
        #     print('login args add as empty')

        args = parser.parse_args()

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
        print(_user, _userPassword, _device_id,
              _appversion, _device_info, _imei, _commit)

        m = hashlib.md5(_userPassword.encode())
        conn = psycopg2.connect(database='mobiletracker', user='torgadmin1023',
                                host='gmsi-rds-db.cua1z6h2gwyu.us-west-2.rds.amazonaws.com', password='Torgadmin03102020')
        cursor = conn.cursor()
        cursor.execute('SELECT username,active FROM tbl_users WHERE username =  \'{username}\' AND password = \'{password}\';'.format(
            username=_user, password=m.hexdigest()))

        # AND active = \'Yes\'

        _sucess_r = None

        data = [dict(((cursor.description[i][0]), value)
                     for i, value in enumerate(row)) for row in cursor.fetchall()]

        x = len(list(data))
        print('data ---')
        # print(data, x)

        if(x == 1):  # first cursor 1 means user is exsiting

            active = data[0]['active']
            # print('active', active)
            if active != 'Yes':
                return {'status': 'failed', 'message': 'Login is blocked your account is inactive, Please contact the administrator!'}

            conn = psycopg2.connect(database='mobiletracker', user='torgadmin1023',
                                    host='gmsi-rds-db.cua1z6h2gwyu.us-west-2.rds.amazonaws.com', password='Torgadmin03102020')
            cursor = conn.cursor()
            cursor.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, tbl_stores.groupname as tblgroupingsid, tbl_stores.tblstoreid, tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid INNER JOIN tbl_stores ON tbl_stores.tblstoreid = tbl_assigned_stores.tblstoreid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_stores.tblstoreid not like \'%GMS%\' AND tbl_stores.tblstoreid not like \'%C100%\' AND active = \'Yes\' '.format(
                username=_user, password=m.hexdigest()))
            data = [dict(((cursor.description[i][0]), value)
                         for i, value in enumerate(row)) for row in cursor.fetchall()]
            data2 = []
            print('data', data)
            if(len(data) > 0):
                # getting the exact role id of user: TL = 1, merchandiser = 2, ACSUP = 5, AC = 6 subtl = 7, manager = 8
                x1 = data[0]['tblsingleroleid']

                groupnameid = data[0]['tblgroupingsid']
                # getting schedule, working time, day_off and schedule_day for users from merchandiser
                if((x1 >= 2 and x1 < 7) or (x1 == 8)):
                    cursor2 = conn.cursor()
                    cursor2.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, tbl_stores.groupname,tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid INNER JOIN tbl_stores ON tbl_stores.tblstoreid = tbl_assigned_stores.tblstoreid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\''.format(
                        username=_user, password=m.hexdigest()))

                    data2 = [dict(((cursor2.description[i][0]), value)
                                  for i, value in enumerate(row)) for row in cursor2.fetchall()]
                    xtras = data2[0]['image_path']

                    expires = datetime.timedelta(days=7)

                    access_token = create_access_token(
                        identity=_user + str(datetime.datetime.now())+m.hexdigest(), fresh=True, expires_delta=expires)
                    refresh_token = create_refresh_token(identity=_user)
                    data2[0]['access_token'] = access_token
                    data2[0]['status'] = 'success'
                    data2[0]['message'] = 'success'
                    data2[0]['image_path'] = request.host_url+xtras
                    cur = conn.cursor()
                    # cur.execute('SELECT tbl_stores.tblstoreid1, tbl_stores.store_name,tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,tbl_stores.address FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' ORDER BY tbl_stores.tblstoreid1 ASC;', (_user, m.hexdigest(), ))
                    cur.execute('SELECT tbl_stores.store_name,tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,null as address,to_char(tbl_stores.app_update,\'yyyy-mm-dd HH24:MI:SS\') AS date_updated FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\' ORDER BY tbl_stores.store_name ASC;'.format(
                        username=_user, password=m.hexdigest()))

                    d = [dict(((cur.description[i][0]), value)
                              for i, value in enumerate(row)) for row in cur.fetchall()]

                    for c in chain(range(0, len(d))):
                        # cur2 = conn.cursor()
                        # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s;', (_user, m.hexdigest(), d[c]['tblstoreid'] ))

                        # d3 = [dict(((cur2.description[i][0]), value)
                        #         for i, value in enumerate(row)) for row in cur2.fetchall()]

                        cur3 = conn.cursor()
                        cur3.execute('SELECT tbl_scheduling_per_store.schedule_type, tbl_scheduling_per_store.working_time, tbl_scheduling_per_store.day_off FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE tbl_users.username =  \'{username}\' AND password = \'{password}\' AND tblstoreid = \'{tblstoreid}\' AND tbl_users.active = \'Yes\' GROUP BY schedule_type, working_time, day_off;'.format(
                            username=_user, password=m.hexdigest(), tblstoreid=d[c]['tblstoreid']))
                        if(cur3.rowcount == 0):
                            pass
                        else:
                            type_and_time = [dict(((cur3.description[i][0]), value)
                                                  for i, value in enumerate(row)) for row in cur3.fetchall()]

                            d[c]['schedule_type'] = type_and_time[0]['schedule_type']
                            d[c]['working_time'] = type_and_time[0]['working_time']
                            d[c]['day_off'] = type_and_time[0]['day_off']
                            d[c]['schedule_day'] = None

                        data2[0]['assigned_stores'] = d

                        return execute_device_lock([data2[0]], conn, _ux, _px, _device_id, _device_info, _appversion, _imei)
                        # _sucess_r = [data2[0]]

                elif(x1 == 1):  # exclusive for tl only

                    cursor3 = conn.cursor()
                    cursor3.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, CONCAT(\'GROUP \',tbl_stores.groupname) as groupname, tbl_stores.tblstoreid, tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid INNER JOIN tbl_stores ON tbl_stores.tblstoreid = tbl_assigned_stores.tblstoreid WHERE tbl_stores.groupname = \'{groupname}\''.format(
                        groupname=groupnameid)+'  AND tbl_stores.tblstoreid not like \'%GMS%\' AND tbl_stores.tblstoreid not like \'%C100%\' AND tbl_single_role.tblsingleroleid != \'6\' AND tbl_single_role.tblsingleroleid != \'5\'AND tbl_single_role.tblsingleroleid != \'8\' AND tbl_users.active = \'Yes\'  order by (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end)')
                    if(cursor3.rowcount == 0):
                        pass
                    else:
                        data3 = [dict(((cursor3.description[i][0]), value)
                                      for i, value in enumerate(row)) for row in cursor3.fetchall()]

                        curs = conn.cursor()
                        curs.execute('SELECT tbl_users.username FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid INNER JOIN tbl_stores ON tbl_stores.tblstoreid = tbl_assigned_stores.tblstoreid WHERE tbl_stores.groupname =  \'{groupname}\''.format(
                            groupname=groupnameid)+'  AND tbl_stores.tblstoreid not like \'%GMS%\' AND tbl_stores.tblstoreid not like \'%C100%\' AND tbl_single_role.tblsingleroleid != \'6\' AND tbl_single_role.tblsingleroleid != \'5\'AND tbl_single_role.tblsingleroleid != \'8\' AND tbl_users.active = \'Yes\' order by (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end)'.format(groupname=groupnameid))
                        if(curs.rowcount == 0):
                            pass
                        else:
                            d2 = [dict(((curs.description[i][0]), value)
                                       for i, value in enumerate(row)) for row in curs.fetchall()]

                            for cc2 in chain(range(0, len(d2))):

                                cur = conn.cursor()
                                # cur.execute('SELECT tbl_stores.tblstoreid1, tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude, latitude, tbl_stores.address FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE tbl_users.username = %s ORDER BY (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end),tbl_stores.tblstoreid1 ASC', (d2[cc2]['username'], ))
                                cur.execute('SELECT tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude, latitude, null as address,to_char(tbl_stores.app_update,\'yyyy-mm-dd HH24:MI:SS\') AS date_updated FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE tbl_users.username = %s AND tbl_users.active = \'Yes\' ORDER BY (case tbl_users.username when ' +
                                            "'{}'".format(_user)+' then 0 end),tbl_stores.store_name ASC', (d2[cc2]['username'], ))

                                d = [dict(((cur.description[i][0]), value)
                                          for i, value in enumerate(row)) for row in cur.fetchall()]

                                for c in chain(range(0, len(d))):
                                    # cur2 = conn.cursor()
                                    # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s order by (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end)', (_user, m.hexdigest(), d[c]['tblstoreid']))

                                    # d3 = [dict(((cur2.description[i][0]), value)
                                    #     for i, value in enumerate(row)) for row in cur2.fetchall()]

                                    cur3 = conn.cursor()
                                    cur3.execute('SELECT tbl_scheduling_per_store.schedule_type, tbl_scheduling_per_store.working_time, tbl_scheduling_per_store.day_off FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE tbl_users.username =  \'{username}\' AND password = \'{password}\' AND tblstoreid = \'{tblstoreid}\' AND tbl_users.active = \'Yes\' GROUP BY schedule_type, working_time, day_off '.format(
                                        username=_user, password=m.hexdigest(), tblstoreid=d[c]['tblstoreid']))
                                    if(cur3.rowcount == 0):
                                        pass
                                    else:
                                        type_and_time = [dict(((cur3.description[i][0]), value)
                                                              for i, value in enumerate(row)) for row in cur3.fetchall()]

                                        d[c]['schedule_type'] = type_and_time[0]['schedule_type']
                                        d[c]['working_time'] = type_and_time[0]['working_time']
                                        d[c]['day_off'] = type_and_time[0]['day_off']
                                        d[c]['schedule_day'] = None

                                    data3[0]['assigned_stores'] = d

                                    length2_ = len(data3)
                                    for c in chain(range(0, length2_)):
                                        xtra = data3[c]['image_path']
                                        data3[c]['image_path'] = request.host_url+xtra

                                    expires = datetime.timedelta(days=7)

                                    # access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m.hexdigest()+str(shid[0][2]), fresh= True, expires_delta=expires)
                                    access_token = create_access_token(
                                        identity=_user + str(datetime.datetime.now())+m.hexdigest(), fresh=True, expires_delta=expires)
                                    refresh_token = create_refresh_token(
                                        identity=_user)
                                    data3[0]['access_token'] = access_token
                                    # data3[0]['device_info'] = str(shid[0][0])
                                    # data3[0]['device_id'] = str(_device_id)
                                    data3[0]['status'] = 'success'
                                    data3[0]['message'] = 'success'

                                    return execute_device_lock(data3, conn, _ux, _px, _device_id, _device_info, _appversion, _imei)
                                    # _sucess_r = data3

                elif(x1 == 7):  # exclusive for sub-tl only

                    cursor3 = conn.cursor()
                    cursor3.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, CONCAT(\'GROUP \',tbl_stores.groupname) as groupname, tbl_stores.tblstoreid, tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid INNER JOIN tbl_stores ON tbl_stores.tblstoreid = tbl_assigned_stores.tblstoreid WHERE tbl_stores.groupname =  \'{groupname}\''.format(
                        groupname=groupnameid)+'  AND tbl_stores.tblstoreid not like \'%GMS%\' AND tbl_stores.tblstoreid not like \'%C100%\' AND tbl_single_role.tblsingleroleid != \'6\' AND tbl_single_role.tblsingleroleid != \'5\'AND tbl_single_role.tblsingleroleid != \'8\' AND tbl_users.active = \'Yes\'  order by (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end)')
                    if(cursor3.rowcount == 0):
                        pass
                    else:
                        data3 = [dict(((cursor3.description[i][0]), value)
                                      for i, value in enumerate(row)) for row in cursor3.fetchall()]

                        curs = conn.cursor()
                        curs.execute('SELECT tbl_users.username FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid INNER JOIN tbl_stores ON tbl_stores.tblstoreid = tbl_assigned_stores.tblstoreid WHERE tbl_stores.groupname =  \'{groupname}\''.format(
                            groupname=groupnameid)+'  AND tbl_stores.tblstoreid not like \'%GMS%\' AND tbl_stores.tblstoreid not like \'%C100%\' AND tbl_single_role.tblsingleroleid != \'6\' AND tbl_single_role.tblsingleroleid != \'5\'AND tbl_single_role.tblsingleroleid != \'8\' AND tbl_users.active = \'Yes\' order by (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end)'.format(groupname=groupnameid))
                        if(curs.rowcount == 0):
                            pass
                        else:
                            d2 = [dict(((curs.description[i][0]), value)
                                       for i, value in enumerate(row)) for row in curs.fetchall()]

                            for cc2 in chain(range(0, len(d2))):

                                cur = conn.cursor()
                                # cur.execute('SELECT tbl_stores.tblstoreid1, tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude, latitude, tbl_stores.address FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE tbl_users.username = %s ORDER BY (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end),tbl_stores.tblstoreid1 ASC', (d2[cc2]['username'], ))
                                cur.execute('SELECT tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude, latitude, null as address,to_char(tbl_stores.app_update,\'yyyy-mm-dd HH24:MI:SS\') AS date_updated FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE tbl_users.username = %s AND tbl_users.active = \'Yes\' ORDER BY (case tbl_users.username when ' +
                                            "'{}'".format(_user)+' then 0 end),tbl_stores.store_name ASC', (d2[cc2]['username'], ))

                                d = [dict(((cur.description[i][0]), value)
                                          for i, value in enumerate(row)) for row in cur.fetchall()]

                                for c in chain(range(0, len(d))):
                                    # cur2 = conn.cursor()
                                    # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s order by (case tbl_users.username when '+"'{}'".format(_user)+' then 0 end)', (_user, m.hexdigest(), d[c]['tblstoreid']))

                                    # d3 = [dict(((cur2.description[i][0]), value)
                                    #     for i, value in enumerate(row)) for row in cur2.fetchall()]

                                    cur3 = conn.cursor()
                                    cur3.execute('SELECT tbl_scheduling_per_store.schedule_type, tbl_scheduling_per_store.working_time, tbl_scheduling_per_store.day_off FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE tbl_users.username =  \'{username}\' AND password = \'{password}\' AND tblstoreid = \'{tblstoreid}\' AND tbl_users.active = \'Yes\' GROUP BY schedule_type, working_time, day_off '.format(
                                        username=_user, password=m.hexdigest(), tblstoreid=d[c]['tblstoreid']))
                                    if(cur3.rowcount == 0):
                                        pass
                                    else:
                                        type_and_time = [dict(((cur3.description[i][0]), value)
                                                              for i, value in enumerate(row)) for row in cur3.fetchall()]

                                        d[c]['schedule_type'] = type_and_time[0]['schedule_type']
                                        d[c]['working_time'] = type_and_time[0]['working_time']
                                        d[c]['day_off'] = type_and_time[0]['day_off']
                                        d[c]['schedule_day'] = None

                                    data3[0]['assigned_stores'] = d

                                    length2_ = len(data3)
                                    for c in chain(range(0, length2_)):
                                        xtra = data3[c]['image_path']
                                        data3[c]['image_path'] = request.host_url+xtra

                                    expires = datetime.timedelta(days=7)

                                    # access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m.hexdigest()+str(shid[0][2]), fresh= True, expires_delta=expires)
                                    access_token = create_access_token(
                                        identity=_user + str(datetime.datetime.now())+m.hexdigest(), fresh=True, expires_delta=expires)
                                    refresh_token = create_refresh_token(
                                        identity=_user)
                                    data3[0]['access_token'] = access_token
                                    # data3[0]['device_info'] = str(shid[0][0])
                                    # data3[0]['device_id'] = str(_device_id)
                                    data3[0]['status'] = 'success'
                                    data3[0]['message'] = 'success'

                                    return execute_device_lock(data3, conn, _ux, _px, _device_id, _device_info, _appversion, _imei)
                                    # _sucess_r = data3
                elif(x1 == 8):
                    cur1 = conn.cursor()
                    cur1.execute('SELECT tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,null as address,to_char(tbl_stores.app_update,\'yyyy-mm-dd HH24:MI:SS\') AS date_updated FROM tbl_stores'.format(username=_user, password=m.hexdigest()))

                    stores = [dict(((cur1.description[i][0]), value)
                                   for i, value in enumerate(row)) for row in cur1.fetchall()]
                    print('stores:' + str(stores))
                    cur = conn.cursor()
                    cur.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\';'.format(
                        username=_user, password=m.hexdigest()))
                    manager = [dict(((cur.description[i][0]), value)
                                    for i, value in enumerate(row)) for row in cur.fetchall()]
                    print('manager:' + str(manager))
                    xtras = manager[0]['image_path']
                    manager[0]['image_path'] = request.host_url+xtras
                    manager[0]['schedule_type'] = 'NA'
                    manager[0]['working_time'] = 'NA'
                    manager[0]['day_off'] = 'NA'
                    manager[0]['schedule_day'] = 'NA'
                    expires = datetime.timedelta(days=7)

                    # access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m.hexdigest()+str(shid[0][2]), fresh= True, expires_delta=expires)
                    access_token = create_access_token(
                        identity=_user + str(datetime.datetime.now())+m.hexdigest(), fresh=True, expires_delta=expires)
                    refresh_token = create_refresh_token(identity=_user)

                    manager[0]['assigned_stores'] = stores
                    manager[0]['access_token'] = access_token
                    manager[0]['status'] = 'success'
                    manager[0]['message'] = 'success'

                    return execute_device_lock(manager, conn, _ux, _px, _device_id, _device_info, _appversion, _imei)
                    # _sucess_r = acacsup

                else:  # bulk for ac and acsup
                    cur = conn.cursor()
                    cur.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\';'.format(
                        username=_user, password=m.hexdigest()))

                    acacsup = [dict(((cur.description[i][0]), value)
                                    for i, value in enumerate(row)) for row in cur.fetchall()]
                    xtras = acacsup[0]['image_path']

                    acacsup[0]['image_path'] = request.host_url+xtras

                    cur2 = conn.cursor()
                    # cur2.execute('SELECT tbl_stores.tblstoreid1, tbl_stores.store_name,  tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,tbl_stores.address FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' ORDER BY tbl_stores.tblstoreid1', (_user, m.hexdigest(), ))
                    cur2.execute('SELECT tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,null as address,to_char(tbl_stores.app_update,\'yyyy-mm-dd HH24:MI:SS\') AS date_updated FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\' ORDER BY tbl_stores.store_name ASC'.format(
                        username=_user, password=m.hexdigest()))

                    acassignstores = [dict(((cur2.description[i][0]), value)
                                           for i, value in enumerate(row)) for row in cur2.fetchall()]

                    for c in chain(range(0, len(acassignstores))):

                        # cur2 = conn.cursor()
                        # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s;', (_user, m.hexdigest(), acassignstores[c]['tblstoreid']))
                        # d3 = [dict(((cur2.description[i][0]), value)
                        #             for i, value in enumerate(row)) for row in cur2.fetchall()]
                        # cur2 = conn.cursor()
                        # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s;', (_user, m.hexdigest(), acassignstores[c]['tblstoreid'] ))
                        # d3 = [dict(((cur2.description[i][0]), value)
                        #     for i, value in enumerate(row)) for row in cur2.fetchall()]
                        # print(d3)

                        cur3 = conn.cursor()
                        cur3.execute('SELECT tbl_scheduling_per_store.schedule_type, tbl_scheduling_per_store.working_time, tbl_scheduling_per_store.day_off FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE tbl_users.username =  \'{username}\' AND password = \'{password}\' AND tblstoreid = \'{tblstoreid}\' AND tbl_users.active = \'Yes\' GROUP BY schedule_type, working_time, day_off;'.format(
                            username=_user, password=m.hexdigest(), tblstoreid=acassignstores[c]['tblstoreid']))
                        if(cur3.rowcount == 0):
                            pass
                        else:
                            type_and_time = [dict(((cur3.description[i][0]), value)
                                                  for i, value in enumerate(row)) for row in cur3.fetchall()]
                            print(type_and_time)
                            acassignstores[c]['schedule_type'] = type_and_time[0]['schedule_type']
                            acassignstores[c]['working_time'] = type_and_time[0]['working_time']
                            acassignstores[c]['day_off'] = type_and_time[0]['day_off']

                        acassignstores[c]['schedule_day'] = None
                    expires = datetime.timedelta(days=7)

                    # access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m.hexdigest()+str(shid[0][2]), fresh= True, expires_delta=expires)
                    access_token = create_access_token(
                        identity=_user + str(datetime.datetime.now())+m.hexdigest(), fresh=True, expires_delta=expires)
                    refresh_token = create_refresh_token(identity=_user)

                    acacsup[0]['assigned_stores'] = acassignstores
                    acacsup[0]['access_token'] = access_token
                    # data3[0]['device_info'] = str(shid[0][0])
                    # data3[0]['device_id'] = str(_device_id)
                    acacsup[0]['status'] = 'success'
                    acacsup[0]['message'] = 'success'

                    return execute_device_lock(acacsup, conn, _ux, _px, _device_id, _device_info, _appversion, _imei)

            else:  # bulk for ac and acsup
                cur = conn.cursor()
                cur.execute('SELECT tbl_single_role.tblsingleroleid, tbl_users.tbluserid, tbl_users.username, tbl_users.firstname, tbl_users.middle_initial, tbl_users.lastname, tbl_users.employeeid AS employee_id, tbl_single_role.userrole AS user_role, tbl_users.image_path FROM tbl_users INNER JOIN tbl_single_role ON tbl_users.tblsingleroleid = tbl_single_role.tblsingleroleid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\';'.format(
                    username=_user, password=m.hexdigest()))

                acacsup = [dict(((cur.description[i][0]), value)
                                for i, value in enumerate(row)) for row in cur.fetchall()]
                xtras = acacsup[0]['image_path']

                acacsup[0]['image_path'] = request.host_url+xtras

                cur2 = conn.cursor()
                # cur2.execute('SELECT tbl_stores.tblstoreid1, tbl_stores.store_name,  tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,tbl_stores.address FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' ORDER BY tbl_stores.tblstoreid1', (_user, m.hexdigest(), ))
                cur2.execute('SELECT tbl_stores.store_name, tbl_stores.tblstoreid AS tblstoreid, tbl_stores.geofence,longitude,latitude,null as address,to_char(tbl_stores.app_update,\'yyyy-mm-dd HH24:MI:SS\') AS date_updated FROM tbl_stores INNER JOIN tbl_assigned_stores ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid INNER JOIN tbl_users ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_users.active = \'Yes\' ORDER BY tbl_stores.store_name ASC'.format(
                    username=_user, password=m.hexdigest()))

                acassignstores = [dict(((cur2.description[i][0]), value)
                                       for i, value in enumerate(row)) for row in cur2.fetchall()]

                for c in chain(range(0, len(acassignstores))):

                    # cur2 = conn.cursor()
                    # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s;', (_user, m.hexdigest(), acassignstores[c]['tblstoreid']))
                    # d3 = [dict(((cur2.description[i][0]), value)
                    #             for i, value in enumerate(row)) for row in cur2.fetchall()]
                    # cur2 = conn.cursor()
                    # cur2.execute('SELECT tbl_scheduling_per_store.schedule_day FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE username =  \'{username}\' AND password = \'{password}\' AND tbl_scheduling_per_store.tblstoreid = %s;', (_user, m.hexdigest(), acassignstores[c]['tblstoreid'] ))
                    # d3 = [dict(((cur2.description[i][0]), value)
                    #     for i, value in enumerate(row)) for row in cur2.fetchall()]
                    # print(d3)

                    cur3 = conn.cursor()
                    cur3.execute('SELECT tbl_scheduling_per_store.schedule_type, tbl_scheduling_per_store.working_time, tbl_scheduling_per_store.day_off FROM tbl_scheduling_per_store INNER JOIN tbl_users ON tbl_users.tbluserid = tbl_scheduling_per_store.tbluserid WHERE tbl_users.username =  \'{username}\' AND password = \'{password}\' AND tblstoreid = \'{tblstoreid}\' AND tbl_users.active = \'Yes\' GROUP BY schedule_type, working_time, day_off;'.format(
                        username=_user, password=m.hexdigest(), tblstoreid=acassignstores[c]['tblstoreid']))
                    if(cur3.rowcount == 0):
                        pass
                    else:
                        type_and_time = [dict(((cur3.description[i][0]), value)
                                              for i, value in enumerate(row)) for row in cur3.fetchall()]
                        print(type_and_time)
                        acassignstores[c]['schedule_type'] = type_and_time[0]['schedule_type']
                        acassignstores[c]['working_time'] = type_and_time[0]['working_time']
                        acassignstores[c]['day_off'] = type_and_time[0]['day_off']

                    acassignstores[c]['schedule_day'] = None
                expires = datetime.timedelta(days=7)

                # access_token = create_access_token(identity=_user + str(datetime.datetime.now())+m.hexdigest()+str(shid[0][2]), fresh= True, expires_delta=expires)
                access_token = create_access_token(
                    identity=_user + str(datetime.datetime.now())+m.hexdigest(), fresh=True, expires_delta=expires)
                refresh_token = create_refresh_token(identity=_user)

                acacsup[0]['assigned_stores'] = acassignstores
                acacsup[0]['access_token'] = access_token
                # data3[0]['device_info'] = str(shid[0][0])
                # data3[0]['device_id'] = str(_device_id)
                acacsup[0]['status'] = 'success'
                acacsup[0]['message'] = 'success'

                return execute_device_lock(acacsup, conn, _ux, _px, _device_id, _device_info, _appversion, _imei)
                # _sucess_r = acacsup

        return {'status': 'failed', 'message': 'Wrong credentials'}
        # except Exception as e:
        #     x = str(e)
        #     x.replace('\n', '')
        #     return {'status' : 'failed', 'message' : 'failed ' + str(e)  }
        # finally:
        #     if conn is not None:
        #         conn.close()


def execute_device_lock(_sucess_r, conn, _ux, _px, _device_id, _device_info, _appversion, _imei):
    try:

        user_details = _sucess_r[0]['firstname'] + ' ' + \
            _sucess_r[0]['lastname'] + ' ('+_sucess_r[0]['user_role']+')'
        status = 'Logged-in Successfully'
        print('user_details', status)

        ExcludeUser = web.excludeLogin()
        # ExcludeUser = ()

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

            #print('continue login...')

            # print('\n_sucess_r------')
            # print(_sucess_r)
            # print('\ntblsingleroleid------')
            # print(_sucess_r[0]['tblsingleroleid'])

            # check and prepare user_auth
            # check on tbl_device_lock if user exist & get data
            device_auth = []
            user_auth = []
            exe2_device = conn.cursor()

            # print('\nquery ----')
            query = "select * from tbl_devices where tbluserid = '" + \
                str(_sucess_r[0]['tbluserid'])+"'"

            # print(query)
            exe2_device.execute(query)
            user_auth = [dict(((exe2_device.description[i][0]), value)
                              for i, value in enumerate(row)) for row in exe2_device.fetchall()]
            exe2_device.close()

            # print('\nuser_auth ----')
            # print(user_auth)

            exe3_device = conn.cursor()

            # print('\ndevice query ----')
            device_query = "select * from tbl_devices where device_id = '" + \
                str(_device_id)+"' AND device_info = '"+str(_device_info)+"'"

            # print(device_query)
            exe3_device.execute(device_query)
            device_auth = [dict(((exe3_device.description[i][0]), value)
                                for i, value in enumerate(row)) for row in exe3_device.fetchall()]
            exe3_device.close()

            # print('\ndevice_auth ----')
            # print(device_auth)

            # print('\nlogin check ----')
            date_updated = str(datetime.datetime.now())
            if len(user_auth) != 0:
                # print(str(user_auth[0]['device_id']) , chknull(_device_id) , str(user_auth[0]['tbluserid']),str(_sucess_r[0]['tbluserid']) , str(user_auth[0]['device_info']) , chknull(_device_info))
                version = str(user_auth[0]['appversion'])
                if version != str(_appversion):
                    print('updating app version..')
                    _up = conn.cursor()
                    _up.execute('UPDATE tbl_devices SET appversion = %s ,date_updated = %s WHERE tbluserid = %s AND device_id = %s AND device_info = %s', (
                        _appversion, date_updated, _sucess_r[0]['tbluserid'], _device_id, _device_info))
                    conn.commit()
                    _up.close()
            else:
                print('No user auth')
                # print(chknull(_device_id),chknull(_device_info))

            # print('\n')
            # check user_infos position
            #diser or sub-tls

            lock_mgs = 'You are not authorize!,\nThis device is locked to other user please contact the administrator!'

            if str(_sucess_r[0]['tblsingleroleid']) in ['2', '7']:

                # find TL
                # get the TLs usercode
                tls_code = None
                for j in chain(range(0, len(_sucess_r))):
                    # print('tls_code ----')
                    tls_code = _sucess_r[j]['tbluserid']
                    # print(tls_code)
                    if str(_sucess_r[j]['tblsingleroleid']) == '1':
                        break

                # print('user tls_code ----')
                # print(tls_code)

                tls_device_auth = []

                exe_device = conn.cursor()
                query = "select * from tbl_devices where tbluserid = '" + \
                    str(tls_code)+"'"
                # print('query ----')
                # print(query)
                exe_device.execute(query)
                tls_device_auth = [dict(((exe_device.description[i][0]), value)
                                        for i, value in enumerate(row)) for row in exe_device.fetchall()]
                exe_device.close()

                # print('tls_device_auth ----')
                # print(tls_device_auth)

                if len(tls_device_auth) != 0 and str(tls_device_auth[0]['device_id']) == chknull(_device_id) and str(tls_device_auth[0]['device_info']) == chknull(_device_info):
                    # print('user check TLs auth and device')
                    register_new_device(status, user_auth, str(
                        _sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    # print('_sucess_r')
                    return _sucess_r

                elif len(user_auth) == 0 and len(device_auth) == 0:
                    # print('user new auth and device')
                    register_new_device(status, user_auth, str(
                        _sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    # print('_sucess_r')
                    return _sucess_r

                elif len(user_auth) != 0:

                    # print('user check existing auth and device')
                    find_user_device = None
                    for i in chain(range(0, len(user_auth))):

                        # print(str(user_auth[i]['device_id']),str(_device_id),str(user_auth[i]['tbluserid']),str(_sucess_r[0]['tbluserid']),str(user_auth[i]['device_info']),str(_device_info))
                        if str(user_auth[i]['device_id']) == chknull(_device_id) and str(user_auth[i]['tbluserid']) == str(_sucess_r[0]['tbluserid']) and str(user_auth[i]['device_info']) == chknull(_device_info):
                            find_user_device = "FOUND!"
                            break

                    # print('find_user_device ----')
                    # print(find_user_device)
                    if find_user_device is not None:
                        # print('_sucess_r')
                        login_log(
                            status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                        return _sucess_r
                    else:

                        if len(tls_device_auth) != 0 and len(user_auth) < 2:
                            register_new_device(status, [], str(
                                _sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                            # print('_sucess_r')
                            return _sucess_r
                        else:
                            # print({'status' : 'failed', 'message' : lock_mgs })
                            status = 'Unauthorized Device'
                            login_log(
                                status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                            return {'status': 'failed', 'message': lock_mgs}

                else:
                    # print({'status' : 'failed', 'message' : lock_mgs })
                    status = 'Unauthorized Device'
                    login_log(
                        status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                    return {'status': 'failed', 'message': lock_mgs}

            # managers or #admin
            elif str(_sucess_r[0]['tblsingleroleid']) == '4':
                print('This user is admin!')
                login_log(status, _sucess_r[0]['tbluserid'],
                          _device_id, _appversion, _device_info, _imei)
                return _sucess_r

            # ac/acsup
            elif str(_sucess_r[0]['tblsingleroleid']) in ['5', '6', '8']:
                # print('user_auth -----')
                # print(user_auth)
                if len(user_auth) == 0 and len(device_auth) == 0:
                    register_new_device(status, user_auth, str(
                        _sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                    # print('_sucess_r')
                    return _sucess_r

                elif len(user_auth) != 0 and str(user_auth[0]['device_id']) == chknull(_device_id) and str(user_auth[0]['tbluserid']) == str(_sucess_r[0]['tbluserid']) and str(user_auth[0]['device_info']) == chknull(_device_info):
                    # print('_sucess_r')
                    login_log(
                        status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                    return _sucess_r
                else:
                    # print({'status' : 'failed', 'message' :  lock_mgs })
                    status = 'Unauthorized Device'
                    login_log(
                        status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                    return {'status': 'failed', 'message':  lock_mgs}
            # TLs
            else:

                # //check if user is not yet authorized
                if len(user_auth) == 0:
                    # //insert to tbl_device_lock
                    if len(device_auth) == 0:
                        register_new_device(status, user_auth, str(
                            _sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                        # print('_sucess_r')
                        return _sucess_r
                    else:
                        existing_device_user = [x['tbluserid']
                                                for x in device_auth]
                        # print('\nexisting_device_user -----')
                        # print(existing_device_user)
                        find_first_user_device = None
                        for i in chain(range(0, len(_sucess_r))):
                            if _sucess_r[i]['tbluserid'] in existing_device_user:
                                find_first_user_device = "FOUND!"
                                break

                        if find_first_user_device is not None:
                            register_new_device(status, user_auth, str(
                                _sucess_r[0]['tbluserid']), _device_id, _appversion, _device_info, _imei)
                            # print('_sucess_r')
                            return _sucess_r
                        else:
                            # print({'status' : 'failed', 'message' : lock_mgs })
                            status = 'Unauthorized Device'
                            login_log(
                                status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                            return {'status': 'failed', 'message':  lock_mgs}

                # //check if device_id is matches on login bulk
                elif len(user_auth) != 0 and str(user_auth[0]['device_id']) == chknull(_device_id) and str(user_auth[0]['tbluserid']) == str(_sucess_r[0]['tbluserid']) and str(user_auth[0]['device_info']) == chknull(_device_info):
                    # print('_sucess_r')
                    login_log(
                        status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                    return _sucess_r

                else:
                    # print({'status' : 'failed', 'message' : lock_mgs })
                    status = 'Unauthorized Device'
                    login_log(
                        status, _sucess_r[0]['tbluserid'], _device_id, _appversion, _device_info, _imei)
                    return {'status': 'failed', 'message': lock_mgs}
            # return _sucess_r
        else:
            status = 'Wrong Crendential'
            login_log(status, _sucess_r[0]['tbluserid'],
                      _device_id, _appversion, _device_info, _imei)
            return {'status': 'failed', 'message': 'Wrong credentials'}
    except Exception as e:
        status = 'Login Error, '+str(e)
        login_log(status, _sucess_r[0]['tbluserid'],
                  _device_id, _appversion, _device_info, _imei)
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


def register_new_device(status, user_auth, tbluserid, device_id, version, device_info, imei):
    print('register_new_device', user_auth, tbluserid,
          device_id, version, device_info, imei)
    login_log(status, tbluserid, device_id, version, device_info, imei)
    if len(user_auth) == 0:

        date_updated = str(datetime.datetime.now())
        conn = psycopg2.connect(database='mobiletracker', user='torgadmin1023',
                                host='gmsi-rds-db.cua1z6h2gwyu.us-west-2.rds.amazonaws.com', password='Torgadmin03102020')
        exe = conn.cursor()
        exe.execute(exe.mogrify(
            "INSERT INTO tbl_devices(tbluserid, device_id ,status,date_updated,appversion,device_info,imei) VALUES ('" +
            str(tbluserid)+"','" +
            str(device_id)+"','" +
            str('active')+"','" +
            date_updated+"','" +
            str(version)+"','" +
            str(device_info)+"','" +
            str(imei)+"')"))
        conn.commit()
        exe.close()
        print('Registered new Device!..')
    else:
        print('Device is not Registered!..')


def login_log(status, tbluserid, device_id, version, device_info, imei):
    print('login_log', status, tbluserid,
          device_id, version, device_info, imei)

    date_updated = str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p"))
    print('login_log > date_updated', date_updated)

    conn = psycopg2.connect(database='mobiletracker', user='torgadmin1023',
                            host='gmsi-rds-db.cua1z6h2gwyu.us-west-2.rds.amazonaws.com', password='Torgadmin03102020')
    exe = conn.cursor()
    exe.execute(exe.mogrify(
        "INSERT INTO tbl_login_logs(tbluserid, device_id ,message,date_updated,appversion,device_info,imei) VALUES ('" +
        str(tbluserid)+"','" +
        str(device_id)+"','" +
        str(status)+"','" +
        str(date_updated)+"','" +
        str(version)+"','" +
        str(device_info)+"','" +
        str(imei)+"')"))
    conn.commit()
