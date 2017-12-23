#!venv/bin/python2.7
import data
import risk
import argparse

def calculate_exposure(ether_pos, conf_int, period, lookback):
	hist_value = data.load_csv(filepath="daily.csv")
	hist_value = risk.sample(hist_value, lookback)
	if ether_pos < 0:
		hist_value *=-1
	alpha = 1-conf_int
	var = risk.calc_var(alpha, period, hist_value, ether_pos)
	exp_shortfall = risk.calc_expsf(alpha, risk.calc_var, var_args = (period, hist_value, ether_pos))
	print "Confidence: {}".format(conf_int)
	print "Period (days): {}".format(period)
	print "Ethereum position: {}".format(ether_pos)
	print "Lookback (days): {}".format(lookback)
	print "VaR($): {}".format(round(var, 1))
	print "Expected shortfall($): {}".format(round(exp_shortfall, 1))
	return 

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Calculate risk exposure for ethereum')
	parser.add_argument('-pos',default=1, type=int,
						help='Net long or short ether position')
	parser.add_argument('-conf', 
						default=.99,
						type=float, 
						help='The confidence interval')
	parser.add_argument('-per', 
						type=int, 
						default=10,
						help='The period of time used in calculating returns, in days')
	parser.add_argument('-lb', 
						type=int, 
						default=100,
						help='The lookback period in days')
	
	args = parser.parse_args()
	assert args.conf > 0, "confidence interval must be greater than 0"
	assert args.conf < 1, "confidence interval must less than one"
	calculate_exposure(args.pos, args.conf, args.per, args.lb)
