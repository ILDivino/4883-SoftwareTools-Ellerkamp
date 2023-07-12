x = [1,2,3,4,5,6,7,8,9,10,11]
y = [6,9.5,13,15,16.5,17.5,18.5,19,19.5,19.7,19.8]
N = length(x)
Sum_lnX = sum(log(x))
Sum_y = sum(y)
Mean_lnX = Sum_lnX/N
Mean_y = Sum_y/N
Sum_Y2 = power(Sum_y,2)
Sum_lnX2 = power(Sum_lnX,2)
Sum_YlnX = sum(log(x).*y)

Sxx = Sum_lnX2 - N*power(Mean_lnX,2)
Syy = Sum_Y2 - N*power(Mean_y,2)
Sxy = Sum_YlnX - N*Mean_lnX*Mean_y

B = Sxy / Sxx
A = Mean_y - B*Mean_lnX

R = Sxy/(Sxx * Syy)
