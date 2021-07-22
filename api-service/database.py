import psycopg2
class Database(object):
    connection = None
 
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
            
            cls.connection = psycopg2.connect(
                dbname='postgres', 
                user='postgres',
                host='database-1.cua1z6h2gwyu.us-west-2.rds.amazonaws.com', 
                password=':FgSBNs~s4s$4L)u', 
                connect_timeout=3,
                keepalives=1,
                keepalives_idle=5,
                keepalives_interval=2,
                keepalives_count=2,
                options='-c statement_timeout=5000000'
            )    

            # cls.connection = psycopg2.connect(
            #     dbname='sales_track_v2', 
            #     user='postgres',
            #     host='db.pcrwpfgzubsfyfbrczlj.supabase.co', 
            #     password='jmgtechplays21x', 
            #     connect_timeout=3,
            #     keepalives=1,
            #     keepalives_idle=5,
            #     keepalives_interval=2,
            #     keepalives_count=2,
            #     options='-c statement_timeout=5000000'
            # )    
        return cls.connection

    def execute(cls, query,result = False,commit = False,log=False):
        """execute query on singleton db connection"""
        
        cursor = None
        rs = None

        try: 
            connection = cls.get_connection()
            print('db connection reused')
            cursor = connection.cursor()
        except psycopg2.ProgrammingError:
            print('db connection created')
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()
          
        cursor.execute(query)
 
        
        if result:
            rs = cursor

        if commit:
            connection.commit()
 
        return rs

    def mogrify(cls, query,data , result = False,commit = False,log=False):
        """execute query on singleton db connection"""
        cursor = None
        rs = None
        try: 
            connection = cls.get_connection()
            # print('db connection reused')
            cursor = connection.cursor()
        
        except psycopg2.ProgrammingError:
            print('db connection created')
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()
            
        query = cursor.mogrify(query,data)
        # print('query',query) 

        cursor.execute(query)
         
        if result:
            rs = cursor

        if commit:
            connection.commit() 

        # finally:
        #     cursor.close() 
        return rs