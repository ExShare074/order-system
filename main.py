import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import sqlite3

def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    status TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
                (customer_name_entry.get(), order_details_entry.get()))
    conn.commit()
    conn.close()

    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)
    view_orders()

def view_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def close_orders():
    selected_items = tree.selection()
    if selected_items:
        order_id = tree.item(selected_items[0])['values'][0]
        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'Закрыт' where id = ?", (order_id,))
        conn.commit()
        conn.close()
        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для закрытия")



app = tk.Tk()
app.title("Система управления заказами")

tk.Label(app, text="Имя клиента").pack()

customer_name_entry = tk.Entry()
customer_name_entry.pack()

tk.Label(app, text="Детали заказа").pack()

order_details_entry = tk.Entry()
order_details_entry.pack()

add_button = ttk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

close_button = ttk.Button(app, text="Закрыть заказ", command=close_orders)
close_button.pack()

columns = ("ID", "customer_name", "order_details", "status")  # Заголовки столбцов
tree = ttk.Treeview(app, columns=columns, show="headings")  # Создание таблицы

for column in columns:
    tree.heading(column, text=column)  # Заголовки столбцов
tree.pack()

init_db()
view_orders()
app.mainloop()
