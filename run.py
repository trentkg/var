#!venv/bin/python2.7

import math
import argparse
import data
import risk

def calculate_exposure(ether_pos, conf_int, period, lookback, hist_value):
	hist_value = risk.sample(hist_value, lookback)
	if ether_pos < 0:
		hist_value *=-1
	alpha = 1-conf_int
	var = risk.calc_var(alpha, period, hist_value, ether_pos)
	exp_shortfall = risk.calc_expsf(alpha, risk.calc_var, var_args = (period, hist_value, ether_pos))
	print "Confidence: {}".format(conf_int)
	print "Period (days): {}".format(period)
	print "Ether position: {}".format(ether_pos)
	print "Lookback (days): {}".format(lookback)
	print "VaR($): {}".format(round(var, 1))
	print "Expected shortfall($): {}".format(round(exp_shortfall, 1))
	return

def calculate_vol_index(hist_value,lookback=90, trading_days_per_year = 365, period=30):
    volatility= risk.calc_volatility(hist_value, lookback, period)
    periods_per_year = math.floor(float(trading_days_per_year)/float(period))
    vix = 100*math.sqrt(periods_per_year)*volatility
    print "Period (days): {}".format(period)
    print "Lookback (days): {}".format(lookback)
    print "30 day annualized Ether VIX (%): {}".format(vix)
    return 

def main(pos, conf, per, lb):
	'''
	Prints the results of question 1 and 2 to stdout
	param:pos position in ether (VaR only)
	param:conf the confidence interval (VaR only)
	param:per the period over which to calculate returns in days (VaR only)
	param:lb the lookback  in days (VaR only)
	'''
	hist_value = data.load_csv(filepath="daily.csv")
	print 'Question 1: VAR'
	print '---------------------\n'
	calculate_exposure(args.pos, args.conf, args.per, args.lb, hist_value)
	print '\n'
	print 'Question 2: Volatility Index'
	print '---------------------\n'
	calculate_vol_index(hist_value)
	return
	
if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Calculate risk exposure and volatility index for ether as of 2017-12-22')
	parser.add_argument('-pos',default=1, type=int,
						help='Net long or short ether position (VaR only)')
	parser.add_argument('-conf', 
						default=.99,
						type=float, 
						help='The confidence interval (VaR only)')
	parser.add_argument('-per', 
						type=int, 
						default=10,
						help='The time period of returns, in days, (VaR only)')
	parser.add_argument('-lb', 
						type=int, 
						default=100,
						help='The lookback period in days (VaR only)')
	
	args = parser.parse_args()
	assert args.conf > 0, "confidence interval must be greater than 0"
	assert args.conf < 1, "confidence interval must less than one"
	main(args.pos, args.conf, args.per, args.lb)
