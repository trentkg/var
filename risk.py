import scipy.stats
import scipy.integrate
import numpy as np

def get_returns(portfolio, period, perc=True):
	now = portfolio.iloc[period:]
	past = portfolio.shift(period).iloc[period:]
	if perc:	
		returns = (now-past)/past
	else:
		returns = (now-past)
	return returns.dropna()

def sample(df, n):
	'''Takes the last n values from df'''
	l=len(df)
	return df.iloc[l-n:l]

def create_ppf(returns):
	'''Returns a normal percent point function or quantile function given a list of historical returns'''
	mean = np.mean(returns)
	sdev = np.std(returns)
	return scipy.stats.norm(loc=mean, scale=sdev).ppf

def calc_var(alpha, period, hist_value, position):
	portfolio = position*hist_value
	cur_value = portfolio.value[len(portfolio)-1]
	returns = get_returns(portfolio, period)
	ppf = create_ppf(returns)
	var = -cur_value*ppf(alpha)
	if hasattr(var, '__getitem__'):
		return var[0]
	else:
		return var

def calc_expsf(alpha, var_func, var_args):
	'''Calcuales the expected shortfall given a var function and corresponding arguments'''
	integral, err = scipy.integrate.quad(var_func, 0.0, alpha, args=var_args)
	return (1.0/alpha) * integral 

def calc_volatility(hist_value, lookback, period):
	hist_value = sample(hist_value, lookback)
	returns = get_returns(hist_value, period)
	vol = np.std(returns)
	if hasattr(vol, '__getitem__'):
		return vol[0]
	else:
		return vol
