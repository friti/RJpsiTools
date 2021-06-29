from utils.trigger import trigger_dict
class category(object):


  def __init__(self, name, df, trigger, mass_range, legend, color, marker, weight):
    self.__name = name
    self.__df = df
    self.__trigger = trigger
    self.__mass_range = mass_range
    self.__legend = legend
    self.__color = color
    self.__marker = marker
    self.__weight = weight
    if(not(trigger == None or mass_range == None)):
        self.__cuts = " & ".join([trigger_dict[trigger], "jpsi_mass > %5.2f & jpsi_mass < %5.2f" % (self.__mass_range[0], 
                                                                                                  self.__mass_range[1])])
  
  def get_color(self):
    return self.__color

  def get_name(self):
    return self.__name

  def get_cuts(self):
    return self.__cuts

  def get_legend(self):
    return self.__legend

  def get_marker(self):
    return self.__marker

  def get_weight(self):
    return self.__weight

  def get_mass_range(self):
    return self.__mass_range

  def get_trigger(self):
    return self.__trigger
     
  def get_df(self):
    if(self.__trigger == None or self.__mass_range == None):
      return self.__df
    else:
      return self.__df.query(self.__cuts)

  def get_mass_mean(self):
    return (self.__mass_range[0] + self.__mass_range[1])/2
