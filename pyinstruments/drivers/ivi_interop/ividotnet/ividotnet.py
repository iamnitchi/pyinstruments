"""
Defines the base class for dotnet drivers
"""

from pyinstruments.drivers.ivi_interop import IviInteropDriver
from pyinstruments.drivers import Driver
from pyinstruments.drivers.ivi_interop.ividotnet.dotnet_communication import \
                                                        get_session_factory
from pyinstruments.drivers.ivi_interop.ividotnet import CONFIG_STORE


class IviDotNetDriver(IviInteropDriver):
    """Base class for ividotnet drivers. Requires a software module in
    addition to the other arguments for Driver"""
    
    _supported_software_modules =  []
    
    def get_driver(self):
        """
        function to get the driver using IVI factory functions
        and initialize communication with the instrument 
        """
        
        driver = get_session_factory().CreateSession(self.software_module)
        driver.Initialize(self.address, \
                          False, \
                          False, \
                          "Simulate = " + str(self.simulate))
        return driver
    
    @classmethod
    def get_software_module(cls, model):
        """
        given the model name,  returns the string corresponding to the 
        supporting software_module
        """
        
        software_module = CONFIG_STORE.get_sm_for_model(model)
        for dot_mod in software_module:
            if dot_mod.name in cls._supported_software_modules:
                return dot_mod.name
 
    @classmethod
    def supports(cls, model):
        """given a model string, returns True if instrument is supported,
        False otherwise
        """

        return cls.get_software_module(model) != None
        #software_module = CONFIG_STORE.get_sm_for_model(model)
        #for dot_mod in software_module:
        #    if dot_mod.name in cls._supported_software_modules:
        #        return True
        #return False