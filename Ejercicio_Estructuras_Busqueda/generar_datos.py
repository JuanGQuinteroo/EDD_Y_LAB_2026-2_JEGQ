import random

nombres = ["Ana", "Carlos", "Maria", "Juan", "Laura", "Pedro", "Sofia", "Diego", "Valentina", "Andres"]

def generar_estudiantes(cantidad):
    estudiantes = []
    for i in range(1, cantidad + 1):
        est = {
            "id": i,
            "nombre": random.choice(nombres),
            "edad": random.randint(17, 25),
            "promedio": round(random.uniform(1.0, 10.0), 1)
        }
        estudiantes.append(est)
    return estudiantes