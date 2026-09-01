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