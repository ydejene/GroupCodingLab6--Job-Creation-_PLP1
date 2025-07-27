#!/usr/bin/env python3

from database import execute_query, get_product_by_id
from utils import clear_screen

def record_sale():
    clear_screen()
    print("="*60)
    print("                    RECORD SALE")
    print("="*60)
    
    query = "SELECT id, name, price, quantity FROM products WHERE quantity > 0 ORDER BY name"
    available_products = execute_query(query)
    
    if not available_products:
        print("No products available for sale.")
        print("Please add products to inventory first.")
        return
    
    print("Available Products:")
    print(f"{'ID':<5} {'Product Name':<25} {'Price':<10} {'Stock':<10}")
    print("-" * 60)
    for product_id, name, price, quantity in available_products:
        print(f"{product_id:<5} {name:<25} ${price:<9.2f} {quantity:<10}")
    
    try:
        product_id = int(input("\nEnter Product ID to sell: "))
        
        product = get_product_by_id(product_id)
        if not product:
            print("Invalid Product ID.")
            return
        
        product_id, product_name, product_price, current_stock = product
        
        if current_stock <= 0:
            print(f"Sorry, {product_name} is out of stock.")
            return
        
        print(f"\nSelected Product: {product_name}")
        print(f"Available Stock: {current_stock}")
        print(f"Unit Price: ${product_price:.2f}")
        
        while True:
            try:
                quantity_to_sell = int(input("Quantity to sell: "))
                if quantity_to_sell <= 0:
                    print("Quantity must be greater than 0.")
                    continue
                if quantity_to_sell > current_stock:
                    print(f"Not enough stock. Available: {current_stock}")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        total_amount = quantity_to_sell * product_price
        
        print("\n" + "-" * 40)
        print("SALE SUMMARY:")
        print(f"Product: {product_name}")
        print(f"Quantity: {quantity_to_sell}")
        print(f"Unit Price: ${product_price:.2f}")
        print(f"Total Amount: ${total_amount:.2f}")
        print("-" * 40)
        
        confirm = input("Confirm this sale? (y/N): ").lower().strip()
        
        if confirm == 'y':
            insert_sale_query = """
                INSERT INTO sales (product_id, product_name, quantity_sold, sale_price, total_amount)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            sale_result = execute_query(insert_sale_query, 
                (product_id, product_name, quantity_to_sell, product_price, total_amount))
            
            if sale_result:
                new_stock = current_stock - quantity_to_sell
                update_stock_query = "UPDATE products SET quantity = %s WHERE id = %s"
                stock_result = execute_query(update_stock_query, (new_stock, product_id))
                
                if stock_result is not None:
                    print("\nSALE RECORDED SUCCESSFULLY!")
                    print(f"Sale ID: {sale_result}")
                    print(f"Remaining Stock: {new_stock}")
                    print(f"Revenue Generated: ${total_amount:.2f}")
                else:
                    print("\nWarning: Sale recorded but stock update failed.")
            else:
                print("\nFailed to record sale. Please try again.")
        else:
            print("\nSale cancelled.")
    
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except Exception as e:
        print(f"Error recording sale: {e}")

def view_sales_history():
    clear_screen()
    print("="*60)
    print("                   SALES HISTORY")
    print("="*60)
    
    query = """
        SELECT id, product_name, quantity_sold, sale_price, total_amount, 
               DATE(sale_date) as sale_date
        FROM sales 
        ORDER BY sale_date DESC, id DESC
    """
    
    sales = execute_query(query)
    
    if not sales:
        print("No sales records found.")
        return
    
    print(f"{'ID':<5} {'Product':<20} {'Qty':<5} {'Price':<8} {'Total':<10} {'Date':<12}")
    print("-" * 70)
    
    total_revenue = 0
    for sale_id, product_name, qty_sold, sale_price, total_amount, sale_date in sales:
        print(f"{sale_id:<5} {product_name:<20} {qty_sold:<5} ${sale_price:<7.2f} ${total_amount:<9.2f} {sale_date}")
        total_revenue += total_amount
    
    print("-" * 70)
    print(f"Total Sales Records: {len(sales)}")
    print(f"Total Revenue: ${total_revenue:.2f}")

def sales_summary():
    clear_screen()
    print("="*60)
    print("                   SALES SUMMARY")
    print("="*60)
    
    total_sales_query = "SELECT COUNT(*), SUM(total_amount) FROM sales"
    total_result = execute_query(total_sales_query)
    
    if not total_result or not total_result[0][0]:
        print("No sales data available.")
        return
    
    total_transactions, total_revenue = total_result[0]
    
    print(f"Total Transactions: {total_transactions}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Average Sale Value: ${total_revenue/total_transactions:.2f}")
    
    print("\n" + "="*40)
    print("TOP SELLING PRODUCTS")
    print("="*40)
    
    top_products_query = """
        SELECT product_name, SUM(quantity_sold) as total_sold, 
               SUM(total_amount) as revenue
        FROM sales 
        GROUP BY product_name 
        ORDER BY total_sold DESC
        LIMIT 10
    """
    
    top_products = execute_query(top_products_query)
    
    if top_products:
        print(f"{'Product':<25} {'Qty Sold':<10} {'Revenue':<12}")
        print("-" * 50)
        for product_name, qty_sold, revenue in top_products:
            print(f"{product_name:<25} {qty_sold:<10} ${revenue:<11.2f}")
    
    print("\n" + "="*40)
    print("RECENT SALES (Last 10)")
    print("="*40)
    
    recent_sales_query = """
        SELECT product_name, quantity_sold, total_amount, DATE(sale_date)
        FROM sales 
        ORDER BY sale_date DESC, id DESC
        LIMIT 10
    """
    
    recent_sales = execute_query(recent_sales_query)
    
    if recent_sales:
        print(f"{'Product':<20} {'Qty':<5} {'Amount':<10} {'Date':<12}")
        print("-" * 50)
        for product_name, qty_sold, amount, sale_date in recent_sales:
            print(f"{product_name:<20} {qty_sold:<5} ${amount:<9.2f} {sale_date}")
    
    print("\n" + "="*60)