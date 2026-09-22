# arbol B+ simplificado, cada hoja puede tener varias claves
# cuando se llena se divide para mantenerse balanceado

ORDEN = 4

class NodoHoja:
    def __init__(self):
        self.claves = []
        self.datos = []
        self.siguiente = None

class NodoInterno:
    def __init__(self):
        self.claves = []
        self.hijos = []


class ArbolBMas:
    def __init__(self):
        self.raiz = NodoHoja()

    def buscar(self, id_buscado):
        nodo = self.raiz
        while isinstance(nodo, NodoInterno):
            i = 0
            while i < len(nodo.claves) and id_buscado >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]

        if id_buscado in nodo.claves:
            pos = nodo.claves.index(id_buscado)
            return nodo.datos[pos]
        return None

    def insertar(self, id_est, nombre, edad, promedio):
        camino = []
        nodo = self.raiz

        while isinstance(nodo, NodoInterno):
            camino.append(nodo)
            i = 0
            while i < len(nodo.claves) and id_est >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]

        pos = 0
        while pos < len(nodo.claves) and nodo.claves[pos] < id_est:
            pos += 1

        nodo.claves.insert(pos, id_est)
        nodo.datos.insert(pos, {"id": id_est, "nombre": nombre, "edad": edad, "promedio": promedio})

        if len(nodo.claves) >= ORDEN:
            self._dividir_hoja(nodo, camino)

    def _dividir_hoja(self, hoja, camino):
        mitad = len(hoja.claves) // 2

        nueva = NodoHoja()
        nueva.claves = hoja.claves[mitad:]
        nueva.datos = hoja.datos[mitad:]

        hoja.claves = hoja.claves[:mitad]
        hoja.datos = hoja.datos[:mitad]

        nueva.siguiente = hoja.siguiente
        hoja.siguiente = nueva

        self._insertar_en_padre(hoja, nueva.claves[0], nueva, camino)

    def _insertar_en_padre(self, izq, clave, der, camino):
        if not camino:
            nueva_raiz = NodoInterno()
            nueva_raiz.claves = [clave]
            nueva_raiz.hijos = [izq, der]
            self.raiz = nueva_raiz
            return

        padre = camino.pop()
        pos = padre.hijos.index(izq)
        padre.claves.insert(pos, clave)
        padre.hijos.insert(pos + 1, der)

        if len(padre.claves) >= ORDEN:
            self._dividir_interno(padre, camino)

    def _dividir_interno(self, nodo, camino):
        mitad = len(nodo.claves) // 2
        clave_sube = nodo.claves[mitad]

        nuevo = NodoInterno()
        nuevo.claves = nodo.claves[mitad + 1:]
        nuevo.hijos = nodo.hijos[mitad + 1:]

        nodo.claves = nodo.claves[:mitad]
        nodo.hijos = nodo.hijos[:mitad + 1]

        self._insertar_en_padre(nodo, clave_sube, nuevo, camino)

    def listar_en_orden(self):
        nodo = self.raiz
        while isinstance(nodo, NodoInterno):
            nodo = nodo.hijos[0]

        resultado = []
        while nodo:
            resultado.extend(nodo.datos)
            nodo = nodo.siguiente
        return resultado

    def buscar_por_rango(self, desde, hasta):
        # ventaja del B+: las hojas estan conectadas, entonces
        # se puede recorrer el rango sin volver a bajar del arbol
        nodo = self.raiz
        while isinstance(nodo, NodoInterno):
            i = 0
            while i < len(nodo.claves) and desde >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]

        resultado = []
        while nodo:
            for i, clave in enumerate(nodo.claves):
                if desde <= clave <= hasta:
                    resultado.append(nodo.datos[i])
                elif clave > hasta:
                    return resultado
            nodo = nodo.siguiente
        return resultado