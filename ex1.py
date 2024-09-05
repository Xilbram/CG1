import tkinter
import tkinter as tk
from tkinter import Toplevel, Entry
from typing import List, Tuple



class GraphicObject:
    def __init__(self, name, obj_type, coordinates):
        self.name = name
        self.obj_type = obj_type  # "point", "line", "wireframe"
        self.coordinates = coordinates  # Lista de coordenadas [(x1, y1), (x2, y2), ...]


# Funções de Transformação de Viewport
def viewport_transform(xw, yw, window, viewport):
    vx = (xw - window['xmin']) / (window['xmax'] - window['xmin'])
    vy = (yw - window['ymin']) / (window['ymax'] - window['ymin'])

    xv = viewport['xmin'] + vx * (viewport['xmax'] - viewport['xmin'])
    yv = viewport['ymin'] + vy * (viewport['ymax'] - viewport['ymin'])

    return xv, yv


# Função de Panning (Movimentação)
def pan(window, dx, dy):
    window['xmin'] += dx
    window['xmax'] += dx
    window['ymin'] += dy
    window['ymax'] += dy


# Função de Zooming
def zoom(window, factor):
    cx = (window['xmin'] + window['xmax']) / 2
    cy = (window['ymin'] + window['ymax']) / 2

    width = (window['xmax'] - window['xmin']) * factor
    height = (window['ymax'] - window['ymin']) * factor

    window['xmin'] = cx - width / 2
    window['xmax'] = cx + width / 2
    window['ymin'] = cy - height / 2
    window['ymax'] = cy + height / 2


# Função para Desenhar Objetos no Canvas
def draw_objects(canvas, display_file, window, viewport):
    canvas.delete("all")  # Limpa o canvas

    for obj in display_file:
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


# Função para Parsing das Coordenadas
def parse_coordinates(input_str: str) -> List[Tuple[float, float]]:
    return list(eval(input_str))


# Classe da Aplicação Tkinter
class CGApp:
    def __init__(self, root):
        self.root = root
        self.objetos = []
        self.root.title("CG 2D")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.window = {'xmin': -10, 'xmax': 10, 'ymin': -10, 'ymax': 10}
        self.viewport = {'xmin': 0, 'xmax': 800, 'ymin': 0, 'ymax': 400}
        self.display_file = []

        self.pan_left_button = tk.Button(root, text="Pan Left", command=lambda: self.pan(-1, 0))
        self.pan_left_button.pack(side=tk.LEFT)
        self.pan_right_button = tk.Button(root, text="Pan Right", command=lambda: self.pan(1, 0))
        self.pan_right_button.pack(side=tk.LEFT)
        self.pan_up_button = tk.Button(root, text="Pan Up", command=lambda: self.pan(0, 1))
        self.pan_up_button.pack(side=tk.LEFT)
        self.pan_down_button = tk.Button(root, text="Pan Down", command=lambda: self.pan(0, -1))
        self.pan_down_button.pack(side=tk.LEFT)
        self.zoom_in_button = tk.Button(root, text="Zoom In", command=lambda: self.zoom(0.9))
        self.zoom_in_button.pack(side=tk.RIGHT)
        self.zoom_out_button = tk.Button(root, text="Zoom Out", command=lambda: self.zoom(1.1))
        self.zoom_out_button.pack(side=tk.RIGHT)

        frame = tk.Frame(root)
        frame.pack()
        ponto_frame = tkinter.LabelFrame(frame)
        ponto_frame.grid(row=0, column=0, padx=20, pady=10)

        #Add ponto
        labelX = tkinter.Label(ponto_frame, text="Coordenada X do ponto")
        labelX.grid(row=0,column=0)
        labelY = tkinter.Label(ponto_frame, text="Coordenada Y do ponto")
        labelY.grid(row=0,column=1)
        pontoX = Entry(ponto_frame)
        pontoY = Entry(ponto_frame)
        pontoX.grid(row=1, column=0)
        pontoY.grid(row=1, column=1)
        botaoAddPonto = tk.Button(ponto_frame, text="Add Ponto", command=self.addPonto)
        botaoAddPonto.grid(row=1,column=2)

        #AddLinha
        labelXLinha = tkinter.Label(ponto_frame, text="Coordenada X da linha")
        labelXLinha.grid(row=2, column=0)
        labelYLinha = tkinter.Label(ponto_frame, text="Coordenada Y da linha")
        labelYLinha.grid(row=2, column=1)
        linhaX = Entry(ponto_frame)
        linhaY = Entry(ponto_frame)
        linhaX.grid(row=3, column=0)
        linhaY.grid(row=3, column=1)
        botaoAddLinha = tk.Button(ponto_frame, text="Add Linha", command=self.addPonto)
        botaoAddLinha.grid(row=3, column=2)

    def addPonto(self,x,y):
        xv, yv = viewport_transform(x, y, self.window, self.viewport)
        self.canvas.create_oval(xv - 2, yv - 2, xv + 2, yv + 2, fill="black")
        obj = GraphicObject("ponto", "ponto", [x,y])
        self.objetos.append(obj)

    def add_object(self):
        input_str = self.entry.get()
        coordinates = parse_coordinates(input_str)
        if len(coordinates) == 1:
            obj_type = "point"
        elif len(coordinates) == 2:
            obj_type = "line"
        else:
            obj_type = "wireframe"

        new_object = GraphicObject("Object" + str(len(self.display_file)), obj_type, coordinates)
        self.display_file.append(new_object)
        self.draw()

    def draw(self):
        draw_objects(self.canvas, self.display_file, self.window, self.viewport)

    def pan(self, dx, dy):
        pan(self.window, dx, dy)
        self.draw()

    def zoom(self, factor):
        zoom(self.window, factor)
        self.draw()


# Inicializando o Tkinter
root = tk.Tk()
app = CGApp(root)
root.mainloop()
