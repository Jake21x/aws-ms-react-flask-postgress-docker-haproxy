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
            to_char(CASE WHEN (select date_updated from stores_skus where storeid = 'DPC4-04' ORDER BY date_updated  DESC LIMIT 1 ) is NULL THEN  (
                select date_updated from skus ORDER BY date_updated  DESC LIMIT 1
            ) END,'yyyy-mm-dd HH24:MI:SS') as latest_update  
            from stores where storeid = '{a}'
            """.format(a=storeid),result=True)
        
        storeinfo =  [dict(((store.description[i][0]), value) for i, value in enumerate(row)) for row in store.fetchall()]

        print('storeinfo',storeinfo)

        skus = conn.execute("select skuid from skus where skuid not in (select skuid from stores_skus where storeid = '{}' and carry = 'No')".format(storeid),result=True)
        
        skulist  = [dict(((skus.description[i][0]), value) for i, value in enumerate(row)) for row in skus.fetchall()]
        
        print('ApiGetAllStores > skulist',skulist)

        if len(storeinfo) != 0:
            storeinfo[0]['sku'] = skulist        
        
        return storeinfo