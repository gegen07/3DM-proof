import random

def generateSetOfTriples(num_vertices, num_triples):
    X = set()
    while len(X) < num_triples:
        a = random.randint(1, num_vertices)
        b = random.randint(1, num_vertices)
        c = random.randint(1, num_vertices)
        X.add((a, b, c))
    return X

def non_deterministic_3dm(triples, k):
    M = []
    q = random.randint(1, k)
    for _ in range(q):
        M.append(random.choice(list(triples)))
    print(M)
    t = M[0]
    v1, v2, v3 = t
    if v1 == v2 or v1 == v3 or v2 == v3:
        return False
    for i in range(1, len(M)):
        x, y, z = M[i]
        if x == y or x == z or y == z:
            return False
        if x == v1 or x == v2 or x == v3 or y == v1 or y == v2 or y == v3 or z == v1 or z == v2 or z == v3: 
            return False
    
    return True

if __name__ == "__main__":
    E = generateSetOfTriples(10, 10)
    print(E)
    if non_deterministic_3dm(E, 4):
        print("YES")
    else:
        print("NO")