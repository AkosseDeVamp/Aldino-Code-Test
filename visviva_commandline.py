import math
from rich.console import Console
from rich.table import Table
import datetime

while True:
    #Prompt for input values
    input_values = input("Enter the pe and ap for the initial and final orbits (in km altitude) in the following format: 200x300 400x500: ")

    #split the input string into separate values
    values = input_values.split(' ')

    # Extract individual values and convert them to integers
    i11, i12 = map(int, values[0].split('x'))
    i21, i22 = map(int, values[1].split('x'))

    #height in km
    d11 = i11
    d12 = i12
    d21 = i21
    d22 = i22

    #make them fuckers strings
    per1 = str(min(d11,d12))
    aps1 = str(max(d11,d12))
    pert = str(min(d11,d12,d21,d22))
    apst = str(max(d11,d12,d21,d22))
    per2 = str(min(d21,d22))
    aps2 = str(max(d21,d22))


    #Radius of earth and mu
    Re = 6.370997e6
    mu = 3.9859e14

    #Function for converting to proper SI units for radius
    def rSI(d1,d2):
        s1 = Re + 1000*d1
        s2 = Re + 1000*d2
        return s1, s2

    # define the velocity calculation formula
    def visviv(r,a):
        return math.sqrt(mu*((2/(r))-(1/a)))

    #Initial Orbit (1) states
    s1p = min(rSI(d11,d12)) #Finds the minimum of d11 and d12 to deduce what periapsis 1 is
    s1a = max(rSI(d11,d12)) #Finds the maximum of d11 and d12 to deduce what apoapsis 1 is
    a1 = 0.5*(s1p+s1a)      #semi-major axis 1
    v1p = visviv(s1p,a1)    #velocity at periapsis 1
    v1a = visviv(s1a,a1)    #velocity at apoapsis 1
    v1p = round(v1p,2)      #rounded for her pleasure
    v1a = round(v1a,2)      
    per1_vel = str(v1p)     #converted to string for table
    aps1_vel = str(v1a)     

    T1 = 2*math.pi*math.sqrt(pow(a1,3)/mu)          #orbital time in seconds
    T1_str = str(datetime.timedelta(seconds=round(T1)))    #string with hours/mins/secs

    #Final Orbit (2) States
    s2p = min(rSI(d21,d22))
    s2a = max(rSI(d21,d22))
    a2 = 0.5*(s2p+s2a)
    v2p = visviv(s2p,a2)
    v2a = visviv(s2a,a2)
    v2p = round(v2p,2)
    v2a = round(v2a,2)
    per2_vel = str(v2p)
    aps2_vel = str(v2a)

    T2 = 2*math.pi*math.sqrt(pow(a2,3)/mu)          #orbital time in seconds
    T2_str = str(datetime.timedelta(seconds=round(T2)))    #string with hours/mins/secs

    #Transfer Orbit (t) States
    stp = s1p
    sta = s2a
    at = 0.5*(stp+sta)
    vtp = visviv(stp,at)
    vta = visviv(sta,at)
    vtp = round(vtp,2)
    vta = round(vta,2)
    pert_vel = str(vtp)
    apst_vel = str(vta)

    Tt = 2*math.pi*math.sqrt(pow(at,3)/mu)          #orbital time in seconds
    Tt_str = str(datetime.timedelta(seconds=round(Tt)))    #string with hours/mins/secs

    #Delta-v
    b1dv = round(abs(vtp-v1p),2)    #First Hohmann transfer
    b2dv = round(abs(vta-v2a),2)    #Second Hohmann Transfer
    bdv_tot = b1dv + b2dv           #Total expended dV

    burn1_dv = str(b1dv)            #Converted into strings
    burn2_dv = str(b2dv)
    burn_dv = str(bdv_tot)

    #building a table
    table = Table(title='Hohmann Transfer - '+ burn_dv + 'm/s')                                     #Table heading with total velocity
    columns = ["Orbit","Pe (km)","Vpe (m/s)","Ap (km)","Vap (m/s)","dV (m/s)","Orbital period"]     #Column headings
    rows = [                                                                                        #Row data
        ["Initial", per1, per1_vel, aps1, aps1_vel, "---", T1_str],
        ["Transfer", pert, pert_vel, apst, apst_vel, burn1_dv, Tt_str],
        ["Final", per2, per2_vel, aps2, aps2_vel, burn2_dv, T2_str],
    ]

    for column in columns:
        table.add_column(column)

    for row in rows:
        table.add_row(*row, style='bright_green')

    console = Console()
    console.print(table)