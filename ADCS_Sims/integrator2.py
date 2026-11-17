# -*- coding: utf-8 -*-
"""
inertia equations rewritten to accomadate full inertia tensor rather than just principal axes
"""

import quaternion
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt



def W_world(q):
    """
    quaternion rate matrix in world coordinates

    """
    q0, q1, q2, q3 = q
    
    return np.array([
        [-q1, q0, -q3, q2 ],
        [-q2, q3, q0, -q1],
        [-q3, -q2, q1, q0]
        ])

def W_body(q):
    """
    quaternion rate matrix in body coordinates

    """
    q0, q1, q2, q3 = q
    
    return np.array([
        [-q1, q0, q3, -q2 ],
        [-q2, -q3, q0, q1],
        [-q3, q2, -q1, q0]
        ])



def get_state_dot(t, state_vec, I, body=True):
    
    
    omega = state_vec[0:3]
    q = state_vec[3:7]
    
    
    # solve general Euler rotation equation: I*omega_dot + omega x (I*omega) = M
    M = np.zeros((3))
    b = M - np.cross(omega, I @ omega)
    omega_dot1, omega_dot2, omega_dot3 = np.linalg.solve(I, b)
    
    
    
    if body:
        W = W_body(q)
    else:
        W = W_world(q)
    
    q_dot = 0.5 * W.T @ omega
    
    
    state_dot = np.array([
        omega_dot1,
        omega_dot2,
        omega_dot3,
        q_dot[0],
        q_dot[1],
        q_dot[2],
        q_dot[3],
        ])    
    
    return state_dot





# initial conditions

# omega datasets
OS1 = np.array([0.02, 0.04, 0.06]) # from [14]

OS4 = np.array([0.01, 0.13, 0.11])
OS5 = np.array([0.098, 0.356, 0.014]) 
OS6 = np.array([0.05, 0.15, 0.1])

omega_i = OS4

q_i = np.array([1, 0, 0, 0])     # normalized q

# inertia tensor datasets
IS4 = np.array([ # kg m^2
    [1000, -100, 500],
    [-100, 4000, 300],
    [500, 300, 5000],
    ])

IS5 = np.array(
    [[ 1.21632284e+04,  2.17227273e+00, -9.37096364e+00],
 [ 2.17227273e+00,  3.97001541e+04, -4.55161091e+01],
 [-9.37096364e+00, -4.55161091e+01,  3.20344781e+04]]
    )

IS6 = np.array([
    [1000, -100, -150],
    [-100, 800, -200],
    [-150, -200, 960],
    ])

I = IS6

"""
for i in range(I.size):
    if I[i] >= sum(I) - I[i]:
        raise ValueError('inertia values violate triangle inequality')
            """
        

state_vec_i = np.append(omega_i, q_i)

rate_truth = 30 # Hz, also determines fps for the 3D visualization module
seconds_per_step = 1/rate_truth

t_f = 100 # duration in seconds
n_steps_truth = int(t_f * rate_truth)
t_span = (0, t_f)
t_eval = np.linspace(0, t_f, n_steps_truth)




# get solution
sol = solve_ivp(get_state_dot, t_span , state_vec_i, t_eval=t_eval, args = (I,), rtol=1e-9, atol=1e-12)

sol_omega = sol.y[0:3]
sol_omega_mags = np.linalg.norm(sol_omega, axis=0)

sol_q = sol.y[3:7]




# NORMALIZE 2D ARRAY (of quaternions) 
sol_q_mags = np.linalg.norm(sol_q, axis=0)   # should all be =1
sol_q = sol_q / sol_q_mags


"""
# check conservation of angular momentum and rotational kinetic energy
H_vec = np.zeros((3,n_steps_truth))
H_mags = np.zeros(n_steps_truth)
T = np.copy(H_mags)

for i in range(np.size(sol_omega, 1)):
    H_vec[:,i] = I * sol_omega[:,i]                     # H = I * omega
    H_mags[i] = (np.linalg.norm(H_vec[:,i]))
    #T[i] = .5 * sol_omega[:,i] @ H_vec[:,i]             # T = 0.5 * omega * H
    T[i] = 0.5 * (I[0] * sol_omega[0,i]**2 + I[1] * sol_omega[1,i]**2 + I[2] * sol_omega[2,i]**2)
"""


if __name__ == '__main__':

    # plot angular velocity
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    
    ax1.plot(sol.t, sol_omega[0], label='$ω_1$')
    ax1.plot(sol.t, sol_omega[1], label='$ω_2$')
    ax1.plot(sol.t, sol_omega[2], label='$ω_3$')
    ax1.set_ylabel('Angular Velocity (rad/s)')
    ax1.set_xlabel('Time (s)')
    ax1.legend()
    ax1.set_title('Angular Velocity')
    ax1.grid(True)
    
    # plot quaternion components
    ax2.plot(sol.t, sol_q[0], label='$q_0$ (real)')
    ax2.plot(sol.t, sol_q[1], label='$q_1$')
    ax2.plot(sol.t, sol_q[2], label='$q_2$')
    ax2.plot(sol.t, sol_q[3], label='$q_3$')
    ax2.set_ylabel('Quaternion Components')
    ax2.set_xlabel('Time (s)')
    ax2.legend()
    ax2.set_title('Attitude (Unit Quaternion)')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()
    


sol_omega=sol_omega.T
    

export = False
if export:
    import os

    # Folder where test.py lives — update this to your actual path
    test_dir = r"C:\Users\MCLART\projects"

    np.save(os.path.join(test_dir, "sol_q.npy"), sol_q.T)

    np.savetxt(
        os.path.join(test_dir, "sol_q.csv"),
        sol_q.T,
        delimiter=",",
        header="q0,q1,q2,q3",
        comments=""
    )

    print(f"Saved sol_q.npy and sol_q.csv to {test_dir}")