import random
import time

from generar_datos import generar_estudiantes
from lista import buscar_en_lista, listar_en_orden_lista
from abb import ArbolABB
from arbol_b_mas import ArbolBMas


def medir_tiempo(funcion_buscar, estructura, ids, repeticiones=10):
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        for id_est in ids:
            funcion_buscar(estructura, id_est)
        tiempos.append(time.perf_counter() - inicio)
    return sum(tiempos) / len(tiempos)


def construir_abb(estudiantes):
    arbol = ArbolABB()
    for e in estudiantes:
        arbol.insertar(e["id"], e["nombre"], e["edad"], e["promedio"])
    return arbol


def construir_bmas(estudiantes):
    arbol = ArbolBMas()
    for e in estudiantes:
        arbol.insertar(e["id"], e["nombre"], e["edad"], e["promedio"])
    return arbol


CANTIDAD = 10000

estudiantes = generar_estudiantes(CANTIDAD)
print("Ejemplo de estudiante:", estudiantes[0])

en_orden = estudiantes
desordenados = estudiantes.copy()
random.shuffle(desordenados)

ids_a_buscar = random.sample(range(1, CANTIDAD + 1), 100)

print("\n--- Insertando en orden ---")

lista1 = list(en_orden)
abb1 = construir_abb(en_orden)
bmas1 = construir_bmas(en_orden)

t_lista = medir_tiempo(buscar_en_lista, lista1, ids_a_buscar)
t_abb = medir_tiempo(lambda arbol, id: arbol.buscar(id), abb1, ids_a_buscar)
t_bmas = medir_tiempo(lambda arbol, id: arbol.buscar(id), bmas1, ids_a_buscar)

print("Lista:", round(t_lista, 4), "s")
print("ABB:  ", round(t_abb, 4), "s")
print("B+:   ", round(t_bmas, 4), "s")

print("\n--- Insertando aleatorio ---")

lista2 = list(desordenados)
abb2 = construir_abb(desordenados)
bmas2 = construir_bmas(desordenados)

t_lista2 = medir_tiempo(buscar_en_lista, lista2, ids_a_buscar)
t_abb2 = medir_tiempo(lambda arbol, id: arbol.buscar(id), abb2, ids_a_buscar)
t_bmas2 = medir_tiempo(lambda arbol, id: arbol.buscar(id), bmas2, ids_a_buscar)

print("Lista:", round(t_lista2, 4), "s")
print("ABB:  ", round(t_abb2, 4), "s")
print("B+:   ", round(t_bmas2, 4), "s")

print("\n--- Listar en orden (primeros 3 ids) ---")
print("Lista:", [e["id"] for e in listar_en_orden_lista(lista2)[:3]])
print("ABB:  ", [e["id"] for e in abb2.listar_en_orden()[:3]])
print("B+:   ", [e["id"] for e in bmas2.listar_en_orden()[:3]])

print("\n--- Extra: busqueda por rango en el B+ (ids 100 a 105) ---")
for est in bmas2.buscar_por_rango(100, 105):
    print(est)