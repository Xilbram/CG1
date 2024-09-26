import tkinter as tk
from GraphicObject import GraphicObject
from Transformador import *
from tkinter import Toplevel, Entry

from ex1.objParser import write_obj, read_obj


# Classe da Aplicação Tkinter
class CGApp:
    def __init__(self, root):
        self.root = root
        self.indexObj = 0
        self.root.title("CG 2D")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.grid(row=0, column=0, rowspan=10, padx=10, pady=10)

        self.window = {'xmin': -10, 'xmax': 10, 'ymin': -10, 'ymax': 10}
        self.viewport = {'xmin': 0, 'xmax': 800, 'ymin': 0, 'ymax': 400}
        self.display_file = []

        # Painel de botões à direita
        self.pan_left_button = tk.Button(root, text="Pan Left", command=lambda: self.pan(-1, 0))
        self.pan_left_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.pan_right_button = tk.Button(root, text="Pan Right", command=lambda: self.pan(1, 0))
        self.pan_right_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.pan_up_button = tk.Button(root, text="Pan Up", command=lambda: self.pan(0, 1))
        self.pan_up_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.pan_down_button = tk.Button(root, text="Pan Down", command=lambda: self.pan(0, -1))
        self.pan_down_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.zoom_in_button = tk.Button(root, text="Zoom In", command=lambda: self.zoom(0.9))
        self.zoom_in_button.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.zoom_out_button = tk.Button(root, text="Zoom Out", command=lambda: self.zoom(1.1))
        self.zoom_out_button.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        #Adiciona objetos
        self.adicionar_objeto_button = tk.Button(root, text="Adicionar Objeto", command=self.adicionar_objeto)
        self.adicionar_objeto_button.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Espaço de seleção de objetos
        self.listBoxObjetos = tk.Listbox(root)
        self.listBoxObjetos.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="ns")

        #Edicao objetos
        self.editar_button = tk.Button(root, text="Editar Objeto", command=self.editar_objeto)
        self.editar_button.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        #Rotaciona window
        self.label_rotacao_window = tk.Label(self.root, text="Angulo para rotacionar a window")
        self.label_rotacao_window.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
        self.angulo_rotacionar_window = Entry(self.root)
        self.angulo_rotacionar_window.grid(row=9, column=2, padx=10, pady=5, sticky="ew")
        self.rotate_window_left = tk.Button(root, text="Rotacionar esquerda",
                                            command=lambda: self.rotate_window(self.angulo_rotacionar_window.get(), "L"))
        self.rotate_window_right = tk.Button(root, text="Rotacionar direita",
                                             command=lambda: self.rotate_window(self.angulo_rotacionar_window.get(), "R"))
        self.rotate_window_left.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
        self.rotate_window_right.grid(row=10, column=2, padx=10, pady=5, sticky="ew")

        self.draw_axes()



    def atualizaListBox(self):
        self.listBoxObjetos.delete(0,tk.END)
        for item in self.display_file:
            self.listBoxObjetos.insert(tk.END,item.obj_type)

    def adicionar_objeto(self):
        nova_janela = Toplevel(self.root)
        nova_janela.title(f"Adicionar objeto")
        nova_janela.geometry("700x200")

        #Ponto
        labelX = tk.Label(nova_janela, text="Coordenada X do ponto")
        labelX.grid(row=0, column=0, padx=5, pady=5)
        labelY = tk.Label(nova_janela, text="Coordenada Y do ponto")
        labelY.grid(row=0, column=1, padx=5, pady=5)
        pontoX = Entry(nova_janela)
        pontoY = Entry(nova_janela)
        pontoX.grid(row=1, column=0, padx=5, pady=5)
        pontoY.grid(row=1, column=1, padx=5, pady=5)
        botaoAddPonto = tk.Button(nova_janela, text="Add Ponto", command=lambda: self.addPonto(pontoX.get(),pontoY.get()))
        botaoAddPonto.grid(row=1, column=2, padx=5, pady=5)

        #Linha
        labelXLinha = tk.Label(nova_janela, text="X inicial da linha")
        labelXLinha.grid(row=2, column=0, padx=5, pady=5)
        labelYLinha = tk.Label(nova_janela, text="Y inicial da linha")
        labelYLinha.grid(row=2, column=1, padx=5, pady=5)
        labelXLinhaFinal = tk.Label(nova_janela, text="X final da linha")
        labelXLinhaFinal.grid(row=2, column=2, padx=5, pady=5)
        labelYLinhaFinal = tk.Label(nova_janela, text="Y final da linha")
        labelYLinhaFinal.grid(row=2, column=3, padx=5, pady=5)
        linhaX1 = Entry(nova_janela)
        linhaY1 = Entry(nova_janela)
        linhaX1.grid(row=3, column=0, padx=5, pady=5)
        linhaY1.grid(row=3, column=1, padx=5, pady=5)
        linhaX2 = Entry(nova_janela)
        linhaY2 = Entry(nova_janela)
        linhaX2.grid(row=3, column=2, padx=5, pady=5)
        linhaY2.grid(row=3, column=3, padx=5, pady=5)
        botaoAddLinha = tk.Button(nova_janela, text="Add Linha", command=lambda: self.addLinha(linhaX1.get(),linhaY1.get()
                                                                                               ,linhaX2.get(),linhaY2.get()))
        botaoAddLinha.grid(row=3, column=4, padx=5, pady=5)

        #Wireframe
        labelPoligono = tk.Label(nova_janela, text="Wireframe (ex.: ((1,1,2,2),(2,2,2,2))")
        labelPoligono.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        entryPoligno = Entry(nova_janela)
        entryPoligno.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        botaoAddPoligono = tk.Button(nova_janela, text="Add Wireframe", command=lambda: self.addWireframe(entryPoligno.get()))
        botaoAddPoligono.grid(row=5, column=4, padx=5, pady=5)


    def editar_objeto(self):
        selected_index = self.listBoxObjetos.curselection()
        if selected_index:
            selected_obj = self.display_file[selected_index[0]]
            nova_janela = Toplevel(self.root)
            nova_janela.title(f"Editar {selected_obj.name}")
            nova_janela.geometry("400x500")

            # --- Seção de Translação com input ---
            trans_frame = tk.LabelFrame(nova_janela, text="Translação", padx=10, pady=10)
            trans_frame.pack(pady=10, fill="x")

            # Labels e Entradas para valores de translação
            label_x = tk.Label(trans_frame, text="Translação em X,Y:")
            label_x.grid(row=0, column=0, sticky="w")
            input_xy = Entry(trans_frame)
            input_xy.grid(row=0, column=1, padx=5)

            trans_button = tk.Button(trans_frame, text="Aplicar Translação",
                                     command=lambda: self.translacao(selected_obj, input_xy.get()))
            trans_button.grid(row=1, column=0, columnspan=2, pady=10)

            # --- Seção de Escalonamento com input ---
            escalonar_frame = tk.LabelFrame(nova_janela, text="Escalonar", padx=10, pady=10)
            escalonar_frame.pack(pady=10, fill="x")

            label_esc = tk.Label(escalonar_frame, text="Escalonar em SX,SY:")
            label_esc.grid(row=0, column=0, sticky="w")
            input_xy_escalonar = Entry(escalonar_frame)
            input_xy_escalonar.grid(row=0, column=1, padx=5)

            esc_button = tk.Button(escalonar_frame, text="Escalonamento Natural",
                                   command=lambda: self.escalonamento(selected_obj, input_xy_escalonar.get()))
            esc_button.grid(row=1, column=0, columnspan=2, pady=10)

            # --- Seção de Rotação com inputs ---
            rotacao_frame = tk.LabelFrame(nova_janela, text="Rotações", padx=10, pady=10)
            rotacao_frame.pack(pady=10, fill="x")

            label_rotacao = tk.Label(rotacao_frame, text="Ângulo a rotacionar:")
            label_rotacao.grid(row=0, column=0, sticky="w")
            input_angulo = Entry(rotacao_frame)
            input_angulo.grid(row=0, column=1, padx=5)

            label_ponto_arbitrario = tk.Label(rotacao_frame, text="Ponto arbitrario:")
            label_ponto_arbitrario.grid(row=1, column=0, sticky="w")
            input_ponto_arbitrario = Entry(rotacao_frame)
            input_ponto_arbitrario.grid(row=1, column=1, padx=5)

            rot_centro_mundo_button = tk.Button(rotacao_frame, text="Rotação em torno do Centro do Mundo",
                                                command=lambda: self.rotacao_centro_mundo(selected_obj,
                                                                                          input_angulo.get()))
            rot_centro_mundo_button.grid(row=2, column=0, columnspan=2, pady=5)

            rot_centro_obj_button = tk.Button(rotacao_frame, text="Rotação em torno do Centro do Objeto",
                                              command=lambda: self.rotacao_centro_obj(selected_obj,input_angulo.get()))
            rot_centro_obj_button.grid(row=3, column=0, columnspan=2, pady=5)

            rot_ponto_arbitrario_button = tk.Button(rotacao_frame, text="Rotação em torno de Ponto Arbitrário",
                                                    command=lambda: self.rotacao_ponto_arbitrario(selected_obj,
                                                                                                  input_angulo.get(),
                                                                                                  input_ponto_arbitrario.get()))
            rot_ponto_arbitrario_button.grid(row=4, column=0, columnspan=2, pady=5)
        else:
            print("Nenhum objeto selecionado.")

    def translacao(self,obj: GraphicObject, values):
        new_obj = transladarObjeto(obj, coordenadas=values)
        self.display_file.remove(obj)
        self.display_file.append(new_obj)
        self.draw_objects()
        return

    def escalonamento(self,obj,values):
        new_obj = escolonarObjeto(obj, values)
        self.display_file.remove(obj)
        self.display_file.append(new_obj)
        self.draw_objects()
        return

    def rotacao_centro_mundo(self,obj, angulo):
        new_obj = rotacionarOrigemMundo(obj, angulo)
        self.display_file.remove(obj)
        self.display_file.append(new_obj)
        self.draw_objects()
        return

    def rotacao_centro_obj(self,obj,angulo):
        new_obj = rotacionarCentroObj(obj, angulo)
        self.display_file.remove(obj)
        self.display_file.append(new_obj)
        self.draw_objects()
        return

    def rotacao_ponto_arbitrario(self,obj,angulo,ponto):
        new_obj = rotacionarPontoArbitrario(obj, angulo,ponto)
        self.display_file.remove(obj)
        self.display_file.append(new_obj)
        self.draw_objects()
        return

    def getIndexValorObjeto(self):
        self.indexObj += 1
        return self.indexObj

    def addPonto(self, x,y):
        x = float(x)
        y = float(y)
        xv, yv = self.viewport_transform(x, y)
        self.canvas.create_oval(xv - 2, yv - 2, xv + 2, yv + 2, fill="black")
        obj = GraphicObject(self.getIndexValorObjeto(), "ponto", [x,y], cor="black")
        self.display_file.append(obj)
        self.atualizaListBox()

    def addLinha(self,x1,y1,x2,y2):
        x1 = int(x1)
        y1  = int(y1)
        x2 = int(x2)
        y2  = int(y2)
        coordenadas = [x1,y1,x2,y2]
        xv1, yv1 = self.viewport_transform(x1, y1)
        xv2, yv2 = self.viewport_transform(x2, y2)
        self.canvas.create_line(xv1, yv1, xv2, yv2)
        obj = GraphicObject(self.getIndexValorObjeto(), "linha", coordenadas,cor="black")
        self.display_file.append(obj)
        self.atualizaListBox()

