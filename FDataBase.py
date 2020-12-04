import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addPost(self, surname, name, third_name, phone, email, times_h, times_m, simptom, status):
        try:
            self.__cur.execute("INSERT INTO mainmenu VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (surname, name, third_name, phone, email, simptom, times_h, times_m, status))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления записи в БД " + str(e))
            return False
        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT surname, name, third_name, phone, email, times_h, times_m, simptom, status FROM mainmenu WHERE id={postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения записи из БД " + str(e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, surname, name, third_name, phone, email, times_h, times_m, simptom, status FROM mainmenu ORDER BY surname DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения записи из БД " + str(e))

        return []