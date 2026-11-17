#%% -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:33:38 2026

@author: Tevin


State: x = [q, omega]

Measurement: z = noisy quaternion measurements
predicted state: x_hat
predicted measurement: z_hat derived from h(x_hat)
"""

import numpy as np
import matplotlib.pyplot as plt

from integrator2 import sol_q, t_f, rate_truth, omega_i, I, n_steps_truth, W_body 
from quaternion_functions import calc_q_error



#%% 
# initialize
dt = 1 / rate_truth
N = n_steps_truth
t = np.arange(N) * dt

sol_q = sol_q.T   # shape (N, 4)  ground truth, validation only
q0_true = sol_q[:,0]
q1_true = sol_q[:,1]
q2_true = sol_q[:,2]
q3_true = sol_q[:,3]


dim_x = 7 # 4 q + 3 omega components
dim_z = 4 # 4 q components
dim_p = 5 # 5 inertia parameters

dim_x_a = dim_x + dim_p # 12


# set up sampling rate ratios
rate_measure = 2 # Hz
n_steps_measure = int(t_f*rate_measure)
M = n_steps_measure

rate_ratio = int(rate_truth / rate_measure)
sol_q_sample = sol_q[::rate_ratio] # creates sample array of sol_q based on rate of measurements





#%% 
# measurement function
def h(x_hat):
    """
    Returns z_hat, size 4
    """
    
    q = x_hat[:4]
    return q



#%% 
# measurement matrix Jacobian function
def H_jac(x_hat):
    """
    Jacobian of h(x_hat) wrt full augmented state
    Only first 4 columns (quaternion) are nonzero
    Returns H shape 4 x 9
    """
    
    H = np.zeros((dim_z, dim_x))
    H[0:4,0:4] = np.eye(4)
    
    return H


#%% 
# state matrix Jacobian

def F_jac(x_hat_old):
    
    q = x_hat_old[:4]
    omega = x_hat_old[4:7]
    
    F = np.eye(dim_x) # derivatives of q and omega wrt themselves
    
    # q block
    q_omega = np.concatenate(([0], omega))
    q_dot_wrt_q = 0.5 * Q_matrix(q_omega) * dt
    F[0:4, 0:4] += q_dot_wrt_q

    q_dot_wrt_omega = 0.5 * W_body(q).T * dt  
    F[0:4, 4:7] = q_dot_wrt_omega

    
    # omega block
    omega_dot_wrt_omega = np.linalg.inv(I) @ (skew_symmetric(I @ omega) - skew_symmetric(omega) @ I)
    F[4:7, 4:7] += dt * omega_dot_wrt_omega
    
    
    return F

def f(x):
    """
    Nonlinear state propagation, one dt step
    parameters held constant (affected only by Q, not f)
    """
    q = x[:4]
    omega = x[4:7]
    

    # quaternion kinematics
    q_dot = calc_q_dot(q, omega)
    q_new = q + dt * q_dot
    q_new /= np.linalg.norm(q_new)

    
    # solve general Euler rotation equation: I*omega_dot + omega x (I*omega) = M
    omega_dot = calc_omega_dot(omega)
    omega_new = omega + dt * omega_dot


    x_new = np.empty_like(x)
    x_new[:4]  = q_new
    x_new[4:7] = omega_new
    return x_new
    

def calc_q_dot(q, omega):
    """
    returns q_dot based using quaternion rate matrix in body frame
    eq from [6]
    """
    return 0.5 * W_body(q).T @ omega


def calc_omega_dot(omega):
    """
    solve general Euler rotation equation: I*omega_dot + omega x (I*omega) = M
    """
    
    #p1, p2, p3, p4, p5 = p
    
    
    M = np.zeros(3)
    b = M - np.cross(omega, I @ omega)
    return np.linalg.solve(I, b)

def skew_symmetric(vector_3d):
    v = vector_3d
    return np.array([
                     [0, -v[2], v[1],],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]
                     ])


def Q_matrix(q): 
    """
    quaternion matrix for quaternion multiplication, eq from [6]
    """
    q0, q1, q2, q3 = q
    
    return np.array([
        [q0, -q1, -q2, -q3],
        [q1, q0, q3, -q2],
        [q2, -q3, q0, q1],
        [q3, q2, -q1, q0]
        ])



#%% 
# noise matrices


# process noise matrix Q, values from [14]
mag = np.linalg.norm(omega_i)
factor = mag/.074833 # omega mag used in literature
sigma_Q_rot = 0.005 * np.sqrt(factor) # literature suggests 0.005


Q = np.eye(dim_x)
Q[:7,:7] *= sigma_Q_rot**2




# measurement noise matrix R
sigma_R = 0.01
R = np.eye(dim_z) * sigma_R**2


q0_meas = sol_q_sample[:,0] + np.random.normal(0, sigma_R, M)
q1_meas = sol_q_sample[:,1] + np.random.normal(0, sigma_R, M)
q2_meas = sol_q_sample[:,2] + np.random.normal(0, sigma_R, M)
q3_meas = sol_q_sample[:,3] + np.random.normal(0, sigma_R, M)


q_meas = np.column_stack([q0_meas, q1_meas, q2_meas, q3_meas])
q_meas = q_meas / np.linalg.norm(q_meas, axis=1, keepdims=True)


# increasing sigma_Q/sigma_R: more responsive but sensitive to measurement noise
# decreasing sigma_Q/sigma_R: more smooth

#%% 
# initial state x and covariance P
x0 = np.zeros(dim_x)
x0[:4] = q_meas[0]
#x0[4:7] = omega_i


# inertia parameters initialization
Ixx, Iyy, Izz = np.diag(I)
Ixy, Ixz, Iyz = -I[0,1], -I[0,2], -I[1,2]



# initial covariance
P = np.empty((N, dim_x, dim_x))
P0 = np.eye(dim_x)

P0[:4,:4] *= sigma_R**2 # for initial q components
P0[4:,4:] *= 1
P[0] = P0


#%% 
# initialize arrays


# predict arrays, use index k, N steps
x_hat = np.empty((N, dim_x))
x_hat[0] = x0
F = np.empty((N, dim_x, dim_x))


# measurement arrays, use index k_meas, M steps
z = q_meas
z_hat = np.empty_like(z)
y_tilde = np.empty_like(z)

H = np.empty((M, dim_z, dim_x)) 
S = np.empty((M, dim_z, dim_z)) 
K = np.empty((M, dim_x, dim_z))


#%% 
# EKF predict/update loop

for k in range(1,N):
    
    # Step 1: predict
    
    F[k] = F_jac(x_hat[k-1])
    
    # predicted state estimate
    x_hat[k] = f(x_hat[k-1])
    
    # normalize q
    x_hat[k,:4] /= np.linalg.norm(x_hat[k,:4])
    
    
    # predicted covariance of state estimate
    
    P[k] = F[k] @ P[k-1] @ F[k].T + Q
    
    
    # Step 2: update
    
    if k % rate_ratio == 0 and k//rate_ratio < M: # only runs when new measurement "arrives" based on rate_measure; inequality makes sure k_meas doesn't exceed M
    
        k_meas = k // rate_ratio # index used for the measurement arrays
        
        # innovation/measurement residual (difference between actual sensor measurements and predicted sensor measurements)
        z_hat[k_meas] = h(x_hat[k])
        y_tilde[k_meas] = z[k_meas] - z_hat[k_meas]
        
        # measurement matrix
        H[k_meas] = H_jac(x_hat[k])
        
        # innovation/residual covariance
        S[k_meas] = H[k_meas] @ P[k] @ H[k_meas].T + R
        
        # near-optimal Kalman gain
        K[k_meas] = P[k] @ H[k_meas].T @ np.linalg.inv(S[k_meas])
        
        # updated state estimate
        x_hat[k] += K[k_meas] @ y_tilde[k_meas]
        
        # renormalize q
        x_hat[k,:4] /= np.linalg.norm(x_hat[k,:4])
                
        # updated covariance of state estimate
        P[k] = (np.eye(dim_x) - K[k_meas] @ H[k_meas]) @ P[k]
    

q_estimates = x_hat[:, :4]

#%% 
# angle error
q_est_unit = q_estimates / np.linalg.norm(q_estimates, axis=1, keepdims=True)
q_true_unit = sol_q / np.linalg.norm(sol_q, axis=1, keepdims=True)

dots = np.abs(np.sum(q_true_unit * q_est_unit, axis=1))       
angle_errors = np.rad2deg(2 * np.arccos(dots)) # converts q scalar to degrees


# error of each q component
q_errors = q_estimates - sol_q
RMSE_q = np.empty(4)
print()
for i in range(4):
    RMSE_q[i] = np.sqrt(np.sum(q_errors[:,i]**2)/N)
    print(f'RMSE q{i}: {RMSE_q[i]:.4f}')

RMSE_deg = np.sqrt(np.sum(angle_errors**2)/N)


#%% 
# plotting

# plot 1: q components and angle error
fig1, axes1 = plt.subplots(5, 1, figsize=(12, 8), sharex=True)

# q plots
labels = ["$q_0$", "$q_1$", "$q_2$", "$q_3$"]
true_arrays = [q0_true, q1_true, q2_true, q3_true]

for idx, (ax, lbl, truth) in enumerate(zip(axes1[:4], labels, true_arrays)):
    ax.plot(t, truth,"k--",  lw=1, label="x")
    ax.plot(t, q_estimates[:, idx], "b-", lw=1,   label="x̂")
    ax.set_ylabel(lbl)
    ax.grid(True)

axes1[0].legend()

# error plot
axes1[4].plot(t, angle_errors, "r-", lw=1)
axes1[4].set_ylabel("Angle error (deg)")
axes1[4].grid(True)

axes1[-1].set_xlabel("Time (s)")

fig1.suptitle("Quaternion-based Attitude JEKF", fontsize=13)
plt.tight_layout()
plt.show()



print(f'\nRMSE δq: {RMSE_deg:.2f} deg')
print(f'Max angle error: {np.max(angle_errors):.2f} deg')
print(f'Final angle error: {angle_errors[-1]:.2f} deg')
# %%
