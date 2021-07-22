from flask_restful import Resource
from database import Database 

class ApiLatestUpdates(Resource):
    def get(self,userid=None):
        conn = Database() 
 
        cursor = conn.execute("""
            SELECT 
            (SELECT to_char(skus.date_updated,'yyyy-mm-dd HH24:MI:SS') FROM skus 
            ORDER BY date_updated DESC LIMIT 1) AS master_sku_latest_update, 
            (SELECT to_char(stores_skus.date_updated,'yyyy-mm-dd HH24:MI:SS') FROM stores_skus 
            ORDER BY stores_skus.date_updated DESC LIMIT 1) AS store_sku_latest_update, 
            (SELECT to_char(category.date_updated,'yyyy-mm-dd HH24:MI:SS') FROM category 
            ORDER BY category.date_updated DESC LIMIT 1) AS cat_latest_update, 
            (SELECT to_char(category_refs.date_updated,'yyyy-mm-dd HH24:MI:SS') FROM category_refs 
            ORDER BY category_refs.date_updated DESC LIMIT 1) AS ref_latest_update, 
            (SELECT to_char(users_schedules.date_updated,'yyyy-mm-dd HH24:MI:SS') FROM users_schedules 
            ORDER BY users_schedules.date_updated ASC LIMIT 1) AS user_store_latest_update, 
            (SELECT to_char(stores.date_updated,'yyyy-mm-dd HH24:MI:SS') FROM stores 
            ORDER BY stores.date_updated  DESC LIMIT 1) AS master_store_latest_update
            """,result=True)

        # print('ApiGetSKUs > cursor',cursor)
        data  = [dict(((cursor.description[i][0]), value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        # print('ApiLatestUpdates > userid',userid)
        
        result_store_sku = conn.execute("""
            SELECT 
            stores_skus.storeid AS store_sku_update,
            to_char(stores_skus.date_updated,'yyyy-mm-dd HH24:MI:SS') AS latest_updated_date 
            FROM stores_skus,users,users_schedules
            where 
            users_schedules.storeid = stores_skus.storeid AND 
            users_schedules.userid = users.userid AND   
            users.userid = '{u}'  
            GROUP BY stores_skus.date_updated, stores_skus.storeid
            ORDER BY stores_skus.date_updated ASC
            """.format(u=userid),result=True)

        ar_result_store_sku = result_store_sku.fetchall()
        store_sku_update = [] if len(ar_result_store_sku) == 0 else [dict(result_store_sku.fetchall())]
        data[0]['store_sku_update'] = store_sku_update

        result_update = conn.execute("""
            SELECT 
            stores.name, 
            longitude,
            latitude,
            geofence,
            address, 
            stores.storeid,'NA' as day_off,
            stores.storeid,'NA' AS schedule_day,
            'NA'AS schedule_type 
            FROM stores 
            INNER JOIN users_schedules ON users_schedules.storeid = stores.storeid 
            WHERE users_schedules.userid = '{u}' 
            """.format(u=userid),result=True)
        
        store_update = [dict(((result_update.description[i][0]), value) for i, value in enumerate(row)) for row in result_update.fetchall()]
        data[0]['store_update'] = store_update
        
        return data 