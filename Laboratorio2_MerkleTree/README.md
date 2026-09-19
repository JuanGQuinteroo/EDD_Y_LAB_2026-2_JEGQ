# Laboratorio 2 - Arbol de Merkle

**Juan Esteban Gil Quintero**

## De que se trata

Este lab consiste en implementar un Arbol de Merkle, que es la estructura
que se usa en blockchain (y en Git tambien) para poder verificar que un
dato pertenece a un conjunto grande sin tener que revisar todo el conjunto.

La idea basica es:
- Cada transaccion se hashea (SHA-256) y eso queda como una hoja del arbol
- Se van combinando las hojas de a pares, hasteando la concatenacion de
  cada par, hasta que queda un solo hash: la raiz (Merkle Root)
- Si el numero de elementos en algun nivel es impar, se duplica el ultimo
  para poder seguir emparejando
- Cualquier cambio en una transaccion, por minimo que sea, termina
  cambiando la raiz completa

## Archivos que hay en esta carpeta

- `merkle_tree.py`: el codigo con todo. Construye el arbol, muestra la
  raiz, prueba que si se cambia una transaccion la raiz cambia, y genera
  una prueba de inclusion para verificar si un dato pertenece al arbol
  (probando tanto con un dato correcto como con uno inventado).
- `evidencia/`: capturas de pantalla de las verificaciones corriendo
- `diagrama.txt`: el arbol dibujado en ASCII

## Como funciona el codigo (rapido)

1. Se crean 5 transacciones de ejemplo (tipo "Juan le paga 10 a Carlos")
2. Se construye el arbol nivel por nivel hasta llegar a la raiz
3. Se cambia una transaccion a proposito y se muestra que la raiz nueva
   es completamente distinta a la original
4. Se genera la "prueba de inclusion" de la transaccion 3, que es
   basicamente los hashes hermanos que se necesitan para reconstruir
   el camino hasta la raiz sin tener que usar el arbol completo
5. Se verifica esa prueba dos veces: una con el hash real de la
   transaccion (deberia dar valido) y otra con un hash inventado
   (deberia fallar)

## Resultados

Raiz original del arbol con las 5 transacciones:

6813176ac2df015d74b1131839b6ecae132734a0852a950a2f36d2e21ac416f1

Al cambiar la transaccion 2 (David le paga 20 -> 9999 a Estefania), la
raiz cambia completamente:

544f227614226a4aec54f2b3a6e01b3a49e46028b45fc731ad30671c6101bfaa

Verificacion de la transaccion 3 con su hash real -> VALIDO
Verificacion con un dato inventado -> NO VALIDO

(ver capturas en la carpeta evidencia/)

## Como correrlo

python merkle_tree.py