from flask_restful import Resource
from database import Database 

class ApiGetSKUs(Resource):
    def get(self):
        conn = Database() 

        cursor = conn.execute("select skuid,refid,catid,sap_name,case_barcode,product_barcode,gross_price_case,gross_price_piece,packs_or_bags,'.' as image_path from skus",result=True)
        print('ApiGetSKUs > cursor',cursor)
        data  = [dict(((cursor.description[i][0]), value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print('ApiGetSKUs > data',data)
        return data