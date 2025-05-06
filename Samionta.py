from ramp import User

"""
 CREATE USERS AND ADD APPLIANCES
 
"""

""" LOW CONSUMPTION HOUSEHOLDS """
LC = User(
    user_name="Low Consumption Household",
    num_users=1
    )

# Adding appliances
LC_bulb = LC.add_appliance(
    name="Light bulb",
    number=1,
    power=8,  # Watt
    fixed_cycle=0,  # bulb has no duty cycle and always work with a single cycle
    func_cycle=120,  # when the appliance is switched on, it remains on at least for a min,
    occasional_use=1,  # it is always present in the energy mix
    func_time=660, # total functioning time of appliance in minutes
    time_fraction_random_variability=0.1, # 10% random variability associated to the total functioning time
    num_windows=2,  # Functioning window: during night and during day
    window_1=[0, 360],  # from midnight to 6:30 AM 
    window_2=[1110, 1440],  # from 18:30 to midnight
    random_var_w=0.1, # 0% randomness assigned to the size of the functioning windows
    fixed="yes", # all the 'n' appliances of this kind are always switched-on together
    flat="yes",
    )

LC_charger = LC.add_appliance(
    name="Phone charger",
    number=1,
    power=5,  # Watt
    num_windows=1,  
    func_cycle = 15,
    func_time=240,
    time_fraction_random_variability=0.2,
    window_1=[360, 1170],  # from 6:00 to 19:30
    )

LC_smartcharger = LC.add_appliance(
    name="Smartphone charger",
    number=1,
    power=10,  # Watt
    num_windows=2,  
    func_cycle = 15,
    func_time=105,
    occasional_use=0.6,
    window_1=[1080, 1320],  # from 19:00 to 22:30 
    window_2=[330, 450],    #from 5:30 to 7:30
    )

""" MEDIUM CONSUMPTION HOUSEHOLDS """
MC = User(
    user_name="Medium Consumption Household",
    num_users=1
    )

# Adding appliances
MC_radio = MC.add_appliance(
    name="Radio",
    number=1,
    power=7,  
    num_windows=1,  
    func_cycle = 30,
    func_time=450,
    time_fraction_random_variability=0.2,
    window_1=[360, 1170],
    )

MC_sec_bulb = MC.add_appliance(
    name="Security light bulb",
    number=2,
    power=8,  
    fixed_cycle=0,  
    func_cycle=120,  
    occasional_use=1,
    func_time=660, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="no", 
    flat="yes"
    )

MC_outdoor_bulb = MC.add_appliance(
    name="Outdoor light bulb",
    number=1,
    power=8,  
    fixed_cycle=0,  
    func_cycle=120,  
    occasional_use=1,
    func_time=660, 
    time_fraction_random_variability=0.1, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="yes", 
    flat="no"
    )

MC_indoor_bulb = MC.add_appliance(
    name="Living room light",
    number=1,
    power=8, 
    fixed_cycle=0,  
    func_cycle=10,  
    occasional_use=1, 
    func_time=100, 
    time_fraction_random_variability=0.1, 
    num_windows=1,  
    window_1=[1110, 1380],  
    random_var_w=0.1, 
    )

MC_charger = MC.add_appliance(
    name="Phone charger",
    number=2,
    power=5,  
    num_windows=1,  
    func_cycle = 15,
    func_time=240,
    time_fraction_random_variability=0.2,
    window_1=[360, 1170],
    )

MC_smartcharger = MC.add_appliance(
    name="Smartphone charger",
    number=1,
    power=10,  
    num_windows=2,  
    func_cycle = 15,
    func_time=105,
    window_1=[1080, 1320],
    window_2=[330, 450]
    )

""" HIGH CONSUMPTION HOUSEHOLDS """
HC = User(
    user_name="High Consumption Household",
    num_users=1
    )

# Adding appliances
HC_TV = HC.add_appliance(
    name="TV and Decoder",
    number=1,
    power=60,  
    num_windows=1,  
    func_cycle = 30,
    func_time=90,
    time_fraction_random_variability=0.2,
    window_1=[1140, 1380],
    random_var_w=0.1,
    )

HC_woofer = HC.add_appliance(
    name="Woofer",
    number=1,
    power=60,  
    num_windows=1,  
    func_cycle = 30,
    occasional_use=0.15,
    func_time=180,
    time_fraction_random_variability=0.2,
    window_1=[360, 1170],
    random_var_w=0.2,
    )

HC_sec_bulb = HC.add_appliance(
    name="Security light bulb",
    number=3,
    power=8,  
    fixed_cycle=0,  
    func_cycle=120,  
    occasional_use=1,
    func_time=660, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="no", 
    flat="yes"
    )

