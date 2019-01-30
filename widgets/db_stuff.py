import sqlite3
import os
import os.path
from datetime import datetime


class DB_Manager(object):
    def __init__(self, db_file, create_new=False):
        self._conn = None
        self._c = None

        if db_file != ':memory:' and os.path.exists(db_file) and not create_new:
            self._connect(db_file)
        else:
            self._create_db(db_file)

    def _connect(self, file_name):
        self._conn = sqlite3.connect(file_name, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._c = self._conn.cursor()

    def _create_db(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

        self._connect(file_name)

        self._c.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)')

        self._c.execute('CREATE TABLE lastUser(id INTEGER PRIMARY KEY, name TEXT UNIQUE, positionCB Integer)')

        self._c.execute('CREATE TABLE sessions(id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER REFERENCES users(id),'
                        'right INTEGER, wrong INTEGER, ts TIMESTAMP)')

        self._c.execute('CREATE TABLE sessionsq(id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER REFERENCES users(id),'
                        'right INTEGER, wrong INTEGER, ts TIMESTAMP, quality INTEGER )')

    def insert_user(self, user_name):
        self._c.execute('INSERT INTO users VALUES(NULL, ?)', (user_name,))
        # self.commit()
        return self._c.lastrowid  # return id of inserted user

    def insert_lastUser(self,userID ,user_name,position):
        self._c.execute('INSERT INTO lastUser VALUES(?, ?,?)', (userID,user_name,position))
        return self._c.lastrowid  # return id of inserted user

    def delete_user(self, user):
        if type(user) == str or type(user) == unicode:
            user = self.get_user_id(user)
        self._c.execute('DELETE FROM users WHERE id==?', (user,))

    def delete_lastUser(self,user):
        # if type(user) == str or type(user) == unicode:
        #     userId = self.get_lastUser_id(user)

        self._c.execute('DELETE FROM lastUser')

    def insert_session(self, user, right_answers, wrong_answers, time_finished=None):
        """
        :param user: you can use the id as well as the name of the user
        """
        if type(user) == str or type(user) == unicode:
            user = self.get_user_id(user)

        self._c.execute('INSERT INTO sessions VALUES(NULL, ?, ?, ?, ?)',
                        (user, right_answers, wrong_answers, time_finished if time_finished is not None else datetime.now()))

    def insert_session_quality(self, user, right_answers, wrong_answers, time_finished=None,quality=0):
        """
        :param user: you can use the id as well as the name of the user
        """
        if type(user) == str or type(user) == unicode:
            user = self.get_user_id(user)

        self._c.execute('INSERT INTO sessionsq VALUES(NULL, ?, ?, ?, ?,?)',
                        (user, right_answers, wrong_answers, time_finished if time_finished is not None else datetime.now(),quality))


    def get_user_id(self, user_name):
        self._c.execute('SELECT id FROM users WHERE name==?', (user_name,))
        return self._c.fetchone()[0]

    def get_lastUser_id(self,user_name):
        self._c.execute('SELECT id FROM lastUser WHERE name==?', (user_name,))
        return self._c.fetchone()

    def get_user_name(self, user_id):
        self._c.execute('SELECT name FROM users WHERE id==?', (user_id,))
        return self._c.fetchone()[0]

    def get_lastUser_name_position(self):
        self._c.execute('SELECT name,positionCB FROM lastUser')
        return self._c.fetchone()

    def get_all_users(self):
        """
        :return: a list of tuples (user_id, user_name)
        """
        self._c.execute('SELECT * FROM users')
        return self._c.fetchall()

    def get_all_user_names(self):
        return [name for _id, name in self.get_all_users()]

    def get_all_sessions(self):
        """
        :return: a list of tuples (user_name, right_answers, wrong_answers, datetime)
        """
        self._c.execute('SELECT users.name, sessions.right, sessions.wrong, sessions.ts '
                        'FROM sessions INNER JOIN users ON sessions.user==users.id')
        return self._c.fetchall()

    def get_all_sessions_of_user(self, user):
        """
        :param user: you can use the id as well as the name of the user
        :return: a list of tuples (right_answers, wrong_answers, datetime)
        """
        if type(user) == str or type(user) == unicode:
            user = self.get_user_id(user)

        self._c.execute('SELECT right, wrong, ts FROM sessions WHERE user==?', (user,))
        return self._c.fetchall()

    def get_all_sessions_of_user_quality(self, user,qualityC):
        """
        :param user: you can use the id as well as the name of the user
        :return: a list of tuples (right_answers, wrong_answers, datetime)
        """
        if type(user) == str or type(user) == unicode:
            user = self.get_user_id(user)

        self._c.execute('SELECT right, wrong, ts,quality FROM sessionsq WHERE quality==? AND user==?', (qualityC,user))
        # self._c.execute('SELECT right, wrong, ts,quality FROM sessionsq WHERE user==?', (user,))
        return sorted(self._c.fetchall(),key=lambda t:t[2])

    def commit(self):
        self._conn.commit()

    def close(self):
        # save (commit) the changes
        self._conn.commit()

        # we can also close the cursor if we are done with it
        self._c.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# with DB_Manager(':memory:') as dbm:
#     dbm.insert_user('pepe')
#     dbm.insert_session('pepe', 5, 7)
#     sessions = dbm.get_all_sessions_of_user('pepe')
#     print(sessions[0])
