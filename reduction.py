import random

def generate_vertices(lit):
    """
    Generate a set of triples of size n.
    """

    n1 = [0, f"a{lit}{1}", f"a{lit}{2}", f"a{lit}{3}", f"a{lit}{4}"]
        
    n2 = [0, f"b{lit}{1}", f"b{lit}{2}", f"b{lit}{3}", f"b{lit}{4}"]

    return n1, n2

def variable_gadget(v):
    t = set()

    n1 = v[0]
    n2 = v[1]

    for i in range(1,4+1):
        if i % 2 == 0:
            t.add((n1[i], n1[((i+1)%4)], n2[i]))
        if i % 2 != 0:
            t.add((n1[i], n1[i+1], n2[i]))
    
    return t

def clause_gadget(v, lit, clause_n, n):
    t = set()

    pt = [ f"p{clause_n}{1}", f"p{clause_n}{2}" ]

    n2 = v[1]

    if not lit:
        t.add((pt[0], pt[1], n2[n+1]))
    else:
        t.add((pt[0], pt[1], n2[n]))
    
    return t

def cleanup_gadget(v1, v2, v3):
    t = set()

    n1 = v1[1]
    n2 = v2[1]
    n3 = v3[1]
    for i in range(1, 4+1):
        l = [ f"l{i}{1}", f"l{i}{2}" ]

        for i in range(1,4+1):
            t.add((l[0], l[1], n1[i]))
            t.add((l[0], l[1], n2[i]))
            t.add((l[0], l[1], n3[i]))

    return t
    

def translateSATto3DM(clause):
    """
    Translate a SAT clause to a 3DM triple.
    Clause should be: (~x1 or x2 or x3) and (x1 or x2 or x3)
    """

    cl1, cl2 = clause.split("and")
    cl1 = list(map(lambda x: x.strip(" ").strip("(").strip(")"), cl1.split("or")))
    cl2 = list(map(lambda x: x.strip(" ").strip("(").strip(")"), cl2.split("or")))

    clauses = [cl1, cl2]

    for cl in clauses:
        for i in range(len(cl)):
            if cl[i][0] == "x":
                cl[i] = True
            elif cl[i][0] == "~":
                cl[i] = False

    # print(clauses)
        

    v1 = generate_vertices(1)
    v2 = generate_vertices(2)
    v3 = generate_vertices(3)

    t = variable_gadget(v1) | variable_gadget(v2) | variable_gadget(v3)

    v = [v1,v2,v3]

    n = 1
    for n_clause, cl in enumerate(clauses):
        for index, lit in enumerate(cl):
            t |= clause_gadget(v[index], lit, n_clause+1, n)
        n+=2
        
    t |= cleanup_gadget(v1, v2, v3)

    # print(t)
    # print(len(t))

    return t

def sol(t, lits, clauses):
    sol = []

    for x in t: ## Solution to group 1
        if x[0][0] == "a":
            last = x[2]
            for n, l in enumerate(lits):
                if n+1 == int(last[1]):
                    if l and int(last[2]) % 2 == 0: # if literal equals true and tip is even include in solution
                        sol.append(x)
                    elif not l and int(last[2]) % 2 != 0: # if literal equals false and tip is odd include in solution
                        sol.append(x)
    
    all_b = [x[2] for x in sol]
    all_a2 = [x[1] for x in sol]
    all_a1 = [x[0] for x in sol]

    for n, l in enumerate(clauses): ## Solution to group 2. Get all clauses and check if they are in the solution
        for x in t:
            if x[0][0] == "p":
                last = x[2]
                if x[2] not in all_b and x[1] not in all_a2 and x[0] not in all_a1:
                    if int(last[1]) == 1 and l[0] == True and int(last[2]) % 2 != 0:
                        sol.append(x)
                    elif int(last[1]) == 1 and l[0] == False and int(last[2]) % 2 == 0:
                        sol.append(x)

                    if int(last[1]) == 2 and l[1] == True and int(last[2]) % 2 != 0:
                        sol.append(x)
                    elif int(last[1]) == 2 and l[1] == False and int(last[2]) % 2 == 0:
                        sol.append(x)

                    if int(last[1]) == 3 and l[2] == True and int(last[2]) % 2 != 0:
                        sol.append(x)
                    elif int(last[1]) == 3 and l[2] == False and int(last[2]) % 2 == 0:
                        sol.append(x)
                all_b = [x[2] for x in sol]
                all_a2 = [x[1] for x in sol]
                all_a1 = [x[0] for x in sol]
            

    all_b = [x[2] for x in sol]
    all_a2 = [x[1] for x in sol]
    all_a1 = [x[0] for x in sol]
    
    for x in t: ## Solution to group 3. Get all that remains and add to solution
        if x[0][0] == "l":
            if x[2] not in all_b and x[1] not in all_a2 and x[0] not in all_a1:
                sol.append(x)
            all_b = [x[2] for x in sol]
            all_a2 = [x[1] for x in sol]
            all_a1 = [x[0] for x in sol]
    
    return sol

def translate_back(sol):
    lits = {}

    for x in sol:  ## translate to literals values
        if x[0][0] == 'a' and int(x[2][2]) % 2 == 0:
            lits[int(x[2][1])] = 1
        elif x[0][0] == 'a' and int(x[2][2]) % 2 != 0:
            lits[int(x[2][1])] = 0

    return lits

def solve_cnf(cnf, lits):
    cl1, cl2 = cnf.split("and")
    cl1 = list(map(lambda x: x.strip(" ").strip("(").strip(")"), cl1.split("or")))
    cl2 = list(map(lambda x: x.strip(" ").strip("(").strip(")"), cl2.split("or")))

    cl1_ans = 0
    for i in range(len(cl1)):
        if cl1[i][0] == "~":
            cl1_ans = cl1_ans | (not lits[i+1])
        else:
            cl1_ans = cl1_ans | lits[i+1]

    cl2_ans = 0
    for i in range(len(cl2)):
        if cl2[i][0] == "~":
            cl2_ans = cl2_ans | (not lits[i+1]) 
        else:
            cl2_ans = cl2_ans | lits[i+1]       
            
    return cl1_ans & cl2_ans

if __name__ == "__main__":
    cnf = "(x1 or ~x2 or x3) and (~x1 or x2 or x3)"
    t = translateSATto3DM(cnf)
    print(f"3-SAT Reduction to 3DM: {sorted(t)}")

    lits = [False, False, False]
    clauses = [[True, False, True], [False, True, True]]

    s = sol(t, lits, clauses)
    print(f"SOLUTION TO 3DM: {sorted(s)}")

    lits_back = translate_back(s)
    print(f"LITS TRANSLATED BACK: {lits_back}")
    print(f"ANSWER FOR 3-SAT: {solve_cnf(cnf, lits_back)}")
  