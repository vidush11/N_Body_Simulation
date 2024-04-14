import numpy as np
import matplotlib.pyplot as plt
import time
import sys
sys.setrecursionlimit(10**5)


class Sun:
    def __init__(self, n, G=1, softening=1, dt=0.001, sun=1000, revolve=False):
        self.G=G
        self.softening= softening
        self.dt=dt

        self.mass=np.ones(n)
        self.positions=np.array(np.random.random((n,2))*2-1)
        self.sun_mass=sun

        
        self.velocities=np.zeros((n,2), dtype=np.float64)
        self.acc=np.zeros((n,2), dtype=np.float64)

        if revolve:
            self.softening=softening if softening<0.000001 else 0.000001
            self.G= G if G<0.1 else 0.1
            self.sun_mass = sun if sun>100000 else 100000
            positions_=self.positions**2
            norm_cons=( (positions_.sum(1))**0.5 )[:, None]
            positions_norm=self.positions/(norm_cons)
            velocities_norm=positions_norm@np.array([[0,1],[-1,0]])
            velocities_constant=(self.G*self.sun_mass/norm_cons)**0.5
            self.velocities=velocities_norm*velocities_constant
            
        self.mass[0]=self.sun_mass
        self.positions[0]=[0,0]
        self.velocities[0]=[0,0]

    def get_acc(self):
        x=self.positions[:,0:1] #it is a 2d array
        y=self.positions[:,1:2] #it is a 2d array
        xdiff=x-x.T
        ydiff=y-y.T

        r=(xdiff**2+ ydiff**2 + self.softening**2)**(-1.5)


        xacc=self.G*((self.mass)@(xdiff*r)) #1d array
        yacc=self.G*((self.mass)@(ydiff*r)) #1d array

        acc=np.array(list(zip(xacc,yacc)))
        return acc
    
    def one_iteration(self):
        acc=self.get_acc()
        vel_inc= acc*self.dt
        pos_inc= self.velocities*self.dt +1/2 * (self.acc * self.dt**2)

        self.velocities+=vel_inc
        self.positions+=pos_inc

    def plot(self, iterations, intensity_by_mass=False, converge=False):
        plt.gca().set_facecolor('black')
        for i in range(iterations):
            
            plt.xlim((-10,10))
            plt.ylim((-10,10))

            colors=( ['#ebc634']+ ['white']*(self.positions.shape[0]-1) )
            if intensity_by_mass:
                alphas=( np.hstack( ([1],self.mass[1:]/((self.mass[1:]**2).sum())**0.5) ) )
                plt.scatter(self.positions[:,0], self.positions[:,1], s=1,alpha=alphas,c=colors)

            else:
                plt.scatter(self.positions[:,0], self.positions[:,1], s=1, c=colors)

            plt.pause(0.000001)
            self.one_iteration()
            if converge and i>10:
                self.update()

            plt.cla()

            # if ((self.velocities)<10**(-1)).all(): //minimizing centre of mass deviation
            #     print(i)
            #     print((self.positions*np.array([[1],[-1]])).sum(axis=0))
        
        plt.close()
        plt.show()

    def update(self, threshold=10**-3):
        x=self.positions[:,0:1]
        y=self.positions[:,1:2]

        xdiff=x-x.T
        ydiff=y-y.T

        indices= (np.abs(xdiff)<threshold) & (np.abs(ydiff)<threshold)
        indices=np.tril(indices,k=-1)
        dels=np.argwhere(indices)

        del_rows=np.unique(dels[:,0], return_index=True)[1]

        dels=dels[del_rows,:]

        for pair in dels:
            i,j=pair

            self.acc[j]=(self.acc[j]*self.mass[j]+self.acc[i]*self.mass[i])/ (self.mass[j]+self.mass[i])
            self.positions[j]=(self.positions[j]*self.mass[j]+self.positions[i]*self.mass[i])/ (self.mass[j]+self.mass[i])
            self.mass[j]+=self.mass[i]

        del_particles=dels[:,0]

        if del_particles.size>0:
            print(del_particles)
        self.mass=np.delete(self.mass, del_particles, axis=0)
        self.positions=np.delete(self.positions, del_particles ,axis=0)
        self.velocities=np.delete(self.velocities, del_particles ,axis=0)
        self.acc=np.delete(self.acc, del_particles ,axis=0)

            
        


    def abc():
        pass

gravity=Sun(1000,revolve=True)
gravity.plot(100000, converge=True, intensity_by_mass=True)
