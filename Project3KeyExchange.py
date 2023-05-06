def point_addition(P, Q, a, p):
    if P == Q:
        # Point doubling
        m = (3*P[0]**2 + a) * pow(2*P[1], -1, p) % p
    else:
        # Point addition
        m = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p

    x = (m**2 - P[0] - Q[0]) % p
    y = (m*(P[0] - x) - P[1]) % p
    return (x, y)

# Initialize the curve and the base point
p = 167
a = 11
b = 19
G = (2, 7)

# Alice's secret value
A_secret = 12

# Bob's secret value
B_secret = 31

# Alice computes a*G
R1 = G
for i in range(1, A_secret):
    R1 = point_addition(R1, G, a, p)
    
# Alice sends R1 to Bob
print("Alice sends: ", R1)

# Bob computes b*G
R2 = G
for i in range(1, B_secret):
    R2 = point_addition(R2, G, a, p)

# Bob sends R2 to Alice
print("Bob sends: ", R2)

# Alice computes a*R2
shared_secret1 = R2
for i in range(1, A_secret):
    shared_secret1 = point_addition(shared_secret1, R2, a, p)

# Bob computes b*R1
shared_secret2 = R1
for i in range(1, B_secret):
    shared_secret2 = point_addition(shared_secret2, R1, a, p)

print("Alice computes shared key: ", shared_secret1)
print("Bob computes shared key: ", shared_secret2)
print("Shared key established!")
