import os
import re
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from models.search import CVPersonalData, ApplicantProfile, ApplicationDetail

""" SQL Queries """

CREATE_TABLES = '''
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        applicant_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        first_name VARCHAR(50) DEFAULT NULL,
        last_name VARCHAR(50) DEFAULT NULL,
        date_of_birth date DEFAULT NULL,
        address VARCHAR(255) DEFAULT NULL,
        phone_number VARCHAR(20) DEFAULT NULL
    );
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        detail_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        applicant_id INT NOT NULL,
        application_role VARCHAR(100) DEFAULT NULL,
        cv_path TEXT,
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
    );
'''

MATCH_APPLICANT_ID = '''
    SELECT applicant_id FROM ApplicantProfile
    WHERE first_name = %s AND last_name = %s AND date_of_birth = %s
    AND address = %s AND phone_number = %s
    LIMIT 1;
'''

INSERT_NEW_APPLICANT_PROFILE = '''
    INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
    VALUES (%s, %s, %s, %s, %s);
'''

INSERT_NEW_APPLICATION_DETAIL = '''
    INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
    VALUES (%s, %s, %s);
'''

SELECT_CV_PATH = '''
    SELECT cv_path FROM ApplicationDetail WHERE detail_id = %s;
'''

SELECT_ALL_CV_PATH = '''
    SELECT cv_path FROM ApplicationDetail;
'''

SELECT_APPLICATION_DETAIL = '''
    SELECT * FROM ApplicationDetail WHERE detail_id = %s;
'''

SELECT_APPLICANT_PROFILE = '''
    SELECT * FROM ApplicantProfile WHERE applicant_id = %s;
'''


try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    print("MySQL connector not available. Database features will be disabled.")
    MYSQL_AVAILABLE = False

class CVDatabase:
    def __init__(self):
        self.db_name = "ats_cv_hrdbawel"
        self.connection = None
        
        if not MYSQL_AVAILABLE:
            print("MySQL not available, using file-based mode")
            return
        
        # Check if MySQL port is open first
        print("Checking if MySQL server is running...")
        if not self._is_mysql_running():
            print("MySQL server is not running or not accessible on localhost:3306")
            return
            
        try:
            print("MySQL server detected. Attempting connection...")
            self.connect()
            
            if self.connection is None:
                print("Failed to establish database connection")
                return
                
            cursor = self.connection.cursor()
            cursor.execute("SHOW DATABASES LIKE %s", (self.db_name,))
            result = cursor.fetchone()
            if result is None:
                print(f"Database {self.db_name} does not exist. Initializing...")
                self.init_database(cursor)
            
            cursor.execute(f"USE {self.db_name}")
            print(f"Database '{self.db_name}' ready.")
            cursor.close()
            
        except Exception as err:
            print(f"Database initialization error: {err}")
            print("Continuing in file-based mode...")
            self.connection = None

    def _is_mysql_running(self):
        """Check if MySQL server is running on localhost:3306"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 2 second timeout
            result = sock.connect_ex(('localhost', 3306))
            sock.close()
            return result == 0
        except Exception as e:
            print(f"Error checking MySQL port: {e}")
            return False

    def init_database(self, cursor):
        cursor.execute(f"CREATE DATABASE {self.db_name}")
        cursor.execute(f"USE {self.db_name}")

        cursor.execute(CREATE_TABLES)
        
        cursor.commit()
        cursor.close()
    
    def seed_database(self, relative_data_directory, role=""):
        if role == "":
            role = "Unknown"
        cursor = self.connection.cursor()
        for file in os.listdir(relative_data_directory):
            if file.endswith('.pdf'):
                cv_path = os.path.join(relative_data_directory, file)
                cv_data: CVPersonalData | None = None       # TO DO: Implement extractor
                # cv_data = CVExtractor.extract_data(cv_path)
                if cv_data is None:
                    continue

                # Check if personal data already exists, if not insert it
                cursor.execute(MATCH_APPLICANT_ID, (cv_data.first_name, cv_data.last_name, cv_data.date_of_birth))
                applicant_id = cursor.fetchone()
                if applicant_id is None:
                    cursor.execute(INSERT_NEW_APPLICANT_PROFILE, (
                        cv_data.first_name, cv_data.last_name, cv_data.date_of_birth,
                        cv_data.address, cv_data.phone_number
                    ))
                    applicant_id = cursor.lastrowid
                
                # Insert application detail
                cursor.execute(INSERT_NEW_APPLICATION_DETAIL, (applicant_id, role, cv_path))
        cursor.commit()
        cursor.close()

    def _connect_with_timeout(self):
        """Internal method to create MySQL connection with proper timeout handling"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                connect_timeout=3,  # Reduced timeout
                autocommit=True,
                use_pure=True,  # Force pure Python implementation
                sql_mode='',
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            return connection
        except Exception as e:
            raise e

    def connect(self):
        if not MYSQL_AVAILABLE:
            return
        
        try:
            print("Attempting MySQL connection with:")
            print("- Host: localhost")
            print("- User: root")
            print("- Password: (empty)")
            print("- Timeout: 3 seconds")
            print("- Using pure Python implementation")
            
            # Use ThreadPoolExecutor to enforce timeout
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._connect_with_timeout)
                try:
                    self.connection = future.result(timeout=5)  # 5 second total timeout
                    print("✓ MySQL connection successful")
                except FutureTimeoutError:
                    print("✗ MySQL connection timed out after 5 seconds")
                    self.connection = None
                    return
                except Exception as e:
                    raise e
            
        except mysql.connector.Error as err:
            print(f"✗ MySQL connection failed: {err}")
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("  → Check username/password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("  → Database does not exist")
            else:
                print(f"  → Error code: {err.errno}")
            self.connection = None
            
        except Exception as err:
            print(f"✗ Unexpected error during MySQL connection: {err}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def get_cv_path(self, detail_id: int) -> str | None:
        if not self.connection:
            print("Database connection is not established.")
            return None
        with self.connection.cursor() as cursor:
            cursor = self.connection.cursor()
            cursor.execute(SELECT_CV_PATH, (detail_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_all_cv_path(self) -> list[str] | None:
        if not self.connection:
            print("Database connection is not established.")
            return None
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CV_PATH)
            results = cursor.fetchall()
            return [row[0] for row in results if row[0] is not None]

    def get_application_detail(self, detail_id: int) -> ApplicationDetail | None:
        if not self.connection:
            print("Database connection is not established.")
            return None
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_APPLICATION_DETAIL, (detail_id,))
            result = cursor.fetchone()
            if result:
                return ApplicationDetail(
                    detail_id=result[0],
                    applicant_id=result[1],
                    application_role=result[2],
                    cv_path=result[3]
                )
            return None

    def get_applicant_profile(self, applicant_id: int) -> ApplicantProfile | None:
        if not self.connection:
            print("Database connection is not established.")
            return None
        with self.connection.cursor() as cursor:
            cursor.execute(SELECT_APPLICANT_PROFILE, (applicant_id,))
            result = cursor.fetchone()
            if result:
                return ApplicantProfile(
                    applicant_id=result[0],
                    first_name=result[1],
                    last_name=result[2],
                    date_of_birth=result[3],
                    address=result[4],
                    phone_number=result[5]
                )
            return None
        

if __name__ == "__main__":
    print("=== MySQL Connection Test ===")
    db = CvDatabase()
    if db.connection:
        print("Database connection established successfully.")
        db.close()
    else:
        print("Database connection failed or not initialized.")