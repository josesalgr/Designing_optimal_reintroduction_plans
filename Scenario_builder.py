def create_scenarios():
	
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	import xlrd 
	import random

	random.seed(69)

	wb = xlrd.open_workbook("Montseny_elicited_values.xls") 
	sheet = wb.sheet_by_index(0) 

	os.chdir("Scenarios")
	mydir = os.getcwd()

	#Removing files-----------------------------
	filelist = [f for f in os.listdir(mydir) ]
	for f in filelist:
		os.remove(os.path.join(mydir, f))


	#Generating different r's-------------------
	x = np.random.gamma(shape=2, scale=0.99, size=scenarios*periods)
	all_scenarios = ((-x+4)/5)
	plt.hist(all_scenarios)
	plt.savefig('r_distribution.png')

	#CLUSTERING


	#Writting-----------------------------------

	#all_scenarios = list(product(vector_r, repeat=periods))




	for s in range(scenarios):
		f= open("Sc{}.dat".format(s+1),"x+")

		f.write("#PARAMS")
		f.write("\n\n")

		f.write("set I :=")
		f.write("\n")
		for k in range(units):
			f.write("{}".format(k+1))
			if (k+1)==units:
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("set T :=")
		f.write("\n")
		for k in range(periods):
			f.write("{}".format(k+1))
			if (k+1)==periods:
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: ki :=")
		f.write("\n")
		for k in range(len(long_tramo)):
			f.write("{} {}".format(k+1, round(long_tramo[k]*sheet.cell_value(s+1, 1),0)))
			if (k+1)==len(long_tramo):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: efficiency :=")
		f.write("\n")
		f.write("{};".format(efficiency[random.sample([0, 1], 1)[0]]))
		f.write("\n\n")

		f.write("param: b_min :=")
		f.write("\n")
		f.write("{};".format(b_min))
		f.write("\n\n")

		f.write("param: b_max :=")
		f.write("\n")
		for k in range(periods):
			#if k==0:
			#	f.write("{} {}".format(k+1, max(first_introductions)))
			#else:
			#	if k==1:
			#		f.write("{} {}".format(k+1, max(second_introductions)))
			#	else:
			f.write("{} {}".format(k+1, random.sample([100, 150, 200, 250, 300],  1)[0]))
			
			if (k+1)==periods:
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: f_intro :=")
		f.write("\n")
		for k in range(len(first_introductions)):
			f.write("{} {}".format(k+1, first_introductions[k]))
			if (k+1)==len(first_introductions):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: f_intro2 :=")
		f.write("\n")
		for k in range(len(second_introductions)):
			f.write("{} {}".format(k+1, second_introductions[k]))
			if (k+1)==len(second_introductions):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: c_open :=")
		f.write("\n")
		for k in range(len(c_open)):
			f.write("{} {}".format(k+1, c_open[k]))
			if (k+1)==len(c_open):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: c_mon :=")
		f.write("\n")
		for k in range(len(c_mon)):
			f.write("{} {}".format(k+1, c_mon[k]))
			if (k+1)==len(c_mon):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: c_mon2 :=")
		f.write("\n")
		for k in range(len(c_mon2)):
			f.write("{} {}".format(k+1, c_mon2[k]))
			if (k+1)==len(c_mon2):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: budget :=")
		f.write("\n")
		f.write("{};".format(budget))
		f.write("\n\n")

		f.write("param: r :=")
		f.write("\n")
		for r in range(periods):
			f.write("{} {}".format(r+1, round(all_scenarios[s*10+r],4)))
			if (r+1)==periods:
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")
		f.close()


