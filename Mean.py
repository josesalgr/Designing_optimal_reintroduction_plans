def print_solutions(s,x,v):
	import matplotlib.pyplot as plt
	import math 

	plt.figure(figsize=(10, 12))
	axis_periods = ["1","2","3","4","5","6","7","8","9","10"]
	font = {
        'color':  'red',
        'weight': 'normal',
        'size': 12,
        }
	font2 = {
        'color':  'blue',
        'weight': 'normal',
        'size': 12,
        }

	grid = plt.GridSpec(6, 2, wspace=0.3, hspace=0.8)
	plt.suptitle('Instance-{}'.format(s+1),fontsize=14,fontweight="bold")

	for i in range(0,units):
    #1
		#plt.subplot(5,2,i+1)

		plt.subplot(grid[math.trunc(i/2),i%2])
		plt.plot(v[i])
		plt.axis([0,9,0,instance.ki[i+1]])
		plt.title('Site {}'.format(i))
		plt.xlabel('Periods')
		plt.xticks(np.arange(periods),axis_periods)
		plt.ylabel('N')
		types = [str(j) for j in x[i]]
		for k,type in enumerate(types):
		    if  int(types[k]) > 0:
		        plt.text(k-0.2, v[i][k]+instance.ki[i+1]/10, type, fontdict=font)

		plt.grid(True)
	

	n_individuals[s] = []
	for t in range(0, periods):
		sum_individuals = 0
		for i in range(0,units):
			sum_individuals = sum_individuals + v[i][t]
		n_individuals[s].append(sum_individuals)


	plt.subplot(grid[5,:])
	plt.plot(n_individuals[s])
	plt.axis([0,9,0,math.trunc(n_individuals[s][periods-1])])
	plt.title('Total individuals'.format(i))
	plt.xlabel('Periods')
	plt.xticks(np.arange(periods),axis_periods)
	plt.ylabel('N')
	plt.text(10-1, n_individuals[s][periods-1]+70, math.trunc(n_individuals[s][periods-1]), fontdict=font2)
	plt.savefig('SC{}_solution.png'.format(s+1))		


def print_comparations(n_individuals, periods):
	import matplotlib.pyplot as plt
	import matplotlib.patches as mpatches
	from matplotlib.colors import colorConverter as cc
	import numpy as np
	 
	def plot_mean_and_CI(mean, lb, ub, color_mean=None, color_shading=None):
		axis_periods = ["1","2","3","4","5","6","7","8","9","10"]
		periods = 10
		plt.figure(0)
	    # plot the shaded range of the confidence intervals
		plt.fill_between(range(mean.shape[0]), ub, lb,
	                     color=color_shading, alpha=.5)
		plt.axis([0,9,0,lb[9]])
		plt.xlabel('Periods')
		plt.xticks(np.arange(periods),axis_periods)
		plt.ylabel('N')

	    # plot the mean on top
		plt.plot(mean, color_mean)
		plt.savefig('Summary_individuals.png')

	ub0 = []
	lb0 = []
	mean0 = []

	for t in range(periods):
		min = 0
		max = 0
		sum = 0
		for s in range(1,datCounter):
			sum = sum + n_individuals[s][t]
			if v[i][t]>max:
				max = n_individuals[s][t]
			if v[i][t]<min:
				min = n_individuals[s][t]
		mean0 = mean0 + [sum/datCounter]
		lb0 = lb0 + [min]
		ub0 = ub0 + [max]
	    
	mean0 = np.array(mean0,dtype=np.float)
	lb0 = np.array(lb0,dtype=np.float)
	ub0 = np.array(ub0,dtype=np.float) 
	plot_mean_and_CI(mean0, ub0, lb0, color_mean='k', color_shading='k')

