
def zoom(self,window, factor):
    cx = (self.window['xmin'] + self.window['xmax']) / 2
    cy = (self.window['ymin'] + self.window['ymax']) / 2

    width = (self.window['xmax'] - self.window['xmin']) * factor
    height = (self.window['ymax'] - self.window['ymin']) * factor

    self.window['xmin'] = cx - width / 2
    self.window['xmax'] = cx + width / 2
    self.window['ymin'] = cy - height / 2
    self.window['ymax'] = cy + height / 2