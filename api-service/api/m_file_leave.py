from flask_restful import Resource,request
from utils import server_generated_id
from database import Database  
from itertools import chain 
import psycopg2 

class ApiPostFileLeave(Resource):
    def post(self):

        conn = Database() 
        json_dict = request.get_json(force=True, silent=True)
        try: 

            x = len(json_dict)
            data = []
            for i in chain(range(0, x)): 
                gid = json_dict[i]['mobile_generated_id'] 
                json_dict[i]['mobile_generated_id'] = server_generated_id() if gid in ('.','') else gid

                data.append((
                    json_dict[i]['tbluserid'],
                    json_dict[i]['tblstoreid'],
                    json_dict[i]['longitude'],
                    json_dict[i]['latitude'],
                    json_dict[i]['leave_category'],
                    json_dict[i]['date_of_leave_from'],
                    json_dict[i]['date_of_leave_to'],
                    json_dict[i]['reason'],
                    json_dict[i]['confirm_by'],
                    json_dict[i]['confirmation'],
                    json_dict[i]['mobile_generated_id'],
                    json_dict[i]['date_created'],
                    ))

            args_str = ','.join(['%s'] * len(data)) 
            query = conn.mogrify("""
                insert into m_file_leave (tbluserid, tblstoreid, longitude, latitude, leave_category, date_of_leave_from, date_of_leave_to, reason, confirm_by, confirmation, mobile_generated_id, date_created) values {}
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

class ApiGetLeavePerMerch(Resource):
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

                # tbl_stores.store_name, tbl_file_leave.tbluserid, tbl_file_leave.tblfileleaveid AS tblfileleaveid, tbl_file_leave.tblstoreid,tbl_users.employeeid AS employee_id, CONCAT(tbl_users.firstname, tbl_users.lastname) AS "employee_name", tbl_single_role.userrole AS employee_role, tbl_file_leave.leave_category, tbl_file_leave.date_of_leave_from, tbl_file_leave.date_of_leave_to, tbl_file_leave.reason, tbl_file_leave.confirmation, tbl_file_leave.confirm_by, tbl_file_leave.mobile_generated_id, date_created

                elif int(tblsingleroleid[0]['tblsingleroleid']) == 6:
                    data = []
                elif int(tblsingleroleid[0]['tblsingleroleid']) == 5:
                    item = conn.execute("""
                        select 
                        (select name from stores where storeid = m_file_leave.tblstoreid) as store_name,
                        tbluserid, 
                        id AS tblfileleaveid, 
                        tblstoreid,
                        tbluserid AS employee_id, 
                        (select CONCAT(trim(firstname),' ',trim(lastname)) from users where userid = m_file_leave.tbluserid ) AS employee_name, 
                        (select userrole from users,users_role where users.roleid = users_role.roleid AND userid = m_file_leave.tbluserid ) AS employee_role, 
                        leave_category, 
                        to_char(date_of_leave_from,'yyyy-mm-dd') as date_of_leave_from, 
                        to_char(date_of_leave_to,'yyyy-mm-dd') as date_of_leave_to, 
                        reason, 
                        confirmation, 
                        confirm_by, 
                        mobile_generated_id, 
                        to_char(date_created,'yyyy-mm-dd HH24:MI:SS') as date_created  
                        from m_file_leave where tbluserid in (
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

            return data

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