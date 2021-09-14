import numpy as numpy
from statsmodels import regression
import statsmodels.api  as sm 
import matplotlib.pyplot as plt 

start = '2016-01-01'
end = '2017-01-01'

asset = get_pricing('APPl',fields='price',start_date=start,end_date=end)

benchmark = get_pricing('SPY',fields='price',start_date=start,end_date=end)

asset_ret = asset.pct_change(1)[1:]
bench_ret = benchmark.pct_change(1)[1:]

asset_ret.plot()
bench_ret.plot()
plt.legend()

plt.scatter(bench_ret,asset_ret,alpha=0.6,s=50)
plt.xlabel('SPY Ret')
plt.ylabel('APPL Ret')

APPL = asset_ret.values
spy = bench_ret.values

spy_constant = sm.add_constant(spy)

model = regression.linear_model.OLS(APPL,spy_constant).fit()
model.params

alpha,beta = model.params

min_spy = bench_ret.values.min()
max_spy = bench_ret.values.max()

spy_line = np.linspace(min_spy,max_spy,100)
y = spy_line*beta + alpha

plt.plot(spy_line,y,'r')
plt.scatter(bench_ret,asset_ret,alpha=0.6,s=50)
plt.xlabel('SPY Ret')
plt.ylabel('APPL Ret')

hedged = -1*(beta*bench_ret) + asset_ret

hedged.plot(label='APPL with Hedge')
asset_ret.plot(alpha=0.5)
bench_ret.plot(alpha=0.5)
plt.legend()

hedged.plot(label='APPL with Hedge')
asset_ret.plot(alpha=0.5)
bench_ret.plot(alpha=0.5)
plt.xlim(['2016-06-01','2016-08-01'])
plt.legend()

def alpha_beta(benchmark_ret,stock):
    benchmark = sm.add_constant(bench_ret)
    model = regression.linear_model.OLS(stock,benchmark).fit()
    return model.params[0],model.params[1]

# 2016 DATA
start = '2016-01-01'
end = '2017-01-01'

asset2016 = get_pricing('APPl',fields='price',start_date=start,end_date=end)

benchmark2016 = get_pricing('SPY',fields='price',start_date=start,end_date=end)

asset_ret2016 = asset2016.pct_change(1)[1:]
benchmark_ret2016 = benchmark2016.pct_change(1)[1:]

aret_values = asset_ret2016.values
bret_values = benchmark_ret2016.values 

alpha2016,beta2016 = alpha_beta(bret_values,aret_values)

print("2016 VALUES")
print("Alpha :: " + str(alpha2016))
print("Beta :: " + str(beta2016))

portfolio = -1*beta2016*benchmark_ret2016 + asset_ret2016

alpha,beta = alpha_beta(benchmark_ret2016,portfolio)

print("PORTFOLIO ALPHA AND BETA")
print("Alpha :: " + str(alpha))
print("Beta :: " + str(beta))

portfolio.plot(alpha=0.9,label='APPL with HEDGE')
asset_ret2016.plot(alpha=0.5)
benchmark_ret2016.plot(alpha=0.5)
plt.ylabel("DAILY RETURN")
plt.legend()

portfolio.mean()
asset_ret2016.mean()

portfolio.std()
asset_ret2016.std()

# 2017 DATA
start = '2017-01-01'
end = '2018-01-01'

asset2017 = get_pricing('APPl',fields='price',start_date=start,end_date=end)

benchmark2017 = get_pricing('SPY',fields='price',start_date=start,end_date=end)

asset_ret2017 = asset2017.pct_change(1)[1:]
benchmark_ret2017 = benchmark2017.pct_change(1)[1:]

aret_values = asset_ret2017.values
bret_values = benchmark_ret2017.values 

alpha2017,beta2017 = alpha_beta(bret_values,aret_values)

print("2017 VALUES")
print("Alpha :: " + str(alpha2017))
print("Beta :: " + str(beta2017))

print(alpha2016)
print(beta2016)

portfolio = -1*beta2016*benchmark_ret2017 + asset_ret2017
alpha,beta = alpha_beta(benchmark_ret2017,portfolio)

print(alpha)
print(beta)

portfolio.mean()

asset_ret2017.mean()

portfolio.std()

asset_ret2017.std()

