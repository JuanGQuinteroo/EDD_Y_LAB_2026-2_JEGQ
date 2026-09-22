# busqueda en lista normal, tiene que recorrer todo hasta encontrar

def buscar_en_lista(lista, id_buscado):
    for est in lista:
        if est["id"] == id_buscado:
            return est
    return None

def listar_en_orden_lista(lista):
    return sorted(lista, key=lambda x: x["id"])