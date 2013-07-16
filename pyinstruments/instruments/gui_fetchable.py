"""
Class GuiFetchable defines a bunch of useful methods for instruments that can be
used to query waveforms.
"""

import numpy
from hdnavigator import nav

class GuiFetchable(object):
    """Defines a bunch of useful methods for instruments that can be
    used to query waveforms."""
    
    _next_name = "some_file"
    _next_dir_name = "some_dir"

    def FetchXY(self):
        raise NotImplementedError("This function should be implemented in the \
                                    wrapper class")

    def save_curve(self):
        """Saves the curve using the hdnavigator module to find the location"""
        import myPandas
        x_y = self.FetchXY()
        myPandas.Series(x_y[1], index = x_y[0]).save(nav.next_file)
        nav.value_changed.emit()
        

    def _setup_fetch_utilities(self, widget):
        """sets up the gui to fetch the waveforms in widget"""
        widget._setup_gui_element("plot_xy")
        widget._setup_gui_element("xy_to_clipboard")
        
        widget_nav = nav._create_widget()
        widget.add_below(widget_nav)

        widget._setup_gui_element("save_curve")

    def plot_xy(self):
        """uses pylab to plot X and Y"""
        import pylab
        data = self.FetchXY()
        pylab.plot(data[0], data[1])
        pylab.show()
    
    
    def xy_to_clipboard(self):
        """copies X Y columnwise in the clipboard"""
        data = self.FetchXY()
        import StringIO
        string = StringIO.StringIO()
        fmt = "%.9g"
        numpy.savetxt(string, data.transpose(), delimiter = "\t", fmt = fmt)
        
        from pyinstruments import _APP
        clip = _APP.clipboard()
        clip.setText(string.getvalue())
        

    
    