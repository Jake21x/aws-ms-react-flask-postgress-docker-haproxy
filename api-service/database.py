import psycopg2

class Database(object):
    connection = None
 
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
            cls.connection = psycopg2.connect(
                database='sales_track_v2', 
                user='postgres',
                host='db.pcrwpfgzubsfyfbrczlj.supabase.co', 
                password='jmgtechplays21x'
            )    
        return cls.connection

    def execute_query(cls, query):
        """execute query on singleton db connection"""
        connection = cls.get_connection()
        try:
            cursor = connection.cursor()
        except psycopg2.ProgrammingError:
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result