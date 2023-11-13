import sqlite3


class Data_Base:

    def __init__(self):
        self.__db = sqlite3.connect('NeroTek_DataBase.db')
        cursore = self.__db.cursor()
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Users_Messages_Shirf` (Users_id INTEGER, Message TEXT, Step INTEGER, Result TEXT)')
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Users_Messages_Deshirf` (Users_id INTEGER, Message TEXT, Step INTEGER, Result TEXT)')
        self.__db.commit()

    def __del__(self):
        self.__db.close()

    async def add_data_shifr(self, Users_id, Message, Step, Result):
        cursore =  self.__db.cursor()
        cursore.execute('''INSERT INTO `Users_Messages_Shirf` VALUES(?,?,?,?)''', (Users_id, Message, Step, Result))
        self.__db.commit()

    async def add_data_deshifr(self, Users_id, Message, Step, Result):
        cursore = self.__db.cursor()
        cursore.execute('''INSERT INTO `Users_Messages_Deshirf` VALUES(?,?,?,?)''', (Users_id, Message, Step, Result))
        self.__db.commit()