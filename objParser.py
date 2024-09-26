def write_obj(filename, graphic_objects):
    with open(filename, 'w') as file:
        for obj in graphic_objects:
            # Escrever os vértices (coordinates)
            for coord in obj.coordinates:
                file.write(f"v {coord[0]} {coord[1]} 0.0\n")

            if obj.obj_type == "point":
                file.write(f"p {len(obj.coordinates)}\n")
            elif obj.obj_type == "line":
                indices = ' '.join([str(i + 1) for i in range(len(obj.coordinates))])
                file.write(f"l {indices}\n")
            elif obj.obj_type == "wireframe":
                indices = ' '.join([str(i + 1) for i in range(len(obj.coordinates))])
                file.write(f"f {indices}\n")


def read_obj(filename):
    graphic_objects = []
    vertices = []

    with open(filename, 'r') as file:
        current_obj = None

        for line in file:
            if line.startswith('v '):  # Processar vértices
                _, x, y, _ = line.strip().split()
                vertices.append((float(x), float(y)))

            elif line.startswith('p '):  # Processar ponto
                _, index = line.strip().split()
                coord = [vertices[int(index) - 1]]
                graphic_objects.append(GraphicObject("point", "point", coord, cor=None))

            elif line.startswith('l '):  # Processar linha
                indices = line.strip().split()[1:]
                coord = [vertices[int(i) - 1] for i in indices]
                graphic_objects.append(GraphicObject("line", "line", coord, cor=None))

            elif line.startswith('f '):  # Processar wireframe (polígono)
                indices = line.strip().split()[1:]
                coord = [vertices[int(i) - 1] for i in indices]
                graphic_objects.append(GraphicObject("wireframe", "wireframe", coord, cor=None))

    return graphic_objects

