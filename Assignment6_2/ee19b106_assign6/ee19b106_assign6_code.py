import numpy as np 
import scipy.signal as sp 
import pylab


def find_H(omega,alpha):
    pol1 = np.poly1d([1, omega])
    pol2 = np.poly1d([1,(2 * omega),((omega * omega)+(alpha * alpha))])
    return pol1, pol2

def plot(x, y, xlabel='t',ylabel='x'):
    pylab.plot(x,y,'-r')
    pylab.xlabel(r'{}'.format(xlabel),fontsize=15)
    pylab.ylabel(r'{}'.format(ylabel),fontsize=15)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def fnc(omega,alpha,t):
    x = np.cos(alpha*t)
    x2 = np.multiply(np.exp(-omega*t),np.heaviside(t,0.5))
    return np.multiply(x,x2)
# Spring system
#decay = 0.5
fignum = [0]
num,den = find_H(0.5,1.5)
den = np.polymul([1,0,2.25], den)
H = sp.lti(num, den)
t = np.linspace(0,50,1000)
sol = sp.impulse(H,T=t)
plot(sol[0],sol[1],'time','x')

#decay = 0.05
num,den = find_H(0.05,1.5)
den = np.polymul([1,0,2.25],den)
H = sp.lti(num,den)
sol = sp.impulse(H,T=t)
plot(sol[0], sol[1],'time','x')

# LTI response over different frequencies of applied force
i = 0
for alpha in np.arange(1.4,1.6,0.05):
    H = sp.lti([1],[1,0,2.25])
    t1 = np.linspace(0,100,1000)
    f,x,_ = sp.lsim(H,fnc(0.05,alpha,t1),t1)
    i += 1
    pylab.subplot(3,2,i)
    pylab.title("f = {}".format(alpha))
    pylab.plot(t1,x,'-r')
pylab.tight_layout()
pylab.savefig('fig{}.png'.format(fignum[0]))
fignum[0] += 1
pylab.close()

# Coupled spring system
t = np.linspace(0,20,1000)
H_x = sp.lti(np.poly1d([1,0,2]),np.poly1d([1,0,3,0]))
sol_x = sp.impulse(H_x,T=t)
H_y = sp.lti(np.poly1d([2]),np.poly1d([1,0,3,0]))
sol_y = sp.impulse(H_y,T=t)
pylab.plot(sol_x[0],sol_x[1])
pylab.plot(sol_y[0],sol_y[1])
pylab.xlabel('time')
pylab.ylabel('signal')
pylab.legend(["x(t)", "y(t)"], loc ="lower right")
pylab.savefig('fig{}.png'.format(fignum[0]))
fignum[0] += 1
pylab.close()


# Two port network
H = sp.lti(np.poly1d([1000000]),np.poly1d([0.000001,100,1000000]))
w,S,phi=H.bode()
pylab.subplot(2,1,1)
pylab.semilogx(w,S)
pylab.ylabel(r'$|H(s)|$')
pylab.subplot(2,1,2)
pylab.semilogx(w,phi)
pylab.ylabel(r'$\angle(H(s))$')
pylab.savefig('fig{}.png'.format(fignum[0]))
fignum[0] += 1
pylab.close()

t = np.linspace(0,30*0.000001,1000)
vi = np.multiply(np.cos(1000*t)-np.cos(1000000*t),np.heaviside(t,0.5))
_,y,svec = sp.lsim(H,vi,t)
plot(t,y,'t',r'$v_{o}(t)$')


t = np.linspace(0,10*0.001,100000)
vi = np.multiply(np.cos(1000*t)-np.cos(1000000*t),np.heaviside(t,0.5))
_,y,svec = sp.lsim(H,vi,t)
plot(t,y,'t',r'$v_{o}(t)$')