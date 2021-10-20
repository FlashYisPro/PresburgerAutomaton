from z3 import *
from prettytable import *
import math

def bin_list_to_val(l):
    val = 0
    for i in range(len(l)):
        val+= l[i]*(2**i)

    return val

def binary_list(x,n):
    b = []
    while x>0:
        r = x%2
        b.append(r)
        x = x//2

    if len(b)==n:
        return b
    else:
        rem = n - len(b)
        return b + [0 for i in range(rem)]

def binary_string(x,n):
    b = ''
    for i in binary_list(x,n):
        b += str(i)

    return b

def atomic_eq(f,b,n):
    vars = []
    coeff = [0 for i in range(n)]
    g = f
    while(g.decl().name()=='+'):
        vars.append(g.arg(1))
        g=g.arg(0)

    vars.append(g)

    for i in vars:
        if i.decl().name()=='*':
            indx = int(str(i.arg(1))[1])
            coeff[indx-1]=int(str(i.arg(0)))
        else:
            indx = int(str(i)[1])
            coeff[indx-1]=1

    wsum = [0 for i in range(2**n)]

    for i in range(2**n):
        binary = binary_list(i,n)
        for j in range(n):
            wsum[i]+= binary[j]*coeff[j]

    summation = 0
    for i in coeff:
        summation += abs(i)
    M = max(abs(int(b)),summation)

    # dfa =  {i:[0 for x in range(2**n)] for i in range(-M,M+1) }

    # for s in dfa:
    #     for j in range(2**n):
    #         new = s - wsum[j]
    #         if new % 2 == 1:
    #             dfa[s][j]='X'
    #         else:
    #             dfa[s][j]=new//2

    dfa =dict()
    accounted = []
    stk = [b]

    while len(stk)>0:
        s = stk.pop()
        if s in accounted:
            continue
        else:
            dfa[s] = [0 for i in range(2**n)]
            for i in range(2**n):
                new = s - wsum[i]
                if new%2 == 1:
                    dfa[s][i]='X'
                else:
                    dfa[s][i]=new//2
                    stk.append(dfa[s][i])
            
            accounted.append(s)

    dfa['X'] = ['X' for i in range(2**n)]

    return (dfa,b,[0])
    


