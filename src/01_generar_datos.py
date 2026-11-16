import sqlite3
import pandas as pd
import os

# Asegurar que existan las carpetas
os.makedirs('data/raw', exist_ok=True)
os.makedirs('database', exist_ok=True)

# 1. Crear Base de Datos SQL (Simula el ERP / Libro Mayor Interno)
conn = sqlite3.connect('database/contabilidad.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS libro_mayor (
    id_asiento TEXT PRIMARY KEY,
    fecha TEXT,
    glosa TEXT,
    cuenta_contable TEXT,
    monto REAL
)
''')

# Limpiar tabla si ya existía
cursor.execute('DELETE FROM libro_mayor')

# Insertar registros contables internos (en pesos chilenos o moneda local)
registros_erp = [
    ('AS-001', '2026-10-01', 'Pago Factura Proveedor A', '110101-Banco', -1500000),
    ('AS-002', '2026-10-02', 'Ingreso Venta Cliente X', '110101-Banco', 3200000),
    ('AS-003', '2026-10-03', 'Pago Arriendo Oficina', '110101-Banco', -850000),
    ('AS-004', '2026-10-05', 'Pago Servicios Básicos', '110101-Banco', -120500), # Diferencia de monto con el banco
    ('AS-005', '2026-10-06', 'Transferencia Cliente Y', '110101-Banco', 950000),
    ('AS-006', '2026-10-07', 'Cheque girado no cobrado', '110101-Banco', -400000) # Está en ERP, no en Banco
]

cursor.executemany('INSERT INTO libro_mayor VALUES (?, ?, ?, ?, ?)', registros_erp)
conn.commit()
conn.close()

# 2. Crear Archivo CSV/Excel (Simula la Cartola Bancaria descargada del banco)
cartola_banco = [
    {'id_trx_banco': 'TRX-901', 'fecha': '2026-10-01', 'descripcion': 'TEF PROV A', 'monto': -1500000},
    {'id_trx_banco': 'TRX-902', 'fecha': '2026-10-02', 'descripcion': 'ABONO CLIENTE X', 'monto': 3200000},
    {'id_trx_banco': 'TRX-903', 'fecha': '2026-10-03', 'descripcion': 'PAGO ARRIENDO', 'monto': -850000},
    {'id_trx_banco': 'TRX-904', 'fecha': '2026-10-05', 'descripcion': 'CARGO SERVICIOS', 'monto': -125000}, # Error: en ERP dice -120500
    {'id_trx_banco': 'TRX-905', 'fecha': '2026-10-06', 'descripcion': 'TEF CLIENTE Y', 'monto': 950000},
    {'id_trx_banco': 'TRX-906', 'fecha': '2026-10-08', 'descripcion': 'COMISION MANTENCION CTA', 'monto': -15900} # Cargo bancario no contabilizado
]

df_banco = pd.DataFrame(cartola_banco)
df_banco.to_csv('data/raw/cartola_banco_oct2026.csv', index=False)

print("✅ Entorno inicializado: Base de datos SQLite y Cartola Bancaria creadas con éxito.")