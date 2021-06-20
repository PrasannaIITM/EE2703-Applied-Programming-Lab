import numpy as np
import scipy.special as sp
import pylab

def g(t, A, B):
    return A * sp.jn(2, t) + B * t

def extract(filename):
    data = []
    data = np.loadtxt(filename, dtype=float)

    time  = np.array(data[:,0])
    y = np.array(data[:,1:])
    

    return time, y

def plotting(time, y):
    pylab.figure(figsize=(7,6))
    for i in range(9):
        pylab.plot(time, y[:,i], label=r'$\sigma$=%.3f'%sigma[i])
    pylab.plot(time, g(time,1.05,-0.105), '-k', label='True Value')
    pylab.legend(loc = 'upper right')
    pylab.ylabel(r'f(t)+noise$\rightarrow$', fontsize=15)
    pylab.xlabel(r't$\rightarrow$', fontsize=15)
    pylab.savefig('data.png')
    pylab.close()


def errorbar_plot(time, y):
    data = y[:,0]
    pylab.errorbar(time[::5], data[::5], sigma[0], fmt='ro', label='errorbar')
    pylab.plot(time, g(time,1.05,-0.105), 'b', label='original')
    pylab.legend(loc='upper right')
    pylab.xlabel(r't$\rightarrow$', fontsize=10)
    pylab.savefig('errorbar_plot.png')
    pylab.close()

def error_function(time, y):
    e = np.zeros((21,21,9))
    A = np.linspace(0,2,21)
    B = np.linspace(-0.2,0,21)

    for k in range(9):
        f = y[:,k]
        for i in range(21):
            for j in range(21):
                e[i][j][k] = np.sum((f -np.array(g(time,A[i],B[j])))**2)/101

    return e, A, B

def contour_plot(e, A, B):
    plot = pylab.contour(A,B,e[:,:,0],20)
    pylab.ylabel(r'B$\rightarrow$')
    pylab.xlabel(r'A$\rightarrow$')
    pylab.clabel(plot,inline=1,fontsize=10)
    #np.unravel_index to obtain the location of the minima in the original array
    a = np.unravel_index(np.argmin(e[:,:,0]),e[:,:,0].shape)
    pylab.plot(A[a[0]],B[a[1]],'o',markersize=3)
    pylab.annotate('(%0.2f,%0.2f)'%(A[a[0]],B[a[1]]),(A[a[0]],B[a[1]]))
    pylab.savefig('contour_plot.png')
    pylab.close()

def plot_error_vs_sigma(erra, errb):
    pylab.plot(sigma,erra,'bo',label='Aerr')
    pylab.plot(sigma,errb,'ro',label='Berr')
    pylab.ylabel(r'Error$\rightarrow$',fontsize=15)
    pylab.xlabel(r'$\sigma_{n}\rightarrow$',fontsize=15)
    pylab.legend(loc='upper left')
    pylab.savefig('error_vs_sigma_plot.png')
    pylab.close()
def plot_error_vs_sigma_log(erra, errb):
    pylab.figure(figsize=(6,6))
    pylab.loglog(sigma,erra,'bo',label='Aerr')
    pylab.loglog(sigma,errb,'ro',label='Berr')
    pylab.xlabel(r'$\sigma_{n}\rightarrow$',fontsize=15)
    pylab.ylabel(r'Error$\rightarrow$',fontsize=15)
    pylab.legend(loc='upper left')
    pylab.savefig('error_vs_sigma_plot_log_scale.png')
    pylab.close()


time, y = extract("fitting.dat")
sigma = np.logspace(-1,-3,9)
plotting(time, y)
errorbar_plot(time, y)

#the matrix equation
fn_column = sp.jn(2,time)
M = pylab.c_[fn_column,time]

A = 1.05; B = -0.105
#parameter array
C = np.array([A,B])
# matrix obtained after matrix multiplication
G = np.matmul(M,C) 
# matrix obtained directly from the function
G1 = np.array(g(time,A,B)) 

print("The matrix g(t, A, B) obtained by both methods is same :", np.array_equal(G,G1))


e, A_ran, B_ran = error_function(time, y)
contour_plot(e, A_ran, B_ran)


#Least mean square estimation
esti = [np.linalg.lstsq(M, y[:,i], rcond=None)[0] for i in range(9)]
esti = np.asarray(esti)

error_in_a = abs(esti[:,0]-A)
error_in_b = abs(esti[:,1]-B)

plot_error_vs_sigma(error_in_a, error_in_b)
plot_error_vs_sigma_log(error_in_a, error_in_b)