HC_outdoor_bulb = HC.add_appliance(
    name="Outdoor light bulb",
    number=1,
    power=8,  
    fixed_cycle=0,  
    func_cycle=120,  
    occasional_use=1,
    func_time=660, 
    time_fraction_random_variability=0.1, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.2, 
    fixed="no",
    flat="no"
    )

HC_indoor_bulb = HC.add_appliance(
    name="Living room light",
    number=1,
    power=8, 
    fixed_cycle=0,  
    func_cycle=10,  
    occasional_use=1, 
    func_time=100, 
    time_fraction_random_variability=0.1, 
    num_windows=1,  
    window_1=[1110, 1380],  
    random_var_w=0.1, 
    )

HC_charger = HC.add_appliance(
    name="Phone charger",
    number=2,
    power=5,  
    num_windows=1,  
    func_cycle = 15,
    func_time=240,
    time_fraction_random_variability=0.2,
    window_1=[360, 1170],
    )

HC_smartcharger = HC.add_appliance(
    name="Smartphone charger",
    number=1,
    power=10,  
    num_windows=2,  
    func_cycle = 15,
    func_time=105,
    window_1=[1080, 1320],
    window_2=[330, 450]
    )

""" CHURCH """
CH = User(
    user_name=" Churches",
    num_users=1
    )

# Adding appliances
CH1_sec_bulb = CH.add_appliance(
    name="Security light bulb",
    number=4,
    power=8,  
    fixed_cycle=0,   
    occasional_use=1,
    func_time=660, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="no", 
    flat="yes"
    )

CH1_in_bulb = CH.add_appliance(
    name="Indoor light bulb",
    number=1,
    power=8,  
    fixed_cycle=0,   
    occasional_use=0.85,
    func_time=1440, 
    time_fraction_random_variability=0.2,
    num_windows=1,  
    window_1=[0, 1440],  
    fixed="no", 
    flat="no"
    )

CH1_amplifier = CH.add_appliance(
    name="Amplifier",
    number=1,
    power=300,  
    num_windows=1,  
    func_cycle = 1,
    occasional_use=0.5,
    func_time=150,
    time_fraction_random_variability=0.3,
    window_1=[540, 840],
    random_var_w=0.1,
    wd_we_type=1,
    )

CH2_sec_bulb = CH.add_appliance(
    name="Outdoor light bulb",
    number=2,
    power=8,  
    fixed_cycle=0,   
    occasional_use=0.5,
    func_time=660, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="no", 
    flat="yes"
    )

""" Small and Medium Enterprise (SME)"""

SME = User(
    user_name="SME",
    num_users=2,
    )

# APPLIANCES
SME_bulb = SME.add_appliance(
    name="Security Light bulb",
    number=1,
    power=8, 
    fixed_cycle=0,  
    func_cycle=120,  
    occasional_use=1, 
    func_time=660, 
    time_fraction_random_variability=0.1, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="yes", 
    flat="yes",
    )

SME_indoor_bulb = SME.add_appliance(
    name="Indoor light",
    number=1,
    power=8, 
    fixed_cycle=0,  
    func_cycle=10,  
    occasional_use=1, 
    func_time=100, 
    time_fraction_random_variability=0.1, 
    num_windows=1,  
    window_1=[1110, 1320],  
    random_var_w=0.1, 
    )

SME_charger = SME.add_appliance(
    name="Phone charger",
    number=2,
    power=5,  # Watt
    num_windows=1,  
    func_cycle = 15,
    func_time=240,
    time_fraction_random_variability=0.2,
    window_1=[360, 1170],
    )

SME_smartcharger = SME.add_appliance(
    name="Smartphone charger",
    number=1,
    power=10,  
    num_windows=2,  
    func_cycle = 15,
    func_time=105,
    window_1=[1080, 1320],
    window_2=[330, 450]
    )

SME_speaker = SME.add_appliance(
    name="Speaker",
    number=1,
    power=20,  
    num_windows=1,  
    func_cycle=30,
    func_time=600,
    occasional_use=0.85,
    time_fraction_random_variability=0.2,
    window_1=[480, 1320],
    )

""" Productive Use of Electricity (PUE)"""

PUE_old = User(
    user_name="Old PUE",
    num_users=1,
    )
PUE = User(
    user_name="PUE",
    num_users=1,
    )

# APPLIANCE
PUE_freezer_old = PUE_old.add_appliance(
    name="Old Freezer",
    number=1,
    power=120,
    num_windows=1,
    func_time=1400,
    time_fraction_random_variability=0,
    func_cycle=30,
    fixed="yes",
    fixed_cycle=3,
    )
