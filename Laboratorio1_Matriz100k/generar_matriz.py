import numpy as np
import struct
import time

N = 100_000
filename = "matriz.bin"
chunk_rows = 1000

MAGIC = b"MTX1"  # identificador del formato de archivo

def escribir_header(f, n_filas, n_columnas):
    """
    Escribe un header al inicio del archivo con la estructura de la matriz.
    Esto convierte el archivo de un simple 'vector de bytes' en un formato
    autodescriptivo: cualquier programa que lo abra conoce sus dimensiones
    sin depender de información externa.
    Formato: 4 bytes magic + 4 bytes filas (uint32) + 4 bytes columnas (uint32)
    """
    header = struct.pack("<4sII", MAGIC, n_filas, n_columnas)
    f.write(header)
    return len(header)

inicio = time.time()

with open(filename, "wb") as f:
    header_size = escribir_header(f, N, N)

    for i in range(0, N, chunk_rows):
        rows = min(chunk_rows, N - i)
        bloque = np.random.randint(0, 2, size=(rows, N), dtype=np.uint8)
        empaquetado = np.packbits(bloque, axis=1)
        f.write(empaquetado.tobytes())
        if i % 10000 == 0:
            print(f"Progreso: {i + rows}/{N} filas", flush=True)

fin = time.time()
tamano_bytes = header_size + (N * N // 8)
print(f"\nListo. Tiempo total: {fin - inicio:.2f} s")
print(f"Header: {header_size} bytes")
print(f"Tamaño real en disco: {tamano_bytes/1e9:.3f} GB")