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

def view_products():
   """Display all products in a formatted table"""
   clear_screen()
   print("="*60)
   print("                   PRODUCT INVENTORY")
   print("="*60)
  
   try:
       query = "SELECT id, name, price, quantity, created_date FROM products ORDER BY name"
       products = execute_query(query)
      
       if products and len(products) > 0:
           print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Stock':<8} {'Date Added':<12}")
           print("-" * 70)
          
           total_products = 0
           total_value = 0
          
           for product in products:
               product_id, name, price, quantity, created_date = product
              
               date_str = str(created_date)[:10] if created_date else "N/A"
              
               product_value = price * quantity
               total_value += product_value
               total_products += 1

               print(f"{product_id:<5} {name[:24]:<25} ${price:<9.2f} {quantity:<8} {date_str:<12}")

           print("-" * 70)
           print(f"Total Products: {total_products}")
           print(f"Total Inventory Value: ${total_value:.2f}")
          
       else:
           print("No products found in inventory.")
           print("\nWould you like to add your first product?")
           print("Select option 1 from the main menu to add a product.")
          
   except Exception as e:
       print(f" Error retrieving products: {e}")
  
   print("\n" + "="*60)
   input("Press Enter to return to main menu...")

def update_product():
   """Update an existing product's information"""
   clear_screen()
   print("="*60)
   print("                   UPDATE PRODUCT")
   print("="*60)
  
   try:
       print("Current products in inventory:")
       print("-" * 50)
      
       query = "SELECT id, name, price, quantity FROM products ORDER BY name"
       products = execute_query(query)
      
       if not products or len(products) == 0:
           print("No products found in inventory.")
           print("Add some products first before updating.")
           input("Press Enter to return to main menu...")
           return

       print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Stock':<8}")
       print("-" * 50)
       for product in products:
           product_id, name, price, quantity = product
           print(f"{product_id:<5} {name[:24]:<25} ${price:<9.2f} {quantity:<8}")
      
       print("-" * 50)

       while True:
           try:
               product_id = int(input("Enter Product ID to update: ").strip())
               break
           except ValueError:
               print("Please enter a valid product ID number.")

       product = get_product_by_id(product_id)
       if not product:
           print(f"Product with ID {product_id} not found!")
           input("Press Enter to return to main menu...")
           return
      
       current_id, current_name, current_price, current_quantity = product
      
       print(f"\nCurrent product details:")
       print(f"Name: {current_name}")
       print(f"Price: ${current_price:.2f}")
       print(f"Stock: {current_quantity}")
      
       print(f"\nWhat would you like to update?")
       print("1. Product Name")
       print("2. Product Price")
       print("3. Stock Quantity")
       print("4. All Details")
       print("5. Cancel")
      
       choice = input("Select option (1-5): ").strip()
      
       if choice == '1':
           new_name = input(f"Enter new name (current: {current_name}): ").strip()
           if new_name:
               update_query = "UPDATE products SET name = %s WHERE id = %s"
               result = execute_query(update_query, (new_name, product_id))
               if result is not None:
                   print(f"Product name updated to '{new_name}'")
               else:
                   print("Failed to update product name")
      
       elif choice == '2':
           try:
               new_price = float(input(f"Enter new price (current: ${current_price:.2f}): $").strip())
               if new_price >= 0:
                   update_query = "UPDATE products SET price = %s WHERE id = %s"
                   result = execute_query(update_query, (new_price, product_id))
                   if result is not None:
                       print(f"Product price updated to ${new_price:.2f}")
                   else:
                       print("Failed to update product price")
               else:
                   print("Price cannot be negative")
           except ValueError:
               print("Invalid price format")
      
       elif choice == '3':
           try:
               new_quantity = int(input(f"Enter new quantity (current: {current_quantity}): ").strip())
               if new_quantity >= 0:
                   update_query = "UPDATE products SET quantity = %s WHERE id = %s"
                   result = execute_query(update_query, (new_quantity, product_id))
                   if result is not None:
                       print(f"Stock quantity updated to {new_quantity}")
                   else:
                       print("Failed to update stock quantity")
               else:
                   print("Quantity cannot be negative")
           except ValueError:
               print("Invalid quantity format")
      
       elif choice == '4':
           print("Enter new details (press Enter to keep current value):")

           new_name = input(f"New name (current: {current_name}): ").strip()
           if not new_name:
               new_name = current_name

           try:
               price_input = input(f"New price (current: ${current_price:.2f}): $").strip()
               new_price = float(price_input) if price_input else current_price
               if new_price < 0:
                   print("Price cannot be negative, keeping current price")
                   new_price = current_price
           except ValueError:
               print("Invalid price format, keeping current price")
               new_price = current_price

           try:
               quantity_input = input(f"New quantity (current: {current_quantity}): ").strip()
               new_quantity = int(quantity_input) if quantity_input else current_quantity
               if new_quantity < 0:
                   print("Quantity cannot be negative, keeping current quantity")
                   new_quantity = current_quantity
           except ValueError:
               print("Invalid quantity format, keeping current quantity")
               new_quantity = current_quantity

           update_query = """
               UPDATE products
               SET name = %s, price = %s, quantity = %s
               WHERE id = %s
           """
           result = execute_query(update_query, (new_name, new_price, new_quantity, product_id))
          
           if result is not None:
               print("All product details updated successfully!")
               print(f"   Name: {new_name}")
               print(f"   Price: ${new_price:.2f}")
               print(f"   Quantity: {new_quantity}")
           else:
               print("Failed to update product details")
      
       elif choice == '5':
           print("Update cancelled")
      
       else:
           print("Invalid option selected")
          
   except Exception as e:
       print(f"Error updating product: {e}")
  
   print("\n" + "="*60)
   input("Press Enter to return to main menu...")

