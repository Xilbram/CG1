from GraphicObject import *
import math

#Entrada de coordenadas deve ser do tipo: x1,y1,x2,y2 ...
def transladarObjeto(obj: GraphicObject, coordenadas):
    coordenadas_originais = obj.coordinates
    coordenadas_int =  list(eval(coordenadas))
    novas_coordenadas = []

    for i in range(len(coordenadas_originais)):
        novas_coordenadas.append(coordenadas_originais[i] + coordenadas_int[i])

    new_obj = GraphicObject(obj.name,obj.obj_type,novas_coordenadas, obj.cor)

    return new_obj

def escolonarObjeto(obj: GraphicObject, coordenadas_escalonar):
    coordenadas_originais = obj.coordinates
    coordenadas_int =  list(eval(coordenadas_escalonar))
    novas_coordenadas = []

#Multiplica x do objeto por Sx e y por Sy

    for i in range(0, len(coordenadas_originais), 2):
        novas_coordenadas.append(coordenadas_originais[i] * coordenadas_int[0])  # Sx
        novas_coordenadas.append(coordenadas_originais[i + 1] * coordenadas_int[1])  # Sy


    new_obj = GraphicObject(obj.name, obj.obj_type, novas_coordenadas, obj.cor)

    return new_obj

def rotacionarOrigemMundo(obj: GraphicObject, angulo):
    theta = math.radians(int(angulo))
    coordenadas_originais = obj.coordinates
    novas_coordenadas = []

    for i in range(0, len(coordenadas_originais), 2):
        x = coordenadas_originais[i]
        y = coordenadas_originais[i + 1]

        # Aplicar as fórmulas de rotação
        x_rotacionado = x * math.cos(theta) - y * math.sin(theta)
        y_rotacionado = x * math.sin(theta) + y * math.cos(theta)

        # Adicionar as novas coordenadas à lista
        novas_coordenadas.append(x_rotacionado)
        novas_coordenadas.append(y_rotacionado)

    new_obj = GraphicObject(obj.name, obj.obj_type, novas_coordenadas, obj.cor)

    return new_obj

def rotacionarCentroObj(obj: GraphicObject, angulo):
    theta = math.radians(int(angulo))
    coordenadas_originais = obj.coordinates
    novas_coordenadas = []

    num_pontos = len(coordenadas_originais) // 2
    x_centro = sum(coordenadas_originais[i] for i in range(0, len(coordenadas_originais), 2)) / num_pontos
    y_centro = sum(coordenadas_originais[i + 1] for i in range(0, len(coordenadas_originais), 2)) / num_pontos

    for i in range(0, len(coordenadas_originais), 2):
        x = coordenadas_originais[i] - x_centro
        y = coordenadas_originais[i + 1] - y_centro

        x_rotacionado = x * math.cos(theta) - y * math.sin(theta)
        y_rotacionado = x * math.sin(theta) + y * math.cos(theta)

        novas_coordenadas.append(x_rotacionado + x_centro)
        novas_coordenadas.append(y_rotacionado + y_centro)

    new_obj = GraphicObject(obj.name, obj.obj_type, novas_coordenadas,obj.cor)

    return new_obj

def rotacionarPontoArbitrario(obj: GraphicObject, angulo,ponto):
    theta = math.radians(int(angulo))
    coordenadas_originais = obj.coordinates
    novas_coordenadas = []

    x_pivot = int(ponto[0])
    #ponto[1] é a virgula
    y_pivot =  int(ponto[2])

    for i in range(0, len(coordenadas_originais), 2):
        x = coordenadas_originais[i] - x_pivot
        y = coordenadas_originais[i + 1] - y_pivot

        x_rotacionado = x * math.cos(theta) - y * math.sin(theta)
        y_rotacionado = x * math.sin(theta) + y * math.cos(theta)

        novas_coordenadas.append(x_rotacionado + x_pivot)
        novas_coordenadas.append(y_rotacionado + y_pivot)


    new_obj = GraphicObject(obj.name, obj.obj_type, novas_coordenadas,obj.cor)

    return new_obj
