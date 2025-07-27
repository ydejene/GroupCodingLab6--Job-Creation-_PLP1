# SmallBiz Inventory Management System

A lightweight and user-friendly inventory and sales management system designed to help small businesses — especially in Africa's informal sector — digitize their operations. It enables product tracking, sales management, and performance summaries using a terminal-based interface powered by Python and MySQL.

---

## Features

- Add, update, delete, and view products
- Record and manage sales transactions
- Track sales history and performance summaries
- Automatic database and table setup with sample data
- Real-time inventory and sales revenue insights
- Command-line interface for maximum accessibility

---

## Project Structure

```plaintext
smallbiz-inventory/
├── main.py             # Main app entry: menu and control flow
├── database.py         # DB setup, connection, and query execution
├── products.py         # Product operations (CRUD)
├── sales.py            # Sales handling: record, history, summary
├── utils.py            # Utility helpers: clear screen, pause
└── README.md           # Project documentation
```

---

## Setup Instructions

### Requirements
- Python 3.x
- MySQL Server running locally
- mysql-connector-python (install via pip)

### Installation & Run

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/smallbiz-inventory.git
   cd smallbiz-inventory
   ```

2. **Install MySQL connector**
   ```bash
   pip install mysql-connector-python
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

If it's your first time, the app will guide you to:
- Create the `smallbiz_inventory` database
- Create a MySQL user `group6@localhost` (password: root)
- Set up tables (products, sales)
- Add initial product data

---

## File Descriptions

### 1. main.py
- Starts the application
- Handles menu navigation and user input
- Routes to the appropriate module based on selection

### 2. database.py
Handles MySQL database configuration and connection

**Includes:**
- Auto-setup of database and user
- Creation of products and sales tables
- Sample product seeding
- Utility functions like `execute_query()`, `get_product_by_id()`, etc.

### 3. products.py
**Functions:**
- `view_products()`: Lists all products in a table
- `update_product()`: Edit name, price, or quantity
- `delete_product()`: Confirm and remove a product
- `get_product_by_id()`: Fetch a specific product's details

### 4. sales.py
**Functions:**
- `record_sale()`: Process and log a product sale
- `view_sales_history()`: View all sales in reverse chronological order
- `sales_summary()`: View total revenue, top products, and recent sales

### 5. utils.py
**Functions:**
- `clear_screen()`: Clears the terminal screen (cls for Windows, clear for UNIX)
- `pause()`: Waits for the user to press Enter before continuing

---

## Usage

Once you run the application with `python main.py`, you'll see a main menu with the following options:

1. **View Products** - Display all products with their details
2. **Add Product** - Add new products to inventory
3. **Update Product** - Modify existing product information
4. **Delete Product** - Remove products from inventory
5. **Record Sale** - Process a sale transaction
6. **View Sales History** - See all past sales
7. **Sales Summary** - View performance metrics and insights
8. **Exit** - Close the application

Navigate through the menu by entering the corresponding number for each option.

---

## Contributing

This is the sole property of GroupCodingLab_6 Members. 
---

## License

This project is open source and available under the MIT License.
