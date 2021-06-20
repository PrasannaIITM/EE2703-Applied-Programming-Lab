import numpy as np 
import pylab
import sys
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from scipy.linalg import lstsq
if(len(sys.argv)==5):#use inputs provided by the user
    Nx=int(sys.argv[1])
    Ny=int(sys.argv[2])
    radius=int(sys.argv[3])  
    Niter=int(sys.argv[4])
else:#use default parameters
    Nx=25 
    Ny=25 
    radius=8 
    Niter=1500 

#initialise
fignum = [0]
phi=np.zeros((Nx,Ny),dtype = float)
x,y=np.linspace(-0.5,0.5,num=Nx,dtype=float),np.linspace(-0.5,0.5,num=Ny,dtype=float)
Y,X=np.meshgrid(y,x,sparse=False)
phi[np.where(X**2+Y**2<(0.35)**2)]=1.0



def plot_potential_config():
    pylab.contourf(Y,X,phi,cmap=pylab.cm.get_cmap("autumn"))
    pylab.xlabel(r'x$\rightarrow$',fontsize=15)
    pylab.ylabel(r'y$\rightarrow$',fontsize=15)
    plt.colorbar()
    pylab.title('Potential Configuration')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def update_phi(phi,phiold):
    phi[1:-1,1:-1]=0.25*(phiold[1:-1,0:-2]+ phiold[1:-1,2:]+ phiold[0:-2,1:-1] + phiold[2:,1:-1])
    return phi

def boundary(phi,mask = np.where(X**2+Y**2<(0.35)**2)):
    #Left
    phi[:,0]=phi[:,1]
    #Right
    phi[:,Nx-1]=phi[:,Nx-2] 
    #Top 
    phi[0,:]=phi[1,:] 
    #Bottom
    phi[Ny-1,:]=0
    #wire
    phi[mask]=1.0
    return phi
    
def plot_semilog_error():
    plt.title("Error on a semilog plot")
    plt.xlabel("No of iterations")
    plt.ylabel("Error")
    plt.semilogy(range(Niter),err)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def plot_loglog_error():
    plt.title("Error on a loglog plot")
    plt.xlabel("No of iterations")
    plt.ylabel("Error")
    plt.loglog((np.asarray(range(Niter))+1),err)
    plt.loglog((np.asarray(range(Niter))+1)[::50],err[::50],'ro')
    plt.legend(["real","every 50th value"])
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def fit(y, Niter, lastn = 0):
    log_err = np.log(err)[-lastn:]
    X = np.vstack([(np.arange(Niter)+1)[-lastn:],np.ones(log_err.shape)]).T
    log_err = np.reshape(log_err,(1,log_err.shape[0])).T
    return lstsq(X, log_err)[0]


def plot_errors(err,Niter,a,a1,b,b1):
    #loglog
    plt.title("Best fit for error on a loglog scale")
    plt.xlabel("No of iterations")
    plt.ylabel("Error")
    x = np.asarray(range(Niter))+1
    plt.loglog(x,err)
    plt.loglog(x[::100],np.exp(a + b*np.asarray(range(Niter)))[::100],'ro')
    plt.loglog(x[::100],np.exp(a1 + b1*np.asarray(range(Niter)))[::100],'go')
    plt.legend(["errors","fit1","fit2"])
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()
    #semilog
    plt.title("Best fit for error on a semilog scale")
    plt.xlabel("No of iterations")
    plt.ylabel("Error")
    plt.semilogy(x,err)
    plt.semilogy(x[::100],np.exp(a+b*np.asarray(range(Niter)))[::100],'ro')
    plt.semilogy(x[::100],np.exp(a1+b1*np.asarray(range(Niter)))[::100],'go')
    plt.legend(["errors","fit1","fit2"])
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def net_error(a,b,Niter):
    return -a/b*np.exp(b*(Niter+0.5))

def plot_cum_error():
    iter=np.arange(100,1501,100)
    plt.grid(True)
    plt.title(r'Plot of Cumulative Error values On a loglog scale')
    plt.loglog(iter,np.abs(net_error(a1,b1,iter)),'ro')
    plt.xlabel("iterations")
    plt.ylabel("maximum error")
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def plot_2D_contour_plot():
    plt.title("2D Contour plot of potential")
    plt.xlabel("X")
    plt.ylabel("Y")
    x_c,y_c=np.where(X**2+Y**2<(0.35)**2)
    #plt.plot((x_c-Nx/2)/Nx,(y_c-Ny/2)/Ny,'ro')
    plt.contourf(Y,X[::-1],phi)
    plt.colorbar()
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def plot_3D_surface_plot():
    fig1=plt.figure(0)     
    ax=p3.Axes3D(fig1)
    plt.title('The 3-D surface plot of the potential')
    surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1, cmap=plt.cm.jet)
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()

def plot_current_density():
    Jx,Jy = (1/2*(phi[1:-1,0:-2]-phi[1:-1,2:]),1/2*(phi[:-2,1:-1]-phi[2:,1:-1]))
    plt.title("Vector plot of current flow")
    plt.quiver(Y[1:-1,1:-1],-X[1:-1,1:-1],-Jx[:,::-1],-Jy)
    x_c,y_c=np.where(X**2+Y**2<(0.35)**2)
    plt.plot((x_c-Nx/2)/Nx,(y_c-Ny/2)/Ny,'ro')
    pylab.savefig('fig{}.png'.format(fignum[0]))
    fignum[0] += 1
    pylab.close()




plot_potential_config()

err = np.zeros(Niter)
for k in range(Niter):
    phiold = phi.copy()
    phi = update_phi(phi,phiold)
    phi = boundary(phi)
    err[k] = np.max(np.abs(phi-phiold))


#semilog plot
plot_semilog_error()

#loglog plot
plot_loglog_error()


b,a = fit(err,Niter)#all
b1,a1 = fit(err,Niter,Niter-500)#after 500
plot_errors(err, Niter, a, a1, b, b1)
plot_cum_error()
plot_2D_contour_plot()
plot_3D_surface_plot()
plot_current_density()
