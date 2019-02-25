import numpy as np
import string
import collections
translator = str.maketrans('', '', string.punctuation+"´"+"¡"+"0"+"1"+"2"+"3"+"4"+"5"+"6"+"7"+"8"+"9"+"»"+"•"+"«"+"—"+"¿") 

#************* CONTEO NGRAMAS *************# 

def ngramas(data,n):
	"""
	Funcion que divide el texto ingresado (data) en los n-gramas indicados (n) 

	Se quitaron los saltos de linea asi como caracteres especiales para formar lista de palabras que
	luego sera dividida en n-gramas

	Regresa una lista con n-gramas
	"""

	data=data.replace('\n',' ')			    #Quita saltos de linea y remplaza por espacios
	data=data.lower()						#Minusculas
	data=data.translate(translator)			#Elimina caracteres especiales
	pal=data.split( )						#Divide en palabras
	ngramas=[]
	for j in pal:							#Recorre lista de palabras
		for i in range((len(j))-(n-1)):		#Itera en el tamaño de la palabra-(n-1)
			ngramas.append(j[i:i+n:])		#Agrega a la lista y avanza en la palabra de i a i+n
	return ngramas


def analizarT(archivo,n):
	"""
	Lee un archivo y le aplica la funcion n-gramas
	Se ordenan los mas repetidos y se toman los n mas comunes

	"""
	with open(archivo) as f:				#Abre archivo
		data=f.read()						#t= trigrama d=diccionario l=lista  r=repetidos
	t=(ngramas(data,3))						#Se dividen palabras en trigramas
	dT = collections.Counter(t)				#Se ordenan por los mas repetidos
	tR = dT.most_common(n)			     	#n ngramas mas comunes
	return tR

#************* DETECTOR DE IDIOMA *************# 

def detector(base_dat,cadena):
	"""
	Toma unicamente los trigramas ordenados y crea una lista de ellos (no toma su valor de repetecion)
	Divide la cadena ingresada con la funcion ngramas

	Compara cuantas veces aparecen los trigramas de la cadena ingresada en la lista listI
	Agrega las coincidencias a otra lista
	Compara el tamaño de cada lista para encontrar el idioma 
	"""
	Esp,Ing,Fra=base_dat[0],base_dat[1],base_dat[2]

	Esp=[(Esp[i][0]) for i,e in enumerate(Esp)] #Recorro la lista de tuplas tomando solo los trigramas; ennumerate= i= indices e=tupla (,)
	Ing=[(Ing[i][0]) for i,e in enumerate(Ing)]
	Fra=[(Fra[i][0]) for i,e in enumerate(Fra)]	

	listI=Esp,Ing,Fra							#Lista de idiomas			

	ngC=ngramas(cadena,3) 
	comparacion=[]
	for i in range(len(listI)):
		comparacion.append([item for item in ngC if item in listI[i]]) #Compara vs la lista de idiomas y agrega coincidencias en comparacion[]
	esp=len(comparacion[0])							#Cuenta coincidencias
	ing=len(comparacion[1])
	fra=len(comparacion[2])

	print("Comparaciones encontradas:\nEspañol= {} Inglés= {} Francés= {}".format(esp,ing,fra))
	if esp>ing and esp>fra:
		print("El idioma es español\n")
	elif ing>esp and ing>fra:
		print("El idioma es inglés\n")
	else:
		print("El idioma es francés\n")



#*********** Main **********#
idiomas=["Spanish.txt","English.txt","French.txt"] #Archivos para analisis y obtencion base_dat
n=100     #n-gramas significativos que se tomaran para el analisis

ltR=[(analizarT(i,n)) for i in idiomas]  #Ver si se puede con map

cadena1="La philosophie s’est comprise très tôt comme une manière de vivre et non pas uniquement comme une réflexion théorique. Dit autrement : être philosophe, c’est aussi vivre et agir d’une certaine façon et non pas seulement se confronter à des questions abstraites14. L’étymologie du terme « philosophie » indique bien que le philosophe est celui qui tend vers la sagesse, qui cherche à vivre comme il faut et plus particulièrement qui recherche le bonheur. La philosophie entendue comme mode de vie met l'accent sur la mise en application dans sa propre vie des résultats de la réflexion philosophique."
detector(ltR,cadena1)

cadena2="Traditionally, the term philosophy referred to any body of knowledge.[14][27] In this sense, philosophy is closely related to religion, mathematics, natural science, education and politics. Newton's 1687 Mathematical Principles of Natural Philosophy is classified in the 2000s as a book of physics; he used the term  because it used to encompass disciplines that later became associated with sciences such as astronomy, medicine and physics."
detector(ltR,cadena2)

cadena3="Según Pitágoras, la vida era comparable a los juegos olímpicos, porque en ellos encontramos tres clases de personas: las que buscan honor y gloria, las que buscan riquezas, y las que simplemente buscan contemplar el espectáculo, que serían los filósofos."
detector(ltR,cadena3)
