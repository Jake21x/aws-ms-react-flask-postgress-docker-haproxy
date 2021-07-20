from flask_restful import Resource
from database import Database  
from itertools import chain

class ApiGetCategory(Resource):
    def get(self):
        conn = Database() 
 
        cats = conn.execute("select catid as tblcategoryid,name as category,to_char(date_updated,\'Dy, DD Mon YYYY HH12:MI:SS\') as app_update,to_char(date_created,\'Dy ,DD Mon YYYY HH12:MI:SS\') as date_transaction from category",result=True)
        x = [dict(((cats.description[i][0]), value) for i, value in enumerate(row)) for row in cats.fetchall()]
        
        for c in chain(range(0, len(x))):
            query = "SELECT brand, refsid as tblrefid,catid as tblcategoryid, segment,\'NA\' as subsegment, percent_share, facing_count, pulloutday,facing_brand,facing_segment FROM category_refs WHERE catid = '{}'".format(str(x[c]['tblcategoryid']))
            print('query',query)
            refs = conn.execute(query,result=True)
            xy = [dict(((refs.description[i][0]), value) for i, value in enumerate(row)) for row in refs.fetchall()]
            x[c]['segment'] = xy

        return x

 