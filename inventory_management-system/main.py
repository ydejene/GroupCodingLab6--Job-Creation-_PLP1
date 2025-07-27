#!/usr/bin/env python3
# Standard library imports for system operations
import os    # Operating system interface functions
import sys   # System-specific parameters and functions

# Import product management functions from products module
from products import add_product, view_products, update_product, delete_product

# Import sales management functions from sales module
from sales import record_sale, view_sales_history, sales_summary

# Import database initialization function
from database import initialize_database

# Import utility functions for user interface
from utils import clear_screen, pause

def display_menu():
    # Clears screen and displays the main menu with all available options
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
    # Initialize database connection at startup
    print("Starting SmallBiz Inventory System...")
    if initialize_database():
        print("System ready!\n")
    else:
        print("Failed to connect to database. Please check your MySQL connection.")
        return
    
    # Main application loop - keeps program running until user exits
    while True:
        display_menu()
        choice = input("Select an option (1-8): ").strip()
        
        # Process user menu selection and call appropriate function
        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            record_sale()
        elif choice == '6':
            view_sales_history()
        elif choice == '7':
            sales_summary()
        elif choice == '8':
            # Exit the application gracefully
            print("\nThank you for using SmallBiz Inventory System!")
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
        
        pause()

# Run the application when script is executed directly
if __name__ == "__main__":
    main()
