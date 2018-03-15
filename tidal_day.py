from PIL import Image
from PIL import ImageDraw
import time

month = 5
day = 6
year = 63

image = Image.new('RGBA',(200,200),(0,0,0,0))
draw = ImageDraw.Draw(image)

min_per_day = 60*24
moon_space = 200
moon_disp = 0
sun_space = 160
sun_disp = 20
tide_space = 120
tide_disp = 40

highest_high_tide = 6
lowest_low_tide = 0

def convert_time_to_minutes(hours, minutes, am):
  if(am == 'AM'):
    if(hours == 12):
      hours = 0
  else:
    hours = hours + 12
  return hours * 60 + minutes

def draw_halves(size, moon_rise, moon_set, day_color, night_color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  rise_angle = 360 * moon_rise / min_per_day
  set_angle = 360 * moon_set / min_per_day
  draw.pieslice((0,0,size, size), rise_angle, set_angle, day_color, 'black')
  draw.pieslice((0,0,size, size), set_angle, rise_angle, night_color, 'black')
  return image

def draw_tide_quad(size, low_height, high_height, color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  length = size*high_height/100
  height = size*low_height/100
  x_dist = (size-length)/2
  y_dist = (size-height)/2
  draw.pieslice((x_dist, y_dist, size-x_dist, size-y_dist), -60, 60, color, 'black')
  return image

def relative_tide_position(feet):
  max_tide = 60
  min_tide = -10
  tidal_range = max_tide - min_tide
  retval = 33+66*(feet - min_tide)/tidal_range
  print('feet: '+repr(feet)+' retval: '+repr(retval))
  return retval


moon_rise = convert_time_to_minutes(8, 12, 'PM')
moon_set = convert_time_to_minutes(7, 50, 'AM')
moon = draw_halves(moon_space, moon_rise, moon_set, 'white', 'black')
image.paste(moon, (moon_disp,moon_disp,moon_space,moon_space), moon)

sun_rise = convert_time_to_minutes(6, 36, 'AM')
sun_set = convert_time_to_minutes(6, 4, 'PM')
sun = draw_halves(sun_space, sun_rise, sun_set, 'yellow', 'brown')
image.paste(sun, (20,20, 180, 180), sun)

# draw the tidal background
high_tide = draw.ellipse((40,40,160,160),'blue','blue')
low_tide = draw.ellipse((60,60,140,140),'red','blue')

first_high = relative_tide_position(52) #95
second_high = relative_tide_position(50) #9585
first_low = relative_tide_position(9) #958545
second_low = relative_tide_position(-2) #958540
first_high_time = convert_time_to_minutes(10, 4, 'AM')
second_high_time = convert_time_to_minutes(11, 7, 'PM')
first_low_time = convert_time_to_minutes(4, 10, 'AM')
second_low_time = convert_time_to_minutes(4, 39, 'PM')

tide = draw_tide_quad(tide_space, first_low, first_high, (0, 0, 0, 200))
first_high_rotation_factor = -360*first_high_time/min_per_day
tide1 = tide.rotate(first_high_rotation_factor)
image.paste(tide1, (40, 40, 160, 160), tide1)
tide = draw_tide_quad(tide_space, first_high, second_low, (0, 0, 0, 200))
first_low_rotation_factor = -360*first_low_time/min_per_day
tide1 = tide.rotate(first_low_rotation_factor)
image.paste(tide1, (40, 40, 160, 160), tide1)
tide = draw_tide_quad(tide_space, second_low, second_high, (0, 0, 0, 200))
second_high_rotation_factor = -360*second_high_time/min_per_day
tide1 = tide.rotate(second_high_rotation_factor)
image.paste(tide1, (40, 40, 160, 160), tide1)
tide = draw_tide_quad(tide_space, second_high, first_low, (0, 0, 0, 200))
second_low_rotation_factor = -360*second_low_time/min_per_day
tide1 = tide.rotate(second_low_rotation_factor)
image.paste(tide1, (40, 40, 160, 160), tide1)

hour = 5
while True:
  hour = hour + 2
  current_time = convert_time_to_minutes(hour, 12, 'AM')
  image.rotate(360*current_time/min_per_day + 90).show()
#  image2.show()
  time.sleep(3)
