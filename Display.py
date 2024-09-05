
def viewport_transform(xw, yw, window, viewport):
    vx = (xw - window[0]) / (window[1] - window[0])
    vy = (yw - window[2]) / (window[3] - window[2])

    xv = viewport[0] + vx * (viewport[1] - viewport[0])
    yv = viewport[2] + vy * (viewport[3] - viewport[2])

    return xv, yv


# Função de Panning (Movimentação)
def pan(window, dx, dy):
    window[0] += dx #xmin
    window[1] += dx #xmax
    window[2] += dy #ymin
    window[3] += dy #ymax


def zoom(window, factor):
    cx = (window[0] + window[1]) / 2
    cy = (window[2] + window[3]) / 2

    width = (window[1] - window[0]) * factor
    height = (window[3] - window[2]) * factor

    window[0] = cx - width / 2
    window[1] = cx + width / 2
    window[2] = cy - height / 2
    window[3] = cy + height / 2

def parseCoordinates():

def draw_objects(canvas, display_file, window, viewport):
    canvas.delete("all")

    for obj in display_file:
        coordenadas =[]

        ##Cria oval
        if obj.obj_type == "point":
            x, y = obj.coordinates[0]
            xv, yv = viewport_transform(x, y, window, viewport)
            canvas.create_oval(xv - 2, yv - 2, xv + 2, yv + 2, fill="black")

        elif obj.obj_type == "line":
            x1, y1 = obj.coordinates[0]
            x2, y2 = obj.coordinates[1]
            xv1, yv1 = viewport_transform(x1, y1, window, viewport)
            xv2, yv2 = viewport_transform(x2, y2, window, viewport)
            canvas.create_line(xv1, yv1, xv2, yv2)

        elif obj.obj_type == "wireframe":
            for i in range(len(obj.coordinates) - 1):
                x1, y1 = obj.coordinates[i]
                x2, y2 = obj.coordinates[i + 1]
                xv1, yv1 = viewport_transform(x1, y1, window, viewport)
                xv2, yv2 = viewport_transform(x2, y2, window, viewport)
                canvas.create_line(xv1, yv1, xv2, yv2)

