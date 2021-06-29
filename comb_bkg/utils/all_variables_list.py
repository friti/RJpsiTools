from variable import variable

#class variable(object):
#    def __init__(self, name, title, xlabel, unit,nbins, xmin, xmax):
#        self.name=name
#        self.title=title
#        self.xlabel=xlabel
#        self.unit=unit
#        self.nbins=nbins
#        self.xmin=xmin
#        self.xmax=xmax


all_variables_list =[
    variable("bvtx_chi2", "3#mu vertex #chi^{2}", "3#mu vertex #chi^{2}", "", 40, 0., 40),
    variable("bvtx_svprob", "3#mu vertex probability", "3#mu vertex probability", "", 40, 0., 1.),
    variable("bvtx_lxy_sig","","","",40 , 0. , 120.),
    variable("bvtx_lxy","","","[cms]", 40 ,0. , 1.),
    variable("bvtx_lxy_unc","","","", 40, 0., 0.02),
    variable("bvtx_vtx_x","3#mu vertex x","3#mu vertex x","[cms]", 30 , -0.3, 0.3),
    variable("bvtx_vtx_y","3#mu vertex y","3#mu vertex y","[cms]", 30 , -0.3, 0.3),
    variable("bvtx_vtx_z","3#mu vertex z","3#mu vertex z","[cms]", 30 , -15., 15.),
    variable("bvtx_vtx_x","3#mu vertex x error","3#mu vertex x error","[cms]", 30 , 0., 0.03),
    variable("bvtx_vtx_y","3#mu vertex y error","3#mu vertex y error","[cms]", 30 , 0., 0.03),
    variable("bvtx_vtx_z","3#mu vertex z error","3#mu vertex z error","[cms]", 30 , .0, 0.06),
    variable("bvtx_cos2D","","","", 50 , 0., 1.),
    variable("jpsivtx_chi2", "2#mu vertex #chi^{2}", "2#mu vertex #chi^{2}", "", 40, 0., 20),
    variable("jpsivtx_svprob", "2#mu vertex probability", "2#mu vertex probability", "", 40, 0., 1.),
    variable("jpsivtx_lxy_sig","","","",40 , 0. , 120.),
    variable("jpsivtx_lxy","","","[cms]", 40 ,0. , 1.),
    variable("jpsivtx_lxy_unc","","","", 40, 0., 0.04),
    variable("jpsivtx_vtx_x","2#mu vertex x","2#mu vertex x","[cms]", 30 , -0.3, 0.3),
    variable("jpsivtx_vtx_y","2#mu vertex y","2#mu vertex y","[cms]", 30 , -0.3, 0.3),
    variable("jpsivtx_vtx_z","2#mu vertex z","2#mu vertex z","[cms]", 30 , -15., 15.),
    variable("jpsivtx_vtx_x","2#mu vertex x error","2#mu vertex x error","[cms]", 30 , 0., 0.03),
    variable("jpsivtx_vtx_y","2#mu vertex y error","2#mu vertex y error","[cms]", 30 , 0., 0.03),
    variable("jpsivtx_vtx_z","2#mu vertex z error","2#mu vertex z error","[cms]", 30 , .0, 0.06),
    variable("jpsivtx_cos2D","","","", 50 , 0., 1.),
    variable("","","","", , , ),
    variable("","","","", , , ),
    variable("","","","", , , ),
    variable("","","","", , , ),
    ]

