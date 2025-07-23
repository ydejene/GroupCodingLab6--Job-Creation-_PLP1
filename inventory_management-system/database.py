#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error
import getpass

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'smallbiz_inventory'
}

ROOT_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '' 
}

def get_root_connection():
    """Get root connection for database setup"""
    try:
        connection = mysql.connector.connect(**ROOT_CONFIG)
        if connection.is_connected():
            return connection
    except Error:
        try:
            print("Root connection requires password.")
            root_password = getpass.getpass("Enter MySQL root password: ")
            root_config = ROOT_CONFIG.copy()
            root_config['password'] = root_password
            
            connection = mysql.connector.connect(**root_config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Root connection failed: {e}")
            return None

def setup_database_and_user():
    """Set up database, user, and grant privileges"""
    print("🔧 Setting up database and user...")
    
    root_connection = get_root_connection()
    if not root_connection:
        print("Could not connect as root. Please ensure MySQL is running and you have root access.")
        return False
    
    try:
        cursor = root_connection.cursor()
        print("Creating database 'smallbiz_inventory'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS smallbiz_inventory")
        print("Database created/verified")

        print("👤 Creating user 'group6'@'localhost'...")
        try:
            cursor.execute("CREATE USER IF NOT EXISTS 'group6'@'localhost' IDENTIFIED BY 'root'")
            print("User created/verified")
        except Error as e:
            if "already exists" in str(e).lower():
                print("User already exists")
            else:
                try:
                    cursor.execute("SELECT User FROM mysql.user WHERE User = 'group6' AND Host = 'localhost'")
                    if not cursor.fetchone():
                        cursor.execute("CREATE USER 'group6'@'localhost' IDENTIFIED BY 'root'")
                        print("User created")
                    else:
                        print("User already exists")
                except Error as e2:
                    print(f"User creation warning: {e2}")
        
        print("Granting privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON smallbiz_inventory.* TO 'group6'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("Privileges granted")
        
        cursor.close()
        root_connection.close()
        
        print("Database and user setup completed successfully!")
        return True
        
    except Error as e:
        print(f"Setup error: {e}")
        if root_connection:
            root_connection.close()
        return False

def create_tables():
    """Create required tables"""
    print("Creating tables...")

    tables = {
        'products': """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                price DECIMAL(10,2) NOT NULL,
                quantity INT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        'sales': """
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                product_name VARCHAR(100),
                quantity_sold INT NOT NULL,
                sale_price DECIMAL(10,2) NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """
    }
    
    try:
        connection = get_connection()
        if not connection:
            print("Could not connect to database for table creation")
            return False
        
        cursor = connection.cursor()
        
        for table_name, table_sql in tables.items():
            print(f"Creating table '{table_name}'...")
            cursor.execute(table_sql)
            print(f"Table '{table_name}' created/verified")

        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        if product_count == 0:
            print("Adding sample products...")
            sample_products = [
                ('Rice', 25.00, 50),
                ('Sugar', 10.00, 80),
                ('Cooking Oil', 15.50, 30),
                ('Flour', 12.00, 45),
                ('Salt', 5.00, 100),
                ('Milk', 8.75, 25)
            ]
            
            insert_query = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
            cursor.executemany(insert_query, sample_products)
            connection.commit()
            print(f"Added {len(sample_products)} sample products")
        
        cursor.close()
        connection.close()
        
        print("Tables created successfully!")
        return True
        
    except Error as e:
        print(f"Table creation error: {e}")
        return False

def get_connection():
    """Create and return MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def test_connection():
    """Test the database connection"""
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            return True
        return False
    except Error as e:
        print(f"Connection test error: {e}")
        return False

def initialize_database():
    """Initialize database with full setup if needed"""
    print("Initializing SmallBiz Inventory Database...")
    print("="*60)

    if test_connection():
        print("Database connection successful!")
        print("Database already set up and ready to use.")
        return True
    
    print("Database not accessible. Starting automatic setup...")
    print("\nThis will create:")
    print("  • Database: smallbiz_inventory")
    print("  • User: group6@localhost")
    print("  • Tables: products, sales")
    print("  • Sample data")
    
    proceed = input("\nProceed with automatic setup? (y/N): ").lower().strip()
    if proceed != 'y':
        print("Setup cancelled by user")
        return False
    
    if not setup_database_and_user():
        print("Failed to setup database and user")
        return False

    print("\nTesting connection after setup...")
    if not test_connection():
        print("Connection still failing after setup")
        return False

    if not create_tables():
        print("Failed to create tables")
        return False
    
    print("\n" + "="*60)
    print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("Your team can now use the application without any SQL setup!")
    print("="*60)
    
    return True

def execute_query(query, params=None):
    """Execute a query and return results"""
    try:
        connection = get_connection()
        if not connection:
            return None
            
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        print(f"Database error: {e}")
        return None

def get_product_by_id(product_id):
    """Get single product by ID"""
    query = "SELECT id, name, price, quantity FROM products WHERE id = %s"
    result = execute_query(query, (product_id,))
    return result[0] if result else None

def show_database_status():
    """Show current database status"""
    print("\n" + "="*60)
    print("              DATABASE STATUS")
    print("="*60)
    
    if test_connection():
        print("Database Connection: WORKING")

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM products")
            product_count = cursor.fetchone()[0]
            print(f"Products in inventory: {product_count}")

            cursor.execute("SELECT COUNT(*) FROM sales")
            sales_count = cursor.fetchone()[0]
            print(f"Sales records: {sales_count}")
  
            if product_count > 0:
                cursor.execute("SELECT name, price, quantity FROM products LIMIT 3")
                products = cursor.fetchall()
                print(f"\nSample products:")
                for name, price, qty in products:
                    print(f"   • {name}: ${price:.2f} (Stock: {qty})")
                if product_count > 3:
                    print(f"   ... and {product_count - 3} more products")
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(f"Error checking database status: {e}")
    else:
        print("Database Connection: FAILED")
        print("Run initialize_database() to set up automatically")
    
    print("="*60)