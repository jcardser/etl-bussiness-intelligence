
---

## 🧩 Capas de la Arquitectura

### 1. **Domain (Núcleo del negocio)**
Contiene las reglas de negocio y modelos del dominio.
- `entities/`: define las entidades del negocio (por ejemplo, `Producto`, `Cliente`).
- `services/`: casos de uso principales (por ejemplo, `ETLService`).
- `validators/`: reglas de validación o políticas de calidad de datos.

👉 Esta capa **no depende de ninguna librería externa**.

---

### 2. **Infrastructure (Infraestructura y adaptadores)**
Implementa los detalles técnicos que interactúan con el exterior:
- `repositories/`: interacción con bases de datos (ORM, SQLAlchemy, etc.)
- `clients/`: llamadas a APIs o servicios externos.
- `utils/`: manejo de configuración, logging, errores, etc.

👉 Esta capa **depende del dominio**, pero no al revés.

---

### 3. **Application (Orquestación del flujo ETL)**
Contiene los scripts o controladores que **coordinan el proceso ETL completo**:
- `extract_job.py`: proceso de extracción.
- `transform_job.py`: transformaciones de datos.
- `load_job.py`: carga en destino (por ejemplo, PostgreSQL).

👉 Esta capa orquesta **servicios del dominio** y **adaptadores de infraestructura**.

---

### 4. **Interface (Interfaz de entrada/salida)**
Define cómo se ejecuta el ETL:
- `cli.py`: comandos de línea (por ejemplo, `python cli.py run-etl`).
- `rest_api.py`: endpoints REST si se expone como API o servicio.

---

### 5. **main.py**
Punto de entrada del proyecto.  
Puede ser usado para:
- Ejecutar el pipeline completo.
- Iniciar el servidor REST.
- Coordinar tareas automatizadas (cron, Airflow, etc.).

---

## ⚙️ Instalación del entorno

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# .\venv\Scripts\activate  # En Windows

# Instalar dependencias base
pip install -r requirements.txt
