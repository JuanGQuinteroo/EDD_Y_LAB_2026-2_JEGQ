import numpy as np

N = 100_000
filename = "matriz.bin"

bytes_por_fila = (N + 7) // 8  # bytes que ocupa cada fila empaquetada

with open(filename, "rb") as f:
    f.seek(0)
    datos = np.frombuffer(f.read(bytes_por_fila * 10), dtype=np.uint8)
    filas = datos.reshape(10, bytes_por_fila)
    desempaquetado = np.unpackbits(filas, axis=1)

print("Shape lógico:", (N, N))
print("Tamaño real en disco (bytes):", N*N // 8)
print("Muestra 10x10 (desempaquetada):")
print(desempaquetado[:10, :10])