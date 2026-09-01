import numpy as np

N = 100_000
filename = "matriz.bin"

# Generar y empaquetar por bloques (chunks) para no saturar RAM
with open(filename, "wb") as f:
    chunk_rows = 2000
    for i in range(0, N, chunk_rows):
        rows = min(chunk_rows, N - i)
        bloque = np.random.randint(0, 2, size=(rows, N), dtype=np.uint8)
        empaquetado = np.packbits(bloque, axis=1)
        f.write(empaquetado.tobytes())
        print(f"Progreso: {i+rows}/{N} filas", flush=True)

print("Listo. Tamaño real en disco: ~", (N*N)//8/1e9, "GB")

#Como hace para distinguir de una fila y la otra
#Donde esta definido el tamaño fijo de la fila