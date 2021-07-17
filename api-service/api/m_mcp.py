import os,base64
import psycopg2
import xlrd
from utils import server_generated_id,UPLOAD_FOLDER_TEMPLATES 
import datetime
from flask_restful import Resource,request
from database import Database  
from itertools import chain  
from datetime import datetime
from calendar import monthrange
from flask import jsonify

class ApiPostMCP(Resource):
    def post(self):

        conn = Database() 
        
        try: 

            json_dict = request.get_json(force=True, silent=True)
            sheets = []

            if str(len(json_dict[0])) is not None or str(len(json_dict[0])) != '0':
                try:
                    excel_file = []
                    x = len(json_dict)
                    print(x, json_dict)

                    xfile = 'MCP'+server_generated_id(json_dict[0]['tbluserid'])
                    print(os.path.join(UPLOAD_FOLDER_TEMPLATES, xfile + ".xlsx"))
                    with open(os.path.join(UPLOAD_FOLDER_TEMPLATES, xfile + ".xlsx"), "wb") as fh:
                        excel_file.append(str(UPLOAD_FOLDER_TEMPLATES + xfile + ".xlsx"), )
                        fh.write(base64.b64decode(json_dict[0]['excel_base64']))

                    book = xlrd.open_workbook(os.path.join(UPLOAD_FOLDER_TEMPLATES, xfile + ".xlsx"))

                    print('book',book)

                    for sheet in book.sheets():
                            sheets.append(sheet.name)
                            print(sheets)
                    sheet = book.sheet_by_name(sheets[0])
                    rows_row = []
                    print('----- rows and cols')
                    print(sheet.ncols)
                    print(sheet.nrows)
                    print('----- ')

                    m_schedules = []
                    m_usercode = []
                    m_storecode = []
                    m_tcp_usercode = []

                    schedule_start = ""

                    buildError = ""

                    prep_schedules = []
                    dupls_schedules = []
                    generated_ids = []

                    if sheet.ncols == 8:
                        for j in range(1+2, sheet.nrows):
                            schedule = str(sheet.cell(j, 0).value)
                            print('schedule',schedule)
                            if '-' in schedule:
                                m_schedules.append(schedule)
                                pass
                            else:
                                return {'status': 'failed', 'message': 'SCHEDULE cell or column format should be text and YYYY-MM-DD format'}

                            username = str(sheet.cell(j, 4).value)
                            usercode = str(sheet.cell(j, 5).value)
                            m_usercode.append(usercode)

                            storename = str(sheet.cell(j, 2).value)
                            excel_storecode = str(sheet.cell(j, 3).value)
                            storecode = ""
                            try:
                                storecode = str(int(float(excel_storecode)))
                                m_storecode.append(storecode)
                            except ValueError:
                                storecode = excel_storecode
                                m_storecode.append(storecode)

                            tcp_usercode = str(sheet.cell(j, 7).value)
                            m_tcp_usercode.append(tcp_usercode)

                            _type = str(sheet.cell(j, 1).value)

                            Result = True
                            yy, mm, dd = schedule.split('-')
                            try:
                                datetime(int(yy), int(mm), int(dd))
                            except ValueError:
                                Result = False

                            if(Result):
                                pass
                            else:
                                return {'status': 'failed', 'message': 'Schedule date is not valid please change or remove ['+schedule+'] \n'}

                            dupls_schedules.append(
                                '['+schedule+' | '+_type+' | '+storecode+' | '+usercode+' | '+tcp_usercode+']')

                            g_date = schedule.replace('-', '')

                            if _type.lower() == 'tcp':
                                prep_schedules.append((schedule, _type.upper().strip(), storecode, str(
                                    json_dict[0]['tbluserid']), tcp_usercode))
                                g_uuid = str(
                                    json_dict[0]['tbluserid']+g_date+_type+storecode+tcp_usercode).upper()
                                generated_ids.append(g_uuid)
                            elif _type.lower() == 'trade check' or _type.lower() == 'office':
                                prep_schedules.append((schedule, _type.upper().strip(
                                ), storecode, str(json_dict[0]['tbluserid']), None))
                                g_uuid = str(
                                    json_dict[0]['tbluserid']+g_date+_type+storecode).upper()
                                generated_ids.append(g_uuid)
                            else:
                                return {'status': 'failed', 'message': _type+' is not valid TYPE Column, Please use only proper value in TYPE column [ OFFICE , TRADE CHECK , TCP ]\n'}

                        print('Process Start ----------')
                        print('generated ids', generated_ids)
                        print('merge schedules', m_schedules)
                        print('merge usercode ', m_usercode)
                        print('merge storecode ', m_storecode)

                        m_tcp_usercode = list(
                        filter(lambda i: i != "", m_tcp_usercode))
                        print('merge tcp_usercode ', m_tcp_usercode)
                        print('find min schedule', min(m_schedules))
                        schedule_start = datetime.strptime(
                            str(min(m_schedules)), '%Y-%m-%d').date()
                        schedule_end = last_day_of_month(schedule_start)
                        print('get the last date from min schedule', schedule_end)

                        qusercodes = 'select userid from users where roleid in (\'5\',\'6\',\'8\')'
                        print('check query  > qusercodes:', qusercodes)

                        upload_cur = conn.execute(qusercodes,result=True) 
                        db_usercodes = [row[0] for row in upload_cur.fetchall()]
                        print('check query  > data ', db_usercodes)

                        invalid_usercode = list(set(m_usercode) - set(db_usercodes))
                        print('invalid_usercode', invalid_usercode)

                        qstorecodes = 'with m_code as ( select unnest(array['+','.join(str(
                        "'"+x+"'") for x in m_storecode) + ']) as id) select DISTINCT(id) from m_code where m_code.id not in (select storeid from stores where storeid in ('+','.join(str("'"+x+"'") for x in m_storecode) + '))'
                        
                        print('check query  > qstorecodes:', qstorecodes)
                        qstorecodes_rest = conn.execute(qstorecodes,result=True) 
                        invalid_storecode = [row[0] for row in qstorecodes_rest.fetchall()]
                        print('invalid_storecode', invalid_storecode)

                        invalid_tcp_usercode = list(set(m_tcp_usercode) - set(db_usercodes))
                        print('invalid_tcp_usercode', invalid_tcp_usercode)

                        print('')
                        print('Process: build error ----------')

                        buildError = "You need to edit or remove the schedule on following column\nReason: STORE or USER CODE not found or not valid\n"

                        if len(invalid_usercode) != 0:
                            buildError = buildError + "USER CODE ("+str(len(invalid_usercode)) +") : " + ','.join(invalid_usercode) + '\n'

                        if len(invalid_storecode) != 0:
                            buildError = buildError + "OFFICE/STORE CODE ("+str(len(invalid_storecode)) +"): " + ','.join(invalid_storecode) + '\n'

                        if len(invalid_tcp_usercode) != 0:
                            buildError = buildError + "TCP MERCHANDISER CODE ("+str(len(invalid_tcp_usercode))+") : " + ','.join(invalid_tcp_usercode)+'\n'

                        if len(invalid_usercode) != 0 or len(invalid_storecode) != 0 or len(invalid_tcp_usercode) != 0:
                            print('\n', buildError)
                            return {'status': 'failed', 'message': buildError}

                        
                        print('')
                        print('Process: find duplis ----------')
                        print('prep_schedules', dupls_schedules)
                        duplicates = list(set([x for x in dupls_schedules if dupls_schedules.count(x) > 1]))
                        buildError = "\nYou need to edit or remove duplicated schedules\n"
                        if len(duplicates) != 0:
                            # buildError = buildError +"Duplicated Schedules ("+str(len(duplicates))+") : \n [SCHEDULE|TYPE|OFC./STORE CODE|USER CODE|TCP MERCH. USER CODE]\n*" + '\n*'.join(duplicates)+'\n'
                            buildError = buildError + "Duplicated Schedules ("+str(len(duplicates))+") : \n*" + '\n*'.join(duplicates)+'\n'
                            print('\n', buildError)
                            return {'status': 'failed', 'message': buildError}

                        
                        # ADD FEEDBACK CHECKING...

                        print('')
                        print('Process: feedbacks ----------')
                        query_feedbacks = 'select * from m_tcp where mobile_generated_id in (select mobile_generated_id from m_mcp where to_char(schedule,\'YYYY-MM-DD\') >= \''+str(
                            schedule_start)+'\' and to_char(schedule,\'YYYY-MM-DD\')  <= \''+str(schedule_end)+'\'  and tbluserid = \''+str(json_dict[0]['tbluserid'])+'\')'
                        print('check query  > query_feedbacks:', query_feedbacks)
                        qfeedback = conn.execute(query_feedbacks,result=True)
                        db_feedbacks = [row for row in qfeedback.fetchall()]
                        print('db_feedbacks :', db_feedbacks)

                        print('')
                        print(
                            'Process: detecting db_schedule_movement conflict ----------')
                        qpendings = 'select to_char(schedule,\'YYYY-MM-DD\'),schedule_type,tc_tcp_store_id,tbluserid,tcp_user_id from confirm_mcp where mobile_generated_id in (select mobile_generated_id from m_mcp where to_char(schedule,\'YYYY-MM-DD\') >= \''+str(
                            schedule_start)+'\' and to_char(schedule,\'YYYY-MM-DD\')  <= \''+str(schedule_end)+'\'  and tbluserid = \''+str(json_dict[0]['tbluserid'])+'\')'
                        print('check query  > qpendings:', qpendings)
                        qpendings_rest = conn.execute(qpendings,result=True)
                        db_schedule_movement = [row for row in qpendings_rest.fetchall()]
                        print('db_schedule_movement :', db_schedule_movement)
                        print('prep_schedules :', prep_schedules)

                        buildError = "You need to edit or remove the following schedules\nReason: Schedule already has change request\n"

                        if len(db_schedule_movement) != 0 or len(db_feedbacks) != 0:
                            conflicts = list(set(db_schedule_movement) & set(prep_schedules))
                            # if len(conflicts) != 0:
                            #     print('schedule has conflict on pending request',conflicts)
                            #     buildError = buildError + "Schedule ("+str(len(conflicts))+"): \n*" + "\n*".join([str(x[0]+' | '+x[1]+' | '+x[2]+' | '+x[3]+' | '+xstr(x[4]) ) for x in conflicts])
                            #     return {'status' : 'failed', 'message' : buildError}
                            print(
                                'schedule has conflict on pending request', conflicts)
                            buildError = "Cannot reupload schedule, Your MCP has requests or feedbacks already, Editing is now within the app only"
                            return {'status': 'failed', 'message': buildError}

                        print('')
                        print('Process: clean schedule----------')
                        existing_schedules = 'delete from m_mcp where to_char(schedule,\'YYYY-MM-DD\') >= \''+str(schedule_start)+'\' and to_char(schedule,\'YYYY-MM-DD\')  <= \''+str(schedule_end)+'\' and tbluserid = \''+str(json_dict[0]['tbluserid'])+'\''
                        print('check query  > existing_schedules:',
                            existing_schedules)
                        conn.execute(existing_schedules,commit=True)

                        toInsert = []
                        for col in prep_schedules:
                            date = col[0].replace('-', '')
                            uuid = str(
                                json_dict[0]['tbluserid']+date+col[1]+col[2]+xstr(col[4])).upper()
                            print('uuid', uuid)
                            toInsert.append((col[0], col[1], col[2], col[3], col[4], uuid, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"), ), )

                        print('toInsert', toInsert)
                        args_str = ','.join(['%s'] * len(toInsert))
                        main_query = """
                            INSERT INTO m_mcp(
                                schedule,schedule_type,
                                tc_tcp_store_id,tbluserid,
                                tcp_user_id,mobile_generated_id,
                                date_created, date_updated) VALUES {} 
                                RETURNING 
                                    (select concat(firstname,\' \',lastname) from users where userid=tcp_user_id limit 1) as tcp_merchandiser,
                                    (SELECT userrole FROM users_role,users WHERE users_role.roleid = users.roleid AND users.userid = tcp_user_id limit 1) as position,
                                    tcp_user_id as tcp_merchandiser_code,
                                    schedule_type,
                                    office as mcp_office,
                                    null as reason,
                                    (SELECT name FROM stores WHERE stores.storeid = tc_tcp_store_id limit 1) as tc_tcp_store_name,
                                    tc_tcp_store_id as tc_tcp_store_code,
                                    schedule as mcp_schedule,
                                    mobile_generated_id
                            """.format(args_str)

                        print('main_query', main_query) 
                        rest = conn.mogrify(main_query,toInsert,commit=True,result=True) 
                        data = [dict(((rest.description[i][0]), value) for i, value in enumerate(row)) for row in rest.fetchall()]

                        return jsonify(data)
                    else:
                        return {'status': 'failed', 'message': 'Missing header in template,\nPlease follow complete header\n[SCHEDULE | TYPE | OFFICE/STORE NAME | OFFICE/STORE CODE | USER NAME | USER CODE | TCP MERCHANDISER NAME | TCP MERCHANDISER CODE]'}
            
                except Exception as e:
                        print('app create/edit', json_dict)
                        print(str(e))  
                         
                        for item in json_dict: 
                            if len(item) == 1:
                                tbl_mcp2 = []
                                tbl_mcp2.append((
                                    item[0]['tbluserid'],
                                    item[0]['tcp_user_id'],
                                    item[0]['schedule'],
                                    item[0]['schedule_type'],
                                    item[0]['tc_tcp_store_id'],
                                    item[0]['adjustment_status'],
                                    item[0]['mobile_generated_id'],
                                    item[0]['confirmed_by'],
                                    item[0]['office'],
                                    item[0]['date_confirmed'],
                                    item[0]['date_created'],
                                    item[0]['date_updated'], 
                                ))

                                str_args = ','.join(['%s'] * len(tbl_mcp2))
                                # print(cur.mogrify('INSERT INTO tbl_mcp(tbluserid,tcp_user_id, schedule, schedule_type, tc_tcp_store_id, adjustment_status, mobile_generated_id, confirmed_by,office, date_confirmed, date_created, date_updated) VALUES {}'.format(str_args), tbl_mcp2).decode('utf8'))
                                conn.mogrify('INSERT INTO m_mcp(tbluserid,tcp_user_id, schedule, schedule_type, tc_tcp_store_id, adjustment_status, mobile_generated_id, confirmed_by,office, date_confirmed, date_created, date_updated) VALUES {}'.format(str_args), tbl_mcp2,commit=True)

                            else:
                                adjusted_entry = []

                                adjustment_entry_insert = []
                                adjustment_entry_insert.append((
                                    item[1]['tbluserid'],
                                    item[1]['tc_tcp_store_id'],
                                    item[1]['tcp_user_id'],
                                    item[1]['mobile_generated_id'],
                                    item[1]['schedule'],
                                    item[1]['schedule_type'],
                                    item[0]['adjustment_status'],
                                    item[1]['office'],
                                    item[1]['confirmed_by'],
                                    item[1]['reason'],
                                    item[1]['date_created'],
                                    item[1]['date_updated'],
                                ))

                                useReason = ""
                                try:
                                    useReason = item[0]['reason']
                                    print('useReason>new')
                                except Exception as e:
                                    useReason = item[1]['reason']
                                    print('useReason>old')

                                adjusted_entry.append((
                                    item[0]['tbluserid'],
                                    item[0]['tc_tcp_store_id'],
                                    item[0]['tcp_user_id'],
                                    item[0]['mobile_generated_id'],
                                    item[0]['schedule'],
                                    item[0]['schedule_type'],
                                    item[0]['adjustment_status'],
                                    item[0]['office'],
                                    item[0]['confirmed_by'],
                                    useReason,
                                    item[0]['date_created'],
                                    item[0]['date_updated'],
                                ))

                        return {'status': 'success', 'message': 'success'}

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
         


def last_day_of_month(date_value):
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])

