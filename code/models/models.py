# erf_model class definition
import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from lmfit import Model

class null_model():
    def __init__(self):
        pass
    def predict_with_quantiles(self, t_eval):
        return np.zeros([len(t_eval), 9])

class erf_model():
    def __init__(self, params0=[1,1,1], fixedParams0=[False,False,False]):
        assert(len(params0) == 3)
        assert(len(fixedParams0) == 3)
        
        self.model = Model(self.erf_curve)
        self.modelResult = None
        
        self.param_names = self.model.param_names
        self.params = self.model.make_params()
        for i in range(len(self.param_names)):
            param_name = self.param_names[i]
            self.params[param_name].value = params0[i]
            self.params[param_name].vary = not fixedParams0[i]
    
    # t is an array of time points []
    def predict(self, t_eval):
        return self.model.eval(self.params, t=t_eval)
    
    # return a matrix with 9 quantiles
    def predict_with_quantiles(self, t_eval):
        quantiles = [10, 20, 30, 40, 50, 60, 70, 80, 90] # 9 different quantiles
        y_pred_lst = self.predict(t_eval)
        
        y_pred_quantiles_lst = []
        for y_pred in y_pred_lst:
            y_pred_quantiles = [y_pred for i in range(len(quantiles))]
            y_pred_quantiles_lst.append(y_pred_quantiles)
        return y_pred_quantiles_lst
    
    # params must have logp, a, b
    def erf_curve(self, t, logp, a, b):
        p = 10**logp
        pred_y = p/2*(1+erf(a*(t-b)))
        return pred_y
    
    # predicts a time window, inclusive 
    def predict_timewindow(self, start, end):
        t = np.arange(start, end)
        pred_y = self.predict(t)
        return pred_y
    
    # fits to array of time and deaths
    def fit(self, T, y):
        self.modelResult = self.model.fit(y, self.params, t=T)
        self.params = self.modelResult.params
        
        # get cov matrix and errors
        # errors = np.sqrt(np.diag(pcov))
        return self

