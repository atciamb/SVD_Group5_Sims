# plant model start
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.spatial.transform import Rotation as R
#Define Properties
"Placeholders for now, if we have and Idea of what it looks like at a more detailed level, fix"
Jx=0.25
Jy=0.28
Jz=0.16
Jxy=0.004
Jxz=-0.002
Jyz=0.003
J=np.array([[Jx,Jxy,Jxz],[Jxy,Jy,Jyz],[Jxz,Jyz,Jz]])
J_inv=np.linalg.inv(J)
#Fundemental attitude EOM
def attitude_eom(t, state, J, J_inv):
    #upack quatarian vector 
    q=state[:4]
    omega=state[4:7]
    #normalize quaternion to prevent drift during integration
    q=q/np.linalg.norm(q)
    wx,wy,wz=omega
    #quarternon kinomatics
    #dq/dt = 0.5 * omega x q
    #Omega matrix for quaternion kinematics, Spcifically the 4x4 anguluar velocity slew-symmetric matrix
    #Needed as ivp solvers do dot prododuct multiplication not cross product multiplication
    Omega_mat=np.array([
        [0,-wx,-wy,-wz],
        [wx,0,wz,-wy],
        [wy,-wz,0,wx],
        [wz,wy,-wx,0]
    ])
    q_dot=0.5*(Omega_mat@q)
    #eulers equations
    tau_ext=state[7:10]
    #gyroscopic cross coupling term
    gyro_coupling=np.cross(omega,J@omega)
    omega_dot=J_inv@(tau_ext-gyro_coupling)
    return np.concatenate((q_dot,omega_dot,tau_ext))
#Set initial conditions
q0=np.array([1.0,0.0,0.0,0.0])
#With some initial conditions
omega0=np.array([0.01,-0.05,0.07])
#inital forces
tau0=np.array([0.0,0.0,0.0])
state0=np.concatenate((q0,omega0,tau0))
#simulation runner
tspan=(0,100)
sol=solve_ivp(attitude_eom,tspan,state0,args=(J,J_inv),rtol=1e-9,atol=1e-9)
#extract state histories
q_history=sol.y[:4,:].T
omega_history=sol.y[4:7,:].T
tau_history=sol.y[7:10,:].T
#scipy rotation uses scalar-last [x,y,z,w] format so collumns are rolled
q_scipy=np.roll(q_history,-1,axis=1)
euler_history=R.from_quat(q_scipy).as_euler('xyz',degrees=True)
#Plot euler angular rates and attitude
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
ax1.plot(sol.t, omega_history[:, 0], label=r'$\omega_x$')
ax1.plot(sol.t, omega_history[:, 1], label=r'$\omega_y$')
ax1.plot(sol.t, omega_history[:, 2], label=r'$\omega_z$')
ax1.set_ylabel('Angular rate (rad/s)')
ax1.set_title('Torque-free attitude dynamics')
ax1.grid(True)
ax1.legend()
ax2.plot(sol.t, euler_history[:, 0], label=r'$\phi$')
ax2.plot(sol.t, euler_history[:, 1], label=r'$\theta$')
ax2.plot(sol.t, euler_history[:, 2], label=r'$\psi$')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Attitude (deg)')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()

