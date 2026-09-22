class NodoABB:
    def __init__(self, id_est, nombre, edad, promedio):
        self.id = id_est
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio
        self.izq = None
        self.der = None


class ArbolABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, id_est, nombre, edad, promedio):
        nodo = NodoABB(id_est, nombre, edad, promedio)

        if self.raiz is None:
            self.raiz = nodo
            return

        actual = self.raiz
        while True:
            if id_est < actual.id:
                if actual.izq is None:
                    actual.izq = nodo
                    return
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nodo
                    return
                actual = actual.der

    def buscar(self, id_buscado):
        actual = self.raiz
        while actual:
            if id_buscado == actual.id:
                return actual
            elif id_buscado < actual.id:
                actual = actual.izq
            else:
                actual = actual.der
        return None

    def listar_en_orden(self):
        # uso una pila porque si inserto en orden el arbol queda muy
        # profundo y la recursion normal se rompe
        resultado = []
        pila = []
        actual = self.raiz

        while actual or pila:
            while actual:
                pila.append(actual)
                actual = actual.izq
            actual = pila.pop()
            resultado.append({"id": actual.id, "nombre": actual.nombre, "edad": actual.edad, "promedio": actual.promedio})
            actual = actual.der

        return resultado