# The Inventory Management System Main Application
#!/usr/bin/env python3
import os
import sys
from products import add_product
# , view_products, update_product, delete_product
# from sales import record_sale, view_sales_history, sales_summary
from database import initialize_database
from utils import clear_screen, pause

def display_menu():
    clear_screen()
    print("="*60)
    print("           SMALLBIZ INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print("1. Add Product")
    print("2. View All Products") 
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Record Sale")
    print("6. View Sales History")
    print("7. Sales Summary")
    print("8. Exit")
    print("-"*60)

def main():
    # Initialize the database connection on startup
    print("Starting SmallBiz Inventory System...")
    if initialize_database():
        print("System ready!\n")
    else:
        print("Failed to connect to database. Please check your MySQL connection.")
        return

    while True:
        display_menu()
        choice = input("Select an option (1-8): ").strip()

        if choice == '1':
            add_product()
        # elif choice == '2':
        #     view_products()
        # elif choice == '3':
        #     update_product()
        # elif choice == '4':
        #     delete_product()
        # elif choice == '5':
        #     record_sale()
        # elif choice == '6':
        #     view_sales_history()
        # elif choice == '7':
        #     sales_summary()
        elif choice == '8':
            print("\nThank you for using SmallBiz Inventory System!")
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

        pause()

if __name__ == "__main__":
    main()
