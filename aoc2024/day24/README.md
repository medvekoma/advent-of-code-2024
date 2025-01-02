 1011
 1011

z[n] = (x[n] ^ y[n]) ^ t[n-1]
t[n] = (x[n] & y[n]) | ((x[n] ^ y[n]) & t[n-1])

t[0] = x[0] & y[0]

---

a[n] = x[n] ^ y[n]
b[n] = x[n] & y[n]
c[n] = a[n] & t[n-1]

t[0] = x[0] & y[0]
t[n] = b[n] | c[n]

z[n] = a[n] ^ t[n-1]