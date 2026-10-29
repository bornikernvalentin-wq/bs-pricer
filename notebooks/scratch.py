import sys
import numpy as np, scipy, pandas, matplotlib, yfinance
from scipy.stats import norm

S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20
q = 0


grilleK = np.linspace(-1, 20, 41)
vi = np.maximum(S-grilleK, 0)

def d1_d2 (S,K,T,r,sigma, q) : 
    
    d1 = (np.log(S/K) + (r-q + (sigma**2/2))*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    return(d1, d2)


def prix_call (S,K,T,r,sigma,q) : 
    
    if not np.all(S > 0) :
        raise ValueError("S doit être strictement positif")
    
    if not np.all(K > 0) :
        raise ValueError("K doit être strictement positif")
   
    if not np.all(T > 0) : 
        if T == 0 : 
            return (np.maximum(S - K, 0)) 
        raise ValueError("T doit être positif")
        
    if not np.all(sigma > 0) : 
        if sigma == 0 : 
            return (np.maximum(S*np.exp(-q*T) - K*np.exp(-r*T), 0))
        raise ValueError("sigma doit être positif")
    
    prix = S*np.exp(-q*T)*norm.cdf(d1_d2(S,K,T,r,sigma,q)[0]) - K*np.exp(-r*T)*norm.cdf(d1_d2(S,K,T,r,sigma,q)[1])
    
    return(prix)


def prix_put (S,K,T,r,sigma,q) : 
    
    prix = -S*np.exp(-q*T)*norm.cdf(-d1_d2(S,K,T,r,sigma,q)[0]) + K*np.exp(-r*T)*norm.cdf(-d1_d2(S,K,T,r,sigma,q)[1])
    
    return(prix)


def test_pariteCP() : 
    
    S = 90
    K = 105
    T = 1
    r = 0.02
    sigma = 0.25
    q = 0.01
    
    assert(abs(prix_call(S, K, T, r, sigma, q) - prix_put(S, K, T, r, sigma, q) - (S*np.exp(-q*T) - K*np.exp(-r*T)))) < 1e-10
    


def test_bornesC() : 
    
    S = 90
    
    T = 1
    r = 0.02
    sigma = 0.25
    q = 0.01
    
    assert(np.all(S*np.exp(-q*T) > prix_call(S, grilleK, T, r, sigma, q)))
    assert(np.all(prix_call(S, grilleK, T, r, sigma, q) > np.maximum(S*np.exp(-q*T) - grilleK*np.exp(-r*T),0)))

def test_bornesP() : 
    
    S = 90
    
    T = 1
    r = 0.02
    sigma = 0.25
    q = 0.01
    
    assert(np.all(grilleK*np.exp(-r*T) > prix_put(S, grilleK, T, r, sigma, q)))
    assert(np.all(prix_put(S, grilleK, T, r, sigma, q) > np.maximum(grilleK*np.exp(-r*T)- S*np.exp(-q*T),0)))

def test_monotonie():
    
    S = 90
    grilleK = np.linspace(80, 120, 41)
    T = 1
    r = 0.02
    sigma = 0.020
    q = 0.01

    assert(np.all(np.diff(prix_call(S,grilleK,T,r,sigma,q)) <= 0))

    sigma = np.linspace(0.05, 1, 41)
    K = 105
    
    assert(np.all(np.diff(prix_call(S,K,T,r,sigma,q)) >= 0))
    
    
    
def test_convexite():
    
    grilleK = np.linspace(80, 120, 41)
    S = 90
    T = 1
    r = 0.02
    sigma = 0.20
    q = 0.01
    
    assert(np.all(prix_call(S,grilleK,T,r,sigma,q)[1:-1] <= (prix_call(S,grilleK,T,r,sigma,q)[:-2] + prix_call(S,grilleK,T,r,sigma,q)[2:])/2))

def greeks(option, S, K, T, r, sigma, q) : 
    if option == "call" : 
        
        delta_call = np.exp(-q*T)*norm.cdf(d1_d2(S, K, T, r, sigma, q)[0])
        
        gamma_call = (np.exp(-q*T)*norm.pdf(d1_d2(S, K, T, r, sigma, q)[0]))/(S*sigma*np.sqrt(T))
        
        theta_call = -(1/2)*(sigma**2)*(S**2)*gamma_call 
        
        vega_call = S*np.exp(-q*T)*norm.pdf(d1_d2(S, K, T, r, sigma, q)[0])*np.sqrt(T)
        
        return(delta_call, gamma_call, theta_call, vega_call) 
    
    if option == "put" :
        
        delta_put = delta_call - np.exp(-q*T) 
        
        gamma_put = gamma_call
        
        theta_put = theta_call - q*S*np.exp(-q*T) + r*K*np.exp(-r*T) 
        
        vega_put = vega_call 
        
        return(delta_put, gamma_put, theta_put, vega_put) 
    
    































