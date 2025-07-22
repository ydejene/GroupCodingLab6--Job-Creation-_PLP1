#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'group6',
    'password': 'root',
    'database': 'smallbiz_inventory'
}

def get_connection():
    """Create and return MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def initialize_database():
    """Test database connection"""
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
        print(f" Database initialization error: {e}")
        return False

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