'''
EE2703 Endsem
Author: Prasanna Bartakke <ee19b106@smail.iitm.ac.in>
'''
from pylab import *

def plot_sections():
	#plot the locations of the sections
	scatter(r_[:,0], r_[:,1])
	grid()
	xlabel(r"$x$", size = 12)
	ylabel(r"$y$", size = 12)
	title("Location of the sections")
	savefig('fig{}.png'.format(fignum[0]))
	fignum[0] += 1
	close()

def plot_current(I):
	#plot the direction of current at each section
	Ix, Iy = I[:,0], I[:,1]
	quiver(r_[:,0], r_[:,1], Ix, Iy, scale=5000)
	grid()
	xlabel(r"$x$", size = 12)
	ylabel(r"$y$", size = 12)
	title("Current Plot")
	savefig('fig{}.png'.format(fignum[0]))
	fignum[0] += 1
	close()

def create_loop_locations():
	#r_ contains coordinates of the sections of the loop 
	rx = expand_dims(a * cos(phi), axis = -1)
	ry = expand_dims(a * sin(phi), axis = -1)
	rz = expand_dims(zeros(N), axis = -1)
	r_ = hstack((rx, ry, rz))
	return r_

def create_current():
	#current 
	Ix = 4*pi*expand_dims(-a * cos(phi) * sin(phi), axis = -1)
	Iy = 4*pi*expand_dims(a * cos(phi) * cos(phi), axis = -1)
	Iz = 4*pi*expand_dims(zeros(N), axis = -1)
	I = hstack((Ix, Iy, Iz))
	return I

def create_current1():
	#current 
	Ix1 = 4*pi*expand_dims(-a * abs(cos(phi)) * sin(phi), axis = -1)
	Iy1 = 4*pi*expand_dims(a * abs(cos(phi)) * cos(phi), axis = -1)
	Iz1 = 4*pi*expand_dims(zeros(N), axis = -1)
	I1 = hstack((Ix1, Iy1, Iz1))
	return I1

def create_dl_bar():
	dl=2*np.pi*10/N*vstack((-sin(phi), cos(phi)))   #dl_bar = dl * phi_cap
	dl = dl.T
	return dl


def create_points():
	#generate x, y, z coordinates of all the required points
	x = arange(-1, 2, 1)
	y = arange(-1, 2, 1)
	z = arange(1,1001,1)

	X, Y, Z = meshgrid(x,y,z)
	r = zeros((3,3,1000,3))
	r[:,:,:,0] = X
	r[:,:,:,1] = Y
	r[:,:,:,2] = Z
	return x, y, z, r

def calc(l):
	return norm(r - r_[l], axis=-1)

def calc_extended(l):
	R = norm(tile(r, 100).reshape(3, 3, 1000, 100, 3) - r_, axis = -1)   
	ai = sum(cos(phi) * exp(-1j * R/10) * dl[:,l] / R, axis = -1)
	#ai = sum(cos(phi) *  dl[:,l] / R, axis = -1)						#static magnetic field 
	return ai

def calculate_A():
	A = zeros((3,3,1000,2), dtype=complex) #A_x, A_y -> last dimension
	for l in range(2):
		A[:,:,:, l] = calc_extended(l)
	return A

def calc_extended1(l):
	R = norm(tile(r, 100).reshape(3, 3, 1000, 100, 3) - r_, axis = -1)   
	ai = sum(abs(cos(phi)) * exp(-1j * R/10) * dl[:,l] / R, axis = -1)
	#ai = sum(cos(phi) *  dl[:,l] / R, axis = -1)						#static magnetic field 
	return ai

def calculate_A1():
	A = zeros((3,3,1000,2), dtype=complex) #A_x, A_y -> last dimension
	for l in range(2):
		A[:,:,:, l] = calc_extended1(l)
	return A

def plot_B(Bz):
	loglog()
	grid()
	plot(z,abs(Bz))
	xlabel(r"$z$", size = 12)
	ylabel(r"$|\vec B|$", size = 12)
	title(r"$|\vec B|$ vs $z$ loglog plot")
	savefig('fig{}.png'.format(fignum[0]))
	fignum[0] += 1
	close()

def fit(Bz):
	a = hstack([ones(len(Bz[k : ]))[:,np.newaxis], log(z[k : ])[:,np.newaxis]])
	log_c, b = lstsq(a, log(abs(Bz[k : ])), rcond = None)[0]
	c = exp(log_c)
	return c, b

def plot_diff(Bz):
	y = [c*pow(zi, b) for zi in z[k:]]
	plot(z[k:], abs(Bz[k:]))
	plot(z[k:], y)
	legend(["approximate value", "original value"])
	xlabel(r"$z$", size = 12)
	ylabel(r"$|\vec B|$", size = 12)
	title(r"Plot of original $|\vec B|$ vs $z$ and approximate $|\vec B|$ vs $z$")
	savefig('fig{}.png'.format(fignum[0]))
	fignum[0] += 1
	close()

fignum = [0]
print("Note : The plots are being saved in the current directory")
N = 100							      #number of sections of loop
a = 10							      	      #radius of the loop
phi = linspace(0, 2 * pi, N + 1)[:-1] #angle of each section

r_ = create_loop_locations()

plot_sections()

#given current
I = create_current()

dl = create_dl_bar()

plot_current(I)

x, y, z, r = create_points()

A = calculate_A()

#calculate Bz
#A[:,:,:,0] = Ax
#A[:,:,:,1] = Ay

Bz = (A[1, 2, :, 1] - A[2, 1, :, 0] - A[1, 0, :, 1] + A[0, 1, :, 0]) / 4



plot_B(Bz)

k = 50    							  #start after kth point
c, b = fit(Bz)
print("The value of coefficients in the first case are c = {:.2f}, b = {:.2f}, if B = cz^b".format(c, b))
plot_diff(Bz)


#using mod(cos(phi)) in the current so that it is anticlockwise in entire circle
I1 = create_current1()

plot_current(I1)

A1 = calculate_A1()

Bz1 = (A1[1, 2, :, 1] - A1[2, 1, :, 0] - A1[1, 0, :, 1] + A1[0, 1, :, 0]) / 4

plot_B(Bz1)

k = 50    							  #start after kth point
c, b = fit(Bz1)
print("The value of coefficients in the second case are c = {:.2f}, b = {:.2f}, if B = cz^b".format(c, b))
plot_diff(Bz1)

