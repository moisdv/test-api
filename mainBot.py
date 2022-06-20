#Importar paquetes a utilicar.

import nltk #Paquete de procesamiento del lenguaje natural.
from nltk.stem.lancaster import LancasterStemmer #transforma palabras para hacerlas mas entendibles para el bot.
stemmer = LancasterStemmer() #Objeto de la clase Lancaste.
import numpy
import tflearn
import tensorflow
import json
import random #Paquete que genera respuesta aleatorias.
import pickle #Para guardar el modelo.

#nltk.download('punkt')

with open("contenido.json", encoding ='utf-8') as archivo:
    datos = json.load(archivo)

#print(datos)

palabras = []
tags =[]
auxX = []
auxY = []

for contenido in datos["contenido"]:
    for patrones in contenido["patrones"]:
        auxPalabra = nltk.word_tokenize(patrones)
        palabras.extend(auxPalabra)
        auxX.append(auxPalabra)
        auxY.append(contenido["tag"])

        if  contenido["tag"] not in tags: #Individualiza los tags

            tags.append(contenido["tag"])

"""print(palabras)
print(auxX)
print(auxY)
print(tags)"""

palabras = [stemmer.stem(w.lower()) for w in palabras if w!="?"]
palabras = sorted(list(set(palabras)))
tags = sorted(tags)

entrenamiento = []
salida = []
salidaVacia = [0 for _ in range(len(tags))]

for x, documento in enumerate(auxX):
    cubeta = []
    auxPalabra = [stemmer.stem(w.lower())for w in documento]
    for w in palabras:
        if w in auxPalabra:
            cubeta.append(1)
        else:
            cubeta.append(0)

    filadeSalida = salidaVacia[:]
    filadeSalida[tags.index(auxY[x])] = 1

    entrenamiento.append(cubeta)
    salida.append(filadeSalida)

"""print(entrenamiento)
print(salida)"""

#Red neuronal

entrenamiento = numpy.array(entrenamiento)
salidad = numpy.array(salida)

tensorflow.compat.v1.reset_default_graph()

red = tflearn.input_data(shape=[None,len(entrenamiento[0])]) #Entrada de entrenamiento(matriz)
red = tflearn.fully_connected(red,20) #columna de Neuronas
red = tflearn.fully_connected(red,20) #Columnas de Neuronas
red = tflearn.fully_connected(red,20) #columna de Neuronas
red = tflearn.fully_connected(red,len(salida[0]),activation="softmax")
red = tflearn.regression(red)

#Entrenamiento

modelo = tflearn.DNN(red)
modelo.fit(entrenamiento,salida,n_epoch=1000,batch_size=8,show_metric=True)
modelo.save("modelo.tflearn")

modelo.load("modelo.tflearn")
def goyobot():
    while True:
        entrada = input("tu:")
        cubeta =[0 for _ in range(len(palabras))]
        entradasProcesada = nltk.word_tokenize(entrada)
        entradasProcesada = [stemmer.stem(palabra.lower()) for palabra in entradasProcesada]
        for palabraIndividual in entradasProcesada:
            for i,palabra in enumerate(palabras):
                if palabra == palabraIndividual:
                    cubeta[i] = 1
        resultados = modelo.predict([numpy.array(cubeta)])
        #print(resultados)
        #resultados = modelo.predict([numpy.array(cubeta)])
        resultadosIndices = numpy.argmax(resultados)
        tag = tags[resultadosIndices]

        for tagAux in datos["contenido"]:
            if tagAux["tag"] == tag:
                respuesta = tagAux["respuestas"]

        print("Goyobot:", random.choice(respuesta))

goyobot()
