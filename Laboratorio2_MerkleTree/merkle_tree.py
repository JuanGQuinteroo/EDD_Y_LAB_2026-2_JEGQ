# Laboratorio 2 - Arbol de Merkle
# La idea es simular como funciona un arbol de merkle usando SHA-256
# cada hoja es el hash de una transaccion, y vamos subiendo de a pares
# hasteando las combinaciones hasta llegar a un solo hash final (la raiz)

import hashlib


def hashear(texto):
    # convierte el texto a bytes porque hashlib lo necesita asi
    # y devuelve el hash en hexadecimal (mas facil de leer/comparar)
    return hashlib.sha256(texto.encode()).hexdigest()


def construir_arbol(transacciones):
    # el primer nivel son directamente los hashes de las transacciones (las hojas)
    nivel = [hashear(t) for t in transacciones]
    arbol = [nivel]

    # vamos combinando de a pares hasta que quede un solo hash (la raiz)
    while len(nivel) > 1:

        # si quedan impares, se duplica el ultimo para poder emparejar
        if len(nivel) % 2 == 1:
            nivel.append(nivel[-1])

        nivel_nuevo = []
        for i in range(0, len(nivel), 2):
            combinado = nivel[i] + nivel[i + 1]
            nivel_nuevo.append(hashear(combinado))

        arbol.append(nivel_nuevo)
        nivel = nivel_nuevo

    return arbol


def mostrar_arbol(arbol):
    for i, nivel in enumerate(arbol):
        if i == 0:
            print(f"\nNivel {i} (hojas):")
        elif i == len(arbol) - 1:
            print(f"\nNivel {i} (raiz):")
        else:
            print(f"\nNivel {i}:")

        for j, h in enumerate(nivel):
            print(f"  {j}: {h[:12]}...")  # solo mostramos un pedazo del hash


def generar_prueba(arbol, indice):
    # esto genera el camino de hashes "hermanos" que se necesitan
    # para poder reconstruir la raiz a partir de una sola hoja
    prueba = []
    idx = indice

    for nivel in arbol[:-1]:
        if idx % 2 == 0:
            hermano = nivel[idx + 1]
            posicion = "derecha"
        else:
            hermano = nivel[idx - 1]
            posicion = "izquierda"

        prueba.append((hermano, posicion))
        idx = idx // 2

    return prueba


def verificar(hash_hoja, prueba, raiz):
    actual = hash_hoja

    for hermano, posicion in prueba:
        if posicion == "derecha":
            actual = hashear(actual + hermano)
        else:
            actual = hashear(hermano + actual)

    return actual == raiz


# ---------------------------------------------------------
# Aca empieza el experimento que pide el enunciado
# ---------------------------------------------------------

transacciones = [
    "Juan le paga 10 a Carlos",
    "Carlos le paga 5 a David",
    "David le paga 20 a Estefania",
    "Estefania le paga 15 a Dahiana",
    "Dahiana le paga 8 a Juan",
]

print("Transacciones:")
for i, t in enumerate(transacciones):
    print(i, "-", t)

# construimos el arbol y sacamos la raiz
arbol = construir_arbol(transacciones)
raiz = arbol[-1][0]

print("\nAsi quedo el arbol:")
mostrar_arbol(arbol)

print("\nRaiz del arbol:", raiz)

# ---------------------------------------------------------
# ahora modificamos una transaccion para ver que la raiz cambia
# ---------------------------------------------------------

print("\n\n--- Probando que pasa si cambiamos una transaccion ---")

transacciones_mod = transacciones.copy()
transacciones_mod[2] = "David le paga 9999 a Estefania"  # cambiamos el monto

print("Cambiamos la transaccion 2 por:", transacciones_mod[2])

arbol_mod = construir_arbol(transacciones_mod)
raiz_mod = arbol_mod[-1][0]

print("\nRaiz original: ", raiz)
print("Raiz nueva:    ", raiz_mod)
print("Son iguales?", raiz == raiz_mod)
# obviamente da False, con eso se demuestra que cualquier cambio
# por chiquito que sea termina afectando toda la raiz

# ---------------------------------------------------------
# prueba de inclusion para la transaccion 3 (indice 2 en la lista)
# ---------------------------------------------------------

print("\n\n--- Prueba de inclusion para la transaccion 3 ---")

indice = 2  # la transaccion 3 (arrancando a contar desde 1) es el indice 2
hash_trans3 = hashear(transacciones[indice])

print("Transaccion 3:", transacciones[indice])
print("Su hash:", hash_trans3)

prueba = generar_prueba(arbol, indice)

print("\nHashes que se necesitan para la prueba:")
for h, pos in prueba:
    print(" -", pos, ":", h[:12], "...")

# verificacion con el dato correcto
print("\nVerificando con el dato correcto...")
resultado = verificar(hash_trans3, prueba, raiz)
print("Resultado:", "VALIDO" if resultado else "NO VALIDO")

# verificacion con un dato que no es el correcto (para que falle)
print("\nAhora verificando con un dato que inventamos (deberia fallar)...")
hash_falso = hashear("David le paga 500000 a Estefania")
resultado_falso = verificar(hash_falso, prueba, raiz)
print("Resultado:", "VALIDO" if resultado_falso else "NO VALIDO")