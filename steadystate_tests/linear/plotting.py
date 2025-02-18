# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 13:45:11 2014

@author: tfuser
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
'''
# Takes in k-matrix and solves for value at t,x,y,z
def F(K,k_max,dk,t,x,y,z):
    out = 0
    for k_x in xrange(-k_max,k_max,dk):
        for k_y in xrange(-k_max,k_max,dk):
            for k_z in xrange(-k_max,k_max,dk):
                out = out + K[t][k_x][k_y][k_z]*np.exp(1j*(k_x*x+k_y*y+k_z*z))
    return out

# Takes in k-matrix and converts to position space matrix
def toPosition(K,k_max,dk,x,y,z):
    X = np.zeros((K.shape[0],len(x),len(y),len(z)))
    for t in xrange(0,1):
        for i in xrange(0,len(x)):
            for j in xrange(0,len(y)):
                for k in xrange(0,len(z)):
                    print 't=',t,' i=',i,' j=',j,' k=',k
                    X[t][i][j][k]=F(K,k_max,dk,t,x[i],y[j],z[k])
    return X
'''

# Takes in X matrix and plots at time t on plane where the dimension d = val
def plotPlane(X,t,d,val):
    plt.figure()    
    if d=='x':
        plt.pcolor(X[t][val][:][:])
        plt.xlabel('y')
        plt.ylabel('z')
    if d=='y':
        plt.pcolor(X[t][:][val][:])
        plt.xlabel('x')
        plt.ylabel('z')
    if d=='z':
        plt.pcolor(X[t][:][:][val])
        plt.xlabel('x')
        plt.ylabel('y')
    plt.colorbar()
    plt.title('')
    plt.draw()
    plt.show()
    
def animatePlane(X,d,val,filename):
    if d=='x':    
        fmin = np.min(X[:,val,:,:])
        fmax = np.max(X[:,val,:,:])
    if d=='y':    
        fmin = np.min(X[:,:,val,:])
        fmax = np.max(X[:,:,val,:]) 
    if d=='z':    
        fmin = np.min(X[:,:,:,val])
        fmax = np.max(X[:,:,:,val]) 
    
    fig = plt.figure(figsize=(5,4))
    gif = anim.FuncAnimation(fig,animate,frames=X.shape[0]-1, fargs=(X,d,val,fmin,fmax))
    gif.save(filename, writer='imagemagick', fps=4)
    
def animate(nframe,X,d,val,fmin,fmax):
    plt.hold(True)    
    plt.clf()
    if d=='x':
        plt.pcolor(X[nframe][val][:][:], vmin=fmin, vmax=fmax)
        plt.xlabel('y')
        plt.ylabel('z')
    if d=='y':  
        plt.pcolor(X[nframe][:][val][:], vmin=fmin, vmax=fmax)
        plt.xlabel('x')
        plt.ylabel('z')
    if d=='z':
        plt.pcolor(X[nframe,:,:,val], vmin=fmin, vmax=fmax)
        plt.xlabel('x')
        plt.ylabel('y')    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.axis([0,X.shape[1],0,X.shape[1]])
    plt.title('t: %f'%(nframe))
    plt.hold(False)    
                        
def main():
    print 'Importing variables...'
    K_x = np.load('K_x.npy')
    K_y = np.load('K_y.npy')
    K_z = np.load('K_z.npy')
    
    params = np.load('params.npy')
    
    print 'Converting to position space...'
    X_x = np.zeros(K_x.shape, dtype=complex)
    X_y = np.zeros(K_y.shape, dtype=complex)    
    X_z = np.zeros(K_z.shape, dtype=complex)       
    for i in xrange(0,K_x.shape[0]-1):
        print 'Time step: ' + str(i)
        X_temp = np.fft.ifftn(K_x[i,:,:,:])
        Y_temp = np.fft.ifftn(K_y[i,:,:,:])
        Z_temp = np.fft.ifftn(K_z[i,:,:,:])
        X_x[i,:,:,:] = X_temp
        X_y[i,:,:,:] = Y_temp
        X_z[i,:,:,:] = Z_temp
    
    X_x = fftshift(X_x,(1,2,3))
    X_y = fftshift(X_y,(1,2,3))
    X_z = fftshift(X_z,(1,2,3))

    print 'Calculating energy'
    energy = X_x**2+X_y**2+X_z**2
    
    plotConv = 1
    conv_arr = np.zeros(energy.shape[0]-2)
    if plotConv == 1:
        for t in range(1,energy.shape[0]-2):
            conv_arr[t-1] = np.linalg.norm(energy[t] - energy[t+1])/np.linalg.norm(energy[t])
            
        print conv_arr
        plt.semilogy(conv_arr)
        plt.xlabel('time step t')
        plt.ylabel('L2 residual error')
        plt.title('residual convergence of linear dampening')
        
        np.save("linear_res_conv",conv_arr)
            
        
            
    
    '''for i in xrange(X_x.shape[0]-1):
    plotPlane(X_x,X_x.shape[0]-1-i,'z',6)
    '''
    plotGraphs = 0
    if plotGraphs == 1:
        print 'Plotting energy...'
        animatePlane(energy,'z',26,'energy.gif')
        print 'Plotting E_x...'
        animatePlane(X_x,'z',26,'E_x.gif')
        print 'Plotting E_y...'
        animatePlane(X_y,'z',26,'E_y.gif')
        print 'Plotting E_z...'    
        animatePlane(X_z,'z',26,'E_z.gif')
    
    
if __name__ == "__main__":
    main()