import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("crypto_tycoon_bot.db")
        self.cursor = self.connection.cursor()
    
    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
        finally:
            self.connection.close()
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            crypt INTEGER DEFAULT 0,
            videocards INTEGER DEFAULT 1,
            upgrades INTEGER DEFAULT 0,
            house TEXT DEFAULT '',
            car TEXT DEFAULT '',
            pet TEXT DEFAULT '',
            entertainment TEXT DEFAULT ''
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def add_user(self, user_id):
        query = "INSERT OR IGNORE INTO users (user_id) VALUES (?)"
        args = (user_id,)
        self.cursor.execute(query, args)        
        self.connection.commit()
    
    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = ?"
        args = (user_id,)
        self.cursor.execute(query, args)
        self.connection.commit()
    
    def buy_video_card(self, videocard_cost,user_id):
        query = "UPDATE users SET videocards = videocards + 1, crypt = crypt - ? WHERE user_id = ?"
        args = (videocard_cost, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()

    def buy_upgrade(self, upgrade_cost, user_id):
        query = "UPDATE users SET upgrades = upgrades + 1, crypt = crypt - ? WHERE user_id = ?"
        args = (upgrade_cost, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()

    def crypt_earned(self, user_id, value):
        query = "UPDATE users SET crypt = crypt + ? WHERE user_id = ?"
        args = (value, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()

    def buy_house(self, user_id, house_name, house_cost):
        query = "UPDATE users SET house = house || ? || ', ', crypt = crypt - ? WHERE user_id = ?"
        args = (house_name, house_cost, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()

    def buy_car(self, user_id, car_name, car_cost):
        query = "UPDATE users SET car = car || ? || ', ', crypt = crypt - ? WHERE user_id = ?"
        args = (car_name, car_cost, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()
    
    def buy_pet(self, user_id, pet_name, pet_cost):
        query = "UPDATE users SET pet = pet || ? || ', ', crypt = crypt - ? WHERE user_id = ?"
        args = (pet_name, pet_cost, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()
    
    def buy_entertainment(self, user_id, entertainment_name, entertainment_cost):
        query = "UPDATE users SET entertainment = entertainment || ? || ', ', crypt = crypt - ? WHERE user_id = ?"
        args = (entertainment_name, entertainment_cost, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()
    
    def save_progress(self, user_id, crypt, upgrades, videocards):
        query = "UPDATE users SET crypt = ?, videocards = ?, upgrades = ? WHERE user_id = ?"
        args = (crypt, videocards, upgrades, user_id)
        self.cursor.execute(query, args)
        self.connection.commit()