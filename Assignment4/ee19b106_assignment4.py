import numpy as np
import math
import scipy.integrate as integrate
import pylab

def exp(x):
    return np.exp(x)
def coscos(x):
    return np.cos(np.cos(x))

def plot_functions():
    x = np.linspace(-2*np.pi, 4*np.pi, 500)

    exp_x = exp(x)
    pylab.semilogy(x, exp_x, 'b')
    pylab.grid(True)
    pylab.ylabel(r'$e^{x}\rightarrow$', fontsize=12)
    pylab.xlabel(r'x$\rightarrow$', fontsize=12)
    pylab.title('Semilog plot of $e^{x}$', fontsize=12)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

    coscos_x = coscos(x)
    pylab.plot(x,coscos_x,'b')
    pylab.grid(True)
    pylab.xlabel(r'x$\rightarrow$', fontsize=12)
    pylab.ylabel(r'$\cos(\cos(x))\rightarrow$', fontsize=12)
    pylab.title('Plot of $\cos(\cos(x))$',fontsize=12)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def fourier_transform(n, function):
    coeff = np.zeros(n)
    def u(x, k, f):
        return f(x)*np.cos(k*x)/np.pi
    def v(x,k,f):
        return f(x)*np.sin(k*x)/np.pi

    coeff[0] = integrate.quad(function,0,2*np.pi)[0]/(2*np.pi)
    for i in range(1,n):
        if i%2:
            coeff[i] = integrate.quad(u,0,2*np.pi,args=((i//2) +1,function))[0]
        else:
            coeff[i] = integrate.quad(v,0,2*np.pi,args=(i//2,function))[0]
    return coeff

def plot_coefficients(coeffs, func):
    pylab.semilogy(range(51),np.abs(coeffs),'ro')
    pylab.grid(True)
    pylab.xlabel(r'n$\rightarrow$',fontsize=12)
    pylab.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=12)
    pylab.title('Semilog Plot of coefficients for '+func,fontsize=12)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

    pylab.loglog(range(51),np.abs(coeffs),'ro')
    pylab.grid(True)
    pylab.xlabel(r'n$\rightarrow$',fontsize=12)
    pylab.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=12)
    pylab.title('Loglog Plot of coefficients of '+func,fontsize=12)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def solve(function):
    x = np.linspace(0,2*np.pi,401)
    x = x[:-1]
    y = np.linspace(0,2*np.pi,400)
    A = np.zeros((400,51))
    A[:,0] = 1
    for i in range(1,26):
        A[:,2*i-1] = np.cos(i*x)
        A[:,2*i] = np.sin(i*x) 
    B = function(x)  
    c = np.linalg.lstsq(A,B,rcond = None)[0]
    return A, c

def plot_comparison(c, coeff, func):
    pylab.semilogy(range(51),np.abs(c),'go',label='Least Squares Approach')
    pylab.semilogy(range(51),np.abs(coeff),'ro',label='True Value')
    pylab.grid(True)
    pylab.xlabel(r'n$\rightarrow$',fontsize=12)
    pylab.ylabel(r'$Coefficient\rightarrow$',fontsize=12)
    pylab.title('Semilog Plot of coefficients for '+func,fontsize=12)
    pylab.legend(loc='upper right')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

    pylab.loglog(range(51),np.abs(c),'go',label='Least Squares Approach')
    pylab.loglog(range(51),np.abs(coeff),'ro',label = 'True Value')
    pylab.grid(True)
    pylab.xlabel(r'n$\rightarrow$',fontsize=12)
    pylab.ylabel(r'$Coefficient\rightarrow$',fontsize=12)
    pylab.title('Loglog Plot of coefficients of '+func,fontsize=15)
    pylab.legend(loc='lower left')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def compute_deviation(c, coeff, function, func):
    dev = abs(coeff - c)
    approximation = np.matmul(A,c)
    x = np.linspace(0,2*np.pi,401)
    x = x[:-1]
    pylab.semilogy(x,approximation,'go',label="Function Approximation")
    pylab.semilogy(x,function(x),'-r',label='True value')
    pylab.grid(True)
    pylab.xlabel(r'n$\rightarrow$',fontsize=12)
    pylab.ylabel(r'$f(x)\rightarrow$',fontsize=12)
    pylab.title('Plot of ' + func + ' and its Fourier series approximation',fontsize=12)
    pylab.legend(loc='upper left')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

fignum = [1]
plot_functions()
exp_coeff = fourier_transform(51, exp)
coscos_coeff = fourier_transform(51, coscos)
plot_coefficients(exp_coeff, "$e^{x}$")
plot_coefficients(coscos_coeff, "$cos(cos(x))$")

A, c_exp = solve(exp)
A, c_coscos = solve(coscos)

plot_comparison(c_exp, exp_coeff, "$e^{x}$")
plot_comparison(c_coscos, coscos_coeff, "$cos(cos(x))$")

compute_deviation(c_exp, exp_coeff, exp, "$e^{x}$")
compute_deviation(c_coscos, coscos_coeff, coscos, "$cos(cos(x))$")


