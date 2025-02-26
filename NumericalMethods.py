import numpy as np 

def k1(f,t,y,h,G,P):
    return f(t,y,G,P)
def k2(f,t,y,h,G,P):
    return f(t + h/2, y + h/2 * k1(f,t,y,h,G,P),G,P)
def k3(f,t,y,h,G,P):
    return f(t + h/2, y + h/2 * k2(f,t,y,h,G,P),G,P)
def k4(f,t,y,h,G,P):
    return f(t + h/2, y + h * k3(f,t,y,h,G,P),G,P)
def RungeKutta4(G,thetazero,P,stepsize,dtheta):
    return thetazero + stepsize/6 * (k1(dtheta,0,thetazero,stepsize,G,P) + 2 * k2(dtheta,0,thetazero,stepsize,G,P) + 2 * k3(dtheta,0,thetazero,stepsize,G,P) + k4(dtheta,0,thetazero,stepsize,G,P))

def A(K):
    if(K == 1):
        return 0
    elif(K == 2):
        return 2/9
    elif(K == 3):
        return 1/3
    elif(K == 4):
        return 3/4
    elif(K == 5):
        return 1
    elif(K == 6):
        return 5/6
    return 0

def B(K,L):
    if(L == 1):
        if(K == 2):
            return 2/9
        elif(K == 3):
            return 1/12
        elif(K == 4):
            return 69/128
        elif(K == 5):
            return -17/12
        elif(K == 6):
            return 65/432
    elif(L == 2):
        if(K == 3):
            return 1/4
        elif(K == 4):
            return -243/128
        elif(K == 5):
            return 27/4
        elif(K == 6):
            return -5/16
    elif(L == 3):
        if(K == 4):
            return 135/64
        elif(K == 5):
            return -27/5
        elif(K == 6):
            return 13/16
    elif(L == 4):
        if(K == 5):
            return 16/15
        elif(K == 6):
            return 4/27
    elif(L == 5):
        if(K == 6):
            return 5/144
    return 0

def CH(K):
    if(K == 1):
        return 47/450
    elif(K == 2):
        return 0
    elif(K == 3):
        return 12/25
    elif(K == 4):
        return 32/225
    elif(K == 5):
        return 1/30
    elif(K == 6):
        return 6/25
    return 0

def Kn(N,x,t,h,dtheta,G,P):
    y = t
    for i in range(1,N):
        y += Kn(i,x,t,h,dtheta,G,P) * B(N,i)
    return h * dtheta(y,x + A(N) * h, G,P)

def RKF(G,thetazero,P,stepsize,dtheta):
    y = thetazero
    for i in range(1,7):
        y += CH(i) * Kn(i,thetazero,0,stepsize,dtheta,G,P)
    return y
