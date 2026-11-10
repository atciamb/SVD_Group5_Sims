import numpy as np
import matplotlib.pyplot as plt

# constants and system parameters
c = 2.998e8; q = 1.602e-19 #m/s, elec charge (C)
R = 200.0; P_out = 10e-3*.9 #laser power, 10% loss collimator
D_rx = 0.025; eta_cc = 0.6; eta_rx = 0.5 #receiver lens dia (m), corner cube efficiency, receiver efficiency
f_tone = 100e6 #Hz
sigma_R = 0.25e-3 / 3 # allowed 1sig noise
B = 1000.0; m = 0.8 # noise bandwidth, modul depth
R0 = 0.4; F = 4.0   #silicon det. respons (A/W), apd moise at 100 gain
margin_db = 10.0 #dB required

errs = [0.145, 0.050, 0.050, 0.030, 0.010, 0.010] #mrad
# adcs (0.145), sensor (0.05), drift (0.05), thruster (0.03), tracking (0.01), wobble (0.01)

e_rss = np.sqrt(sum(e**2 for e in errs)) # RSS combining eror
e_design = 0.42 # conservative design pointing error from ocsd flight heritage [mrad]

# receiver power required from range noise requirement
wavelength_eff = c / (2 * f_tone) # round-trip modulation wavelength [m]
sig_phi = 2 * np.pi * sigma_R / wavelength_eff # max allowed phase noise [rad]
cnr = 1 / (2 * sig_phi**2) # required carrier-to-noise ratio [unitless]

#min optic power to carry CNR
a = m**2 / 2; b = cnr * B * 2 * q * F / R0; cc = cnr * B * (1e-12)**2
P_req = (b + np.sqrt(b**2 + 4 * a * cc)) / (2 * a) #min detector power W

# min beam brightness hitting detector
A_patch = np.pi * (D_rx / 2)**2 # area of light collected
I_need = P_req / (eta_cc * eta_rx * A_patch) #min irad (W/m2)
I_cut = I_need * 10**(margin_db / 10) * 2 # margin + 2x

th = np.linspace(0.5, 10, 400) * 1e-3 # divergence angle [rad]
I_cube = 8 * P_out / (np.pi * R**2 * th**2) # peak gaussian irradiance at distance R [W/m^2]
e_allow = th * np.sqrt(np.log(2) / 8) # half-power (fwhm/2) off-axis angle [rad]

# solve for min and max allowable divergence bounds [rad]
th_min = (e_design * 1e-3) / np.sqrt(np.log(2) / 8)
th_max = np.sqrt(8 * P_out / (np.pi * R**2 * I_cut))
th_mrad = th * 1e3
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
l1, = ax1.loglog(th_mrad, I_cube * 1e3, color='tab:blue', linestyle='-', label='irradiance at cube')
l2 = ax1.axvline(th_max * 1e3, color='tab:blue', linestyle='--', label='max divergence (irradiance limit)')
l3, = ax2.loglog(th_mrad, e_allow * 1e3, color='tab:orange', linestyle='-', label='beam pointing tolerance')
l4 = ax2.axvline(th_min * 1e3, color='tab:orange', linestyle='--', label='min divergence (pointing limit)')
ax1.set_xlabel('beam divergence (mrad)'); ax1.set_ylabel('irradiance (mW/m^2)'); ax2.set_ylabel('pointing error (mrad)')
lines = [l1, l2, l3, l4]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels,loc='upper center') #
plt.title('laser divergence tradeoff')
plt.grid(True); plt.show()
print(f"bottom-up pointing rss: {e_rss:.3f} mrad (using {e_design} mrad design value)")
print(f"detector power needed:  {P_req*1e9:.1f} nW")
print(f"valid divergence range: {th_min*1e3:.2f} to {th_max*1e3:.2f} mrad")