from repository import get_suppliers

def supplier_id_to_name(supplier_id):
    if supplier_id is None:
        return "-"
    for s in get_suppliers():
        if s.id == supplier_id:
            return s.name
    return "-"
