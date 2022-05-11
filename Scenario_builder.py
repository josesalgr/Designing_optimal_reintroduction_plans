def create_scenarios():
	
	import numpy as np
	import pandas as pd
	import matplotlib.pyplot as plt
	import xlrd 
	import random

	random.seed(14)

	wb = xlrd.open_workbook("Specie_specific_values.xls") 
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

	#Writting-----------------------------------
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
		for k in range(len(c_monitoring)):
			f.write("{} {}".format(k+1, c_monitoring[k]))
			if (k+1)==len(c_monitoring):
				f.write(";")
				f.write("\n\n")
			else:
				f.write("\n")

		f.write("param: c_mon2 :=")
		f.write("\n")
		for k in range(len(c_monitoring_two)):
			f.write("{} {}".format(k+1, c_monitoring_two[k]))
			if (k+1)==len(c_monitoring_two):
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

if __name__ == "__main__":
	
	import os
	import numpy as np
	from itertools import product

	#Parameters---------------------------------
	periods = 10
	units = 10
	scenarios = 1000
	efficiency = [0.5,0.25]
	b_min = 50
	c_open = np.random.randint(5000,35000, periods)
	c_monitoring = np.random.randint(4000,5000, periods)
	c_monitoring_two = np.random.randint(2000,3000, periods)
	budget = 15000
	long_tramo = np.random.randint(200,1000, periods)
	first_introductions = [0,0,0,0,0,0,0,0,0]
	second_introductions = [0,0,0,0,0,0,0,0,0]

	create_scenarios()


