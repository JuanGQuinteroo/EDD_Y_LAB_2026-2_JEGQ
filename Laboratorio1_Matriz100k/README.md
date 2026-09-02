# Laboratorio 1 - Matriz 100.000 x 100.000 en disco

**Juan Esteban Gil Quintero** 

## Objetivo
Escribir una matriz de 100.000 x 100.000 en disco duro resolviendo
los problemas de consumo excesivo de RAM, escritura lenta a disco,
y optimización de almacenamiento/lectura.

## Enfoque de la solución
- **Matriz binaria empaquetada:** cada valor lógico es 0 o 1. Se
  empaquetan 8 valores por byte físico (`np.packbits`), reduciendo
  el tamaño en disco de ~10 GB (1 byte/valor) a ~1.25 GB.
- **Procesamiento por bloques (chunking):** la matriz nunca existe
  completa en memoria. Se genera y escribe en bloques de 1000 filas,
  manteniendo el uso de RAM en ~100-200 MB constantes, sin importar
  el tamaño total de la matriz.
- **Escritura binaria secuencial:** se usan pocas escrituras grandes
  en vez de millones de escrituras pequeñas, acelerando el proceso.
- **Lectura optimizada con memmap:** la verificación usa
  `np.memmap`, que accede a partes específicas del archivo sin
  cargarlo completo a RAM.

  ## Estructura del archivo y acceso eficiente

### Header autodescriptivo
El archivo `matriz.bin` no es un bloque de bytes sin contexto: comienza
con un **header de 12 bytes** que contiene:
- 4 bytes: identificador de formato (`MTX1`)
- 4 bytes: número de filas (uint32)
- 4 bytes: número de columnas (uint32)

Esto hace que el archivo sea autodescriptivo — cualquier programa puede
leer sus dimensiones directamente desde el header, sin depender de
información externa ni de que el código que lo generó esté disponible.

### Por qué no se usan marcadores de fin de fila
Se evaluó usar marcadores de fin de fila, pero se descartaron porque
son útiles solo cuando las filas tienen **tamaño variable** (ej. texto).
En esta matriz, **todas las filas ocupan exactamente el mismo tamaño**
(12.500 bytes, ya que 100.000 bits / 8 = 12.500 bytes por fila empaquetada).

Esto permite calcular la posición de cualquier fila con una fórmula
directa, sin necesidad de escanear el archivo:

posicion_fila(i) = tamano_header + i * bytes_por_fila

Agregar marcadores sería contraproducente: obligaría a leer
secuencialmente para encontrarlos, exactamente lo que se busca evitar.

### Acceso a una fila (O(1), sin cargar el archivo completo)
Gracias a la fórmula anterior, leer cualquier fila requiere una sola
lectura de 12.500 bytes desde disco (usando `np.memmap`), sin importar
en qué parte del archivo esté ni cuál sea el tamaño total del archivo.

### Acceso a una columna (con trade-off honesto)
El archivo se almacena "por filas" (row-major), por lo que leer una
columna completa requiere tocar 1 byte de cada una de las 100.000 filas.
Aun así, esto **nunca carga el archivo completo a RAM**: solo se traen
a memoria ~100 KB (un byte por fila), en vez de los 1.25 GB totales.

| Operación         | Bytes leídos a RAM | % del archivo completo |
|-------------------|--------------------:|------------------------:|
| Leer 1 fila        | 12.500 bytes (~12 KB) | 0.001% |
| Leer 1 columna      | 100.000 bytes (~100 KB) | 0.008% |
| Cargar todo el archivo | 1.250.000.000 bytes (1.25 GB) | 100% |

Esto demuestra que ninguna operación de búsqueda requiere cargar el
documento completo en memoria, cumpliendo con el objetivo de acceso
eficiente a datos individuales dentro de una matriz de gran escala.

## Archivos
- `generar_matriz.py`: genera la matriz y la escribe en disco por
  bloques. Documentado explicando cómo resuelve cada problema.
- `verificar_matriz.py`: verifica tamaño del archivo y muestra
  contenido real en distintas zonas (inicio, medio, final) usando
  acceso optimizado por memmap.
- `evidencia/output.txt`: salida de consola de ambas ejecuciones.

## Cómo ejecutar
\`\`\`bash
pip install numpy
python generar_matriz.py
python verificar_matriz.py
\`\`\`

## Resultados
- Tamaño lógico: 100.000 x 100.000 = 10.000.000.000 valores
- Tamaño real en disco: ~1.25 GB
- Tiempo de generación: ver evidencia/output.txt
- RAM pico usada: ~100-200 MB (nunca la matriz completa)

Nota: `matriz.bin` no se incluye en el repositorio por su tamaño;
se genera localmente ejecutando `generar_matriz.py`.