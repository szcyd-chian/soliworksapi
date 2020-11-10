"""This module creates an python interface to Solidworks"""

import os
import subprocess as sb

import win32com.client

from .interfaces.isldworks import ISldWorks
from .modeldoc import ModelDoc


class SolidWorks(ISldWorks):
    """SolidWorks creates an interface to the current primary SolidWorks
    session.

    If no SolidWorks session currently exist, a session will be created upon
    instantiation. Note that this session will be running in the background and
    its existiance will not be apparent. To make this session visible, set its
    visibility attribute :attr:'visible' to True.
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"<{self.__class__.__name__}><{self.get_process_id()}>"

    def __str__(self):
        return f"{self.__class__.__name__}"

    @staticmethod
    def start(*args):
        """Starts a SolidWorks session.

        This method starts a new SolidWorks Session. It is equivalent to
        launching SolidWorks manually and all add-in, user-preference, etc.
        will be loaded using this method. If SolidWorks session with all the
        user preferences loaded is desired. Launch the session using this
        static method proir to instantiating an instance of :class:'SolidWorks'

        Args: version (int, optional): Last 2-digits of the year of the
            SolidWorks instance you would like to use. If there is only one
            version of SolidWorks installed on your machine DO NOT enter an
            arguement

        Examples: SolidWorks.start(20)
        """

        if not args:
            SW_PROCESS_NAME = (
                r"C:/Program Files/SOLIDWORKS Corp/SOLIDWORKS/SLDWORKS.exe"
            )
            sb.Popen(SW_PROCESS_NAME)
        else:
            year = int(args[0][-1])
            SW_PROCESS_NAME = f"SldWorks.Application.{(20 + (year - 2))}"
            win32com.client.Dispatch(SW_PROCESS_NAME)

    @staticmethod
    def kill():
        """Force kill SLDWORKS.exe process.

        This method will force kill the current solidworks session. This method
        is independ of the SolidWorks API and terminates the SolidWorks session
        killing the the SLDWORKS.exe process.

        This method should be used in the case that SolidWorks is not
        responding. The prefered method for shutting down the SolidWorks
        session is 'shutdown()'
        """
        sb.call("Taskkill /IM SLDWORKS.exe /F")

    @property
    def process_id(self):
        """Returns SolidWorks process ID"""
        return self.get_process_id()

    def open(self, path, options=1, configuration=str()):
        """Opens a native SolidWorks documents

        Args:
            path (str): The path of the SolidWorks file you want to load
            options (int, optional): The mode you wish to open the document in.
            Defaults to 1. See SolidWorks API for alternate options
            configuration (str, optional): The configuration of the model to be
            opened. Defaults to str() which opens the lasted opened
            configuration

        Raises:
            ValueError: File must me a SolidWorks native file. Acceptable file
            extensions include [.SLDPRT, .SLDASM, .SLDDRW]

        Returns:
            Error: Error raised while opening the document
            Warning: Warnings returned while opening the document
        """

        if os.path.splitext(path)[1] == ".SLDPRT":
            type_value = 1
        elif os.path.splitext(path)[1] == ".SLDASM":
            type_value = 2
        elif os.path.splitext(path)[1] == ".SLDDRW":
            type_value = 3
        else:
            raise ValueError("Incompatible File Type")

        err, warn = self._opendoc6(path, type_value, options, configuration)
        return err.value, warn.value

    def shutdown(self):
        """Exits the SolidWorks session

        shutdown is the prefered method for terminating as solidworks session
        """
        self.exit_app()

    def get_model(self):
        """Returns the model document currently active in the SolidWorks session

        Returns:
            ModelDoc: A SolidWorks model or document
        """
        return ModelDoc()

    def get_models(self):
        """Returns all the model documents currently loaded in the SolidWorks
        session

        Returns:
            List of ModelDoc: A list of all the model/documents loaded in the
            SolidWorks session
        """
        return [ModelDoc(system_object) for system_object in self._get_documents()]
