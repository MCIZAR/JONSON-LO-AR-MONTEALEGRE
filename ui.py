import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from repository import (
    add_part, get_parts, delete_part, update_part,
    add_supplier, get_suppliers, delete_supplier, update_supplier, find_part_by_code, low_stock_alerts
)
from models import Part, Supplier

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")  # Black/white feel

# ---------------------- Helper Functions ----------------------
def supplier_id_to_name(supplier_id):
    if supplier_id is None:
        return "-"
    for s in get_suppliers():
        if s.id == supplier_id:
            return s.name
    return "-"

# ---------------------- Parts Table ----------------------
def refresh_parts_table(table, search_text=""):
    for widget in table.winfo_children():
        widget.destroy()
    parts = get_parts()
    if search_text:
        parts = [p for p in parts if search_text.lower() in p.name.lower() or search_text.lower() in p.code.lower()]
    for idx, p in enumerate(parts):
        bg = "#000000" if idx % 2 == 0 else "#222222"
        row_frame = ctk.CTkFrame(table, fg_color=bg)
        row_frame.pack(fill="x", pady=1)
        values = [p.code, p.name, p.description or "", f"{p.price:.2f}", p.quantity, supplier_id_to_name(p.supplier_id)]
        for i, val in enumerate(values):
            ctk.CTkLabel(row_frame, text=val, width=120, anchor="w", fg_color=bg, text_color="white").grid(row=0, column=i, padx=5, pady=5)
        ctk.CTkButton(row_frame, text="Edit", width=50, command=lambda p=p: part_form(table, part=p)).grid(row=0, column=len(values), padx=5)
        ctk.CTkButton(row_frame, text="Delete", width=60, command=lambda p=p: delete_part_confirm(p, table)).grid(row=0, column=len(values)+1, padx=5)

def delete_part_confirm(part, table):
    if messagebox.askokcancel("Delete Part", f"Delete {part.name}?"):
        delete_part(part.id)
        refresh_parts_table(table)

def part_form(parent_table, part=None):
    form = ctk.CTkToplevel()
    form.title("Add/Edit Part")
    form.state('zoomed')

    ctk.CTkLabel(form, text="Part Details", font=("Arial", 30, "bold")).pack(pady=20)

    code_var = tk.StringVar(value=part.code if part else "")
    name_var = tk.StringVar(value=part.name if part else "")
    desc_var = tk.StringVar(value=part.description if part else "")
    price_var = tk.StringVar(value=str(part.price) if part else "0")
    qty_var = tk.StringVar(value=str(part.quantity) if part else "0")
    supplier_names = ["-"] + [s.name for s in get_suppliers()]
    supplier_var = tk.StringVar(value=supplier_id_to_name(part.supplier_id) if part else "-")

    for label_text, var in [("Code", code_var), ("Name", name_var), ("Description", desc_var), ("Price", price_var), ("Quantity", qty_var)]:
        ctk.CTkLabel(form, text=label_text, font=("Arial", 16)).pack(pady=5)
        ctk.CTkEntry(form, textvariable=var, width=400).pack(pady=5)

    ctk.CTkLabel(form, text="Supplier", font=("Arial", 16)).pack(pady=5)
    ctk.CTkOptionMenu(form, values=supplier_names, variable=supplier_var).pack(pady=5)

    def save():
        try:
            supplier_id = None
            for s in get_suppliers():
                if s.name == supplier_var.get():
                    supplier_id = s.id
                    break
            if part:
                part.code = code_var.get()
                part.name = name_var.get()
                part.description = desc_var.get()
                part.price = float(price_var.get())
                part.quantity = int(qty_var.get())
                part.supplier_id = supplier_id
                update_part(part)
            else:
                if find_part_by_code(code_var.get()):
                    messagebox.showerror("Error", "Part code already exists")
                    return
                new_part = Part(None, code_var.get(), name_var.get(), desc_var.get(), float(price_var.get()), int(qty_var.get()), supplier_id)
                add_part(new_part)
            refresh_parts_table(parent_table)
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(form, text="Save", width=200, command=save).pack(pady=20)
    ctk.CTkButton(form, text="Cancel", width=200, command=form.destroy).pack()

