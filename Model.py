#!/usr/bin/env python
# coding: utf-8

from pyomo.environ import *
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pyomo.core import Var

import numpy as np

model = AbstractModel()

#Sets-------------------------------------------------------------------------------------------------------------

units = 10
partitions = 5

#Set of units
model.I = Set()
#Set of periods
model.T = Set()

#Parameters--------------------------------------------------------------------------------------------------------

#Ki
model.ki = Param(model.I)
#Efficiency
model.efficiency = Param()
#B min
model.b_min = Param()
#B max
model.b_max = Param(model.T)
#C open
model.c_open = Param(model.I)
#C monitoring
model.c_mon = Param(model.I)
#C non release
model.c_mon2 = Param(model.I)
#Budget
model.budget = Param()
#R
model.r = Param(model.T)
#First Introductions
model.f_intro = Param(model.I)
#Second Introductions
model.f_intro2 = Param(model.I)

#Variables---------------------------------------------------------------------------------------------------------

#x_it: Quantity of species that add in the unity i in the period t in the scenario s
def fb(model, i, t):
   return (0, model.ki[i])

model.x = Var(model.I, model.T, within=NonNegativeIntegers)

#q_it = 1, if the capacity isn't enough
model.q = Var(model.I, model.T, within=NonNegativeIntegers)

#w_it: Quantity of species that keep in the period t in the scenario s
model.w = Var(model.I, model.T, within=Boolean)

#v_it: Quantity of species that live in the unity i in the period t
model.v = Var(model.I, model.T, within=NonNegativeIntegers)

#y_it = 1, if the site i is open in the period t
model.y = Var(model.I, model.T, within=Boolean)

#z_it = 1, if the site i needs to monitoring in the period t
model.z = Var(model.I, model.T, within=Boolean)

#p_it: 
model.p = Var(model.I, model.T, within=Reals)

#Objective function------------------------------------------------------------------------------------------------
def obj_rule(model):
    return sum(model.v[i,10] for i in model.I) -sum(model.q[i,t] for i in model.I for t in model.T)

model.obj = Objective(rule=obj_rule, sense=maximize)


#Constraints-------------------------------------------------------------------------------------------------------

#Limitations constraints
#The number of individuals cannot exceed the capacity of the site
def limit1_rule(model,i,t):
    return model.v[i,t] <= model.ki[i]

model.limit1 = Constraint(model.I, model.T, rule=limit1_rule)


def limit5_rule(model,i,t):
    return (model.x[i,t] >= model.b_min*model.z[i,t])

model.limit5 = Constraint(model.I, model.T, rule=limit5_rule)



#Maximum of individuals to release in a period
def limit4_rule(model,t):
    if t>=0 :
        return sum(model.x[i,t] + model.q[i,t] for i in model.I) == model.b_max[t]
    else:
        return Constraint.Skip
    
model.limit4 = Constraint(model.T, rule=limit4_rule)


#Monitoring constraints
#Only can to introduce in opened sites
def monit1_rule(model,i,t):
    if t>=0:
        return model.x[i,t] <= 10000*model.z[i,t]
    else:
        return Constraint.Skip

model.monit1 = Constraint(model.I, model.T, rule=monit1_rule)

#The units can be open only once
def monit2_rule(model,i):
    return sum(model.y[i,t] for t in model.T) <= 1

model.monit2 = Constraint(model.I, rule=monit2_rule)


#Y and YA relation
def monit3_rule(model,i,t):
    if t>=0:
        return model.x[i,t] <= 10000*model.w[i,t]
    else:
        return Constraint.Skip

model.monit3 = Constraint(model.I,model.T, rule=monit3_rule)


#Y and YA relation
def monit4_rule(model,i,t):
    return sum(model.y[i,td] for td in model.T if td<=t) >= model.w[i,t]
    
model.monit4 = Constraint(model.I,model.T, rule=monit4_rule)


#Y and YA relation
def monit5_rule(model,i,t):
    return model.y[i,t] <= model.x[i,t]
    
model.monit5 = Constraint(model.I,model.T, rule=monit5_rule)


#Y and YA relation
def monit6_rule(model,i,t,td):
    if td>=t:
        return model.y[i,t] <= model.w[i,td]
    else:
        return Constraint.Skip
    
model.monit6 = Constraint(model.I,model.T,model.T, rule=monit6_rule)

#Cost constraints
def cost1_rule(model,t):
    if t>=0:
        return (sum(model.y[i,t]*model.c_open[i] for i in model.I) + 
                sum(model.z[i,t]*model.c_mon[i] for i in model.I) +
                sum((model.w[i,t]-model.z[i,t])*model.c_mon2[i] for i in model.I) <= model.budget)
    else:
        return Constraint.Skip
        
model.cost1 = Constraint(model.T, rule=cost1_rule)


#Growth
def growth1_rule(model,i,t):
    if t>=2:
        return (model.v[i,t] <= (model.x[i,t]*model.efficiency + model.p[i,t-1] + model.v[i,t-1]))
    else:
        return (model.v[i,t] <= (model.x[i,t]*model.efficiency))
        
model.growth1 = Constraint(model.I,model.T, rule=growth1_rule)


#Piecewise
model.bpts = {}
def bpts_build(model, i,t):
    model.bpts[i] = []
    for t in model.T:
        model.bpts[i,t] = []
        for q in range(0,partitions+1):
            #print(i, " " , t, " ", bp[i-1,t])
            bp = model.ki[i]*(q/partitions)
            model.bpts[i,t].append(bp)

        
model.BuildBpts = BuildAction(model.I,model.T, rule=bpts_build)

model.values = {}
def f4(model, i,t):
    m = np.zeros((units, partitions+1))
    
    model.values[i] = []
    for t in model.T:
        model.values[i,t] = []
        for q in range(0,partitions+1):
            bp = model.ki[i]*(q/partitions)
            m  = (bp*model.ki[i]*exp(model.r[t])/(model.ki[i]+bp*(exp(model.r[t])-1))) - bp
            model.values[i,t].append(m)

model.BuildValues = BuildAction(model.I,model.T,  rule=f4)


model.ComputePieces = Piecewise(model.I,model.T,
                              model.p,model.v,
                              pw_pts=model.bpts,
                              pw_repn='INC',
                              pw_constr_type='EQ',
                              f_rule=model.values,
                              unbounded_domain_var = True)