def create_structure_scenarios():

	f= open("ScenarioStructure.dat","x+")

	f.write("#  IMPORTANT - THE STAGES ARE ASSUMED TO BE IN TIME-ORDER.")
	f.write("\n\n")
	f.write("set Stages := ")
	for k in range(periods):
		f.write("Stage{}".format(k+1, capacity[k]))
		if (k+1)==periods:
			f.write(";")
			f.write("\n\n")
		else:
			f.write(" ")

	f.write("set Nodes := RootNode")
	f.write("\n")
	for t in range(periods-1):
		permutaciones = list(product(vector_r, repeat=t+1))
		for i in range(len(permutaciones)):
			f.write("Stage{}".format(t+2))
			for j in range(len(permutaciones[i])):
				f.write("-{}".format(list(product(vector_r, repeat=t+1))[i][j]))
			f.write("\n")
		if (t+1)==periods-1:
			f.write(";")
			f.write("\n\n")
	
	f.write("param NodeStage := RootNode Stage1")
	f.write("\n")
	for t in range(periods-1):
		permutaciones = list(product(vector_r, repeat=t+1))
		for i in range(len(permutaciones)):
			f.write("Stage{}".format(t+2))
			for j in range(len(permutaciones[i])):
				f.write("-{}".format(list(product(vector_r, repeat=t+1))[i][j]))
			f.write(" Stage{}".format(t+2))
			f.write("\n")
		if (t+1)==periods-1:
			f.write(";")
			f.write("\n\n")


	f.write("set Children[RootNode] := ")
	f.write("\n")
	for t in range(periods-1):
		if(t==0):
			permutaciones = list(product(vector_r, repeat=t+1))
			for i in range(len(permutaciones)):
				f.write("Stage{}".format(t+2))
				for j in range(len(permutaciones[i])):
					f.write("-{}".format(list(product(vector_r, repeat=t+1))[i][j]))
				f.write("\n")
			f.write("; \n\n")
		else:
			permutacion_anterior = list(product(vector_r, repeat=t))	
			permutaciones = list(product(vector_r, repeat=t+1))
			for p in range(len(permutacion_anterior)):
				f.write("set Children[Stage{}".format(t+1))
				father = ""
				for j in range(len(permutacion_anterior[p])):
					father = father + "-" + str(list(product(vector_r, repeat=t))[p][j])
					f.write("-{}".format(list(product(vector_r, repeat=t))[p][j]))
				f.write("] := \n")

				son = ""
				for i in range(len(permutaciones)):
					is_father = False
					son_extended = ""
					son = "Stage" + str(t+2)
					#f.write("Stage{}".format(t+2))
					for j in range(len(permutaciones[i])):
						son_extended = son_extended + "-" + str(list(product(vector_r, repeat=t+1))[i][j])
						if j==(len(permutaciones[i])-2):
							if son_extended != father:
								break
							else:
								is_father = True
								continue
						if is_father == True:
							f.write(son + son_extended)
							f.write("\n")
				f.write(";")
				f.write("\n\n")		

	f.write("param ConditionalProbability := RootNode 1.0")
	f.write("\n")
	for t in range(periods-1):
		permutaciones = list(product(vector_r, repeat=t+1))
		for i in range(len(permutaciones)):
			f.write("Stage{}".format(t+2))
			for j in range(len(permutaciones[i])):
				f.write("-{}".format(list(product(vector_r, repeat=t+1))[i][j]))
			f.write(" {}".format(1/len(vector_r)))
			f.write("\n")
		if (t+1)==periods-1:
			f.write(";")
			f.write("\n\n")

	f.write("set Scenarios := ")
	permutaciones = list(product(vector_r, repeat=periods-1))
	for i in range(len(permutaciones)):
		f.write("Sc{}".format(i+1))
		f.write("\n")
	if (t+1)==periods-1:
		f.write(";")
		f.write("\n\n")

	f.write("param ScenarioLeafNode := ")
	f.write("\n")
	permutaciones = list(product(vector_r, repeat=periods-1))
	for i in range(len(permutaciones)):
		f.write("Sc{}".format(i+1))
		f.write(" Stage{}".format(periods))
		for j in range(len(permutaciones[i])):
			f.write("-{}".format(list(product(vector_r, repeat=t+1))[i][j]))
		f.write("\n")
	if (t+1)==periods-1:
		f.write(";")
		f.write("\n\n")

	for k in range(periods):
		f.write("set StageVariables[Stage")
		f.write("{}] := ".format(k+1))
		f.write("x[*,{}]".format(k+1))
		f.write("\n")
		f.write("y[*,{}]".format(k+1))
		f.write("\n")
		f.write("v[*,{}]".format(k+1))
		f.write("\n")
		f.write("w[*,{}]".format(k+1))
		f.write("\n")
		f.write("z[*,{}]".format(k+1))
		f.write(";")
		f.write("\n\n")

	f.write("param StageCost := ")
	for k in range(periods):
		f.write("Stage{} n_individuals[{}]".format(k+1,k+1))
		f.write("\n")
	f.write(";")
	f.write("\n\n")


if __name__ == "__main__":
	
	import os
	from itertools import product

	#Parameters---------------------------------
	#poniente
	periods = 10
	units = 10
	scenarios = 1000
	efficiency = [0.179,0.678]
	b_min = 50
	c_open = [15713.40, 9573.60, 33651.20, 5100.00, 5102.40, 34487.60, 14939.4, 5112.00, 94510.8, 5112.0]
	c_mon = [4480.80, 4480.80, 4471.20, 4476.00, 4480.80, 4483.20, 4488.00, 4500.00, 4480.8, 4500.00]
	c_mon2 = [2420.40, 2420.40, 2415.60, 2418.00, 2420.40, 2421.60, 2424.00, 2430.00, 2420.40, 2430]
	budget = 15000
	long_tramo = [655,276,528,496,792,448,607, 1591,957,810]
	first_introductions = [0,0,0,0,0,0,0,0,0]
	second_introductions = [0,0,0,0,0,0,0,0,0]



	#ORIENTE
	#periods = 11
	#units = 7
	#scenarios = 1000
	#efficiency = [0.179,0.678]
	#b_min = 50
	#c_open = [5106, 269992.8, 91501.2, 73766, 5094, 181689.2, 130684.8]
	#c_mon = [4488, 4461.6, 4461.6, 4464, 4464, 4454.4, 4476]
	#c_mon2 = [ 2424,2410.8, 2410.80, 2412, 2412, 2407.20, 2418]
	#budget = 20000
	#long_tramo = [1093, 902, 1131, 1184, 671, 702, 1382]
	#first_introductions = [0,0,0,0,0,0,0]
	#second_introductions = [100,0,0,0,0,0,0]



	#-------------------------------------------
	#all_scenarios = list(product(vector_r, repeat=periods))

	create_scenarios()

	
	#create_structure_scenarios()
