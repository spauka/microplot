import framebuf
from quokka import *

class Chart():
  def __init__(self,
    display=None,
    values=None, max_value_count=50,
    label=None, y_labels=True, y_label_width=4,
    start_x=None, end_x=None,
    start_y=None, end_y=None):
    
    self.display = display
    self.char_width, self.char_height = 8, 8
    self.values = [] if values == None else values 
    self.max_value_count = max_value_count

    self.label = label
    self.y_labels = y_labels
    self.y_label_width = y_label_width 

    self.start_x, self.end_x = start_x, end_x 
    self.start_y, self.end_y = start_y, end_y 

    self.screen_start_x = len(self.label)*8 + 1 if self.label != None else 0
    self.screen_end_x = self.display.width - (self.y_label_width*self.char_width + 1) if self.y_labels else self.display.width
    self.screen_start_y = 0
    self.screen_end_y = self.display.height
  
  def update(self, value):
    self.values.append(value)
    if len(self.values) > self.max_value_count:
      self.values.pop(0)

  def scale(self, x=None, y=None):
    # Get range of values
    start_x = 0 if self.start_x == None else self.start_x
    end_x = start_x+len(self.values) if self.end_x == None else self.end_x
    start_y = min(self.values) if self.start_y == None else self.start_y
    end_y = max(self.values) if self.end_y == None else self.end_y
    range_x = 1 if end_x - start_x == 0 else end_x - start_x
    range_y = 1 if end_y - start_y == 0 else end_y - start_y
    screen_range_x = self.screen_end_x - self.screen_start_x
    screen_range_y = self.screen_end_y - self.screen_start_y

    if x != None:
      return self.screen_start_x + int((x - start_x)/range_x * screen_range_x)
    if y != None:
      return self.screen_start_y + int((y - start_y)/range_y * screen_range_y)

  def show(self):
    # Draw the values
    self.display.fill(1)
    prev_x, prev_y = 0, self.values[0] if self.values else 0
    for x, y in enumerate(self.values):
      self.display.line(self.scale(x=prev_x), self.scale(y=prev_y), self.scale(x=x), self.scale(y=y), 0)
      prev_x, prev_y = x, y

    # Draw the labels
    if self.label:
      y = self.display.height//2
      self.display.text(self.label, 0, y, 0)

    if self.y_labels and self.values:
      self.display.text(str(min(self.values)).center(self.y_label_width), self.screen_end_x+1, 0, 0)
      self.display.text(str(self.values[-1]).center(self.y_label_width), self.screen_end_x+1, self.display.height//2, 0)
      self.display.text(str(max(self.values)).center(self.y_label_width), self.screen_end_x+1, self.display.height - self.char_height, 0)

    # Show the chart
    self.display.show()


chart = Chart(display)
while True:
  x,y,z = accelerometer.x, accelerometer.y, accelerometer.z
  chart.update(x)
  chart.show()
  sleep(2000)
