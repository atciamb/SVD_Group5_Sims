# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:01:58 2024

@author: campbr3
This module contains functions and classes for solving ODEs
"""
import numpy as np
import find_root
class ODESolver(object):
    """abstract ODE solver Base Class"""
    def __init__(self, dynamics1):
        """this initializes whatever ODE solver class that you are trying to create
        ins and outs:
        Ins: dynamics, an instance of the growth class
        outs: Initialized thing"""
        self.dynamics=dynamics1
    def solve_ivp(self, tspan, u0, num_steps):
        """This function sets up to solve the IVP differential equation
        ins and outs:
        inputs: tspan, A 1D array of t values that span the part, u0 a 1d array with just the initial U value, num_steps is the number of steps you want to take\
        outputs: The solved ivp"""
        if tspan[0]>tspan[1]:
            raise ValueError("End T is earlier than start T")
        if type(num_steps)!=int:
            raise TypeError("Num steps must be an int")
        if num_steps<1:
            raise ValueError("Number of steps cannot be less than 1")
        if type(u0)!=np.ndarray:
            raise TypeError("u0 must be numpy ndarray")
        if u0.ndim>1:
            raise ValueError("u0 must be a 0d or 1d ndarray")
        t=np.linspace(tspan[0], tspan[1], num=num_steps+1)
        u=np.zeros((np.size(u0),np.size(t)))
        if np.ndim(u0)>0:
            for i in range(u.shape[0]):
                u[i][0]=u0[i]
        else:
            u[0][0]=u0
        for j in range(u.shape[0]):
            for i in range(t.shape[0]-1):
               u[j,i+1]=self.step(t[i],t[i+1]-t[i], u[j][i])
        return(t, u)
    def step(self, t_old, dt, u_old):
        """Placeholder function to make sure that it is not used, needs to be used in a subclass
        ins and outs:
        t_old, dt, u_old
        step"""
        raise NotImplementedError("Do not call this function in this class, it is for the subclasses")
class ForwardEuler(ODESolver):
    """subclass of base class for solving using forward euler"""
    def step(self, t_old, dt, u_old):
        """computes one step of forward euler
        ins and outs:
        Ins: t_old, old t, dt, the delta t that you are caclulating over, u_old the old thing that you are calculating
        outs: the u after one step of forwards euler"""
        u_new=(u_old+(dt*(self.dynamics.func(t_old,u_old))))
        return(u_new)
class ExplicitMidpoint(ODESolver):
    """subclass of base class for solving using explicit midpoint"""
    def step(self, t_old, dt, u_old):
        """computes one step of explicit midpoint
        ins and outs:
        Ins: t_old, old t, dt, the delta t that you are caclulating over, u_old the old thing that you are calculating
        outs: the u after one step of explicit midpoint"""
        k1=dt*self.dynamics.func(t_old,u_old)
        k2=dt*self.dynamics.func(t_old+(1/2)*dt,u_old+(1/2)*k1)
        u_new=u_old+k2
        return(u_new)
class RungeKutta4th(ODESolver):
    """subclass of base class for solving using rk4"""
    def step(self, t_old, dt, u_old):
        """computes one step of rk4
        ins and outs:
        Ins: t_old, old t, dt, the delta t that you are caclulating over, u_old the old thing that you are calculating
        outs: the u after one step of explicit midpoint"""
        k1=dt*self.dynamics.func(t_old,u_old)
        k2=dt*self.dynamics.func(t_old+(1/2)*dt,u_old+(1/2)*k1)
        k3=dt*self.dynamics.func(t_old+(1/2)*dt,u_old+(1/2)*k2)
        k4=dt*self.dynamics.func(t_old+dt,u_old+k3)
        u_new=u_old+((1/6)*(k1+(2*k2)+(2*k3)+k4))
        return(u_new)
class BackwardEuler(ODESolver):
    """subclass of base class for solving using backward euler"""
    def step(self, t_old, dt, u_old):
        """computes one step of backward euler
        ins and outs:
        Ins: t_old, old t, dt, the delta t that you are caclulating over, u_old the old thing that you are calculating
        outs: the u after one step of baclward euler"""
        u_guess=ForwardEuler.step(self, t_old, dt, u_old)
        def resid(u_new):
            f=u_old+(dt*self.dynamics.func((t_old+dt),u_new))-u_new
            df=dt*self.dynamics.jac(t_old+dt,u_new)-1
            return(f, df)
        u_new, turns=find_root.newton(resid, u_guess)
        return(u_new)