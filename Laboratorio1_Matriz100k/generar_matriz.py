"""
Genera una matriz binaria de 100.000 x 100.000 y la escribe en disco.

Problemas que resuelve:
1. Consumo excesivo de RAM:
   - Nunca se crea la matriz completa en memoria (eso requeriría ~10 GB
     usando 1 byte por valor, o ~80 GB con float64).
   - Se procesa por bloques (chunks) de filas. Cada bloque se genera,
     se escribe a disco y se descarta antes de crear el siguiente.
   - Pico de RAM real: ~ chunk_rows * N bytes (aprox. 100-200 MB),
     sin importar que la matriz lógica tenga 10.000 millones de valores.

2. Escritura lenta a disco:
   - Se escribe en bloques grandes (binario puro, f.write(bytes)),
     no valor por valor ni en formato de texto (CSV sería ~7x más
     pesado y mucho más lento de parsear/escribir).
   - Pocas llamadas de escritura (50 en total) en vez de millones.

3. Optimización de almacenamiento:
   - Cada valor es 0 o 1, empaquetado con np.packbits: 8 valores
     lógicos comparten 1 byte físico real en disco.
   - Tamaño final: 100.000 x 100.000 bits / 8 = ~1.25 GB,
     en vez de los 10 GB (int8) u 80 GB (float64) que tomaría
     un enfoque ingenuo.
"""

import numpy as np
import time

N = 100_000
filename = "matriz.bin"
chunk_rows = 1000  # filas procesadas por iteración (controla el uso de RAM)

inicio = time.time()

with open(filename, "wb") as f:
    for i in range(0, N, chunk_rows):
        rows = min(chunk_rows, N - i)

        # Genera SOLO este bloque en memoria (no la matriz completa)
        bloque = np.random.randint(0, 2, size=(rows, N), dtype=np.uint8)

        # Empaqueta 8 valores binarios en 1 byte real -> reduce el
        # tamaño escrito a disco en un factor de 8
        empaquetado = np.packbits(bloque, axis=1)

        # Una sola escritura binaria grande por bloque (rápido, pocas
        # llamadas al sistema de archivos)
        f.write(empaquetado.tobytes())

        # 'bloque' y 'empaquetado' se liberan automáticamente al
        # terminar la iteración -> RAM no se acumula

        if i % 10000 == 0:
            print(f"Progreso: {i + rows}/{N} filas", flush=True)

fin = time.time()

tamano_bytes = N * N // 8
print(f"\nListo. Tiempo total: {fin - inicio:.2f} segundos")
print(f"Tamaño real en disco: {tamano_bytes / 1e9:.2f} GB")
print(f"RAM pico aproximada usada por bloque: "
      f"{(chunk_rows * N) / 1e6:.1f} MB")