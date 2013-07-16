""" """

from Tkinter import *
from virtual_box_manager import VirtualBoxManager, VirtualBoxVM

class VmFrame(Frame):
  
  def __init__(self, parent, vm_data):
    """ """
    Frame.__init__(self, parent)
    Label(self, text = vm_data.name).pack(fill="both", expand="yes")
    Button(self, text = 'Term').pack()
    self.pack()
  
  
class VirtualBoxManagerMainWindow(Frame):
    
  def __init__(self, parent, vbox_data):
    """ """
    Frame.__init__(self, parent, width=200)
    for vm in vbox_data.vms:
      frame = VmFrame(self, vm)
    self.pack()
    self.initUI()
        
  def initUI(self):
    pass
        
        
if __name__ == '__main__':
    
  if VirtualBoxManager.is_vbox_installed():
    vb_manager = VirtualBoxManager()
    vb_manager.load_vms()
    root = Tk()
    root.minsize(500,300)
    main_window = VirtualBoxManagerMainWindow(parent=root, vbox_data=vb_manager)
    main_window.mainloop()
  else:
    pass
    # TODO message box 
      
  