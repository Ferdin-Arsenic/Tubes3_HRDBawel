import os
import re
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    print("MySQL connector not available. Database features will be disabled.")
    MYSQL_AVAILABLE = False

class CVExtractor:
    def extract_data():
        pass

class CvDatabase:
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
            print("Continuing in file-based mode...")
            return
            
        try:
            print("MySQL server detected. Attempting connection...")
            self.connect()
            
            if self.connection is None:
                print("Failed to establish database connection, using file-based mode")
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
                content TEXT,
                FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
            );
        ''')
    
    def seed_database(self, cursor, data_directory):
        for file in os.listdir(data_directory):
            if file.endswith('.pdf'):
                cv_path = os.path.join(data_directory, file)
                cv_data = CVExtractor.extract_data(cv_path)

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
        print(f"DATABASE: Searching CV Path for detail_id: {detail_id}")
        return f"dataset/pdf/{detail_id}.pdf"

    def get_applicant_data(self, detail_id: int) -> dict | None:
        print(f"DATABASE: Searching data for detail_id: {detail_id}")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        txt_path = os.path.join(base_dir, 'dataset', 'txt', f'{detail_id}.txt')
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            name_search = re.search(r'([a-zA-Z\s]+)\n', content)
            name = name_search.group(1).strip().title() if name_search else f"Applicant {detail_id}"

            return {"name": name, "content": content}
        except FileNotFoundError:
            return {"name": f"Applicant {detail_id}", "content": "File konten tidak ditemukan."}
        except Exception as e:
            print(f"Error reading file for {detail_id}: {e}")
            return None

if __name__ == "__main__":
    print("=== MySQL Connection Test ===")
    db = CvDatabase()
    if db.connection:
        print("✓ Database connection successful and initialized.")
        db.close()
    else:
        print("✗ Running in file-based mode.")
        print("\nTo fix this:")
        print("1. Install MySQL/XAMPP/WAMP")
        print("2. Start MySQL service") 
        print("3. Make sure it's running on localhost:3306")
        print("4. Default user 'root' with empty password should work")
        print("5. If still hanging, try restarting XAMPP MySQL service")