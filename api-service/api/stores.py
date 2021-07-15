from flask_restful import Resource
from database import Database  

class ApiGetAllStores(Resource):
    def get(self):
        conn = Database() 

        cursor = conn.execute("select storeid as tblstoreid,storecode,stores.name as store_name , chains.name as chain  from stores,chains where stores.chainid = chains.chainid",result=True)
        print('ApiGetAllStores > cursor',cursor)
        data  = [dict(((cursor.description[i][0]), value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print('ApiGetAllStores > data',data)
        return data


class ApiGetStoreSKUs(Resource):
    def get(self,storeid=None):
        conn = Database() 

        store = conn.execute("""
            select 
            storeid as tblstoreid,
            name as store_name, 
            to_char(CASE WHEN (select date_updated from stores_skus where storeid = '{a}' ORDER BY date_updated  DESC LIMIT 1 ) is NULL THEN  (
                select date_updated from skus ORDER BY date_updated  DESC LIMIT 1
            ) END,'yyyy-mm-dd HH24:MI:SS') as latest_update  
            from stores where storeid = '{a}'
            """.format(a=storeid),result=True)
        
        storeinfo =  [dict(((store.description[i][0]), value) for i, value in enumerate(row)) for row in store.fetchall()]

        print('storeinfo',storeinfo)

        skus = conn.execute("select skuid as tblskuid from skus where skuid not in (select skuid from stores_skus where storeid = '{}' and carry = 'No')".format(storeid),result=True)
        
        skulist  = [dict(((skus.description[i][0]), value) for i, value in enumerate(row)) for row in skus.fetchall()]
        
        print('ApiGetAllStores > skulist',skulist)

        if len(storeinfo) != 0:
            storeinfo[0]['sku'] = skulist        
        
        return storeinfo

class ApiGetAssignUsersInStore(Resource):
    def get(self,storeid=None):
        conn = Database() 

        
        query = "with ids as (select userid from users_schedules where storeid = '{}'), users as (select users.userid,users.roleid,concat(firstname,' ',lastname) as name,users.agencyid from ids,users,users_role where ids.userid = users.userid and users_role.roleid =users.roleid )select * from users".format(storeid)
        print('query',query)
        users = conn.execute(query,result=True)
        data = users.fetchall()
        print('ApiGetAssignUsersInStore > data ',data)
        ac = list(filter(lambda m: m[1] == 6, data))
        print('ac', ac)
        ac_usercode = '' if len(ac) == 0 else ac[0][0]
        ac_name = '' if len(ac) == 0 else ac[0][2]
        tl = list(filter(lambda m: m[1] == 1, data))
        print('tl', tl)
        tl_usercode = '' if len(tl) == 0 else tl[0][0]
        tl_name = '' if len(tl) == 0 else tl[0][2]
        agency = '' if len(ac) == 0 else ac[0][3]

        
        return [
            {
                'ac_usercode': ac_usercode,
                'ac_name': ac_name,
                'tl_usercode': tl_usercode,
                'tl_name': tl_name,
                'agency': agency,

            }
        ]