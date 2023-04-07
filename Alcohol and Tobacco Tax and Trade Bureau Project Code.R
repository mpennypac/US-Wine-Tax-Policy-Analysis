

prices = read.csv('avg-annual-prices.csv')
returns = read.csv('wine-returns.csv')
Average.Annual.Return = returns$Average.Annual.Return
accidents = read.csv('drunk-driving-accidents.csv')
Number.of.Drunk.Driving.Accidents = accidents$Number.of.Drunk.Driving.Accidents

data = cbind(prices, Average.Annual.Return, Number.of.Drunk.Driving.Accidents)

library(vars)

model = VAR(data[,-1],p=1)
print(summary(model))

plot(c(1:nrow(data)), data$Average.Annual.Return, type='l')