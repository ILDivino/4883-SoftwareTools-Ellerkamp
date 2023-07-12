x = [1.1,2.2,3.3,4.4,5.5,6,7.1,8,9]
y = [2.2,0.8,4.2,3.5,4.9,6,6.7,7.5,7.9]

N = length(x)
Sum_X = sum(x)
Sum_X2 = sum(x.^2)
Sum_Y = sum(y)
Sum_Y2 = sum(y.^2)
Sum_XY = sum(x.*y)
Mean_X = mean(x)
Mean_Y = mean(y)

m_num = (N*Sum_XY)-(Sum_X*Sum_Y)
m_denom = (N*Sum_X2-power(Sum_X,2))
m = m_num / m_denom
b = Mean_Y - (m * Mean_X)
r = ((N * Sum_XY) - Sum_X * Sum_Y) / (sqrt(N * Sum_X2 - power(Sum_X,2)) * sqrt(N * Sum_Y2 - power(Sum_Y,2)))

display("\nData below!!!!\n")
m
b
r
