from flask_restful import Resource
from database import Database 

class ApiGetUserHeirarchyACSUP(Resource):
    def get(self,userid=None):
        conn = Database() 

        cursor = conn.execute("""
            select 
            userid as tbluserid,
            concat(firstname,' ',lastname) as mechandiser, 
            (select userrole from users_role where roleid = users.roleid) users_role 
            from users where userid in 
                ( 
                    select userid from users_schedules where storeid in (
                        select storeid  from users_schedules where userid = '{u}'
                    ) and userid != '{u}'
                ) and roleid ='6'
            """.format(u=userid),result=True)
             
        data  = [dict(((cursor.description[i][0]), value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print('ApiGetUserHeirarchyACSUP > data',data)
        
        # [{
        #     "tbluserid": "c100011",
        #     "mechandiser": "JANINE FERNANDO",
        #     "user_role": "Account Coordinator"
        # }]

        return data

class ApiGetUserHeirarchyAC(Resource):
    def get(self,userid=None):
        conn = Database() 

        cursor = conn.execute("""
            select 
            userid as tbluserid,
            concat(firstname,' ',lastname) as mechandiser, 
            (select userrole from users_role where roleid = users.roleid) users_role 
            from users where userid in 
                ( 
                    select userid from users_schedules where storeid in (
                        select storeid  from users_schedules where userid = '{u}'
                    ) and userid != '{u}'
                ) and roleid not in ('1','2','7','12','11');
            """.format(u=userid),result=True)
             
        data  = [dict(((cursor.description[i][0]), value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print('ApiGetUserHeirarchyAC > data',data)

        # [{
        #     "tbluserid": "m100911",
        #     "mechandiser": "JAYVEEABAD",
        #     "user_role": "TEAM LEADER"
        # }]

        return data