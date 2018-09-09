Jp_di = 88846
Jp_ds = 483632000
Er_di = 7926
Er_ds = 92957100
Su_di = 864938
SJ_radius = round(Su_di/Jp_di,2)
print('Sun-to-Jupiter radius ratio:', SJ_radius)
SE_radius = round(Su_di/Er_di,2)
print('Sun-to-Earth radius ratio:', SE_radius)
JE_radius = round(Jp_di/Er_di,2)
print('Jupiter-to-Earth radius ratio:', JE_radius, end='\n\n')
JE_sun_distance = round(Jp_ds/Er_ds,2)
print('Jupiter-to-Earth Sun distance ratio:', JE_sun_distance)
SJ_volume = round((Su_di/2)**3/(Jp_di/2)**3,2)
print('Sun-to-Jupiter volume ratio:', SJ_volume)
SE_volume = round((Su_di/2)**3/(Er_di/2)**3,2)
print('Sun-to-Earth volume ratio:', SE_volume)
JE_volume = round((Jp_di/2)**3/(Er_di/2)**3,2)
print('Jupiter-to-Earth volume ratio:', JE_volume, end='\n\n')
SE_light_travel_time = round(Er_ds/186000/60,2)
print('Sun to Earth light travel time in minutes:', SE_light_travel_time)
SJ_light_travel_time = round(Jp_ds/186000/60,2)
print('Sun to Jupiter light travel time in minutes:', SJ_light_travel_time)