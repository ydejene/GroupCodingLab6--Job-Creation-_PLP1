#!/usr/bin/env python3

from database import execute_query
from utils import clear_screen
import mysql.connector

def add_product():
    clear_screen()
    print("="*60)
    print("                    ADD NEW PRODUCT")
    print("="*60)
    
    try:
        print("Please enter the product details:")
        print("-" * 40)
        
        while True:
            name = input("Product Name: ").strip()
            if name:
                break
            print("The product name cannot be empty. Please try again.")
        
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
        
        print("\n" + "-" * 40)
        print("PRODUCT INFORMATION SUMMARY:")
        print(f"Name: {name}")
        print(f"Price: ${price:.2f}")
        print(f"Quantity: {quantity}")
        print("-" * 40)
        
        confirm = input("Do you want to save this product? (y/N): ").lower().strip()
        
        if confirm == 'y' or confirm == 'yes':
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

def view_products():
    clear_screen()
    print("="*60)
    print("                    ALL PRODUCTS")
    print("="*60)
    
    query = "SELECT id, name, price, quantity FROM products ORDER BY name"
    products = execute_query(query)
    
    if not products:
        print("No products found in inventory.")
        print("Use 'Add Product' option to add products first.")
        return
    
    print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Quantity':<10}")
    print("-" * 60)
    
    total_products = 0
    total_value = 0
    
    for product_id, name, price, quantity in products:
        print(f"{product_id:<5} {name:<25} ${price:<9.2f} {quantity:<10}")
        total_products += quantity
        total_value += price * quantity
    
    print("-" * 60)
    print(f"Total Products: {len(products)} types")
    print(f"Total Items in Stock: {total_products}")
    print(f"Total Inventory Value: ${total_value:.2f}")

def update_product():
    clear_screen()
    print("="*60)
    print("                   UPDATE PRODUCT")
    print("="*60)
    
    query = "SELECT id, name, price, quantity FROM products ORDER BY name"
    products = execute_query(query)
    
    if not products:
        print("No products available to update.")
        return
    
    print("Current Products:")
    print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Quantity':<10}")
    print("-" * 60)
    for product_id, name, price, quantity in products:
        print(f"{product_id:<5} {name:<25} ${price:<9.2f} {quantity:<10}")
    
    try:
        product_id = int(input("\nEnter Product ID to update: "))
        
        product_query = "SELECT id, name, price, quantity FROM products WHERE id = %s"
        product_result = execute_query(product_query, (product_id,))
        
        if not product_result:
            print("Invalid Product ID.")
            return
        
        current_id, current_name, current_price, current_quantity = product_result[0]
        
        print(f"\nCurrent Product Details:")
        print(f"Name: {current_name}")
        print(f"Price: ${current_price:.2f}")
        print(f"Quantity: {current_quantity}")
        
        print("\nEnter new values (press Enter to keep current value):")
        
        new_name = input(f"New name [{current_name}]: ").strip()
        if not new_name:
            new_name = current_name
        
        price_input = input(f"New price [{current_price:.2f}]: ").strip()
        if price_input:
            try:
                new_price = float(price_input)
                if new_price < 0:
                    print("Price cannot be negative. Keeping current price.")
                    new_price = current_price
            except ValueError:
                print("Invalid price format. Keeping current price.")
                new_price = current_price
        else:
            new_price = current_price
        
        quantity_input = input(f"New quantity [{current_quantity}]: ").strip()
        if quantity_input:
            try:
                new_quantity = int(quantity_input)
                if new_quantity < 0:
                    print("Quantity cannot be negative. Keeping current quantity.")
                    new_quantity = current_quantity
            except ValueError:
                print("Invalid quantity format. Keeping current quantity.")
                new_quantity = current_quantity
        else:
            new_quantity = current_quantity
        
        print("\n" + "-" * 40)
        print("UPDATED PRODUCT INFORMATION:")
        print(f"Name: {new_name}")
        print(f"Price: ${new_price:.2f}")
        print(f"Quantity: {new_quantity}")
        print("-" * 40)
        
        confirm = input("Save these changes? (y/N): ").lower().strip()
        
        if confirm == 'y':
            update_query = """
                UPDATE products 
                SET name = %s, price = %s, quantity = %s 
                WHERE id = %s
            """
            
            result = execute_query(update_query, (new_name, new_price, new_quantity, product_id))
            
            if result is not None:
                print("\nProduct updated successfully!")
            else:
                print("\nFailed to update product.")
        else:
            print("\nUpdate cancelled.")
    
    except ValueError:
        print("Invalid input. Please enter numbers only for ID.")
    except Exception as e:
        print(f"Error updating product: {e}")

def delete_product():
    clear_screen()
    print("="*60)
    print("                   DELETE PRODUCT")
    print("="*60)
    
    query = "SELECT id, name, price, quantity FROM products ORDER BY name"
    products = execute_query(query)
    
    if not products:
        print("No products available to delete.")
        return
    
    print("Current Products:")
    print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Quantity':<10}")
    print("-" * 60)
    for product_id, name, price, quantity in products:
        print(f"{product_id:<5} {name:<25} ${price:<9.2f} {quantity:<10}")
    
    try:
        product_id = int(input("\nEnter Product ID to delete: "))
        
        product_query = "SELECT id, name, price, quantity FROM products WHERE id = %s"
        product_result = execute_query(product_query, (product_id,))
        
        if not product_result:
            print("Invalid Product ID.")
            return
        
        product_id, name, price, quantity = product_result[0]
        
        print(f"\nProduct to delete:")
        print(f"Name: {name}")
        print(f"Price: ${price:.2f}")
        print(f"Quantity: {quantity}")
        
        print("\nWARNING: This action cannot be undone!")
        print("All sales records for this product will also be deleted.")
        
        confirm = input("Are you sure you want to delete this product? (y/N): ").lower().strip()
        
        if confirm == 'y':
            delete_query = "DELETE FROM products WHERE id = %s"
            result = execute_query(delete_query, (product_id,))
            
            if result is not None:
                print(f"\nProduct '{name}' deleted successfully!")
            else:
                print("\nFailed to delete product.")
        else:
            print("\nDeletion cancelled.")
    
    except ValueError:
        print("Invalid input. Please enter numbers only for ID.")
    except Exception as e:
        print(f"Error deleting product: {e}")