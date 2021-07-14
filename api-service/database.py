import psycopg2
class Database(object):
    connection = None
 
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
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
            cls.connection = psycopg2.connect(
                dbname='youtube', 
                user='postgres',
                host='127.0.0.1', 
                password='mysuperpassword', 
                port=5432,
                connect_timeout=3,
                keepalives=1,
                keepalives_idle=5,
                keepalives_interval=2,
                keepalives_count=2,
                options='-c statement_timeout=5000000'
            )    
        return cls.connection

    def execute(cls, query):
        """execute query on singleton db connection"""
        cursor = None
        try: 
            connection = cls.get_connection()
            print('db connection reused')
            cursor = connection.cursor()
        except psycopg2.ProgrammingError:
            print('db connection created')
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()
         
        # try:
        cursor.execute(query)
        result = cursor.fetchall() 
        # except psycopg2.ProgrammingError:
        #     print('error') 
        return result

    def mogrify(cls, query,data):
        """execute query on singleton db connection"""
        cursor = None
        try: 
            connection = cls.get_connection()
            print('db connection reused')
            cursor = connection.cursor()
        except psycopg2.ProgrammingError:
            print('db connection created')
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()

        # try:
        cursor.execute(cursor.mogrify(query,data))
        result = cursor.fetchall() 
        # finally:
        #     cursor.close() 
        return result