def atomic_le(f,b,n):
    vars = []
    coeff = [0 for i in range(n)]
    g = f
    while(g.decl().name()=='+'):
        vars.append(g.arg(1))
        g=g.arg(0)

    vars.append(g)

    for i in vars:
        if i.decl().name()=='*':
            indx = int(str(i.arg(1))[1])
            coeff[indx-1]=int(str(i.arg(0)))
        else:
            indx = int(str(i)[1])
            coeff[indx-1]=1

    wsum = [0 for i in range(2**n)]

    for i in range(2**n):
        binary = binary_list(i,n)
        for j in range(n):
            wsum[i]+= binary[j]*coeff[j]

    summation = 0
    for i in coeff:
        summation += abs(i)
    M = max(abs(int(b)),summation)

    dfa =dict()
    accounted = []
    stk = [b]

    while len(stk)>0:
        s = stk.pop()
        if s in accounted:
            continue
        else:
            dfa[s] = [0 for i in range(2**n)]
            for i in range(2**n):
                new = s - wsum[i]
                dfa[s][i]=math.floor(new//2)
                stk.append(dfa[s][i])
        
            accounted.append(s)


    # dfa =  {i:[0 for x in range(2**n)] for i in range(-M,M+1) }


    # for s in dfa:
    #     if s>=0:
    #         final_states.append(s)
    #     for j in range(2**n):
    #         new = s - wsum[j]
    #         dfa[s][j]= math.floor(new/2)

    final_states = []
    for i in dfa:
        if i>=0:
            final_states.append(i)
        
    return (dfa,b,final_states)

#Each automaton ai is expected to be given in form of ( dfa:dict , initial_state:int , final_state:list )
def do_and(a1,a2,n):
    dfa_1 = a1[0]
    initial_state_1 = a1[1]
    final_states_1 = a1[2]
    dfa_2 = a2[0]
    initial_state_2 = a2[1]
    final_states_2 = a2[2]

    new_states = []

    for i in list(dfa_1):
        for j in list(dfa_2):
            new_states.append((i,j))

    dfa_new = {i:[0 for x in range(2**n)] for i in new_states}

    for s in dfa_new:
        p1=s[0]
        p2=s[1]
        for j in range(2**n):
            dfa_new[s][j]=(dfa_1[p1][j],dfa_2[p2][j])

    new_final_states = []
    new_initial_state = (initial_state_1,initial_state_2)

    

    dfa = dict()
    stk = [new_initial_state]
    accounted=[]

    while len(stk)>0:
        s = stk.pop()
        if s in accounted:
            continue
        else:
            dfa[s] = [0 for i in range(2**n)]
            for i in range(2**n):
                dfa[s][i]=dfa_new[s][i]
                stk.append(dfa[s][i])
        
            accounted.append(s)

    for i in dfa:
        x=i[0]
        y=i[1]

        if x in final_states_1 and y in final_states_2:
            new_final_states.append(i)

    return (dfa,new_initial_state,new_final_states)


def do_or(a1,a2,n):
    dfa_1 = a1[0]
    initial_state_1 = a1[1]
    final_states_1 = a1[2]
    dfa_2 = a2[0]
    initial_state_2 = a2[1]
    final_states_2 = a2[2]

    new_states = []

    for i in list(dfa_1):
        for j in list(dfa_2):
            new_states.append((i,j))

    dfa_new = {i:[0 for x in range(2**n)] for i in new_states}

    for s in dfa_new:
        p1=s[0]
        p2=s[1]
        for j in range(2**n):
            dfa_new[s][j]=(dfa_1[p1][j],dfa_2[p2][j])

    new_final_states = []
    new_initial_state = (initial_state_1,initial_state_2)

    dfa = dict()
    stk = [new_initial_state]
    accounted=[]

    while len(stk)>0:
        s = stk.pop()
        if s in accounted:
            continue
        else:
            dfa[s] = [0 for i in range(2**n)]
            for i in range(2**n):
                dfa[s][i]=dfa_new[s][i]
                stk.append(dfa[s][i])
        
            accounted.append(s)

    for i in dfa:
        x=i[0]
        y=i[1]

        if x in final_states_1 or y in final_states_2:
            new_final_states.append(i)

    return (dfa,new_initial_state,new_final_states)

def do_not(a1):
    dfa = a1[0]
    initial_state = a1[1]
    final_states = a1[2]

    new_final_states = []

    for i in dfa:
        if i not in final_states:
            new_final_states.append(i)

    return (dfa,initial_state,new_final_states)



def atomic(f,n):
    if f.decl().name() == '=':
        return atomic_eq(f.arg(0),int(str(f.arg(1))),n)
    if f.decl().name() == '<=':
        return atomic_le(f.arg(0),int(str(f.arg(1))),n)

    
def print_automaton(a1,n):
    dfa = a1[0]
    initial_state = a1[1]
    final_states = a1[2]
    header = ['States'] + [binary_string(i,n) for i in range(2**n)]
    t = PrettyTable(header)
    for i in dfa:
        anchor = str(i)
        if i == initial_state:
            anchor += '<I>'
        if i in final_states:
            anchor+= '<F>'
        row = [anchor]+dfa[i]
        t.add_row(row)
    
    print(t)
    print("\n")


def run_automaton(a,value_list):
    n = len(value_list)
    max_num = max(value_list)
    max_num_bdigits = math.ceil(math.log2(max_num))+5
    value_list_binary = [binary_list(i,max_num_bdigits) for i in value_list]
    words_to_run = []

    for i in range(max_num_bdigits):
        word = []
        for j in value_list_binary:
            word.append(j[i])
        
        words_to_run.append(word)

    words_to_run_val = [bin_list_to_val(i) for i in words_to_run]

    dfa = a[0]
    initial_state = a[1]
    final_states = a[2]

    curr_state = initial_state

    for i in words_to_run_val:
        if curr_state == 'X':
            break
        curr_state=dfa[curr_state][i]

    if curr_state in final_states:
        print("Accepted!")
    else:
        print("Rejected!")


# def post_order(f,post):
#     if f.decl().name() == 'or' or f.decl().name() == 'and':
#         post_order(f.arg(0),post)
#         post_order(f.arg(1),post)
#     if f.decl().name() == 'not':
#         post_order(f.arg(0),post)
    
#     post.append(f)

def isAtomic(f):
    if f.decl().name() == '=' or f.decl().name() == '<=':
        return True
    else:
        return False

def isAnd(f):
    if f.decl().name() == 'and':
        return True
    else:
        return False

def isOr(f):
    if f.decl().name() == 'or':
        return True
    else:
        return False

def isNot(f):
    if f.decl().name() == 'not':
        return True
    else:
        return False


def final_automaton(f,n):
    if isAtomic(f):
        a = atomic(f,n)
    if isAnd(f):
        a1 = final_automaton(f.arg(0),n)
        a2 = final_automaton(f.arg(1),n)
        a = do_and(a1,a2,n)
    if isOr(f):
        a1 = final_automaton(f.arg(0),n)
        a2 = final_automaton(f.arg(1),n)
        a = do_or(a1,a2,n)
    if isNot(f):
        a1 = final_automaton(f.arg(0),n)
        a = do_not(a1)
    

    print("Automaton for: {}".format(f))
    print_automaton(a,n)
    return a


def main_solver(f,n,value_list):
    a = final_automaton(f,n)
    
    print("Running the automaton on: ")
    for i in range(n):
        print("x{} ---> {}".format(i,value_list[i]))
    
    run_automaton(a,value_list)