from hexi.plugin.InputPlugin import InputPlugin


class PluginInputFlightAttitude(InputPlugin):
  def __init__(self):
    super().__init__();
    self.configurable = True

  def print_name(self):
    print("Flight Attitude")