PUE_freezer_old.windows([0, 1440])
PUE_freezer_old.specific_cycle_1(p_11=120, t_11=10, p_12=2, t_12=20, r_c1=0.5) # Standard
PUE_freezer_old.specific_cycle_2(p_21=120, t_21=12, p_22=2, t_22=18, r_c2=0.5) # Intermediate
PUE_freezer_old.specific_cycle_3(p_31=120, t_31=15, p_32=2, t_32=15, r_c3=0.5) # Intensive
PUE_freezer_old.cycle_behaviour(
    cw11=[0, 419],
    cw21=[420, 599],
    cw31=[600, 1379],
    cw12=[1380, 1440]
    )

PUE_freezer = PUE.add_appliance(
    name="Freezer",
    number=3,
    power=100,
    num_windows=1,
    func_time=1400,
    time_fraction_random_variability=0,
    func_cycle=30,
    fixed="yes",
    fixed_cycle=3,
    )
PUE_freezer.windows([0, 1440])
PUE_freezer.specific_cycle_1(p_11=100, t_11=10, p_12=2, t_12=20, r_c1=0.5) 
PUE_freezer.specific_cycle_2(p_21=100, t_21=12, p_22=2, t_22=18, r_c2=0.5) 
PUE_freezer.specific_cycle_3(p_31=100, t_31=15, p_32=2, t_32=15, r_c3=0.5) 
PUE_freezer.cycle_behaviour(
    cw11=[0, 419],
    cw21=[420, 599],
    cw31=[600, 1379],
    cw12=[1380, 1440]
    )

PUE_mill = PUE.add_appliance(
    name="Grain mill",
    number=2,
    func_time=480,
    num_windows=2,
    window_1=[480, 720],  # from 08:00 to 12:00
    window_2=[840, 1200], # from 14:00 to 20:00
    random_var_w=0.05,
    occasional_use=0.85, 
    fixed="yes",
    fixed_cycle=1,
    p_11=6500,
    t_11=1,
    p_12=1800,
    t_12=12,
    continuous_duty_cycle=0,
    )

PUE_incubator = PUE.add_appliance(
    name="Incubator",
    number=1,
    power=600,
    num_windows=1,
    func_time=1400,
    time_fraction_random_variability=0,
    func_cycle=15,
    fixed="yes",
    fixed_cycle=3,
    )
PUE_incubator.windows([0, 1440])
PUE_incubator.specific_cycle_1(p_11=600, t_11=1, p_12=30, t_12=14, r_c1=0.5) 
PUE_incubator.specific_cycle_2(p_21=600, t_21=2, p_22=30, t_22=13, r_c2=0.5) 
PUE_incubator.specific_cycle_3(p_31=600, t_31=3, p_32=30, t_32=12, r_c3=0.5) 
PUE_incubator.cycle_behaviour(
    cw31=[0, 419],
    cw21=[420, 599],
    cw11=[600, 1379],
    cw32=[1380, 1440]
    )

""" SCHOOL """

SCH = User(
    user_name="School",
    num_users=1,
    )

SCH_sec_bulb = SCH.add_appliance(
    name="Security light",
    number=2,
    power=8,  
    func_time=660,
    func_cycle=120, 
    time_fraction_random_variability=0.1, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="yes", 
    flat="yes",
    )

SCH_in_bulb = SCH.add_appliance(
    name="Office light",
    number=1,
    power=8,  
    func_time=180,
    func_cycle=60, 
    time_fraction_random_variability=0.1, 
    num_windows=2,  
    window_1=[420, 750],  
    window_2=[870, 1140],  
    random_var_w=0.1,
    wd_we_type=0,
    )

SCH_radio = SCH.add_appliance(
    name="Radio",
    number=1,
    power=7,   
    func_cycle = 30,
    func_time=180,
    time_fraction_random_variability=0.2,
    num_windows=2,  
    window_1=[420, 750],  
    window_2=[870, 1140],  
    random_var_w=0.1,
    wd_we_type=0,
    )

SCH_smartcharger = SCH.add_appliance(
    name="Smartphone charger",
    number=1,
    power=10,  
    func_time=90,
    func_cycle=30,
    occasional_use=0.5,
    time_fraction_random_variability=0.2,   
    num_windows=2,
    window_1=[420, 750],  
    window_2=[870, 1140],  
    random_var_w=0.1,
    wd_we_type=0,
    )

SCH_printer = SCH.add_appliance(
    name="Printer",
    number=1,
    power=27,  
    func_time=10,
    func_cycle=1,
    occasional_use=0.3,
    time_fraction_random_variability=0.2,   
    num_windows=2,
    window_1=[420, 750],  
    window_2=[870, 1140],  
    random_var_w=0.1,
    wd_we_type=0,
    )

SCH_computer = SCH.add_appliance(
    name="Computer",
    number=1,
    func_time=240,
    wd_we_type=0,
    num_windows=2,
    window_1=[420, 750],  
    window_2=[870, 1140], 
    fixed_cycle=1,
    p_11=65,
    t_11=60,
    p_12=10,
    t_12=180,
    continuous_duty_cycle=0,
    )


