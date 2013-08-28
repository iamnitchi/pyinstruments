from pyinstruments.curvefinder.qtgui.gui import CurveCreateWidget
from pyinstruments.curvefinder.models import Window, Tag, curve_db_from_curve

from pyhardware.utils.guiwrappersutils import graphical_exception
import pyhardware.utils.gui_fetch_utils
from pyhardware.utils.gui_fetch_utils import FetcherMixin

import json
from PyQt4 import QtCore, QtGui

def monkey_patch(func):
    setattr(FetcherMixin, func.__name__, func)
    return func

@monkey_patch
def _get_initial_defaults(self):
    return {"default_name":'curve_%s'%self.__class__.__name__, \
     "default_window":'%s'%self.__class__.__name__, \
     "tags":["all"], \
     "comment":""}

@monkey_patch          
def get_curve(self):
    return curve_db_from_curve(self._get_curve())

@monkey_patch
def _get_defaults(self):
    settings = QtCore.QSettings("pyinstruments", "pyinstruments")
    kwds_str = str(settings.value("default_" + self.__class__.__name__).toString())
    if kwds_str != "":
        kwds = json.loads(kwds_str)
    else:
        kwds = self._get_initial_defaults()
    return kwds

@monkey_patch
def _save_defaults(self, **kwds):
    settings = QtCore.QSettings("pyinstruments", "pyinstruments")
    settings.setValue("default_" + self.__class__.__name__, json.dumps(kwds))

@monkey_patch
def _save_curve(self, curve):
    curve = curve_db_from_curve(curve)
    try:
        db_widget = self._dbwidget
    except AttributeError:
        pass
    else:
        curve.name = self._dbwidget.name
        curve.window_txt = self._dbwidget.window
        curve.save()
    
        tags = self._dbwidget.tags
        for tag_name in tags:
            (tag, new) = Tag.objects.get_or_create(name = tag_name)
            curve.tags.add(tag)
        curve.comment = self._dbwidget.comment
        
        self._save_defaults(default_name=curve.name, \
                            default_window=curve.window.name, \
                            comment=curve.comment, \
                            tags=tags)
    finally:
        curve.save()

@monkey_patch
def _setup_fetch_buttons(self, widget):
    """sets up the gui to fetch the waveforms in widget"""

    self._dbwidget = CurveCreateWidget(**self._get_defaults())
    self._dbwidget.hide_save_button()
    p = self._dbwidget.palette()
    p.setColor(self._dbwidget.backgroundRole(), QtCore.Qt.gray)
    self._dbwidget.setPalette(p)
    self._dbwidget.setAutoFillBackground(True)


    widget.add_below(self._dbwidget)
    widget._setup_horizontal_layout()
    self.button_save = QtGui.QPushButton('save')
    self.button_save.pressed.connect(graphical_exception(self.save_curve))
    
    widget.current_layout.addWidget(self.button_save)
    widget._exit_layout()




#class TraceGuiDB(DBFetchable, IviSpecAnGui.TraceGui):
#    _type_str = 'specan'

#class ChannelGuiDB(DBFetchable, IviScopeGui.ChannelGui):
#    _type_str = 'scope'
        
#class MeasurementGuiDB(DBFetchable, IviNaGui.ChannelGui.MeasurementGui):
#    _type_str = 'na'
        
#    def get_curve_complex(self):
#        return curve_db_from_curve( \
#                    super(MeasurementGuiDB, self).get_curve_complex())
        
#    def get_curve_formatted(self):
#        return curve_db_from_curve( \
#                    super(MeasurementGuiDB, self).get_curve_formatted())
        
        
        
        
#IviSpecAnGui.TraceGui = TraceGuiDB
#IviScopeGui.ChannelGui = ChannelGuiDB
#IviNaGui.ChannelGui.MeasurementGui = MeasurementGuiDB