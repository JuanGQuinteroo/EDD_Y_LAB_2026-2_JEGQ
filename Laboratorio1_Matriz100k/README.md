# Laboratorio 1 - Matriz 100.000x100.000 en disco

## Enunciado
Escribir una matriz de 100.000x100.000 en disco duro y mostrarla.

## Enfoque
Matriz binaria (valores 0/1) con bits empaquetados (`np.packbits`),
escrita por bloques con streaming a disco para no saturar la RAM.
Cada uno de los 10.000 millones de valores está físicamente presente
en disco, codificado 8 valores por byte.

- Tamaño lógico: 100.000 x 100.000 = 10.000.000.000 elementos
- Tamaño real en disco: ~1.25 GB (10.000.000.000 bits / 8)

## Archivos
- `generar_matriz.py`: crea el archivo binario en disco
- `mostrar_matriz.py`: lee y muestra una muestra de la matriz + metadata
- `evidencia/output.txt`: salida de consola de la ejecución

## Cómo correrlo
\`\`\`bash
pip install numpy
python generar_matriz.py
python mostrar_matriz.py
\`\`\`

Nota: el archivo `matriz.bin` generado no se incluye en el repo por su
tamaño (~1.25 GB).