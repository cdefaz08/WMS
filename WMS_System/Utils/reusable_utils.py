
# utils/reusable_utils.py

from PyQt5.QtWidgets import QComboBox, QTableWidgetItem

def get_updated_fields(original: dict, current: dict) -> dict:
    """Devuelve los campos que cambiaron entre original y actual."""
    return {
        k: v for k, v in current.items()
        if str(v).strip() != str(original.get(k, "")).strip()
    }

def populate_combobox(combobox, items, label_field, value_field):
    """Llena un QComboBox con datos desde una lista de diccionarios."""
    combobox.clear()
    for item in items:
        combobox.addItem(item[label_field], item[value_field])

def get_table_item_text(table, row, col):
    """Obtiene el texto de una celda en QTableWidget."""
    item = table.item(row, col)
    return item.text().strip() if item else ""

def safe_disconnect_signal(widget, signal):
    """Desconecta una señal sin lanzar error si ya está desconectada."""
    try:
        signal.disconnect()
    except TypeError:
        pass

def calculate_total_pieces(qty, uom, config):
    """Convierte la cantidad en unidades a piezas totales."""
    per_case = config.get("pieces_per_case", 1)
    per_pallet = config.get("boxes_per_pallet", 1)

    if uom == "Pieces":
        return qty
    elif uom == "Carton":
        return qty * per_case
    elif uom == "Pallets":
        return qty * per_case * per_pallet
    return qty

def calculate_total_price(unit_price, total_pieces):
    """Calcula el precio total."""
    try:
        return float(unit_price) * float(total_pieces)
    except:
        return 0.0

def load_lines_from_api(api_client, endpoint, parent_id):
    """Carga líneas desde un endpoint por ID padre."""
    try:
        response = api_client.get(f"{endpoint}/{parent_id}")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def handle_upc_change(upc_value, api_client):
    """Consulta un item por UPC y devuelve el primer resultado."""
    if not upc_value or not upc_value.isdigit():
        return {}

    response = api_client.get(f"/items?upc={upc_value}")
    if response.status_code != 200:
        return {}

    items = response.json()
    return items[0] if items else {}

def delete_backend_record(api_client, endpoint, record_id):
    """Elimina un registro en el backend por ID."""
    try:
        response = api_client.delete(f"{endpoint}/{record_id}")
        return response.status_code in (200, 204)
    except:
        return False
