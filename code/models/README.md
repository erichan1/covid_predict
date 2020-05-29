# IHME Style Model
By Eric Han

## Overview
Implements a gaussian erf model class. 
This model depends on three parameters, alpha, beta, and p. 
Approximately, alpha = growth rate, beta = inflection, p = maximum final death number
Currently uses Italy Data

## Required Libraries
Pandas, Numpy, Scipy, Bokeh, holoviews, gitpython, lmfit

Notes:
Bokeh, holoviews -> graphing 
Need to install separate git for python
lmfit is great for fitting models, much better than scipy.optimize. 