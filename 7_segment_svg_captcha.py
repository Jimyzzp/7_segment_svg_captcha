import random

class captcha:

 BITS = (128,64,32,16,8,4,2,1)
 SEGMENTS = ((-0.5, 1, 0.5, 1), (-0.5, 0, -0.5, 1), (0.5, 0, 0.5, 1), (-0.5, 0, 0.5, 0), (-0.5, 0, -0.5, -1), (0.5, 0, 0.5, -1), (-0.5, -1, 0.5, -1))
 FONT = (119, 36, 93, 109, 46, 107, 123, 39, 255, 111, 0, 0, 0, 0, 0, 0, 0, 63, 0, 83, 0, 91, 27, 0, 62, 0, 117, 0, 82, 0, 0, 0, 31, 0, 0, 0, 0, 118)

 def __init__(self, width, height):
  # Size of the whole svg image
  self.width = width
  self.height = height
  self.lines = []

  # Font size
  self.sizex = 16
  self.sizey = 16

  # Start positions
  self.xpos = int(self.sizex)*2.5
  self.ypos = int(height/2)


 def output(self, filename):
  
  str1 = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
  str1.append('<svg width="'+str(self.width)+'" height="'+str(self.height)+'" xmlns="http://www.w3.org/2000/svg">\n')
 
  # Filling / Border
  str1.append('<rect x="0" y="0" width="'+str(self.width)+'" height="'+str(self.height)+'" fill="black" stroke-width="1" />\n')

  for point in self.lines:
   str1.append('<line x1="'+ str(round(point[0])) +'" y1="'+ str(round(point[1])) +'" x2="'+ str(round(point[2])) +'" y2="'+str(round(point[3]))+'" stroke="white" />\n')
 
  str1.append('</svg>' + '\n')

  file = open(filename, "w")
  file.write(''.join(str1))
  file.close()


 def create_7segchar(self, c):
  c = ord(c) - 48
  if c < 0 or c > len(self.FONT):
   return [[]]
 
  bits = self.FONT[c]
  
  coordinates = []
  a = 1
  for i in range(0, 7):
   if (bits & a):
    coordinates.append(list(self.SEGMENTS[i])) #.copy()
   a <<= 1

  # Obfuscating
  if 1:
   rpart = 0 #(random.random()/2 + 0.5)
   ipart = 1 #(1 - random.random() * 2) / 2
   z1 = complex(rpart, ipart)
   
   z2 = complex(0,0)
   z3 = complex(0,0)
   
   for p in range (0, len(coordinates)):
    for i in [0,2]:
     z2 = complex(coordinates[p][i], coordinates[p][i+1])
     z3 = z2 * z1
     coordinates[p][i] = z3.real
     coordinates[p][i+1] = z3.imag
 
 
  return coordinates



 def plot_str(self, str1):
  char_nr = 0
  for c in str1:
   new_char = self.create_7segchar(c)
   #new_char = self.create_char(c)
       
   for line_nr in range(0, len(new_char)):
   
    # Apply size
    for i in [0,2]:
     new_char[line_nr][i] *= self.sizex
     new_char[line_nr][i+1] *= self.sizey
   
    # Move to positive screen and current position
    for i in [0,2]:
     new_char[line_nr][i] += char_nr * self.sizex * 3 + self.xpos
     new_char[line_nr][i+1] += self.ypos
 
    # Transform y-axis (from top)
    new_char[line_nr][1] = self.height - new_char[line_nr][1]
    new_char[line_nr][3] = self.height - new_char[line_nr][3]
  
    # Add to string
   self.lines += new_char
   char_nr += 1
  
  # Shuffle lines (otherwise you can assume the characters by looking into the source)
  random.shuffle(self.lines)

a = captcha(500, 80)

rand_str = random.choices(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'C', 'E', 'F', 'H', 'J', 'L', 'P', 'U'], k = 15)
rand_str = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'C', 'E', 'F', 'H', 'J', 'L', 'P', 'U']

rand_str = ''.join(rand_str)
a.plot_str(rand_str)
a.output('test.svg')
