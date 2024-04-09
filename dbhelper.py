import sqlite3


class Users:
    
    
    def __init__(self, dbname = "users.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)


    def setup(self):
        statement1 = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, chatid INTEGER UNIQUE, points INTEGER DEFAULT 0 )"
        self.conn.execute(statement1)
        self.conn.commit()


    def add_user(self, username_):
        statement = "INSERT OR IGNORE INTO users (chatid) VALUES (?)"
        args = (username_, )
        self.conn.execute(statement, args)
        self.conn.commit()
    

    def update_points(self, amount, userid):
        statement = "UPDATE users SET points = ? WHERE chatid = ?"
        args = (amount, userid)
        self.conn.execute(statement, args)
        self.conn.commit()
        
        
        
    def get_points(self, owner):
        statement = "SELECT points FROM users WHERE chatid = ?"
        args = (owner,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


    def get_users(self):
        statement = "SELECT chatid FROM users"
        return [x[0] for x in self.conn.execute(statement)]
    
    
    def get_all_stats(self):
        statement = "SELECT chatid, points FROM users"
        return [x for x in self.conn.execute(statement)]