from hexi.plugin.InputPlugin import InputPlugin

class PluginInputFlightAttitude(InputPlugin):
  def __init__(self):
    self.configurable = True

  def print_name(self):
    print("Flight Attitude")
