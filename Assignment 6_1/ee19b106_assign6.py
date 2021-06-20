from pylab import *
import pylab
import numpy as np
from prettytable import PrettyTable
import sys

if len(sys.argv)==6:
    n=sys.argv[0]       # spatial grid size.
    M=sys.argv[1]       # number of electrons injected per turn.
    nk=sys.argv[2]      # number of turns to simulate.
    u0=sys.argv[3]      # threshold velocity.
    p=sys.argv[4]       # probability that ionization will occur
    Msig=sys.argv[5]    # deviation of elctrons injected per turn
    param = [n,M,nk,u0,p,Msig]
else:
    param = [100,5,500,5,0.25,2]

def simulate(params):
    n = params[0]
    M = params[1]
    nk = params[2]
    u0 = params[3]
    p = params[4]
    Msig = params[5]
    xx = np.zeros((n*M))  # electron position
    u = np.zeros((n*M))   # electron velocity
    dx = np.zeros((n*M))  # displacement in current turn

    I = []
    V = []
    X = []
    
    for i in range(1, nk):
        ii = where(xx>0)                #indices of positions greater 
                                        #than zero
        dx[ii] = u[ii] + 0.5            #displacement
        xx[ii] += dx[ii]                #update position
        u[ii] += 1                      #update velocity

        overshoot = where(xx[ii]>n)     #contains the indices whose disp, 
                                        #vel, pos have to set to 0
        xx[ii[0][overshoot]] = 0
        u[ii[0][overshoot]] = 0
        dx[ii[0][overshoot]] = 0


        kk = where(u>=u0)               #v greater than threshold
        ll = where(rand(len(kk[0])) <= p)
        kl=kk[0][ll]                    #contains the indices of energetic 
                                        #electrons that suffer collision
        u[kl]=0                         #velocity becomes 0 after collision
        
        rho = rand(len(kl)) 
        xx[kl] = xx[kl]-dx[kl]*rho      #actual value of x where it collides

        I.extend(xx[kl].tolist())

        m = int(rand()*Msig + M)        #number of new electrons to be added
        vacant = where(xx==0)           #empty spaces where electrons 
                                        #can be injected
        nv=(min(n*M-len(vacant),m)) 
        xx[vacant[:nv]]=1               #inject the new electrons
        u[vacant[0][:nv]]=0             #velocity zero
        dx[vacant[0][:nv]]=0            #displacement zero
        X.extend(xx.tolist())
        V.extend(u.tolist())
    return X,V,I
def plot_intensity(u0, p):
    histogram = hist(I,bins=np.arange(0,101,1),rwidth=0.8,color='r')
    title('Intensity histogram with $u_0=$%.2f and p=%.2f'%(u0,p))
    xlabel('$x$')
    ylabel('Intensity')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()
    return histogram
def plot_no_of_elec(u0,p):            #plot the number of electrons vs x
    hist(X,bins=np.arange(0,101,1),rwidth=0.8,color='g')
    title('Number of Electrons vs $x$ with $u_0=$%.2f and p=%.2f'%(u0,p))
    xlabel('$x$')
    ylabel('Number of electrons')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()
def plot_phase_space(u0,p):           #plot the phase space
    plt.plot(X,V,'x',markersize = 5)
    title('Electron Phase Space with $u_0=$%.2f and p=%.2f'%(u0,p))
    xlabel('$x$')
    ylabel('Velocity-$v$')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()
def plot_intensity_map(u0, p):         #plot the intensity map
    x=xpos
    y=population
    fig, (ax) = plt.subplots(nrows=1, sharex=True)
    extent = [min(x), max(x), 0, 1]
    intensity=ax.imshow(y[np.newaxis,:], cmap="gray", aspect="auto", extent=extent)
    ax.set_yticks([])
    ax.set_xlim(extent[0], extent[1])
    plt.title('Intensity map with $u_0=$%.2f and p=%.2f'%(u0,p))
    plt.xlabel('$x$')
    plt.colorbar(intensity)
    plt.tight_layout()
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()
    

fignum = [0]
X,V,I = simulate(param)
histogram = plot_intensity(param[3], param[4])
plot_no_of_elec(param[3], param[4])
plot_phase_space(param[3], param[4])
population = histogram[0]
bins = histogram[1]
xpos = 0.5 * (bins[0:-1] + bins[1:])
plot_intensity_map(param[3], param[4])

table = PrettyTable()
table.add_column("xpos",xpos)
table.add_column("count", population)
print(table)