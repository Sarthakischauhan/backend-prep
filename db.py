import sqlite3

class DB():
    def __init__(self):
        self.connection = None
        self.cursor = None
    def connect(self):
        try:
            self.connection = sqlite3.connect('orders.db',check_same_thread=False)
            self.cursor = self.connection.cursor()
        except:
            raise Exception("Not connected with db")

    def get_connection(self):
        return self.connection

    def cursor(self):
        return self.cursor()

    def check_table(self, table_name):
        check_table_query = f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
        """
        if self.cursor:
            self.cursor.execute(check_table_query)
            exists = self.cursor.fetchone()
            return True if exists else False
        return False

    def create_tables(self):

        create_table_script = f"""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ); 

        create table if not exists vehicles(
        id integer primary key autoincrement, 
        model_name varchar(10), 
        year int not null,
        vin text unique not null
        );        


        create table if not exists orders(
        id integer primary key autoincrement, 
        user_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        foreign key (user_id) references users(id),
        foreign key (vehicle_id) references vehicles(id) 
        );
        """
        if self.cursor:
            self.cursor.executescript(create_table_script)

    def populate_tables(self): 
        # ChatGPT generated code to handle repetitive task
        users_data = [
            ("Sarthak Chauhan", "sarthak@example.com"),
            ("Elon Musk", "elon@tesla.com"),
            ("Jane Doe", "jane.doe@example.com"),
            ("John Smith", "john.smith@example.com"),
            ("Alice Johnson", "alice.johnson@example.com")
        ]

        # Tesla Vehicles Only
        vehicles_data = [
            ("S", 2022, "5YJSA1E26JF278938"),
            ("3", 2023, "5YJ3E1EA5KF316789"),
            ("X", 2021, "5YJXCAE21LF232456"),
            ("Y", 2024, "5YJYGDEE5MF058219"),
            ("CT", 2025, "7GNSK5EJ1MF987654")
        ]

        # Insert Users
        user_insert_query = "INSERT INTO users (name, email) VALUES (?, ?) ON CONFLICT(email) DO NOTHING;"
        self.cursor.executemany(user_insert_query, users_data)

        # Insert Vehicles
        vehicle_insert_query = "INSERT INTO vehicles (model_name, year, vin) VALUES (?, ?, ?) ON CONFLICT(vin) DO NOTHING;"
        self.cursor.executemany(vehicle_insert_query, vehicles_data)

        self.connection.commit()
        print("✅ Users and Tesla vehicles inserted successfully!")

    
    def insert_data(self, table, columns, values):
        table_names = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in values]) 
        insert_query = f"INSERT INTO {table} ({table_names}) VALUES ({placeholders});"

        try:
            self.cursor.execute(insert_query, values)  
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")