if __name__ == "__main__":

	from pyomo.environ import *
	import pyomo.environ as pyo
	from pyomo.opt import SolverFactory
	from pyomo.core import Var

	import numpy as np
	import GrowthSpecies as gr

	import glob
	import os
	import sys

	import xlwt 
	from xlwt import Workbook 
	from xlutils.copy import copy
	from xlrd import *

	import time
	
	os.chdir("Scenarios")
	mydir = os.getcwd()
	datCounter = len(glob.glob1(mydir,"*.dat"))
	n_individuals = {}

	#for s in range(53,1000):
	for s in range(datCounter):
		start = time.time()
		instance = gr.model.create_instance('Sc{}.dat'.format(s+1))
		opt = pyo.SolverFactory('cplex')
		opt.options["mipgap"] = 0.03
		sys.stdout = open('Output_Sc{}.dat'.format(s+1), 'w+')
		results = opt.solve(instance, tee=True)
		results.write()
		sys.stdout.fileno()
		end = time.time()

		#Plotting


		#Writting excel output
		units = 10
		periods = 10

		if s==0:
			wb = Workbook() 

			#Instance information---------------------------------------------
			sheet1 = wb.add_sheet('instances')
			sheet1.write(s+1,0, 'Instance-{}'.format(s+1))

			for i in range(0, units):
				sheet1.write(0,i+1, 'Capacity Site{} (K{})'.format(i+1,i+1))
				sheet1.write(s+1,i+1, value(instance.ki[i+1]))

			sheet1.write(0,units+1, 'First year survival')
			sheet1.write(s+1,units+1, value(instance.efficiency))

			sheet1.write(0,units+2, 'Minimum release')
			sheet1.write(s+1,units+2, value(instance.b_min))

			for i in range(0, periods):
				sheet1.write(0,units+3+i, 'Available individuals period{} '.format(i+1))
				sheet1.write(s+1,units+3+i, value(instance.b_max[i+1]))

			for i in range(0, periods):
				sheet1.write(0,units+periods+3+i, 'Growth (r) period{} '.format(i+1))
				sheet1.write(s+1,units+periods+3+i, value(instance.r[i+1]))

			#Releases--------------------------------------------------------
			sheet1 = wb.add_sheet('releases (x)')

			x = {}
			for i in range(0,units):
				x[i] = []
				for t in range(0,periods):
					if i==0:
						sheet1.write(i, t+2, 'Period{}'.format(t+1))
					if t==0:
						sheet1.write(i+1, t, 'Instance-{}'.format(s+1))
						sheet1.write(i+1, t+1, 'Site-{}'.format(i+1))
					if value(instance.x[i+1,t+1]) <0.1:
						sheet1.write(i+1, t+2, 0)
						x[i].append(0) 
					else:
						sheet1.write(i+1, t+2, round(value(instance.x[i+1,t+1])))
						x[i].append(round(value(instance.x[i+1,t+1])))

			#Growth----------------------------------------------------------
			sheet1 = wb.add_sheet('number of individuals (n)')

			v = {}
			for i in range(0,units):
				v[i] = []
				for t in range(0,periods):
					if i==0:
						sheet1.write(i, t+2, 'Period{}'.format(t+1))
					if t==0:
						sheet1.write(i+1, t, 'Instance-{}'.format(s+1))
						sheet1.write(i+1, t+1, 'Site-{}'.format(i+1))
					if value(instance.v[i+1,t+1]) <0.1:
						sheet1.write(i+1, t+2, 0)
						v[i].append(0)  
					else:
						sheet1.write(i+1, t+2, value(instance.v[i+1,t+1]))
						v[i].append(value(instance.v[i+1,t+1]))

			#Costs----------------------------------------------------------
			sheet1 = wb.add_sheet('costs')

			global_cost = 0
			for i in range(0,units):
				total_cost = 0
				for t in range(0,periods):
					if i==0:
						sheet1.write(i, t+2, 'Period{}'.format(t+1))
					if t==0:
						sheet1.write(i+1, t, 'Instance-{}'.format(s+1))
						sheet1.write(i+1, t+1, 'Site-{}'.format(i+1))
					sheet1.write(i+1, t+2, round(value(instance.y[i+1,t+1])*value(instance.c_open[i+1])+value(instance.z[i+1,t+1])*value(instance.c_mon[i+1]) + (value(instance.w[i+1,t+1])-value(instance.z[i+1,t+1]))*value(instance.c_mon2[i+1])))
					total_cost = total_cost + round(value(instance.y[i+1,t+1])*value(instance.c_open[i+1])+value(instance.z[i+1,t+1])*value(instance.c_mon[i+1]) + (value(instance.w[i+1,t+1])-value(instance.z[i+1,t+1]))*value(instance.c_mon2[i+1]))
				global_cost = total_cost + global_cost
				sheet1.write(i+1,periods+2, total_cost)
			sheet1.write(0, periods+2, 'Total cost')

			#Summary results-----------------------------------------
			sheet1 = wb.add_sheet('Summary')

			sheet1.write(s+1,0, 'Instance-{}'.format(s+1))

			sheet1.write(0,1, 'Total cost')
			sheet1.write(s+1,1, global_cost)

			sheet1.write(0,2, 'N total (obj)')
			sheet1.write(s+1,2, value(instance.obj))

			sheet1.write(0,3, 'Variables')
			sheet1.write(s+1,3, value(instance.nvariables()))

			sheet1.write(0,4, 'Constraints')
			sheet1.write(s+1,4, value(instance.nconstraints()))

			sheet1.write(0,5, 'Time(s)')
			sheet1.write(s+1,5, end - start)


			wb.save('Results.xlsx')

			#print_solutions(s,x,v)

		else:	
			w = copy(open_workbook('Results.xlsx'))

			w.get_sheet(0).write(s+1,0, 'Instance-{}'.format(s+1))

			for i in range(0, units):
				w.get_sheet(0).write(s+1,i+1, value(instance.ki[i+1]))

			w.get_sheet(0).write(s+1,units+1, value(instance.efficiency))
			w.get_sheet(0).write(s+1,units+2, value(instance.b_min))

			for i in range(0, periods):
				w.get_sheet(0).write(s+1,units+3+i, value(instance.b_max[i+1]))

			for i in range(0, periods):
				w.get_sheet(0).write(s+1,periods+units+3+i, value(instance.r[i+1]))

			#Releases------------------------------------------------------------------------------------
			x = {}
			for i in range(0,units):
				x[i] = []
				for t in range(0,periods):
					if t==0:
						w.get_sheet(1).write(i+1+units*s, t, 'Instance-{}'.format(s+1))
						w.get_sheet(1).write(i+1+units*s, t+1, 'Site-{}'.format(i+1))
					if value(instance.x[i+1,t+1]) <0.1:
						w.get_sheet(1).write(i+1+units*s, t+2, 0) 
						x[i].append(0) 
					else:
						w.get_sheet(1).write(i+1+units*s, t+2, round(value(instance.x[i+1,t+1])))
						x[i].append(round(value(instance.x[i+1,t+1])))

			#Growth-------------------------------------------------------------------------------------
			v = {}
			for i in range(0,units):
				v[i] = []
				for t in range(0,periods):
					if t==0:
						w.get_sheet(2).write(i+1+units*s, t, 'Instance-{}'.format(s+1))
						w.get_sheet(2).write(i+1+units*s, t+1, 'Site-{}'.format(i+1))
					if value(instance.v[i+1,t+1]) <0.1:
						w.get_sheet(2).write(i+1+units*s, t+2, 0) 
						v[i].append(0)
					else:
						w.get_sheet(2).write(i+1+units*s, t+2, value(instance.v[i+1,t+1]))
						v[i].append(value(instance.v[i+1,t+1]))

			#Costs--------------------------------------------------------------------------------------
			global_cost = 0
			for i in range(0,units):
				total_cost = 0
				for t in range(0,periods):
					if t==0:
						w.get_sheet(3).write(i+1+units*s, t, 'Instance-{}'.format(s+1))
						w.get_sheet(3).write(i+1+units*s, t+1, 'Site-{}'.format(i+1))
					w.get_sheet(3).write(i+1+units*s, t+2, round(value(instance.y[i+1,t+1])*value(instance.c_open[i+1])+value(instance.z[i+1,t+1])*value(instance.c_mon[i+1]) + (value(instance.w[i+1,t+1])-value(instance.z[i+1,t+1]))*value(instance.c_mon2[i+1])))
					total_cost = total_cost + round(value(instance.y[i+1,t+1])*value(instance.c_open[i+1])+value(instance.z[i+1,t+1])*value(instance.c_mon[i+1]) + (value(instance.w[i+1,t+1])-value(instance.z[i+1,t+1]))*value(instance.c_mon2[i+1]))
					w.get_sheet(3).write(i+1+units*s,periods+2, total_cost)
				global_cost = total_cost + global_cost

			#Summary-------------------------------------------------------------------------------------
			w.get_sheet(4).write(s+1,0, 'Instance-{}'.format(s+1))
			w.get_sheet(4).write(s+1,1, global_cost)
			w.get_sheet(4).write(s+1,2, value(instance.obj))
			w.get_sheet(4).write(s+1,3, value(instance.nvariables()))
			w.get_sheet(4).write(s+1,4, value(instance.nconstraints()))
			w.get_sheet(4).write(s+1,5, end - start)

			w.save('Results.xlsx')

			#print_solutions(s,x,v)

	print_comparations(n_individuals, periods)



			



