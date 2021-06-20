from pylab import *

def calculate_dft(function, N, range, phase_limit, x_lim, wrange):
	t = linspace(-range, range, N + 1); t = t[:-1]

	y = function_map[function](t)
	Y = fftshift(fft(y)) / N
	w = linspace(-wrange, wrange, N + 1); w = w[:-1]
	if function == 'gauss' : 
		Y = fftshift(abs(fft(y)))/N
		# Normalizing for the case of gaussian
		Y = Y*sqrt(2*pi) / max(Y)
		Y_ = exp(-w**2/2)*sqrt(2*pi)
		print("max error is {}".format(abs(Y-Y_).max()))
	figure()
	subplot(2, 1, 1)
	plot(w, abs(Y), lw = 2)
	xlim([-x_lim, x_lim])
	ylabel(r"$|y|$", size = 16)
	ttl = title_map[function]
	title(ttl)
	grid(True)
	subplot(2,1,2)
	plot(w,angle(Y),'ro',lw=2)
	ii = where(abs(Y)>phase_limit)
	plot(w[ii], angle(Y[ii]), 'go', lw=2)
	xlim([-x_lim,x_lim])
	ylabel(r"Phase of $Y$", size=16)
	xlabel(r"$k$", size=16)
	grid(True)
	savefig('fig{}.png'.format(fignum[0]))
	fignum[0] += 1
	close()
    

fignum = [0]
title_map = { 'sin': r"Spectrum of $sin(t)$",
			  'am' : r"Spectrum of $(1 + 0.1cos(t))cos(10t)$",
			  'cos3': r"Spectrum of $cos^3(t)$",
			  'sin3': r"Spectrum of $sin^3(t)$",
			  'fm': r"Spectrum of $cos(20t+5cos(t))$",
              'gauss': r"Spectrum of $\exp(-t^2/2)$"}

function_map = { 'sin' : lambda x : sin(5*x),
			 'am' : lambda x : (1 + 0.1 * cos(x))*cos(10*x),
			 'cos3' : lambda x : cos(x)**3,
  			 'sin3' : lambda x : sin(x)**3,
  			 'fm' : lambda x : cos(20*x+5*cos(x)),
             'gauss' : lambda x : exp(-x**2/2) }

calculate_dft('sin', 128, 2*pi, 1e-3, 15, 64)
calculate_dft('am', 512, 4*pi, 1e-3, 15, 64)


#assignment
calculate_dft('cos3', 512, 4*pi, 1e-3, 15, 40)
calculate_dft('sin3',512, 4*pi, 1e-3, 15, 40)
calculate_dft('fm',512, 4*pi, 1e-3, 40, 40)

#vary time range
calculate_dft('gauss',512, 4*pi, 1e-3, 10, 32)
calculate_dft('gauss',512, 8*pi, 1e-3, 10, 32)
calculate_dft('gauss',512, 12*pi, 1e-3, 10, 32)

#vary sampling rates
calculate_dft('gauss',256, 8*pi, 1e-3, 10, 32)
calculate_dft('gauss',1024, 8*pi, 1e-3, 10, 32)





