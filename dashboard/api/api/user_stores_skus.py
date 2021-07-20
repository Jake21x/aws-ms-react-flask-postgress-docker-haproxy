from flask_restful import Resource,reqparse
from database import Database  
from itertools import chain 

class ApiGetUserStoresSKU(Resource):
    def get(self,userid=None):
        conn = Database()  

        user_stores = conn.execute("""
        SELECT users_schedules.storeid, to_char(users_schedules.date_updated,'yyyy-mm-dd HH24:MI:SS') as date_updated FROM 
        users_schedules WHERE userid = '{u}'
        """.format(u=userid),result=True)
        xy = user_stores.fetchall()

        stores = []

        for item in xy:
            stores.append({str(item[0]): str(item[1])})

        
        # select skuid as tblskuid from skus where skuid not in (select skuid from stores_skus where storeid = '{}' and carry = 'No')

        for i in chain(range(len(xy))):
            skus = conn.execute("select skuid as tblskuid from skus where skuid not in (select skuid from stores_skus where storeid = '{}' and carry = 'No')".format(xy[i][0]),result=True)
            y = skus.fetchall()
            stores[i]['sku'] = [str(item[0]) for item in y]
                        
        return stores