def delete_product():
   """Delete a product from the inventory"""
   clear_screen()
   print("="*60)
   print("                   DELETE PRODUCT")
   print("="*60)
  
   try:
       print("Current products in inventory:")
       print("-" * 50)
      
       query = "SELECT id, name, price, quantity FROM products ORDER BY name"
       products = execute_query(query)
      
       if not products or len(products) == 0:
           print("No products found in inventory.")
           print("Nothing to delete.")
           input("Press Enter to return to main menu...")
           return

       print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Stock':<8}")
       print("-" * 50)
       for product in products:
           product_id, name, price, quantity = product
           print(f"{product_id:<5} {name[:24]:<25} ${price:<9.2f} {quantity:<8}")
      
       print("-" * 50)

       while True:
           try:
               product_id = int(input("Enter Product ID to delete: ").strip())
               break
           except ValueError:
               print("Please enter a valid product ID number.")
 
       product = get_product_by_id(product_id)
       if not product:
           print(f"Product with ID {product_id} not found!")
           input("Press Enter to return to main menu...")
           return
      
       current_id, current_name, current_price, current_quantity = product

       print(f"\nCONFIRM DELETION")
       print(f"Product to delete:")
       print(f"   ID: {current_id}")
       print(f"   Name: {current_name}")
       print(f"   Price: ${current_price:.2f}")
       print(f"   Stock: {current_quantity}")
      
       print(f"\nWARNING: This action cannot be undone!")
       confirm = input("Are you sure you want to delete this product? (type 'DELETE' to confirm): ").strip()
      
       if confirm == 'DELETE':
           delete_query = "DELETE FROM products WHERE id = %s"
           result = execute_query(delete_query, (product_id,))
          
           if result is not None:
               print(f"\nSUCCESS!")
               print(f"Product '{current_name}' has been deleted from inventory.")
           else:
               print(f"\nFAILED!")
               print("Could not delete product. Please try again.")
       else:
           print(f"\nDeletion cancelled.")
           print("Product was not deleted.")
          
   except Exception as e:
       print(f"Error deleting product: {e}")
  
   print("\n" + "="*60)
   input("Press Enter to return to main menu...")

def get_product_by_id(product_id):
   """Get single product by ID"""
   query = "SELECT id, name, price, quantity FROM products WHERE id = %s"
   result = execute_query(query, (product_id,))
   return result[0] if result else None

