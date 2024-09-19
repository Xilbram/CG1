class GraphicObject:
    def __init__(self, name, obj_type, coordinates,cor):
        self.name = name #isso aq é um index pra remover
        self.obj_type = obj_type  # "point", "line", "wireframe"
        self.coordinates = coordinates  # Lista de coordenadas [(x1, y1), (x2, y2), ...]
        self.cor = cor

