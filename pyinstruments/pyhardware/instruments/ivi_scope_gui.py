"""
class to add gui-capabilities to IVI-compliant spectrum analyzers
"""
from pyinstruments.utils.curve import Curve
from pyinstruments.pyhardware.instruments import choices
from pyinstruments.pyhardware.instruments.gui_fetchable import GuiFetchable
from pyinstruments.pyhardware.wrappers import Wrapper
from pyinstruments.pyhardware.instruments.ivi_instrument import \
                                                IntermediateCollection
from pyinstruments.pyhardware.factories import use_for_ivi
from pyinstruments.pyhardware.instruments.iviguiinstruments import IviGuiInstrument

from pyinstruments.utils.guiwrappersutils import GuiWrapper
from numpy import array,linspace
import pandas

@use_for_ivi("IviScope")
class IviScopeGui(Wrapper, IviGuiInstrument):
    """
    class to add gui-capabilities to IVI-compliant spectrum analyzers
    """
    
    def __init__(self, *args, **kwds):
        super(IviScopeGui,self).__init__(*args,**kwds)
        IviGuiInstrument.__init__(self)
        self._wrap_attribute("Channels", \
                        IntermediateCollection(self.Channels, \
                        IviScopeGui.ChannelGui))
        
    def _setupUi(self, widget):
        """sets up the graphical user interface"""
        
        widget._setup_horizontal_layout()
        widget._setup_gui_element("Acquisition.Start")
        widget._setup_gui_element("Acquisition.Stop")
        widget._exit_layout()
        widget._setup_horizontal_layout()
        widget._setup_gui_element("Acquisition.TimePerRecord")
        widget._setup_gui_element("Acquisition.RecordLength")
        widget._exit_layout()
        widget._setup_horizontal_layout()
        widget._setup_gui_element("Acquisition.SampleRate")
        widget._setup_gui_element("Acquisition.StartTime")
        widget._exit_layout()
        widget._setup_horizontal_layout()
        widget._setup_gui_element("Acquisition.Type", \
                                  normal = 0, \
                                  peakDetect = 1, \
                                  hiRes = 2, \
                                  enveloppe = 3, \
                                  average = 4)
        widget._setup_gui_element("Acquisition.NumberOfAverages") 
        widget._exit_layout()
        widget._setup_tabs_for_collection("Channels")

    class ChannelGui(Wrapper, GuiWrapper, GuiFetchable):
        """
        class to add gui-capabilities to the sub object Channel
        """
        
        def __init__(self, *args, **kwds):
            Wrapper.__init__(self, *args,**kwds)
            GuiWrapper.__init__(self)
            GuiFetchable.__init__(self)
        
        def FetchXY(self):
            """returns an array with the X and Y columns filled.
            """
                
            (y_values, start, step) = self.FetchWaveform()
            n = len(y_values)
            return array([linspace(start, \
                                   start+step*n, \
                                   n, \
                                   endpoint = False), \
                          y_values])
        

        
        acquisition_types = choices.scope_acquisition_types
        couplings = choices.scope_couplings
        
        def get_curve(self):
            x_y = self.FetchXY()
            meta = dict()
            
            meta["acquisition_type"] = self.acquisition_types[ \
                    self.wrapper_parent.Acquisition.Type][0]
            meta["averaging"] = self.wrapper_parent.Acquisition.NumberOfAverages
            meta["start_time"] = self.wrapper_parent.Acquisition.StartTime
            meta["record_length"] = self.wrapper_parent.Acquisition.RecordLength
            meta["sample_rate"] = self.wrapper_parent.Acquisition.SampleRate
            meta["coupling"] = self.couplings[ \
                    self.wrapper_parent.Coupling][0]
            meta["full_range"] = self.Range
            meta["offset"] = self.Offset
            meta["input_freq_max"] = self.InputFrequencyMax
            meta["input_impedance"] = self.InputImpedance
            meta["channel"] = self.wrapper_name
            meta["curve_type"] = "ScopeCurve"
            meta["instrument_logical_name"] = \
                                self.wrapper_parent.logical_name
            
            curve = Curve(pandas.Series(x_y[1], index = x_y[0]), meta = meta)
            return curve
            
        def _setupUi(self, widget):
            """sets up the graphical user interface"""

            widget._setup_horizontal_layout()            
            widget._setup_gui_element("Enabled")
            widget._setup_gui_element("Coupling", \
                                      AC = 0, \
                                      DC = 1, \
                                      GND = 2)
            widget._exit_layout()
            widget._setup_horizontal_layout()     
            widget._setup_gui_element("Offset")
            widget._setup_gui_element("Range")
            widget._exit_layout()
            widget._setup_horizontal_layout()     
            widget._setup_gui_element("InputFrequencyMax")
            widget._setup_gui_element("InputImpedance")
            widget._exit_layout()
            self._setup_fetch_utilities(widget)