#((1,1,1,1),(5,5,5,5))
    def addWireframe(self,coordenadas_wireframe):
        coordenadas = list(eval(coordenadas_wireframe))
        obj = GraphicObject(self.getIndexValorObjeto(), "wireframe", coordenadas,cor="black")
        self.display_file.append(obj)

        for i in range(len(coordenadas)):
            x1, y1,x2,y2 = coordenadas[i]
            xv1, yv1 = self.viewport_transform(x1, y1)
            xv2, yv2 = self.viewport_transform(x2, y2)
            self.canvas.create_line(xv1, yv1, xv2, yv2)

        self.atualizaListBox()

    def zoom(self, factor):
        cx = (self.window['xmin'] + self.window['xmax']) / 2
        cy = (self.window['ymin'] + self.window['ymax']) / 2

        width = (self.window['xmax'] - self.window['xmin']) * factor
        height = (self.window['ymax'] - self.window['ymin']) * factor

        self.window['xmin'] = cx - width / 2
        self.window['xmax'] = cx + width / 2
        self.window['ymin'] = cy - height / 2
        self.window['ymax'] = cy + height / 2

        self.draw_objects()


    def draw_objects(self):
        self.canvas.delete("all")  # Limpa o canvas
        self.draw_axes()
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
                x1, y1, x2, y2 = obj.coordinates
                xv1, yv1 = self.viewport_transform(x1, y1)
                xv2, yv2 = self.viewport_transform(x2, y2)
                self.canvas.create_line(xv1, yv1, xv2, yv2, fill=obj.cor)

            elif obj.obj_type == "wireframe":
                for i in range(len(obj.coordinates)):
                    x1, y1,x2,y2  = obj.coordinates[i]
                    xv1, yv1 = self.viewport_transform(x1, y1)
                    xv2, yv2 = self.viewport_transform(x2, y2)
                    self.canvas.create_line(xv1, yv1, xv2, yv2, fill=obj.cor)

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
        self.draw_objects()

    def rotate_window(self, angle, direction):
        # Converta o ângulo para radianos
        angulo_rad  = math.radians(float(angle))

        if direction == "R":
            angulo_rad  = -angulo_rad

        # Pegue o centro da janela atual
        x_centro = (self.window['xmin'] + self.window['xmax']) / 2
        y_centro = (self.window['ymin'] + self.window['ymax']) / 2

        # Função de rotação
        def rotacionar_ponto(x, y):
            x_rot = (x - x_centro) * math.cos(angulo_rad) - (y - y_centro) * math.sin(angulo_rad) + x_centro
            y_rot = (x - x_centro) * math.sin(angulo_rad) + (y - y_centro) * math.cos(angulo_rad) + y_centro
            return x_rot, y_rot


        x_min_rot, y_min_rot = rotacionar_ponto(self.window['xmin'], self.window['ymin'])
        x_max_rot, y_max_rot = rotacionar_ponto(self.window['xmax'], self.window['ymax'])

        # Atualiza os valores da window
        self.window['xmin'], self.window['ymin'] = x_min_rot, y_min_rot
        self.window['xmax'], self.window['ymax'] = x_max_rot, y_max_rot

        # Redesenhe os objetos após a rotação
        self.draw_objects()

    def draw_axes(self):
        # Função que desenha os eixos X e Y no canvas
        cx = (self.window['xmin'] + self.window['xmax']) / 2
        cy = (self.window['ymin'] + self.window['ymax']) / 2
        x_axis_start = self.viewport_transform(self.window['xmin'], cy)
        x_axis_end = self.viewport_transform(self.window['xmax'], cy)
        y_axis_start = self.viewport_transform(cx, self.window['ymin'])
        y_axis_end = self.viewport_transform(cx, self.window['ymax'])

        # Desenha os eixos no canvas
        self.canvas.create_line(x_axis_start[0], x_axis_start[1], x_axis_end[0], x_axis_end[1], fill="red")
        self.canvas.create_line(y_axis_start[0], y_axis_start[1], y_axis_end[0], y_axis_end[1], fill="green")


    def parseToWaveFrontObj(self):
        write_obj("objs.txt",self.display_file)

    def parseFromWaveFrontObj(self):
        objetos_lidos = read_obj("objs.txt")
        self.display_file.append(objetos_lidos)
        self.draw_objects()


# Inicializando o Tkinter
root = tk.Tk()
app = CGApp(root)
root.mainloop()
