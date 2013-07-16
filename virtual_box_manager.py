
""" Gets Information about the virtual box vms installed in the """

import traceback
import subprocess
import re

class VirtualBoxVM(object):
  """ """
  def __init__(self, name = '', ip = '', running = ''):
    """"""
    self.name = name
    self.ip = ip
    self.running = running

  def __str__(self):
    """"""
    output = '[ (name, {0}) (ip, {1}) (running, {2}) ]'.format(self.name, self.ip, self.running)
    return output

    
class VirtualBoxManager(object):
  """  """
  
  VBOX_EXE = 'VBoxManage'
  VBOX_LIST_VMS = 'list vms'
  VBOX_LIST_RUNNING_VMS = 'list runningvms'
  VBOX_GET_PROPERTY = 'guestproperty get'
  VBOX_IP_PROPERTY = '"/VirtualBox/GuestInfo/Net/0/V4/IP"'

  # GET NAMES = VBoxManage list vms
  # GET IP = VBoxManage guestproperty get Development_Box  "/VirtualBox/GuestInfo/Net/0/V4/IP"

  def __init__(self):
    self._vms = []
  
  @staticmethod      
  def _execute_command_and_return_output(command):
    """ """
    output = []
    try:
      #print 'Executing {0}....'.format(command)
      proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout, stderr = proc.communicate()
    except Exception, e:
      traceback.print_exc(file=sys.stdout)
    else:
      lines = stdout.split('\n')
      lines = [line.strip() for line in lines]
      output = filter(None, lines)
    return output

  @staticmethod
  def is_vbox_installed():
    """ TODO: check that vbox is installed checking that VBoxManage is in the path"""
    installed = True
    try:
      subprocess.call([VirtualBoxManager.VBOX_EXE], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
      installed = False
    return installed

  def _get_ip(self, vm_name):
    """ """
    command = " ".join([ self.VBOX_EXE, self.VBOX_GET_PROPERTY, vm_name, self.VBOX_IP_PROPERTY])
    raw_ip = VirtualBoxManager._execute_command_and_return_output(command)
    vm_ip = None
    if len(raw_ip) > 0:
      raw_ip = raw_ip[0].replace(' ', '')
      match = re.search(r'^Value:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', raw_ip)
      if match:
        vm_ip = match.group(1)
    
    return vm_ip

  def _get_running_vms(self):
    """ """
    running_vms = []
    command = " ".join([ self.VBOX_EXE, self.VBOX_LIST_RUNNING_VMS ])
    raw_names = VirtualBoxManager._execute_command_and_return_output(command)
    for vm_name in raw_names:
      match = re.search(r'(".*")(.*){(.*)}', vm_name)
      if match:
        running_vms.append(match.group(1))
    return running_vms

  def _get_vm_names(self):
    """  """
    command = " ".join([ self.VBOX_EXE, self.VBOX_LIST_VMS ])
    raw_names = VirtualBoxManager._execute_command_and_return_output(command)
    names = []
    for vm_name in raw_names:
      match = re.search(r'(".*")(.*){(.*)}', vm_name)
      if match:
        names.append(match.group(1))
    return names

  def load_vms(self):
    """  """
    self.vms = []
    vm_names = self._get_vm_names()
    running_vms = self._get_running_vms()
    for vm_name in vm_names:
      vm = VirtualBoxVM()
      vm.name = vm_name
      vm.ip = self._get_ip(vm_name)
      if vm_name in running_vms:
        vm.running = True
      else:
        vm.running = False
      self.vms.append(vm)
        
  def __str__(self):
    """ """
    output = ''
    for vm in self.vms:
      output = output + str(vm) + '\n'
    return output
        
if __name__ == '__main__':
    
  print 'Virtual Box Manager\n'
  
  if VirtualBoxManager.is_vbox_installed():
    vb_manager = VirtualBoxManager()
    vb_manager.load_vms()
    print vb_manager 
  else:
    print "\nERROR: Can't find Virtual Box!\n"
    
  print 'Exiting...\n'
        
        
