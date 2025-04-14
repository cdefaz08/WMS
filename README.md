# 🏷️ Defaz WMS

**Defaz WMS** es un sistema de gestión de almacenes (Warehouse Management System) desarrollado por Carlos Defaz. Incluye una interfaz de escritorio desarrollada con PyQt y una API REST construida con FastAPI. Pensado para ofrecer eficiencia, trazabilidad y escalabilidad en operaciones de inventario.

---

## 🚀 Funcionalidades

- 📄 Gestor de Órdenes de Compra (PO)
- 🚚 Recepción y procesamiento de mercancía
- 📆 Generación automática de números de orden (po_number)
- 🔐 Autenticación JWT y control de usuarios
- 📁 Control de ubicaciones y movimientos de inventario
- 🔹 Rastreabilidad: Registro de usuario creador/modificador
- 💻 Interfaz de escritorio intuitiva para operadores

---

## 🛠️ Tecnologías utilizadas

| Componente       | Tecnología         |
|------------------|---------------------|
| Backend API      | FastAPI             |
| ORM y DB         | SQLAlchemy + SQLite (opcional PostgreSQL/SQL Server) |
| Migraciones      | Alembic             |
| Interfaz Desktop | PyQt5 + Qt Designer |
| Autenticación    | JWT Tokens          |

---

## 📂 Estructura del Proyecto

```
WMS_System/
├── crud/                   # Operaciones CRUD
├── routers/                # Rutas de FastAPI
├── models/                 # Tablas SQLAlchemy
├── schemas/                # Pydantic Schemas
├── Layout/                 # Interfaces PyQt
├── Security/               # Token, login y protección de rutas
├── main.py                 # Punto de entrada principal
├── README.md
└── requirements.txt
```

---

## 🚀 Cómo ejecutar el proyecto

1. **Clona el repositorio:**
```bash
git clone https://github.com/tuusuario/defaz-wms.git
cd defaz-wms
```

2. **Activa entorno virtual e instala dependencias:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Aplica migraciones de base de datos:**
```bash
alembic upgrade head
```

4. **Levanta el servidor API:**
```bash
uvicorn main:app --reload
```

5. **Abre Swagger UI:**  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 Usuario de prueba (ejemplo)

```
Usuario: admin
Contraseña: 123456
```

---

## 📊 Características técnicas clave

- Los tokens JWT incluyen el ID y el username del usuario.
- Todas las operaciones CRUD registran el usuario que las ejecuta.
- El número de PO se genera en formato: `PO-00001`, `PO-00002`, etc.
- La interfaz de PyQt es independiente pero se conecta a la misma API REST.

---

## 📄 Documentación adicional (opcional)

Puedes incluir más detalles en una carpeta `docs/`:

- `docs/database_schema.md` ✔️ Esquema de base de datos
- `docs/api_reference.md` ✔️ Uso de endpoints
- `docs/architecture.md` ✔️ Diagrama de componentes

---

## 👩‍💼 Desarrollador

**Carlos Defaz**  
📧 defaz.dev@email.com  
📍 Dover, NJ  

---

> ✨ Si tienes preguntas o necesitas soporte, no dudes en abrir un issue o contactar directamente. Este sistema fue diseñado para evolucionar contigo.

