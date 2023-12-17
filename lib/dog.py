import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @staticmethod
    def create_table():
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """)
        CONN.commit()

    @staticmethod
    def drop_table():
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id:
           
            CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?", (self.name, self.breed, self.id))
        else:
            
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            self.id = CURSOR.lastrowid
        CONN.commit()
        return self

    @staticmethod
    def create(name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @staticmethod
    def new_from_db(row):
        return Dog(row[1], row[2], row[0])

    @staticmethod
    def get_all():
        CURSOR.execute("SELECT * FROM dogs")
        return [Dog.new_from_db(row) for row in CURSOR.fetchall()]

    @staticmethod
    def find_by_name(name):
        CURSOR.execute("SELECT * FROM dogs WHERE name=?", (name,))
        row = CURSOR.fetchone()
        if row:
            return Dog.new_from_db(row)
        return None

    @staticmethod
    def find_by_id(dog_id):
        CURSOR.execute("SELECT * FROM dogs WHERE id=?", (dog_id,))
        row = CURSOR.fetchone()
        if row:
            return Dog.new_from_db(row)
        return None

    @staticmethod
    def find_or_create_by(name, breed):
        dog = Dog.find_by_name(name)
        if dog:
            return dog
        return Dog.create(name, breed)

    def update(self):
        if not self.id:
            raise ValueError("Dog instance must already exist in the database to be updated")
        self.save()
        return self

    
    pass
