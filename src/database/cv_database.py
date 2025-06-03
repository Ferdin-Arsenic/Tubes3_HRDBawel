import os
import mysql.connector

class CVExtractor:
    def extract_data():
        pass

class DBConnection:
    def __init__(self):
        self.db_name = "ats_cv_hrdbawel"

        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (self.db_name,))
        result = cursor.fetchone()
        if result is None:
            print(f"Database {self.db_name} does not exist. Initializing...")
            self.init_database(cursor)

    def init_database(self, cursor):
        cursor.execute(f"CREATE DATABASE {self.db_name}")
        cursor.execute(f"USE {self.db_name}")

        cursor.execute('''
            CREATE TABLE ApplicantProfile (
                applicant_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                first_name VARCHAR(50) DEFAULT NULL,
                last_name VARCHAR(50) DEFAULT NULL,
                date_of_birth date DEFAULT NULL,
                address VARCHAR(255) DEFAULT NULL,
                phone_number VARCHAR(20) DEFAULT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE ApplicationDetail (
                detail_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                applicant_id INT NOT NULL,
                application_role VARCHAR(100) DEFAULT NULL,
                cv_path TEXT,
                
                FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
            );
        ''')
    
    def seed_database(self, cursor, data_directory):
        for file in os.listdir(data_directory):
            if file.endswith('.pdf'):
                cv_path = os.path.join(data_directory, file)
                # Simulate CV extraction
                cv_data = CVExtractor.extract_data(cv_path)

    def connect(self):
        # Simulate a database connection
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
        else:
            print("No active database connection to close.")


if __name__ == "__main__":
    import subprocess

    # Start server
    server = subprocess.Popen("mysqld")

    db = DBConnection()

    server.terminate()
    server.wait()

