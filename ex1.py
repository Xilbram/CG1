import tkinter as tk
from GraphicObject import GraphicObject
from Transformador import *
from tkinter import Toplevel, Entry


# Classe da Aplicação Tkinter
class CGApp:
    def __init__(self, root):
        self.root = root
        self.indexObj = 0
        self.root.title("CG 2D")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.grid(row=0, column=0, rowspan=8, padx=10, pady=10)

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

        # Quadro para adicionar objetos
        ponto_frame = tk.LabelFrame(root, text="Adicionar Objetos")
        ponto_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

        # Espaço de seleção de objetos
        self.listBoxObjetos = tk.Listbox(root)
        self.listBoxObjetos.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="ns")

        self.editar_button = tk.Button(root, text="Editar Objeto", command=self.editar_objeto)
        self.editar_button.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Adicionar ponto
        labelX = tk.Label(ponto_frame, text="Coordenada X do ponto")
        labelX.grid(row=0, column=0, padx=5, pady=5)
        labelY = tk.Label(ponto_frame, text="Coordenada Y do ponto")
        labelY.grid(row=0, column=1, padx=5, pady=5)
        self.pontoX = Entry(ponto_frame)
        self.pontoY = Entry(ponto_frame)
        self.pontoX.grid(row=1, column=0, padx=5, pady=5)
        self.pontoY.grid(row=1, column=1, padx=5, pady=5)
        botaoAddPonto = tk.Button(ponto_frame, text="Add Ponto", command=self.addPonto)
        botaoAddPonto.grid(row=1, column=2, padx=5, pady=5)

        # Adicionar linha
        labelXLinha = tk.Label(ponto_frame, text="X inicial da linha")
        labelXLinha.grid(row=2, column=0, padx=5, pady=5)
        labelYLinha = tk.Label(ponto_frame, text="Y inicial da linha")
        labelYLinha.grid(row=2, column=1, padx=5, pady=5)
        labelXLinhaFinal = tk.Label(ponto_frame, text="X final da linha")
        labelXLinhaFinal.grid(row=2, column=2, padx=5, pady=5)
        labelYLinhaFinal = tk.Label(ponto_frame, text="Y final da linha")
        labelYLinhaFinal.grid(row=2, column=3, padx=5, pady=5)

        self.linhaX1 = Entry(ponto_frame)
        self.linhaY1 = Entry(ponto_frame)
        self.linhaX1.grid(row=3, column=0, padx=5, pady=5)
        self.linhaY1.grid(row=3, column=1, padx=5, pady=5)
        self.linhaX2 = Entry(ponto_frame)
        self.linhaY2 = Entry(ponto_frame)
        self.linhaX2.grid(row=3, column=2, padx=5, pady=5)
        self.linhaY2.grid(row=3, column=3, padx=5, pady=5)
        botaoAddLinha = tk.Button(ponto_frame, text="Add Linha", command=self.addLinha)
        botaoAddLinha.grid(row=3, column=4, padx=5, pady=5)

        # Adicionar polígono (wireframe)
        labelPoligono = tk.Label(ponto_frame, text="Wireframe (ex.: ((1,1,2,2),(2,2,2,2))")
        labelPoligono.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.entryPoligno = Entry(ponto_frame)
        self.entryPoligno.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        botaoAddPoligono = tk.Button(ponto_frame, text="Add Wireframe", command=self.addWireframe)
        botaoAddPoligono.grid(row=5, column=4, padx=5, pady=5)



    def atualizaListBox(self):
        self.listBoxObjetos.delete(0,tk.END)
        for item in self.display_file:
            self.listBoxObjetos.insert(tk.END,item.obj_type)

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

    def addPonto(self):
        x = int(self.pontoX.get())
        y = int(self.pontoY.get())
        xv, yv = self.viewport_transform(x, y)
        self.canvas.create_oval(xv - 2, yv - 2, xv + 2, yv + 2, fill="black")
        obj = GraphicObject(self.getIndexValorObjeto(), "ponto", [x,y], cor="branco")
        self.display_file.append(obj)
        self.atualizaListBox()

    def addLinha(self):
        x1 = int(self.linhaX1.get())
        y1  = int(self.linhaY1.get())
        x2 = int(self.linhaX2.get())
        y2  = int(self.linhaY2.get())
        coordenadas = [x1,y1,x2,y2]
        xv1, yv1 = self.viewport_transform(x1, y1)
        xv2, yv2 = self.viewport_transform(x2, y2)
        self.canvas.create_line(xv1, yv1, xv2, yv2)
        obj = GraphicObject(self.getIndexValorObjeto(), "linha", coordenadas,cor="branco")
        self.display_file.append(obj)
        self.atualizaListBox()

    def addWireframe(self):
        coordenadas = list(eval(self.entryPoligno.get()))
        obj = GraphicObject(self.getIndexValorObjeto(),"wireframe",coordenadas,cor="branco")
        self.display_file.append(obj)
        for i in range(len(coordenadas)):
            x1, y1,x2,y2 = coordenadas[i]
            xv1, yv1 = self.viewport_transform(x1, y1)
            xv2, yv2 = self.viewport_transform(x2, y2)
            self.canvas.create_line(xv1, yv1, xv2, yv2)
        obj = GraphicObject(self.getIndexValorObjeto(), "wireframe", coordenadas,cor="branco")
        self.display_file.append(obj)
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
        self.draw_objects()

# Inicializando o Tkinter
root = tk.Tk()
app = CGApp(root)
root.mainloop()
