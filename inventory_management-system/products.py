#!/usr/bin/env python3

from database import execute_query
from utils import clear_screen
import mysql.connector

def add_product():
    """Add a new product to the inventory"""
    clear_screen()
    print("="*60)
    print("                    ADD NEW PRODUCT")
    print("="*60)
    
    try:
        # Get product information from user
        print("Please enter the product details:")
        print("-" * 40)
        
        # Get product name
        while True:
            name = input("Product Name: ").strip()
            if name:
                break
            print("The product name cannot be empty. Please try again.")
        
        # Get product price
        while True:
            try:
                price_input = input("Product Price ($): ").strip()
                price = float(price_input)
                if price >= 0:
                    break
                else:
                    print("Price cannot be negative. Please enter a valid price.")
            except ValueError:
                print("Invalid price format. Please enter a number (e.g., 10.50)")
        
        # Get quantity in stock
        while True:
            try:
                quantity_input = input("Quantity in Stock: ").strip()
                quantity = int(quantity_input)
                if quantity >= 0:
                    break
                else:
                    print("Quantity cannot be negative. Please enter a valid number.")
            except ValueError:
                print("Invalid quantity format. Please enter a whole number.")
        
        # Display entered information for confirmation
        print("\n" + "-" * 40)
        print("PRODUCT INFORMATION SUMMARY:")
        print(f"Name: {name}")
        print(f"Price: ${price:.2f}")
        print(f"Quantity: {quantity}")
        print("-" * 40)
        
        # Confirm before saving
        confirm = input("Do you want to save this product? (y/N): ").lower().strip()
        
        if confirm == 'y' or confirm == 'yes':
            # Insert product into database
            insert_query = """
                INSERT INTO products (name, price, quantity) 
                VALUES (%s, %s, %s)
            """
            
            result = execute_query(insert_query, (name, price, quantity))
            
            if result is not None:
                print("\nSUCCESS!")
                print(f"Product '{name}' has been added to inventory successfully!")
                print(f"Product ID: {result}")
                print(f"You can now sell this product or update its details anytime.")
            else:
                print("\nFAILED!")
                print("Could not add product to database. Please try again.")
                
        else:
            print("\nProduct addition cancelled.")
            
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            print(f"\nERROR: A product with the name '{name}' already exists!")
            print("Please choose a different product name or update the existing product.")
        else:
            print(f"\nDatabase constraint error: {e}")
            
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please contact system administrator if this problem persists.")