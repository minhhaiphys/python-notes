""" Animation for macrospin demos
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


def angle2xyz(thetas,phis):
    """ Convert spherical coordinates to Cartesian ones
    """
    xs = np.sin(thetas)*np.cos(phis)
    ys = np.sin(thetas)*np.sin(phis)
    zs = np.cos(thetas)
    return xs,ys,zs

def xyz2angle(xs,ys,zs):
    """ Convert Cartesian coordinates to spherical ones
    """
    rs = np.linalg.norm(np.array([xs,ys,zs]).transpose(),axis=1)
    thetas = np.arccos(zs/rs)
    # Because arccos returns value between 0 and pi, we need to take care of the other quadrants ourselves
    # signs = (np.sign(ys)-1)/2 # If y is positive, returns 0; if negative, return -1
    signs = np.sign(ys)
    phis = np.arccos(xs/np.linalg.norm(np.array([xs,ys]).transpose(),axis=1))*signs
    return thetas,phis

class SpinAnimation(object):
    """ Spin Animation: animated macrospin dynamics
    data: 2 arrays (theta,phi) or 3 arrays (x,y,z)
    view: 'angle' (default) or 'xyz'
    fps: number of frames per second, default = 25
    average: number of data points in each step, default = 1
    """
    def __init__(self,data,view='angle',fps=25,average=1):
        super(SpinAnimation,self).__init__()
        self.data = data
        self.view = view
        self.fps = fps
        self.avg = max(average,1)
        self.update_params()

    def update_params(self,**kwargs):
        """ Update parameters """
        for k,v in kwargs.items():
            if k in self.keys():
                setattr(self,k,v)
        self.fps = max(min(self.fps,25),1) # Maximum 25 frames per second, enough for human eyes
        self.data = np.array(self.data).transpose()
        # Check shape of data
        if len(self.data.shape)!=2:
            print("Error: Cannot handle array with dimension = %d" %(len(self.data.shape)))
            self.data = None
        else:
            Ncols = self.data.shape[1]
            if Ncols==2:
                # First column = thetas; Second column = phis
                self.thetas = np.flipud(self.data[:,0][::-self.avg])
                self.phis = np.flipud(self.data[:,1][::-self.avg])
                # Calculate Cartesian coordinates
                self.xs, self.ys, self.zs = angle2xyz(self.thetas,self.phis)
            elif Ncols==3:
                # Array of (xs,ys,zs)
                self.xs = np.flipud(self.data[:,0][::-self.avg])
                self.ys = np.flipud(self.data[:,1][::-self.avg])
                self.zs = np.flipud(self.data[:,2][::-self.avg])
                # Convert to polar coordinates
                self.thetas, self.phis = xyz2angle(self.xs,self.ys,self.zs)
            else:
                print("Error: Cannot handle data with %d columns" %Ncols)
                self.data = None

    def init_figure(self,*args,**kwargs):
        self.fig = plt.figure(*args,**kwargs)
        self.ax1 = self.fig.add_subplot(2,2,1,projection='3d')
        self.ax2 = self.fig.add_subplot(2,2,2)
        self.ax3 = self.fig.add_subplot(2,2,3)
        self.ax4 = self.fig.add_subplot(2,2,4)
        # Set axis labels
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("y")
        self.ax1.set_zlabel("z")
        if self.view=="angle":
            self.ax2.set_xlabel("t")
            self.ax2.set_ylabel("theta")
            self.ax3.set_xlabel("t")
            self.ax3.set_ylabel("phi")
            self.ax4.set_xlabel("phi")
            self.ax4.set_ylabel("theta")
        else:
            self.ax2.set_xlabel("x")
            self.ax2.set_ylabel("z")
            self.ax3.set_xlabel("y")
            self.ax3.set_ylabel("z")
            self.ax4.set_xlabel("x")
            self.ax4.set_ylabel("y")
        # Set axis limits
        self.ax1.set_xlim3d(min(self.xs),max(self.xs))
        self.ax1.set_ylim3d(min(self.ys),max(self.ys))
        self.ax1.set_zlim3d(min(self.zs),max(self.zs))
        if self.view=="angle":
            self.ax2.set_xlim(0,len(self.xs))
            self.ax2.set_ylim(0,np.pi)
            self.ax3.set_xlim(0,len(self.xs))
            self.ax3.set_ylim(-np.pi,np.pi)
            self.ax4.set_xlim(-np.pi,np.pi)
            self.ax4.set_ylim(0,np.pi)
        else:
            self.ax2.set_xlim(min(self.xs),max(self.xs))
            self.ax2.set_ylim(min(self.zs),max(self.zs))
            self.ax3.set_xlim(min(self.ys),max(self.ys))
            self.ax3.set_ylim(min(self.zs),max(self.zs))
            self.ax4.set_xlim(min(self.xs),max(self.xs))
            self.ax4.set_ylim(min(self.ys),max(self.ys))

    def plot(self,i=None):
        # Remove existing lines to clean up the plots
        for axis in plt.gcf().axes:
            for line in axis.lines:
                line.remove()
        if i is None:
            i = len(self.xs) # Draw all data points
        i = min(i,len(self.xs)) # Just in case some idiot specifies i > lenth of data
        self.ax1.plot(self.xs[:i],self.ys[:i],self.zs[:i],linestyle='-',linewidth=1,color='b')
        if i>0: # Draw a tracing red dot
            self.ax1.plot([self.xs[i-1]],[self.ys[i-1]],[self.zs[i-1]],marker='o',color='r')
        if self.view=="angle":
            self.ax2.plot(self.thetas[:i],linestyle='-',linewidth=1,color='b')
            self.ax3.plot(self.phis[:i],linestyle='-',linewidth=1,color='b')
            self.ax4.plot(self.phis[:i],self.thetas[:i],linestyle='-',linewidth=1,color='b')
        else:
            self.ax2.plot(self.xs[:i],self.zs[:i],linestyle='-',linewidth=1,color='b')
            self.ax3.plot(self.ys[:i],self.zs[:i],linestyle='-',linewidth=1,color='b')
            self.ax4.plot(self.xs[:i],self.ys[:i],linestyle='-',linewidth=1,color='b')
        plt.draw()
        return True

    def clear(self):
        pass
        return True

    def animate(self):
        return animation.FuncAnimation(self.fig,self.plot,np.arange(1,len(self.xs)+1),init_func=self.clear,
                                        interval = 1000/self.fps,repeat=False,blit=True)

# Test
if __name__=="__main__":
    xs = np.linspace(-1,1,100)
    thetas = np.arccos(xs)
    phis = np.arcsin(xs)
    ani = SpinAnimation([thetas,phis],average=2,fps=20,view='xyz')
    ani.init_figure(figsize=(10,8))
    ani.animate()
