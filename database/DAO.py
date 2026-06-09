from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_sightings(anno, shape): #nodi
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s 
                        where year(s.`datetime`)=%s and s.shape = %s"""
            cursor.execute(query, (anno, shape, ))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_anni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as y
                        from sighting s 
                        order by year(s.`datetime`) DESC """
            cursor.execute(query)

            for row in cursor:
                result.append(row["y"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_archi(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct t1.id as id1, t2.id as id2
                        from
                            (select s.*
                            from sighting s 
                            where year(s.`datetime`)=%s and s.shape = %s) as t1, 
                            (select s.*
                            from sighting s 
                            where year(s.`datetime`)=%s and s.shape = %s) as t2
                        where t1.id<t2.id and t1.state=t2.state"""
            cursor.execute(query, (anno, shape, anno, shape))

            for row in cursor:
                result.append((row["id1"], row["id2"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shape(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.shape) as s
                                from sighting s 
                                where s.shape!="" and year(s.`datetime`)=%s
                                order by s.shape """
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["s"])
            cursor.close()
            cnx.close()
        return result
