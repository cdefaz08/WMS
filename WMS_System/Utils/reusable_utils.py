
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

def fetch_item_by_upc(api_client, upc_value):
    """Devuelve el primer item encontrado por UPC, junto con su configuración."""
    if not upc_value or not upc_value.isdigit():
        return None, None

    try:
        response = api_client.get(f"/items?upc={upc_value}")
        if response.status_code != 200:
            return None, None

        items = response.json()
        if not items:
            return None, None

        product = items[0]
        item_id = product["id"]

        # Cargar configuración del item
        config_response = api_client.get(f"/item-config/item-maintance/default/{item_id}")
        config = config_response.json() if config_response.status_code == 200 else {}

        return product, config
    except Exception as e:
        print(f"⚠️ Error during UPC lookup: {e}")
        return None, None

def delete_backend_record(api_client, endpoint, record_id):
    """Elimina un registro en el backend por ID."""
    try:
        response = api_client.delete(f"{endpoint}/{record_id}")
        return response.status_code in (200, 204)
    except:
        return False

def get_default_item_config(api_client, item_id):
    """Consulta la configuración por defecto de un item."""
    if not item_id:
        return {}

    try:
        response = api_client.get(f"/item-config/item-maintance/default/{item_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"⚠️ Error fetching config: {e}")
    return {}
