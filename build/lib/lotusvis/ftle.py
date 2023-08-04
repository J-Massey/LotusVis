import numpy as np


def computeFTLE(self, r, shape, grid, t0, t1, dt):

        # FORWARD vs BACKWARD
        sign = 1
        if(t1<t0): sign = -1

        # integrate in time
        for time in np.arange(t0, t1, sign*dt):
            k1 = dt*self.at(r,time)
            k2 = dt*self.at(r+0.5*k1,time+0.5*dt)
            k3 = dt*self.at(r+0.5*k2,time+0.5*dt)
            k4 = dt*self.at(r+k3,time+dt)
            r += sign*(k1+2*k2+2*k3+k4)/6

        # compute jacobian
        X = r[:,0].reshape(shape)
        Y = r[:,1].reshape(shape)
        FTLE = Jacobian(X, Y, grid[0], grid[1])

        return np.log(np.sqrt(FTLE[1:-1,1:-1]))


def Jacobian(X,Y,dx,dy):

    # shapes
    nx, ny = X.shape

    # storage arrays
    J = np.empty([2,2],float)
    FTLE = np.empty([nx,ny],float)
    
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            J[0,0] = (X[i+1,j]-X[i-1,j])/(2*dx)
            J[0,1] = (X[i,j+1]-X[i,j-1])/(2*dy)
            J[1,0] = (Y[i+1,j]-Y[i-1,j])/(2*dx)
            J[1,1] = (Y[i,j+1]-Y[i,j-1])/(2*dy)
			
			# Green-Cauchy tensor
            C = np.dot(np.transpose(J),J)
			# its largest eigenvalue
            lamda = np.linalg.eigvals(C)
            FTLE[i,j] = max(lamda)
    return FTLE