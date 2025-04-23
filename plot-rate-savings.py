import matplotlib.pyplot as plt
import numpy as np

X_MIN = 26

def interval_bd_rate(rate_ref, psnr_ref, rate_new, psnr_new):
  log_rate_ref = np.log(rate_ref)
  log_rate_new = np.log(rate_new)

  spline_ref = np.polyfit(psnr_ref, log_rate_ref, 3)
  spline_new = np.polyfit(psnr_new, log_rate_new, 3)
  int_ref = np.polyint(spline_ref)
  int_new = np.polyint(spline_new)

  # two ends
  x_min = max(min(psnr_ref), min(psnr_new))
  x_max = min(max(psnr_ref), max(psnr_new))
  x_min = np.ceil(x_min * 2) / 2.0
  x_max = np.floor(x_max * 2) / 2.0
  x_min = X_MIN if x_min < X_MIN else x_min
  x = np.arange(x_min, x_max, 0.5)

  y = np.zeros_like(x)

  for i, x_i in enumerate(x):

    delta_log_rate = (
      np.polyval(int_new, x_i+.5) - np.polyval(int_new, x_i)
    - np.polyval(int_ref, x_i+.5) + np.polyval(int_ref, x_i)
    )
    delta_rate = np.exp(delta_log_rate / 0.5)
    y[i] = (delta_rate -1.0) * 100
  
  delta_log_rate = (
    np.polyval(int_new, x_max) - np.polyval(int_new, x_min)
  - np.polyval(int_ref, x_max) + np.polyval(int_ref, x_min)
  )
  delta_rate = np.exp(delta_log_rate / (x_max - x_min))
  bd_rate = (delta_rate -1.0) * 100  

  return x+0.25, y, bd_rate

# Demo
rate_ref = None
psnr_ref = None

rate_new = None
psnr_new = None
x, y, bd_rate = interval_bd_rate(
    rate_ref, psnr_ref,
    rate_new, psnr_new
)
plt.plot(x, y, ".-", color="C1")
plt.grid()
