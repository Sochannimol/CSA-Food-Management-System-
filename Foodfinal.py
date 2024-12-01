import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Database functions
def create_tables():
    conn = sqlite3.connect('food_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS food_items (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        ingredients TEXT,
                        location TEXT,
                        price REAL,
                        user_id INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        total REAL,
                        transportation TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                        id INTEGER PRIMARY KEY,
                        order_id INTEGER,
                        food_item_id INTEGER,
                        FOREIGN KEY(order_id) REFERENCES orders(id),
                        FOREIGN KEY(food_item_id) REFERENCES food_items(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transportation (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_history (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        order_details TEXT,
                        total REAL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# Authentication functions
def register_user(username, password):
    try:
        conn = sqlite3.connect('food_manager.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = sqlite3.connect('food_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Food management functions
def add_food_item(name, ingredients, location, price, user_id):
    try:
        conn = sqlite3.connect('food_manager.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO food_items (name, ingredients, location, price, user_id) VALUES (?, ?, ?, ?, ?)",
                       (name, ingredients, location, price, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add food item: {e}")
        return False

def update_food_item(food_id, name, ingredients, location, price):
    try:
        conn = sqlite3.connect('food_manager.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE food_items SET name = ?, ingredients = ?, location = ?, price = ? WHERE id = ?",
                       (name, ingredients, location, price, food_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update food item: {e}")
        return False

def delete_food_item(food_id):
    try:
        conn = sqlite3.connect('food_manager.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM foodo_items WHERE id = ?", (food_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete food item: {e}")
        return False

def get_food_items(user_id):
    conn = sqlite3.connect('food_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE user_id = ?", (user_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def search_food_items(query):
    conn = sqlite3.connect('food_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE name LIKE ? OR location LIKE ?", ('%' + query + '%', '%' + query + '%'))
    items = cursor.fetchall()
    conn.close()
    return items

def save_order_to_history(user_id, order_details, total):
    conn = sqlite3.connect('food_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO order_history (user_id, order_details, total) VALUES (?, ?, ?)",
                   (user_id, order_details, total))
    conn.commit()
    conn.close()

# GUI Functions
class FoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Manager App")
        self.user_id = None  # Placeholder for user ID
        self.order_list = []  # Placeholder for the user's order list

        self.create_main_ui()

    def create_main_ui(self):
        # Frame for login or main app content
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        # Login screen
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        self.password_entry = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.login_frame, text="Username", font=("Arial", 14)).grid(row=0, column=0)
        tk.Label(self.login_frame, text="Password", font=("Arial", 14)).grid(row=1, column=0)

        # Register/Login Buttons
        tk.Button(self.login_frame, text="Login", font=("Arial", 14), command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", font=("Arial", 14), command=self.register).grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login_user(username, password)
        if user:
            self.user_id = user[0]
            messagebox.showinfo("Login", "Login successful!")
            self.login_frame.destroy()  # Remove login screen
            self.create_food_manager_ui()
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if register_user(username, password):
            messagebox.showinfo("Registration", "Registration successful!")
            self.login_frame.destroy()  # Remove login screen
            self.create_food_manager_ui()
        else:
            messagebox.showerror("Error", "Registration failed. Username may already exist.")

    def create_food_manager_ui(self):
        # Main screen frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Add food item UI
        tk.Label(self.main_frame, text="Food Name", font=("Arial", 14)).grid(row=0, column=0)
        tk.Label(self.main_frame, text="Ingredients", font=("Arial", 14)).grid(row=1, column=0)
        tk.Label(self.main_frame, text="Location", font=("Arial", 14)).grid(row=2, column=0)
        tk.Label(self.main_frame, text="Price", font=("Arial", 14)).grid(row=3, column=0)

        self.food_name_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.ingredients_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.location_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.price_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.food_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.ingredients_entry.grid(row=1, column=1, padx=10, pady=10)
        self.location_entry.grid(row=2, column=1, padx=10, pady=10)
        self.price_entry.grid(row=3, column=1, padx=10, pady=10)

        # Add food button
        tk.Button(self.main_frame, text="Add Food Item", font=("Arial", 14), command=self.add_food_item).grid(row=4, column=0, columnspan=2, pady=10)

        # Search bar for food items
        self.search_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.search_entry.grid(row=5, column=0, padx=10, pady=10)
        tk.Button(self.main_frame, text="Search Food", font=("Arial", 14), command=self.search_food).grid(row=5, column=1, padx=10, pady=10)

        # List food items
        self.food_listbox = tk.Listbox(self.main_frame, font=("Arial", 14), width=50, height=10)
        self.food_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.update_food_list()

        # Buttons for order and history
        tk.Button(self.main_frame, text="View Order History", font=("Arial", 14), command=self.view_order_history).grid(row=7, column=0, pady=10)
        tk.Button(self.main_frame, text="Manage Orders", font=("Arial", 14), command=self.manage_orders).grid(row=7, column=1, pady=10)

    def add_food_item(self):
        name = self.food_name_entry.get()
        ingredients = self.ingredients_entry.get()
        location = self.location_entry.get()
        price = float(self.price_entry.get())

        if add_food_item(name, ingredients, location, price, self.user_id):
            messagebox.showinfo("Success", "Food item added successfully!")
            self.update_food_list()
        else:
            messagebox.showerror("Error", "Failed to add food item.")

    def update_food_list(self):
        self.food_listbox.delete(0, tk.END)
        food_items = get_food_items(self.user_id)
        for item in food_items:
            self.food_listbox.insert(tk.END, f"{item[1]} - {item[3]} - ${item[4]}")

    def search_food(self):
        query = self.search_entry.get()
        results = search_food_items(query)
        self.food_listbox.delete(0, tk.END)
        for item in results:
            self.food_listbox.insert(tk.END, f"{item[1]} - {item[3]} - ${item[4]}")

    def view_order_history(self):
        self.main_frame.pack_forget()
        self.order_history_frame = tk.Frame(self.root)
        self.order_history_frame.pack(padx=20, pady=20)

        self.order_history_listbox = tk.Listbox(self.order_history_frame, font=("Arial", 14), width=50, height=10)
        self.order_history_listbox.pack(padx=10, pady=10)

        conn = sqlite3.connect('food_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT order_details, total, date FROM order_history WHERE user_id = ?", (self.user_id,))
        history = cursor.fetchall()
        conn.close()

        for item in history:
            self.order_history_listbox.insert(tk.END, f"{item[0]} - Total: ${item[1]} - Date: {item[2]}")

        tk.Button(self.order_history_frame, text="Back", font=("Arial", 14), command=self.back_to_main).pack(pady=10)

    def manage_orders(self):
        self.main_frame.pack_forget()
        self.order_frame = tk.Frame(self.root)
        self.order_frame.pack(padx=20, pady=20)

        # Listbox for available food items to order
        tk.Label(self.order_frame, text="Available Food Items", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.available_food_listbox = tk.Listbox(self.order_frame, font=("Arial", 14), width=30, height=10)
        self.available_food_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.update_available_food_list()

        # Listbox for current order items
        tk.Label(self.order_frame, text="Current Order", font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)
        self.order_listbox = tk.Listbox(self.order_frame, font=("Arial", 14), width=30, height=10)
        self.order_listbox.grid(row=1, column=1, padx=10, pady=10)

        # Add/Remove buttons
        tk.Button(self.order_frame, text="Add to Order", font=("Arial", 14), command=self.add_to_order).grid(row=2, column=0, pady=10)
        tk.Button(self.order_frame, text="Remove from Order", font=("Arial", 14), command=self.remove_from_order).grid(row=2, column=1, pady=10)

        # Place order button
        tk.Button(self.order_frame, text="Place Order", font=("Arial", 14), command=self.place_order).grid(row=3, column=0, columnspan=2, pady=10)

        # Back button
        tk.Button(self.order_frame, text="Back", font=("Arial", 14), command=self.back_to_main).grid(row=4, column=0, columnspan=2, pady=10)

    def update_available_food_list(self):
        self.available_food_listbox.delete(0, tk.END)
        food_items = get_food_items(self.user_id)
        for item in food_items:
            self.available_food_listbox.insert(tk.END, f"{item[1]} - {item[3]} - ${item[4]}")

    def add_to_order(self):
        selected_item = self.available_food_listbox.get(tk.ACTIVE)
        if selected_item:
            self.order_listbox.insert(tk.END, selected_item)
            self.order_list.append(selected_item.split(" - ")[0])  # Just the food name

    def remove_from_order(self):
        selected_item_index = self.order_listbox.curselection()
        if selected_item_index:
            self.order_listbox.delete(selected_item_index)
            del self.order_list[selected_item_index[0]]

    def place_order(self):
        if self.order_list:
            order_details = ", ".join(self.order_list)
            total = sum([float(item.split(" - ")[2][1:]) for item in self.order_listbox.get(0, tk.END)])
            save_order_to_history(self.user_id, order_details, total)
            self.order_listbox.delete(0, tk.END)
            self.order_list.clear()
            messagebox.showinfo("Order", "Order placed successfully!")
        else:
            messagebox.showwarning("Order", "No items in the order.")

    def back_to_main(self):
        if hasattr(self, 'order_history_frame'):
            self.order_history_frame.pack_forget()
        if hasattr(self, 'order_frame'):
            self.order_frame.pack_forget()
        self.main_frame.pack(padx=20, pady=20)

if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()
