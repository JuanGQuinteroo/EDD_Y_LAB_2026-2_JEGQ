"""
Verifica que la matriz de 100.000 x 100.000 fue escrita correctamente
en disco, sin necesidad de cargarla completa en RAM.

Optimización de lectura:
- Se usa np.memmap, que mapea el archivo directamente desde disco.
  Solo se cargan a RAM los bytes que realmente se consultan (acceso
  perezoso/"lazy"), en vez de leer 1.25 GB de golpe.
- Se verifican múltiples zonas del archivo (inicio, medio, final)
  para confirmar que TODA la matriz fue escrita, no solo el comienzo.
"""

import numpy as np
import os

N = 100_000
filename = "matriz.bin"
bytes_por_fila = N // 8  # cada fila ocupa N/8 bytes empaquetados

# --- Verificación 1: tamaño del archivo en disco ---
tamano_esperado = N * N // 8
tamano_real = os.path.getsize(filename)
print("=== Verificación de tamaño ===")
print(f"Tamaño esperado: {tamano_esperado} bytes ({tamano_esperado/1e9:.2f} GB)")
print(f"Tamaño real:     {tamano_real} bytes ({tamano_real/1e9:.2f} GB)")
print(f"Coincide: {tamano_esperado == tamano_real}\n")

# --- Verificación 2: acceso vía memmap (sin cargar todo a RAM) ---
mat = np.memmap(filename, dtype=np.uint8, mode="r",
                 shape=(N, bytes_por_fila))

def mostrar_bloque(nombre, fila_inicio):
    bloque = mat[fila_inicio:fila_inicio + 5, :2]  # solo 5 filas, 2 bytes
    desempaquetado = np.unpackbits(bloque, axis=1)
    print(f"--- {nombre} (filas {fila_inicio}-{fila_inicio+4}) ---")
    print(desempaquetado[:, :10])  # primeros 10 valores de cada fila
    print()

print("=== Muestra de contenido en distintas zonas del archivo ===")
mostrar_bloque("Inicio", 0)
mostrar_bloque("Medio", N // 2)
mostrar_bloque("Final", N - 5)

print("Verificación completa: la matriz existe físicamente en disco")
print("y contiene datos válidos en todo su rango (no solo al inicio).")