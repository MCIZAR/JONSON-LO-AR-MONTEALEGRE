from database import get_connection, initialize_database
from models import User, Supplier, Part
from typing import List, Optional

initialize_database()

# ------------- Users -------------
def ensure_admin_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "123456", "admin"))
    conn.commit()
    conn.close()

def authenticate(username: str, password: str) -> Optional[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    r = cur.fetchone()
    conn.close()
    if r:
        return User(id=r['id'], username=r['username'], password=r['password'], role=r['role'])
    return None

# ------------- Suppliers -------------
def add_supplier(supplier: Supplier) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO suppliers (name, contact, address) VALUES (?, ?, ?)", (supplier.name, supplier.contact, supplier.address))
    conn.commit()
    supplier_id = cur.lastrowid
    conn.close()
    return supplier_id

def get_suppliers() -> List[Supplier]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [Supplier(id=r['id'], name=r['name'], contact=r['contact'], address=r['address']) for r in rows]

def update_supplier(supplier: Supplier):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE suppliers SET name=?, contact=?, address=? WHERE id=?", (supplier.name, supplier.contact, supplier.address, supplier.id))
    conn.commit()
    conn.close()

def delete_supplier(supplier_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
    conn.commit()
    conn.close()

# ------------- Parts -------------
def add_part(part: Part) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO parts (code, name, description, price, quantity, supplier_id) VALUES (?, ?, ?, ?, ?, ?)",
                (part.code, part.name, part.description, part.price, part.quantity, part.supplier_id))
    conn.commit()
    part_id = cur.lastrowid
    conn.close()
    return part_id

def update_part(part: Part):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE parts SET code=?, name=?, description=?, price=?, quantity=?, supplier_id=? WHERE id=?",
                (part.code, part.name, part.description, part.price, part.quantity, part.supplier_id, part.id))
    conn.commit()
    conn.close()

def delete_part(part_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM parts WHERE id=?", (part_id,))
    conn.commit()
    conn.close()

def get_parts() -> List[Part]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM parts ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [Part(id=r['id'], code=r['code'], name=r['name'], description=r['description'], price=r['price'], quantity=r['quantity'], supplier_id=r['supplier_id']) for r in rows]

def find_part_by_code(code: str) -> Optional[Part]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM parts WHERE code=?", (code,))
    r = cur.fetchone()
    conn.close()
    if r:
        return Part(id=r['id'], code=r['code'], name=r['name'], description=r['description'], price=r['price'], quantity=r['quantity'], supplier_id=r['supplier_id'])
    return None

def low_stock_alerts(threshold: int = 5) -> List[Part]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM parts WHERE quantity <= ? ORDER BY quantity ASC", (threshold,))
    rows = cur.fetchall()
    conn.close()
    return [Part(id=r['id'], code=r['code'], name=r['name'], description=r['description'], price=r['price'], quantity=r['quantity'], supplier_id=r['supplier_id']) for r in rows]

# ------------- Search Functionality -------------
def search_parts(keyword: str) -> List[Part]:
    conn = get_connection()
    cur = conn.cursor()
    keyword = f"%{keyword}%"
    cur.execute("SELECT * FROM parts WHERE code LIKE ? OR name LIKE ? ORDER BY name", (keyword, keyword))
    rows = cur.fetchall()
    conn.close()
    return [Part(id=r['id'], code=r['code'], name=r['name'], description=r['description'], price=r['price'], quantity=r['quantity'], supplier_id=r['supplier_id']) for r in rows]