def xstr(s):
    if s is None:
        return ''
    return str(s)

class ApiPostTCP(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                 
                data.append((
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['tbluserid'],
                    json_dict[i]['tcp_date'],
                    json_dict[i]['score'],
                    json_dict[i]['feedback'],
                    json_dict[i]['mcp_id'],
                    json_dict[i]['mcp_user_id'],
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['_type'],
                    json_dict[i]['date_created'],
                    json_dict[i]['date_updated'],
                    ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_tcp (tblstoreid, tbluserid, tcp_date, score, feedback, tblmcpid, mcp_user_id, mobile_generated_id, _type, date_created, date_updated) values {};
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


class ApiPostMCPChangeRequest(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        print('json_dict',json_dict)
        try:  
            tbluserid = str(json_dict[0]['tbluserid'])
            tc_tcp_store_id = str(json_dict[0]['tc_tcp_store_id'])
            tcp_user_id = str(json_dict[0]['tcp_user_id'])
            schedule_type = str(json_dict[0]['schedule_type'])
            schedule = str(json_dict[0]['schedule'])
            reason = str(json_dict[0]['reason'])
            date_created = str(json_dict[0]['date_created'])
            mobile_generated_id = str(json_dict[0]['mobile_generated_id'])

            conf_data = []

            # always get the last request base on mobile_generated_id
            q_conf = str('SELECT * from confirm_mcp where mobile_generated_id = \'' +mobile_generated_id + '\' AND adjustment_status = \'pending\' order by date_created desc limit 1')
            print('mcp>new>request', q_conf)
            res =conn.execute(q_conf,result=True) 
            conf_data = [dict(((res.description[i][0]), value) for i, value in enumerate(row)) for row in res.fetchall()]
            print('mcp>new>request', conf_data)

            if len(conf_data) == 0: 
                # sales agent (reseller)
                # area sales manager / account manager (coords)
                # regional sales manager
                # national sales manager

                useTcpUserId = 'NULL'
                if tcp_user_id != 'None':
                    useTcpUserId = "'{}'".format(tcp_user_id)

                print('mcp>new>request', mobile_generated_id, reason) 

                item = [(tbluserid,tc_tcp_store_id,useTcpUserId,mobile_generated_id,schedule,schedule_type,'pending',reason,date_created,date_created)]
                args_str = ','.join(['%s'] * len(item)) 
                conn.mogrify('INSERT INTO confirm_mcp(tbluserid,tc_tcp_store_id,tcp_user_id,mobile_generated_id,schedule,schedule_type,adjustment_status,reason, date_created,date_updated) VALUES {} '.format(args_str),item,commit=True)

            else:
                useTcpUserId = 'NULL'
                if tcp_user_id != 'None':
                    useTcpUserId = "'{}'".format(tcp_user_id)

                print('mcp>update>quest', mobile_generated_id,
                    conf_data[0]['id'], reason, tcp_user_id, useTcpUserId) 
                conn.execute("UPDATE confirm_mcp  SET tcp_user_id = "+useTcpUserId+", schedule = '{a}',schedule_type = '{b}',tc_tcp_store_id = '{c}',reason = '{d}',date_created='{e}',date_updated='{f}',date_sync ='{g}' WHERE mobile_generated_id = '{h}' AND id ='{i}'".format(a=schedule, b=schedule_type, c=tc_tcp_store_id, d=reason, e=date_created, f=date_created, g=date_created, h=mobile_generated_id, i=conf_data[0]['id']),commit=True)
                
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
class ApiGetMCPPending(Resource):
    def get(self,userid=None):

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


class ApiGetMCPNotPending(Resource):
    def get(self,userid=None):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try:  
             
            data = []
            user = conn.execute('SELECT roleid as tblsingleroleid,agencyid FROM users WHERE userid = \'{}\''.format(userid) ,result=True )

            tblsingleroleid = [dict(((user.description[i][0]), value) for i, value in enumerate(row)) for row in user.fetchall() if row]

            if len(tblsingleroleid) !=0:
                if int(tblsingleroleid[0]['tblsingleroleid']) == 8:
                    print('request for 8 manager')
                    data =  [] 
                elif int(tblsingleroleid[0]['tblsingleroleid']) == 6:
                    data = []
                elif int(tblsingleroleid[0]['tblsingleroleid']) == 5:
                    item = conn.execute("""
                        select  
                        tbluserid, 
                        mobile_generated_id, 
                        adjustment_status, 
                        confirmed_by, 
                        reason , 
                        (select CONCAT(trim(firstname),' ',trim(lastname)) from users where userid = confirm_mcp.tbluserid ) AS mpc_user,
                        schedule ,
                        schedule_type,
                        office,
                        tc_tcp_store_id,
                        (select name from stores where storeid = confirm_mcp.tblstoreid) AS tc_tcp_store_name,
                        tcp_user_id,
                        (select userrole from users,users_role where users.roleid = users_role.roleid AND userid = confirm_mcp.tbluserid ) AS userrole,
                         (select CONCAT(trim(firstname),' ',trim(lastname)) from users where userid = confirm_mcp.tcp_user_id ) AS tcp_user, 
                        date_created, 
                        date_updated   
                        from confirm_mcp where tbluserid in (
                        select userid as tbluserid from users where userid in (
                        select  userid  from users where userid in 
                        ( 
                            select userid from users_schedules where storeid in (
                                select storeid  from users_schedules where userid = '{u}'
                            ) and userid != '{u}'
                        )
                        ) and roleid = '6'
                        ) and date_sync::date >= now()::date - INTERVAL '3 DAY' 
                        """.format(u=userid),result=True)
                    data =  [dict(((item.description[i][0]), value) for i, value in enumerate(row)) for row in item.fetchall() if row]

            return jsonify(data)

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
