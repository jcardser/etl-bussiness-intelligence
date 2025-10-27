Descripción

El proyecto consistió en el desarrollo de un proceso ETL (Extracción, Transformación y Carga) aplicado a un conjunto de datos de la plataforma Airbnb, con el fin de analizar información relacionada con alojamientos, reseñas y disponibilidad. Para ello, se implementaron clases en Python que permitieron extraer los datos desde MongoDB, transformarlos mediante limpieza y normalización, y finalmente cargarlos en una base de datos PostgreSQL y en archivos Excel para su posterior análisis.

Objetivo
Desarrollar un proceso ETL que permita obtener, limpiar, transformar y almacenar datos de Airbnb de manera estructurada, garantizando su calidad y facilitando su uso en futuros análisis y visualizaciones.

*INTEGRANTES*

Juan Manuel Valencia Giraldo:
Se encargó de la fase de extracción de datos, estableciendo la conexión con la base de datos local de MongoDB y desarrollando la clase Extracción en Python. Implementó la obtención de los datos de las colecciones listings, reviews y calendar, asegurando su correcta conversión a DataFrames de pandas y el registro de los eventos en los archivos de log.

Ziuvar Ruiz Alvarez:
Tuvo la responsabilidad del análisis exploratorio de datos (EDA). Realizó la revisión de la estructura, tipos de datos, valores nulos, duplicados y posibles valores atípicos. Además, documentó los principales hallazgos con gráficos interpretativos, identificando oportunidades de mejora en la calidad de los datos y proponiendo transformaciones adecuadas para su limpieza y estandarización.

Darwin Alexander Osorio Ospina:
Fue responsable del desarrollo de la fase de transformación de datos, implementando la clase Transformación en Python. Ejecutó las tareas de normalización de precios, conversión de formatos de fecha, categorización de variables y expansión de campos anidados. También integró el manejo de logs dentro del proceso para registrar las acciones y garantizar la trazabilidad de las modificaciones realizadas.

Juan Sebastian Cardona Serna:
Se encargó de la fase de carga y documentación final del proyecto, desarrollando la clase Carga para insertar los datos transformados en una base de datos PostgreSQL y exportarlos a archivos Excel. Además, participó en la elaboración del informe final, estructurando la descripción del dataset, el resumen de los hallazgos, las conclusiones sobre la calidad y utilidad de los datos, y la documentación general del flujo ETL.


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
