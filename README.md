# 2022_Designing_optimal_reintroduction_plans

This is the repository of our article "Designing an optimal large-scale reintroduction plan for a critically endangered species ".

# Software pre-requisites

-   Python 3.3+
-   Pandas
-   xlrd
-   pyomo
-   xlutils
-   cplex (requires licence): It can obtained free through an [academic licence](https://www.ibm.com/support/pages/how-do-i-download-cplex-optimization-studio?mhsrc=ibmsearch_a&mhq=cplex)

# Installation

You can clone this repository using git as follows:

```{bash}
git clone https://github.com/josesalgr/2022_Designing_optimal_reintroduction_plans.git
```

Or download it directly from this page.

## Running scenarios

The script (Scenario_builder.py) creates the indicated number of scenarios that will then be used by the model. This takes as input the file called "Specie_specific_values.xls" which contains simulated survival and density values. In turn, other parameters such as costs and planning periods are informed within its main function. The structure of the scenarios is followed according to Pyomo, the open-source optimization modeling language used. The resulting scenarios are saved in the Scenarios folder. To run in console:

```{bash}
python3 Scenario_builder.py
```

## Model

The model (Model.py) is coded in Pyomo, a python-based optimization modeling language. It is parameterized to take each previously generated scenario as input. The structure of the script is divided into the definition of parameters, variables, the optimization objective (maximization of individuals in the last planning period) and then the constraints of the mathematical model.

## Optimization

The script (Main.py) takes the scenarios from the "Scenarios" folder and feeds them to the model (Model.py), using the cplex optimizer (license required) calculates the solutions and then exports a "Results.xls" file with the most important values of outputs.

```{bash}
python3 Main.py
```