# ---------------------- Suppliers Table ----------------------
def refresh_suppliers_table(table, search_text=""):
    for widget in table.winfo_children():
        widget.destroy()
    suppliers = get_suppliers()
    if search_text:
        suppliers = [s for s in suppliers if search_text.lower() in s.name.lower()]
    for idx, s in enumerate(suppliers):
        bg = "#000000" if idx % 2 == 0 else "#222222"
        row_frame = ctk.CTkFrame(table, fg_color=bg)
        row_frame.pack(fill="x", pady=1)
        values = [s.name, s.contact or "", s.address or ""]
        for i, val in enumerate(values):
            ctk.CTkLabel(row_frame, text=val, width=150, anchor="w", fg_color=bg, text_color="white").grid(row=0, column=i, padx=5, pady=5)
        ctk.CTkButton(row_frame, text="Edit", width=50, command=lambda s=s: supplier_form(table, supplier=s)).grid(row=0, column=len(values), padx=5)
        ctk.CTkButton(row_frame, text="Delete", width=60, command=lambda s=s: delete_supplier_confirm(s, table)).grid(row=0, column=len(values)+1, padx=5)

def delete_supplier_confirm(supplier, table):
    if messagebox.askokcancel("Delete Supplier", f"Delete {supplier.name}?"):
        delete_supplier(supplier.id)
        refresh_suppliers_table(table)

def supplier_form(parent_table, supplier=None):
    form = ctk.CTkToplevel()
    form.title("Add/Edit Supplier")
    form.state('zoomed')

    ctk.CTkLabel(form, text="Supplier Details", font=("Arial", 30, "bold")).pack(pady=20)

    name_var = tk.StringVar(value=supplier.name if supplier else "")
    contact_var = tk.StringVar(value=supplier.contact if supplier else "")
    address_var = tk.StringVar(value=supplier.address if supplier else "")

    for label_text, var in [("Name", name_var), ("Contact", contact_var), ("Address", address_var)]:
        ctk.CTkLabel(form, text=label_text, font=("Arial", 16)).pack(pady=5)
        ctk.CTkEntry(form, textvariable=var, width=400).pack(pady=5)

    def save():
        try:
            if supplier:
                supplier.name = name_var.get()
                supplier.contact = contact_var.get()
                supplier.address = address_var.get()
                update_supplier(supplier)
            else:
                new_supplier = Supplier(None, name_var.get(), contact_var.get(), address_var.get())
                add_supplier(new_supplier)
            refresh_suppliers_table(parent_table)
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(form, text="Save", width=200, command=save).pack(pady=20)
    ctk.CTkButton(form, text="Cancel", width=200, command=form.destroy).pack()

# ---------------------- Low Stock Alert ----------------------
def low_stock_alerts_popup():
    alerts = low_stock_alerts()
    if alerts:
        msg = "\n".join([f"{p.name} (Code: {p.code}) - Qty: {p.quantity}" for p in alerts])
        messagebox.showinfo("Low Stock Items", msg)
    else:
        messagebox.showinfo("Low Stock Items", "No low stock items")

# ---------------------- Analytics ----------------------
def show_analytics(analytics_frame):
    for widget in analytics_frame.winfo_children():
        widget.destroy()
    parts = get_parts()
    if not parts:
        tk.Label(analytics_frame, text="No parts to display", font=("Arial", 20), fg="white", bg="black").pack(pady=50)
        return
    # Stock levels
    part_names = [p.name for p in parts]
    quantities = [p.quantity for p in parts]
    low_stock_parts = [p for p in parts if p.quantity <= 5]

    tk.Label(analytics_frame, text=f"Total Parts: {len(parts)}", font=("Arial", 16), fg="white", bg="black").pack(pady=5)
    tk.Label(analytics_frame, text=f"Low Stock Parts (<=5): {len(low_stock_parts)}", font=("Arial", 16), fg="white", bg="black").pack(pady=5)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    bars = ax1.bar(part_names, quantities, color="#555555")
    for bar, qty in zip(bars, quantities):
        if qty <= 5:
            bar.set_color("red")
    ax1.set_xlabel("Part Name")
    ax1.set_ylabel("Quantity")
    ax1.set_title("Stock Levels of All Parts")
    ax1.set_xticklabels(part_names, rotation=45, ha="right", fontsize=9)
    plt.tight_layout()
    canvas1 = FigureCanvasTkAgg(fig1, master=analytics_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill="both", expand=True, pady=20)

    # Parts per supplier
    suppliers = get_suppliers()
    supplier_names = [s.name for s in suppliers]
    supplier_counts = [sum(p.quantity for p in parts if p.supplier_id == s.id) for s in suppliers]

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(supplier_names, supplier_counts, color="#888888")
    ax2.set_xlabel("Supplier")
    ax2.set_ylabel("Total Quantity of Parts")
    ax2.set_title("Total Parts per Supplier")
    ax2.set_xticklabels(supplier_names, rotation=45, ha="right", fontsize=9)
    plt.tight_layout()
    canvas2 = FigureCanvasTkAgg(fig2, master=analytics_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True, pady=20)

