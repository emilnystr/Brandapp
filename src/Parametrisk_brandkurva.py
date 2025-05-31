import json
import math

def parametrisk_kurva(tid_sekunder):
    with open("config.json", 'r') as f:
        cfg = json.load(f)

    Av = cfg["Av"]
    At = cfg["At"]
    heq = cfg["heq"]
    b = cfg["b"]
    q_td = cfg["q_td"]
    tillväxt = cfg["growth_rate"]
    t_lim = tillväxt / 60  

    O = Av*(heq**0.5)/At
    Gamma = (O/b)**2/((0.04/1160)**2)
    
    tid_timmar = tid_sekunder / 3600
    t_star = tid_timmar * Gamma
    
    t_max_vent = (0.2e-3 * q_td) / O
    t_max = max(t_max_vent, t_lim)  

    
    O_lim = 0.1e-3 * q_td / t_lim
    Gamma_lim = (O_lim/b)**2 / (0.04/1160)**2
    
    if O > 0.04 and q_td < 75 and b < 1160:
        k = 1 + ((O-0.04)/0.04)*((q_td-75)/75)*((1160-b)/1160)
        Gamma_lim *= k

    if t_max == t_lim:
        t_star = tid_timmar * Gamma_lim
    
    t_star_max = t_max * Gamma

    T_max = 20 + 1325*(1 - 0.324*math.exp(-0.2*t_star_max) 
                     - 0.204*math.exp(-1.7*t_star_max) 
                     - 0.472*math.exp(-19*t_star_max))

    if tid_timmar <= t_max:
        T = 20 + 1325*(1 - 0.324*math.exp(-0.2*t_star) 
                        - 0.204*math.exp(-1.7*t_star) 
                        - 0.472*math.exp(-19*t_star))
    else:
        if t_max > t_lim:
            x = 1
        else:
            x = t_lim * Gamma / t_star_max

        if t_star_max <= 0.5:
            T = T_max - 625*(t_star - t_star_max*x)
        elif 0.5 < t_star_max < 2:
            T = T_max - 250*(3 - t_star_max)*(t_star - t_star_max*x)
        else:
            T = T_max - 250*(t_star - t_star_max*x)
    if T < 20:
        return 20

    return T
