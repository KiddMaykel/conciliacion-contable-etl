\# 📊 Pipeline ETL de Conciliación Bancaria y Auditoría Contable



Automatización desarrollada en \*\*Python\*\* y \*\*SQL\*\* para optimizar el cierre contable mediante el cruce masivo de registros internos (Libro Mayor / ERP) contra cartolas bancarias externas, detectando discrepancias de montos, partidas pendientes y cargos no contabilizados de forma automática.



\---



\## 🎯 Problema de Negocio



En los procesos tradicionales de cierre financiero, la conciliación bancaria suele realizarse de forma manual mediante cruces en hojas de cálculo. Este enfoque presenta tres riesgos críticos:

1\. \*\*Lentitud operativa:\*\* Horas invertidas buscando diferencias en grandes volúmenes de transacciones.

2\. \*\*Riesgo de error humano:\*\* Omisión de comisiones bancarias, duplicidades o errores de digitación.

3\. \*\*Falta de trazabilidad:\*\* Dificultad para auditar rápidamente qué partidas requieren ajuste contable.



\## 💡 Solución Implementada



Este proyecto construye un flujo \*\*ETL (Extract, Transform, Load)\*\* automatizado que:

\* \*\*Extrae\*\* los asientos contables desde una base de datos relacional (\*\*SQLite\*\*) simulando el Libro Mayor de un ERP.

\* \*\*Ingesta\*\* la cartola bancaria en formato estructurado (`.csv`).

\* \*\*Ejecuta reglas de validación contable\*\* mediante `pandas` (Full Outer Join) para emparejar transacciones y clasificar automáticamente cada movimiento en:

&#x20; \* `Conciliado OK`

&#x20; \* `Solo en ERP (Pendiente de cobro/pago)`

&#x20; \* `Solo en Banco (No contabilizado / Comisión)`

\* \*\*Genera un reporte de auditoría\*\* listo para revisión gerencial en formato Excel (`.xlsx`).



\---



\## 🛠️ Stack Tecnológico



\* \*\*Lenguaje:\*\* Python 3

\* \*\*Manipulación y Análisis de Datos:\*\* `pandas`

\* \*\*Gestión de Base de Datos:\*\* SQL (`sqlite3`)

\* \*\*Generación de Reportes:\*\* `openpyxl`



\---



\## 📁 Estructura del Proyecto



```text

conciliacion-contable-etl/

├── data/

│   ├── raw/                  # Cartolas bancarias de entrada (.csv)

│   └── output/               # Reportes de auditoría generados (.xlsx)

├── database/

│   └── contabilidad.db       # Base de datos SQLite (Libro Mayor simulado)

├── src/

│   ├── 01\_generar\_datos.py   # Generación de entorno SQLite y datos con casuística contable

│   └── 02\_conciliacion.py    # Pipeline ETL de extracción, cruce contable y exportación

├── requirements.txt          # Dependencias del proyecto

└── README.md                 # Documentación ejecutiva y técnica

