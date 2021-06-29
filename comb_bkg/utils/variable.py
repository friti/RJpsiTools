class variable(object):
    def __init__(self, name, title, xlabel, unit,nbins, xmin, xmax):
        self.name=name
        self.title=title
        self.xlabel=xlabel
        self.unit=unit
#        self._cut=cut
        self.nbins=nbins
        self.xmin=xmin
        self.xmax=xmax
