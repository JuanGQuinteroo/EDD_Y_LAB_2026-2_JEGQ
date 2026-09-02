import numpy as np
import struct
import os

filename = "matriz.bin"
MAGIC = b"MTX1"

def leer_header(filename):
    with open(filename, "rb") as f:
        raw = f.read(12)
        magic, n_filas, n_columnas = struct.unpack("<4sII", raw)
        assert magic == MAGIC, "Formato de archivo no reconocido"
        return n_filas, n_columnas, 12

N, M, HEADER_SIZE = leer_header(filename)
bytes_por_fila = M // 8

print("=== Estructura del archivo (leída del header) ===")
print(f"Filas: {N}, Columnas: {M}, Header: {HEADER_SIZE} bytes\n")

# memmap: mapea el archivo, NO lo carga a RAM. Los bytes se leen
# desde disco bajo demanda, solo cuando se acceden.
mm = np.memmap(filename, dtype=np.uint8, mode="r")

def leer_fila(i):
    """
    Lee UNA sola fila sin tocar el resto del archivo.
    Acceso O(1): la posición se calcula matemáticamente,
    no se necesita escanear porque todas las filas miden lo mismo.
    """
    inicio = HEADER_SIZE + i * bytes_por_fila
    fin = inicio + bytes_por_fila
    fila_bytes = mm[inicio:fin]        # solo 12.500 bytes leídos
    return np.unpackbits(fila_bytes)

def leer_columna(j):
    """
    Lee UNA sola columna sin cargar el archivo completo.
    Como el formato es por filas, se toca 1 byte de cada fila
    (N accesos), pero solo se traen a RAM ~100 KB, nunca 1.25 GB.
    """
    byte_idx = j // 8
    bit_idx = j % 8
    posiciones = HEADER_SIZE + byte_idx + np.arange(N) * bytes_por_fila
    bytes_columna = mm[posiciones]     # solo N bytes (~100 KB) a RAM
    return (bytes_columna >> (7 - bit_idx)) & 1

# --- Demostración ---
print("=== Fila 50.000, primeros 20 valores ===")
print(leer_fila(50_000)[:20])

print("\n=== Columna 50.000, primeros 20 valores ===")
print(leer_columna(50_000)[:20])

print("\n=== Comparación de RAM usada por operación ===")
print(f"leer_fila():    {bytes_por_fila} bytes ({bytes_por_fila/1024:.1f} KB)")
print(f"leer_columna(): {N} bytes ({N/1024:.1f} KB)")
print(f"Tamaño total del archivo: {os.path.getsize(filename)/1e9:.2f} GB")
print("=> Ninguna operación cargó el archivo completo a RAM.")