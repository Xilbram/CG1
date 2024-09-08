import tkinter
import tkinter as tk
from tkinter import Toplevel, Entry



class GraphicObject:
    def __init__(self, name, obj_type, coordinates):
        self.name = name
        self.obj_type = obj_type  # "point", "line", "wireframe"
        self.coordinates = coordinates  # Lista de coordenadas [(x1, y1), (x2, y2), ...]



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
        self.pontoX = Entry(ponto_frame)
        self.pontoY = Entry(ponto_frame)
        self.pontoX.grid(row=1, column=0)
        self.pontoY.grid(row=1, column=1)
        botaoAddPonto = tk.Button(ponto_frame, text="Add Ponto", command=self.addPonto)
        botaoAddPonto.grid(row=1,column=2)

        #AddLinha
        labelXLinha = tkinter.Label(ponto_frame, text="Coordenada X do ponto inicial da linha")
        labelXLinha.grid(row=2, column=0)
        labelYLinha = tkinter.Label(ponto_frame, text="Coordenada Y do ponto inicial da linha")
        labelYLinha.grid(row=2, column=1)
        labelXLinha = tkinter.Label(ponto_frame, text="Coordenada X do ponto final da linha")
        labelXLinha.grid(row=2, column=2)
        labelYLinha = tkinter.Label(ponto_frame, text="Coordenada Y do ponto final da linha")
        labelYLinha.grid(row=2, column=3)
        self.linhaX1 = Entry(ponto_frame)
        self.linhaY1 = Entry(ponto_frame)
        self.linhaX1.grid(row=3, column=0)
        self.linhaY1.grid(row=3, column=1)
        self.linhaX2 = Entry(ponto_frame)
        self.linhaY2 = Entry(ponto_frame)
        self.linhaX2.grid(row=3, column=2)
        self.linhaY2.grid(row=3, column=3)
        botaoAddLinha = tk.Button(ponto_frame, text="Add Linha", command=self.addLinha)
        botaoAddLinha.grid(row=3, column=4)

        #AddPoligno equivalente a um wireframe
        labelPoligono = tkinter.Label(ponto_frame, text="Insira em quadruplas. Exemplo: (1,1,10,10),(5,10,15,10)")
        labelPoligono.grid(row=4,column=1)
        self.entryPoligno = Entry(ponto_frame)
        self.entryPoligno.grid(row=5,column=1)
        botaoAddPoligono = tk.Button(ponto_frame, text="Add Wireframe", command=self.addWireframe)
        botaoAddPoligono.grid(row=5, column=2)


    def addPonto(self):
        x = int(self.pontoX.get())
        y = int(self.pontoY.get())
        xv, yv = self.viewport_transform(x, y)
        self.canvas.create_oval(xv - 2, yv - 2, xv + 2, yv + 2, fill="black")
        obj = GraphicObject("ponto", "ponto", [x,y])
        self.display_file.append(obj)

    def addLinha(self):
        x1 = int(self.linhaX1.get())
        y1  = int(self.linhaY1.get())
        x2 = int(self.linhaX2.get())
        y2  = int(self.linhaY2.get())
        xv1, yv1 = self.viewport_transform(x1, y1)
        xv2, yv2 = self.viewport_transform(x2, y2)
        self.canvas.create_line(xv1, yv1, xv2, yv2)
        obj = GraphicObject("linha", "linha", [x1,y1,x2,y2])
        self.display_file.append(obj)

    def addWireframe(self):
        coordenadas = list(eval(self.entryPoligno.get()))
        obj = GraphicObject("wireframe","wireframe",coordenadas)
        self.display_file.append(obj)
        for i in range(len(coordenadas)):
            x1, y1,x2,y2 = coordenadas[i]
            xv1, yv1 = self.viewport_transform(x1, y1)
            xv2, yv2 = self.viewport_transform(x2, y2)
            self.canvas.create_line(xv1, yv1, xv2, yv2)




    def draw(self):
        self.draw_objects()

    def zoom(self, factor):
        cx = (self.window['xmin'] + self.window['xmax']) / 2
        cy = (self.window['ymin'] + self.window['ymax']) / 2

        width = (self.window['xmax'] - self.window['xmin']) * factor
        height = (self.window['ymax'] - self.window['ymin']) * factor

        self.window['xmin'] = cx - width / 2
        self.window['xmax'] = cx + width / 2
        self.window['ymin'] = cy - height / 2
        self.window['ymax'] = cy + height / 2

        self.draw()


    def draw_objects(self):
        self.canvas.delete("all")  # Limpa o canvas

        #for item in self.display_file:
        #    print(item.obj_type)
        #    print(item.coordinates)


        for obj in self.display_file:
            if obj.obj_type == "ponto":
                x = obj.coordinates[0]
                y = obj.coordinates[1]
                xv, yv = self.viewport_transform(x, y)
                self.canvas.create_oval(xv - 2, yv - 2, xv + 2, yv + 2, fill="black")

            elif obj.obj_type == "linha":
                x1 = obj.coordinates[0]
                y1 = obj.coordinates[1]
                x2 = obj.coordinates[2]
                y2 = obj.coordinates[3]
                xv1, yv1 = self.viewport_transform(x1, y1)
                xv2, yv2 = self.viewport_transform(x2, y2)
                self.canvas.create_line(xv1, yv1, xv2, yv2)

            elif obj.obj_type == "wireframe":
                for i in range(len(obj.coordinates)):
                    x1, y1,x2,y2  = obj.coordinates[i]
                    xv1, yv1 = self.viewport_transform(x1, y1)
                    xv2, yv2 = self.viewport_transform(x2, y2)
                    self.canvas.create_line(xv1, yv1, xv2, yv2)

    def viewport_transform(self, xw, yw):
        vx = (xw - self.window['xmin']) / (self.window['xmax'] - self.window['xmin'])
        vy = (yw - self.window['ymin']) / (self.window['ymax'] - self.window['ymin'])

        xv = self.viewport['xmin'] + vx * (self.viewport['xmax'] - self.viewport['xmin'])
        yv = self.viewport['ymin'] + vy * (self.viewport['ymax'] - self.viewport['ymin'])

        return xv, yv

    def pan(self, dx, dy):
        self.window['xmin'] += dx
        self.window['xmax'] += dx
        self.window['ymin'] += dy
        self.window['ymax'] += dy
        self.draw()

# Inicializando o Tkinter
root = tk.Tk()
app = CGApp(root)
root.mainloop()
