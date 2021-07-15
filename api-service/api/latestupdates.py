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
        print('ApiLatestUpdates > userid',userid)
        data[0]['store_sku_update'] = []
        data[0]['store_update'] = []
        data[0]['user_store_latest_update'] = "null"
        return data
        
        # return [
        #     {
        #         "cat_latest_update": "2021-01-20 15:28:15",
        #         "master_sku_latest_update": "2021-07-14 08:48:01",
        #         "master_store_latest_update": "2021-07-15 12:19:42",
        #         "ref_latest_update": "2021-06-01 18:32:16",
        #         "store_sku_latest_update": "2021-07-16 14:11:32",
        #         "store_sku_update": [
        #         {
        #             "testmercury2": "2021-07-14 14:36:51",
        #             "torgteststore01": "2021-07-14 14:36:51"
        #         }
        #         ],
        #         "store_update": [],
        #         "user_store_latest_update": "2021-04-12 12:48:04"
        #     }
        #     ]