"""
Enhanced Database Setup with User Management
Creates tables for: users, alerts, user_sessions
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Anurag*29'
DB_NAME = 'car'

def create_database_and_tables():
    """Create database and all required tables"""
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"✓ Database '{DB_NAME}' created/verified")
            
            # Use the database
            cursor.execute(f"USE {DB_NAME}")
            
            # Drop existing tables to recreate with new schema
            cursor.execute("DROP TABLE IF EXISTS user_sessions")
            cursor.execute("DROP TABLE IF EXISTS user_alerts")
            cursor.execute("DROP TABLE IF EXISTS alerts")
            cursor.execute("DROP TABLE IF EXISTS users")
            
            # Create users table
            create_users_table = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uid VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                display_name VARCHAR(255),
                email_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                role ENUM('user', 'admin') DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE
            )
            """
            cursor.execute(create_users_table)
            print("✓ Table 'users' created")
            
            # Create alerts table (enhanced with user reference)
            create_alerts_table = """
            CREATE TABLE alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                object_class VARCHAR(50),
                confidence FLOAT,
                distance FLOAT,
                image_path VARCHAR(255),
                image_data LONGBLOB,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_alerts_table)
            print("✓ Table 'alerts' created")
            
            # Create user_sessions table
            create_sessions_table = """
            CREATE TABLE user_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                logout_time TIMESTAMP NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_sessions_table)
            print("✓ Table 'user_sessions' created")
            
            # Create admin user
            admin_email = "admin@adas.com"
            admin_uid = "admin-" + datetime.now().strftime("%Y%m%d%H%M%S")
            
            insert_admin = """
            INSERT INTO users (uid, email, display_name, email_verified, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_admin, (admin_uid, admin_email, "Admin", True, "admin"))
            print(f"✓ Admin user created: {admin_email}")
            print(f"  Note: Create Firebase account with this email to access admin panel")
            
            connection.commit()
            print("\n✅ Database setup complete!")
            print(f"📊 Database: {DB_NAME}")
            print(f"📋 Tables created: users, alerts, user_sessions")
            print(f"\n🔐 Admin Account:")
            print(f"   Email: {admin_email}")
            print(f"   Password: Set this in Firebase Authentication")
            
    except Error as e:
        print(f"❌ Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n✓ Database connection closed")

if __name__ == "__main__":
    print("🚀 Setting up ADAS Database...\n")
    create_database_and_tables()
