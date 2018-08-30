import tkinter

class Slider(tkinter.Toplevel):
   def __init__(self, variable = "x", minVal = 0, maxVal = 100,
                value = None, parent = None):
      tkinter.Toplevel.__init__(self, parent)
      self.wm_title(variable)
      self.protocol('WM_DELETE_WINDOW',self.destroy)
      self.frame = tkinter.Frame(self)
      self.variable = variable
      if value == None:
         value = (maxVal + minVal) / 2.0
      resolution = .1 # (maxVal - minVal) / 100.0
      ticks = (maxVal - minVal) / 4.0
      self.scale = tkinter.Scale(self.frame, orient=tkinter.HORIZONTAL,
                                 length = 300, from_=minVal, to=maxVal,
                                 tickinterval=ticks, command = self.getValue,
                                 resolution = resolution)
      self.scale.set(value)
      self.frame.pack(fill = "both")
      self.scale.pack(fill = "both")

   def setValue(self, value):
      self.variable = value
      
   def getValue(self, event = None):
      return self.scale.get()

if __name__ == '__main__':
   # just to test
   app = tkinter.Tk()
   app.withdraw()
   slider = Slider("x", 0.0, 10.0, parent = app)
   app.mainloop()