""" HEALTH CENTER """

HOS = User(
    user_name="Hospital",
    num_users=1,
    )

HOS_freezer = HOS.add_appliance(
    name="Freezer",
    number=1,
    power=100,
    num_windows=1,
    func_time=1400,
    time_fraction_random_variability=0,
    func_cycle=30,
    fixed="yes",
    fixed_cycle=3,
    )
HOS_freezer.windows([0, 1440])
HOS_freezer.specific_cycle_1(p_11=100, t_11=10, p_12=2, t_12=20, r_c1=0.5) 
HOS_freezer.specific_cycle_2(p_21=100, t_21=12, p_22=2, t_22=18, r_c2=0.5) 
HOS_freezer.specific_cycle_3(p_31=100, t_31=15, p_32=2, t_32=15, r_c3=0.5) 
HOS_freezer.cycle_behaviour(
    cw11=[0, 419],
    cw21=[420, 599],
    cw31=[600, 1379],
    cw12=[1380, 1440]
    )

HOS_fan = HOS.add_appliance(
    name="Fan",
    number=1,
    power=50,  
    num_windows=1,  
    func_cycle = 60,
    func_time=480,
    occasional_use=0.5,
    time_fraction_random_variability=0.2,
    window_1=[660, 1320],
    )

HOS_sec_bulb = HOS.add_appliance(
    name="Security light bulb",
    number=2,
    power=8,   
    func_cycle=120, 
    func_time=660, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="no", 
    flat="yes"
    )

HOS_outdoor_bulb = HOS.add_appliance(
    name="Outdoor light bulb",
    number=2,
    power=8,  
    fixed_cycle=0,  
    func_cycle=120,  
    occasional_use=1,
    func_time=660, 
    time_fraction_random_variability=0.1, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1,
    )

HOS_indoor_bulb = HOS.add_appliance(
    name="Indoor light",
    number=1,
    power=8, 
    fixed_cycle=0,  
    func_cycle=10,  
    occasional_use=1, 
    func_time=100, 
    time_fraction_random_variability=0.1, 
    num_windows=1,  
    window_1=[1110, 1380],  
    random_var_w=0.1, 
    )

HOS_charger = HOS.add_appliance(
    name="Phone charger",
    number=2,
    power=5, 
    func_time=240,  
    func_cycle=30,
    time_fraction_random_variability=0.2,  
    num_windows=1,
    window_1=[480, 1320],
    )

HOS_smartcharger = HOS.add_appliance(
    name="Smartphone charger",
    number=1,
    power=10,  
    func_cycle=30,
    func_time=120,
    time_fraction_random_variability=0.2,  
    num_windows=1,
    window_1=[480, 1320],
    )

""" POWERHOUSE SELF CONSUMPTION """

SC = User(
    user_name="Self Consumption",
    num_users=1,
    )

SC_AC = SC.add_appliance(
    name="Air Conditioner",
    number=1,
    power=1200,
    num_windows=2,
    func_time=480,
    time_fraction_random_variability=0,
    func_cycle=30,
    fixed="yes",
    fixed_cycle=3,
    )
SC_AC.windows([540, 960], [1380, 1440])
SC_AC.specific_cycle_1(p_11=1200, t_11=17, p_12=200, t_12=13, r_c1=0.2) 
SC_AC.specific_cycle_2(p_21=1200, t_21=25, p_22=200, t_22=5, r_c2=0.2) 
SC_AC.specific_cycle_3(p_31=1200, t_31=29, p_32=200, t_32=1, r_c3=0.2) 
SC_AC.cycle_behaviour(
    cw11=[540, 599],
    cw21=[600, 689],
    cw31=[690, 960],
    cw12=[1380, 1409],
    cw22=[1410, 1440]
    )

SC_Cam = SC.add_appliance(
    name="Camera",
    number=1,
    power=7,
    func_time=1440,
    func_cycle=60,
    num_windows=1,
    window_1=[0, 1440],
    )

SC_WiFi = SC.add_appliance(
    name="WiFi",
    number=1,
    power=10,
    func_time=1440,
    func_cycle=60,
    num_windows=1,
    window_1=[0, 1440],
    )

SC_sec_bulb = SC.add_appliance(
    name="Security light",
    number=1,
    power=8,
    func_time=1440,
    func_cycle=120,
    num_windows=1,
    window_1=[0, 1440],
    flat="yes",
    )

""" PUBLIC LIGHTING """

PL = User(
    user_name="Public Light",
    num_users=1,
    )

PL_LED = PL.add_appliance(
    name="Street lamp",
    number=8,
    power=65,
    func_cycle=120, 
    func_time=660, 
    num_windows=2,  
    window_1=[0, 360],  
    window_2=[1110, 1440],  
    random_var_w=0.1, 
    fixed="yes",
    )