# ---------------------- Login Window ----------------------
def login_window():
    login = ctk.CTk()
    login.title("JLM III - Login")
    login.state('zoomed')

    ctk.CTkLabel(login, text="JLM III - Auto Supply System", font=("Arial", 30, "bold")).pack(pady=50)

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    ctk.CTkLabel(login, text="Username", font=("Arial", 16)).pack(pady=10)
    ctk.CTkEntry(login, textvariable=username_var, width=400).pack(pady=5)

    ctk.CTkLabel(login, text="Password", font=("Arial", 16)).pack(pady=10)
    ctk.CTkEntry(login, textvariable=password_var, show="*", width=400).pack(pady=5)

    def login_check():
        if username_var.get() == "admin" and password_var.get() == "123456":
            login.destroy()
            show_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    ctk.CTkButton(login, text="Login", width=200, command=login_check).pack(pady=50)
    login.mainloop()

# ---------------------- Main Window ----------------------
def show_main_window():
    main = ctk.CTk()
    main.title("JLM III - Auto Supply System")
    main.state('zoomed')

    tabview = ctk.CTkTabview(main)
    tabview.pack(expand=True, fill="both")
    tabview.add("Parts")
    tabview.add("Suppliers")
    tabview.add("Analytics")

    # Parts tab
    parts_frame = ctk.CTkScrollableFrame(tabview.tab("Parts"))
    parts_frame.pack(expand=True, fill="both", padx=20, pady=20)

    search_var_parts = tk.StringVar()
    ctk.CTkEntry(parts_frame, textvariable=search_var_parts, placeholder_text="Search by Code or Name", width=400).pack(pady=5)
    ctk.CTkButton(parts_frame, text="Search", width=200, command=lambda: refresh_parts_table(parts_table, search_var_parts.get())).pack(pady=5)

    ctk.CTkButton(parts_frame, text="Add Part", width=200, command=lambda: part_form(parts_frame)).pack(pady=10)
    ctk.CTkButton(parts_frame, text="Low Stock Alerts", width=200, command=low_stock_alerts_popup).pack(pady=10)
    parts_table = ctk.CTkScrollableFrame(parts_frame, width=1000, height=500)
    parts_table.pack(fill="both", expand=True, pady=20)
    refresh_parts_table(parts_table)

    # Suppliers tab
    sup_frame = ctk.CTkScrollableFrame(tabview.tab("Suppliers"))
    sup_frame.pack(expand=True, fill="both", padx=20, pady=20)

    search_var_sup = tk.StringVar()
    ctk.CTkEntry(sup_frame, textvariable=search_var_sup, placeholder_text="Search by Name", width=400).pack(pady=5)
    ctk.CTkButton(sup_frame, text="Search", width=200, command=lambda: refresh_suppliers_table(sup_table, search_var_sup.get())).pack(pady=5)

    ctk.CTkButton(sup_frame, text="Add Supplier", width=200, command=lambda: supplier_form(sup_frame)).pack(pady=10)
    sup_table = ctk.CTkScrollableFrame(sup_frame, width=1000, height=500)
    sup_table.pack(fill="both", expand=True, pady=20)
    refresh_suppliers_table(sup_table)

    # Analytics tab
    analytics_frame = ctk.CTkScrollableFrame(tabview.tab("Analytics"))
    analytics_frame.pack(expand=True, fill="both", padx=20, pady=20)
    ctk.CTkButton(analytics_frame, text="Refresh Analytics", width=200, command=lambda: show_analytics(analytics_frame)).pack(pady=10)
    show_analytics(analytics_frame)

    main.mainloop()
