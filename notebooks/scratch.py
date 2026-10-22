import sys
import numpy as np, scipy, pandas, matplotlib, yfinance
from scipy.stats import norm

S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20
q = 0


a = np.linspace(80, 120, 41)
vi = np.maximum(S-a, 0)

def d1_d2 (S,K,T,r,sigma, q) : 
    
    d1 = (np.log(S/K) + (r-q + (sigma**2/2))*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    return(d1, d2)


def prix_call (S,K,T,r,sigma,q) : 
    
    prix = S*np.exp(-q*T)*norm.cdf(d1_d2(S,K,T,r,sigma,q)[0]) - K*np.exp(-r*T)*norm.cdf(d1_d2(S,K,T,r,sigma,q)[1])
    
    return(prix)


def prix_put (S,K,T,r,sigma,q) : 
    
    prix = -S*np.exp(-q*T)*norm.cdf(-d1_d2(S,K,T,r,sigma,q)[0]) + K*np.exp(-r*T)*norm.cdf(-d1_d2(S,K,T,r,sigma,q)[1])
    
    return(prix)