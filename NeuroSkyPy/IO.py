import json
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.preprocessing import normalize

# por mejorar
# guardar si eso en pandas
# Guardar usando parquet


def generate_hex_color():
	'''
	Function to generate an hexadecimal color
	:return:
	'''
	r = lambda: random.randint(0, 255)
	hex_number = '#%02X%02X%02X' % (r(), r(), r())
	# second way:
	# random_number = random.randint(1118481, 16777215)
	# hex_number = str(hex(random_number))
	# hex_number = '#' + hex_number[2:]
	return hex_number


def save_session(dic, config):
	'''
	Function to store the data in the path and files chosen
	:param dic: dic of values
	:param config: variable where the configurariton data must be saved
	:return: nothing
	'''

	# labels to be drawn ( remove raw and poor signal ) Check them afterwards


	# raw signal se puede utilizar para identificar el ruido y como hace el paciente uso del casco
	# y poor signal para verificar los datos
	for i in config['exclude_from_drawing']:
		del dic[i]

	# preparamos los datos
	data = {
		'x': list(dic[list(dic.keys())[0]].keys()),
		'y': [dic[i].values() for i in dic.keys()]
	}

	# pintamos y guardamos los datos
	plot_graphics(data, list(dic.keys()), config, save_img=True)


def plot_graphics(data, var_names, config, save_img=False, transparent=False):
	'''
	Draw the graphics and also store in its rigthful folder
	:param data:
	:param var_names:
	:param config:
	:param save_img:
	:param transparent:
	:return:
	'''

	# declaramos el path to save
	path_to_save = "./"+config['folder_exp']+"/Resultados_"+config['name']+"_"+config['hour_exp']+"/Imagenes/"

	# extraemos los datos y fijamos los colores
	x = np.array(data['x'])
	lines = [np.array(list(i)) for i in data['y']]
	lines_norm = [normalize(np.array(list(i))[:, np.newaxis], axis=0, norm='max').ravel() for i in data['y']]
	labels = var_names
	color_predefined = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
	colors = []
	for idx in range(len(labels)):
		if idx < len(color_predefined): colors.append(color_predefined[idx])
		else: colors.append(generate_hex_color())

	for idy, y in enumerate([lines_norm, lines]):
		# fijamos la variable de guardado
		if idy == 0: save_var = "normalized"
		else: 	save_var = "unnormalized"
		# Ponemos leyenda y titulo
		plt.title("Señales del usuario: "+config['name']+" para el experimento: "+config['hour_exp'])
		plt.xlabel("Time in seconds")
		plt.ylabel("Intensity")

		for i, c, l in zip(y, colors, labels):
			plt.plot(x, i, c, label='l')
			plt.legend(labels)

		# guardamos la imagen
		if save_img: plt.savefig(path_to_save+"All_signals_"+save_var+".png", transparent=transparent)
		# la mostramos
		plt.show()
		# la borramos y volvemos a dibujar
		plt.clf()

	# pintamos cada una de las graficas por separado
	for idx, i in enumerate(lines):
		plt.title("Variable: " + var_names[idx] + " " + config['name'] + "_" + config['hour_exp'])
		plt.xlabel("Time in seconds")
		plt.ylabel("Intensity")
		plt.plot(x, i, colors[idx])
		if save_img: plt.savefig(path_to_save+var_names[idx]+".png", transparent=transparent)
		plt.show()
		plt.clf()


if __name__ == "__main__":
	from datetime import datetime
	var_names=["Attention", "Meditation", "Alpha"]
	x = np.arange(1,10)
	data = {
		'x':x,
		'y':[x, x*2, x*3]
	}
	config = {
		'name': 'usuario_x',
		'hour_exp': datetime.now().strftime("%Y%M%d%H%m%S"),
		'folder_exp':"Resultados_Exp",
		'session_time':60, # in seconds
		'port': "COM3"
	}
	plot_graphics(data, var_names, config)