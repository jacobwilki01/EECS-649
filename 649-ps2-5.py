TIME = 5

s = [0,1,1,1,1,1]
v = [0]*(TIME+1)
w = [0]*(TIME+1)
x = [0]*(TIME+1)
y = [0]*(TIME+1)
z = [0]*(TIME+1)

print("t s v w x y z")
for t in range(TIME):
    print(t, s[t], v[t], w[t], x[t], y[t], z[t])

    v[t+1] = int (s[t] >= 1)
    w[t+1] = int ((s[t] - v[t]) >= 1)
    x[t+1] = int ((s[t] + w[t]) >= 2)
    y[t+1] = int ((s[t] + x[t]) >= 2)
    z[t+1] = int ((y[t] - s[t]) >= 1)

print(t+1, s[t+1], v[t+1], w[t+1], x[t+1], y[t+1], z[t+1])
