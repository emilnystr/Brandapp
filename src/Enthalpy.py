from numba import njit
import numpy as np
from D_FemCalc import *
from A_Material import *

@njit
def getE(element_sizes, element_material_indices, material_databas, T):
    '''Iitiera en entalpivektor'''

    E = np.zeros(len(T))


    #första noden. enbart bidrag från hälften av första elementet, vi behåller det flexibelt, om starttemperaturen inte är 20 grader
    E[0] = linjär_interpolering(material_databas[element_material_indices[0]][0],material_databas[element_material_indices[0]][4], T[0]) * element_sizes[0] * 0.5

    #inre noder, bidrag kommer från två element
    for i in range(1, len(T) - 1):
        E[i] = (linjär_interpolering(
                material_databas[element_material_indices[i - 1]][0],
                material_databas[element_material_indices[i - 1]][4],
                T[i]) * element_sizes[i - 1] * 0.5 + linjär_interpolering(material_databas[element_material_indices[i]][0],
                                   material_databas[element_material_indices[i]][4], T[i]) * element_sizes[i] * 0.5)
        
    E[-1] = linjär_interpolering(material_databas[element_material_indices[-1]][0], material_databas[element_material_indices[-1]][4], T[-1]) * element_sizes[-1] * 0.5

    return E





@njit
def getTfromE(element_sizes, element_material_indices, material_databas, T_prev, E):
    n = len(E)
    T_out = np.zeros(n)

    V = np.zeros(n, dtype=np.float32)
    V[0] = 0.5 * element_sizes[0]
    V[-1] = 0.5 * element_sizes[-1]
    for i in range(1, n-1):
        V[i] = 0.5 * element_sizes[i-1] + 0.5 * element_sizes[i]

    T_guess = T_prev.copy()

    for nod in range(n):
        #Homogena noder
        if nod == 0 or nod == n - 1 or element_material_indices[nod - 1] == element_material_indices[nod]:
            if nod == 0:
                mat_idx = element_material_indices[0]
            elif nod == n - 1:
                mat_idx = element_material_indices[-1]
            else:
                mat_idx = element_material_indices[nod]

            temp_tabell = material_databas[mat_idx][0]
            entalpivärden = material_databas[mat_idx][4]
            e_target = E[nod] / V[nod]

            #interpoleringsalgoritm 
            for j in range(len(entalpivärden) - 1):
                #Samma temperatur men olika entalpi (latent värme)
                if temp_tabell[j] == temp_tabell[j + 1] and entalpivärden[j] != entalpivärden[j + 1]:
                    if entalpivärden[j] <= e_target < entalpivärden[j + 1]:
                        T_out[nod] = temp_tabell[j]
                        break
                #(kontinuerlig entalpikurva) linjär interpolering
                else:
                    T_out[nod] = temp_tabell[j] + (e_target - entalpivärden[j]) / (entalpivärden[j + 1] - entalpivärden[j]) * (temp_tabell[j + 1] - temp_tabell[j])
                    break

        #Gränsnoder
        else:
            cnt = 0
            rel_fel = 1

            # vi använder samma skillnad som TASEF-2 (1%)
            while rel_fel > 0.01 and cnt < 50:
                # vänster och höger material för aktuell nod
                mat_vänster = element_material_indices[nod - 1]
                mat_höger = element_material_indices[nod]
                dx_vänster = 0.5 * element_sizes[nod - 1]
                dx_höger = 0.5 * element_sizes[nod]

                #derivata för vänster material vid aktuell gissning
                T_tab_vänster = material_databas[mat_vänster][0]
                e_tab_vänster = material_databas[mat_vänster][4]
                e_vänster = 0
                dEdT_vänster = 0
                
                #hitta temperaturintervall i tabellen där vår gissade nodtemperatur ligger
                for j in range(len(T_tab_vänster) - 1):
                    Tj = T_tab_vänster[j]
                    Tj1 = T_tab_vänster[j+1]
                    ej = e_tab_vänster[j]
                    ej1 = e_tab_vänster[j+1]


                    if (Tj <= T_guess[nod] <= Tj1) or (Tj1 <= T_guess[nod] <= Tj):
                        if Tj1 != Tj:
                            frac = (T_guess[nod] - Tj) / (Tj1 - Tj)
                            e_vänster = ej + frac * (ej1 - ej)
                            dEdT_vänster = (ej1 - ej) / (Tj1 - Tj)
                        else:
                            e_vänster = ej
                            dEdT_vänster = ej1 - ej
                        break

                #derivata för höger material vid aktuell gissning
                T_tab_höger = material_databas[mat_höger][0]
                e_tab_höger = material_databas[mat_höger][4]
                e_höger = 0
                dEdT_höger = 0
                for j in range(len(T_tab_höger) - 1):
                    Tj = T_tab_höger[j]
                    Tj1 = T_tab_höger[j+1]
                    ej = e_tab_höger[j]
                    ej1 = e_tab_höger[j+1]
                    if (Tj <= T_guess[nod] <= Tj1) or (Tj1 <= T_guess[nod] <= Tj):
                        if Tj1 != Tj:
                            frac = (T_guess[nod] - Tj) / (Tj1 - Tj)
                            e_höger = ej + frac * (ej1 - ej)
                            dEdT_höger = (ej1 - ej) / (Tj1 - Tj)
                        else:
                            e_höger = ej
                            dEdT_höger = ej1 - ej
                        break

                #beräkna nodens entalpi och kapacitans
                E_uppskattad = e_vänster * dx_vänster + e_höger * dx_höger
                Cm_nod = dEdT_vänster * dx_vänster + dEdT_höger * dx_höger

                #Newton-raphson 
                T_ny = T_guess[nod] + (E[nod] - E_uppskattad) / Cm_nod
        
                rel_fel = 2 * abs(T_guess[nod] - T_ny) / T_guess[nod] + T_ny
                

                #justera temperatur om det tar för lång tid att 
                # konvergera, denna rutin är vanlig vid fasövergångar där
                #där temperaturen kan hoppa fram och tillbaka
                if cnt > 40:
                    diff = abs(T_guess[nod] - T_ny)
                    if T_guess[nod] > T_ny:
                        T_guess[nod] -= 0.05 * diff
                    else:
                        T_guess[nod] += 0.05 * diff
                else:
                    # normal Newton-uppdatering
                    T_guess[nod] = T_ny

                cnt += 1

            T_out[nod] = T_guess[nod]

    
    return T_out


