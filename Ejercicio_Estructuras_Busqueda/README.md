# Ejercicio - Sistema de busqueda de estudiantes

**Juan Esteban Gil Quintero**

## De que se trata

Se pidio comparar 3 formas distintas de guardar y buscar datos:
una lista normal, un Arbol Binario de Busqueda (ABB) y un Arbol B+.
La idea es tener 10,000 estudiantes y ver que tan rapido puede cada
estructura buscar uno por su id, ademas de poder insertar nuevos y
listar todo ordenado.

## Archivos

- `generar_datos.py`: Crea los 10,000 estudiantes con datos aleatorios (id, nombre, edad, promedio)
- `lista.py`: Busqueda y listado usando una lista comun de python
- `abb.py`: El arbol binario de busqueda
- `arbol_b_mas.py`: El arbol B+ (mas complejo, pero se mantiene balanceado solo)
- `main.py`: Aca se corre todo el experimento y se comparan los tiempos

## Como funciona cada uno

**Lista:** Para buscar un id tiene que ir mirando uno por uno hasta
encontrarlo (o hasta terminar la lista si no esta). Es la mas simple
pero tambien la mas lenta con muchos datos.

**ABB:** Cada nodo tiene un hijo izquierdo (ids menores) y uno derecho
(ids mayores), entonces al buscar se puede saltar la mitad del arbol
en cada paso. El problema es que si se inserta los ids ya ordenados
(1, 2, 3...) el arbol no se acomoda para ningun lado y termina siendo
una fila larga, practicamente igual de lento que la lista.

**B+:** Parecido al ABB pero cada nodo aguanta varias claves, y cuando
se llena se divide solo para mantenerse parejo. No importa en que
orden inserte, siempre queda balanceado. Ademas las hojas estan
conectadas entre si, lo que lo hace muy bueno buscando rangos
(por ejemplo "todos los estudiantes con id entre 100 y 105").

## Resultados

Se hicieron 100 busquedas aleatorias sobre 10,000 estudiantes,
promediando 10 corridas para que el tiempo sea mas estable.

**Insertando los ids en orden (1, 2, 3...):**

Lista: 0.0105 s
ABB: 0.0160 s
B+: 0.0001 s

Aca el ABB sale igual de lento o hasta peor que la lista. Esto pasa
porque al insertar en orden, cada nuevo id es mas grande que el
anterior, entonces siempre se va para la derecha y el arbol termina
pareciendo una lista enlazada, no un arbol balanceado.

**Insertando los ids desordenados:**

Lista: 0.0226 s
ABB: 0.0001 s
B+: 0.0001 s

Aca si se nota la diferencia. El ABB mejora un monton porque al
insertar en desorden el arbol queda mas equilibrado entre izquierda
y derecha, entonces cada busqueda descarta como la mitad de los
nodos en cada paso. El B+ se mantiene igual de rapido en los dos
casos, porque no depende del orden de insercion.

## Extra: busqueda por rango

Se agrego una funcion para buscar por rango de ids en el arbol B+,
que es la ventaja que tiene sobre el ABB (ademas de que no se
desbalancea). Se probo buscando los estudiantes con id entre 100 y 105:

{'id': 100, 'nombre': 'Andres', 'edad': 20, 'promedio': 8.1}
{'id': 101, 'nombre': 'Maria', 'edad': 23, 'promedio': 2.3}
{'id': 102, 'nombre': 'Diego', 'edad': 25, 'promedio': 7.2}
{'id': 103, 'nombre': 'Andres', 'edad': 24, 'promedio': 6.2}
{'id': 104, 'nombre': 'Juan', 'edad': 23, 'promedio': 3.6}
{'id': 105, 'nombre': 'Ana', 'edad': 18, 'promedio': 9.5}


## Como correrlo

python main.py