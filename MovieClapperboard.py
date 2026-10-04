''' Movie workbench, Movie Clapperboard to record and play animation and videos in FreeCAD '''

# ***************************************************************************
# *   Copyright (c) 2023 Francisco Rosa                                     *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

"""Creates a Clapperboard to save the animation of objects and cameras to play in FreeCAD."""

import os
import FreeCAD
import FreeCADGui as Gui
import shutil
import time
from PySide.QtGui import QFileDialog
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieAnimation as ma

#New
from PySide import QtWidgets
import tempfile

translate = FreeCAD.Qt.translate

_dir = os.path.dirname(__file__)
IconPath = os.path.join(_dir, 'icons')
LanguagePath = os.path.join(_dir, 'translations')
Gui.addLanguagePath(LanguagePath)

#=================================================
# 0. Globals
#=================================================

MESSAGE = translate('MovieClapperboard',
                    'Note: \n'
                    'This version of FreeCAD seems unable to import cv2!\n'
                    'To create or play back a video, try a different version, like 1.0, \n'
                    'or use the images generated here in an external recording program.')  + '\n'
#print(f'MESSAGE = {MESSAGE}')
TIP_ANIM_INIT = translate('App::Property',
                        'Initial step of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the step and/or frame which this \n'
                        'section of the animation and/or recording \n'
                        'will begin.')
#print(f'TIP_ANIM_INIT = {TIP_ANIM_INIT}')
TIP_ANIM_END = translate('App::Property',
                        'End step of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the step which this section of \n'
                        'the animation will finish.')
TIP_FRAME_NAME = translate('App::Property',
                        'Name of frame of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the main name of frames. Write a \n'
                        'short name, as this will be inserted in \n'
                        'the nomenclature of each one created.')
TIP_FRAME_WIDTH = translate('App::Property',
                        'Width of frames of the Clapperboard animation.\n'
                        '\n'
                        'Configure the width in pixels of the frames.')
TIP_FRAME_HEIGHT = translate('App::Property',
                        'Height of frames of the Clapperboard animation.\n'
                        '\n'
                        'Configure the height in pixels of the frames.')
TIP_FRAME_OUTPUT = translate('App::Property',
                        'Output path of the Clapperboard animation frames.\n'
                        '\n'
                        'Confirm the folder where the animation frames \n'
                        'will be saved.\n'
                        '\n'
                        'If you wish to preserve the generated images \n'
                        '(in the case of rendered ones, for example), \n'
                        'specify a folder other than the temporary folder.')
TIP_FRAME_TYPE = translate('App::Property',
                        'Type of frame of the Clapperboard animation.\n'
                        '\n'
                        'Indicates the type of frame to be saved. \n'
                        'To generate rendered images, you need to have \n'
                        'the Render Workbench installed and a project \n'
                        'already prepared.')
TIP_VIDEO_NAME = translate('App::Property',
                        'Name of the video of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the main name for the created videos. \n'
                        'If you prefer, chose to add manually “3D view“ \n'
                        'text or “Render” one, according to the origin \n'
                        'of the frames.')
TIP_VIDEO_NUMBER = translate('App::Property',
                        'Number of the video of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the initial number of the videos. This will \n'
                        'be inserted in the nomenclature of each one created.')
TIP_VIDEO_OUTPUT = translate('App::Property',
                        'Output path for the video of the Clapperboard \n'
                        'animation.\n'
                        '\n'
                        'Set path to folder to save created videos by \n'
                        'clicking on the button with the three dots \n'
                        'on the right.')
TIP_VIDEO_FPS = translate('App::Property',
                        'Fps of the video of the Clapperboard animation.\n'
                        '\n'
                        'Indicate the frames per second (fps) of the video \n'
                        'that will be created.')
TIP_VIDEO_PLAY = translate('App::Property',
                        'Read-only. \n'
                        '\n'
                        'Indicates whether the animation video will play \n'
                        'automatically after being generated.')

CL = None

#from MovieCamera import VIEW_00, VIEW_01

# ======================================================================================
# 1. Classes

# 1.1. Clapperboard - Movie Record toolbar

class Clapperboard:

    """Creates a object to save the settings of a Clapperboard."""

    def __init__(self,obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self,obj):

        """Gives the object properties to Clapperboard."""

        pl = obj.PropertiesList

        # Animation config
        if not 'Clap_01AnimIniStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Clap_01AnimIniStep', 'Animation config',
                                                TIP_ANIM_INIT).Clap_01AnimIniStep = 1
        if not 'Clap_02AnimCurrentStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Clap_02AnimCurrentStep', 'Animation config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                'Current step of the Clapperboard animation.\n'
                                                '\n'
                                                'It is only indicative.'
                                                )).Clap_02AnimCurrentStep = 1
        if not 'Clap_03AnimEndStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Clap_03AnimEndStep', 'Animation config',
                                                TIP_ANIM_END).Clap_03AnimEndStep = 100
        if not 'Clap_04AnimTotalSteps' in pl:
            obj.addProperty('App::PropertyInteger', 'Clap_04AnimTotalSteps', 'Animation config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                'Total steps of the Clapperboard animation.\n'
                                                '\n'
                                                'Indicates the number of steps through which \n'
                                                'the animation and/or the recording will be \n'
                                                'performed in this section.\n'
                                                '\n'
                                                'It is only indicative.'
                                                )).Clap_04AnimTotalSteps = 100
        if not 'Clap_05AnimFps' in pl:
            obj.addProperty('App::PropertyInteger', 'Clap_05AnimFps', 'Animation config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                'Animation fps of the Clapperboard.\n'
                                                '\n'
                                                'Indicate the fps through which the \n'
                                                'section of the animation will be \n'
                                                'performed. \n'
                                                '\n'
                                                'It is a simulation and will depend \n'
                                                'on the computer performance.'
                                                )).Clap_05AnimFps = 30
        if not 'Clap_06AnimTime' in pl:
            obj.addProperty('App::PropertyString', 'Clap_06AnimTime', 'Animation config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                'Animation time of the Clapperboard.\n'
                                                '\n'
                                                'Time in hours, minutes and seconds. \n'
                                                'It is only indicative.'
                                                )).Clap_06AnimTime = time.strftime("%H:%M:%S",
                                                                                    time.gmtime(
                                                                                    3.33))
        # Clapperboard config
        if not 'Clap_01Name' in pl:
            obj.addProperty('App::PropertyString', 'Clap_01Name', 'Clapperboard config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                               'Name for this Clapperboard.\n'
                                               '\n'
                                               'It will indicate the Clapperboard \n'
                                               'through which the animation and \n'
                                               'the recording will be performed. \n'
                                               '\n'
                                               'Write a short name, as this will \n'
                                               'be inserted in the nomenclature \n'
                                               'of each frame created.'
                                               )).Clap_01Name = 'Clap_00'
        if not 'Clap_02Take' in pl:
            obj.addProperty('App::PropertyString', 'Clap_02Take', 'Clapperboard config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                               'Take of the Clapperboard animation.\n'
                                               '\n'
                                               'Indicate the take of each recording \n'
                                               'made. Write a short name, as this \n'
                                               'will be inserted in the nomenclature \n'
                                               'of each frame created.'
                                               )).Clap_02Take = 'Take_01'
        if not 'Clap_03AnimationSelection' in pl:
            obj.addProperty('App::PropertyLinkList', 'Clap_03AnimationSelection', 'Clapperboard config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                'Selection of the Clapperboard animation.\n'
                                                '\n'
                                                'Select the MovieCameras and/or the MovieObjects \n'
                                                'to animate with this Clapperboard.'
                                                )).Clap_03AnimationSelection = None
        if not 'Clap_04OnRec' in pl:
            obj.addProperty('App::PropertyBool', 'Clap_04OnRec', 'Clapperboard config',
                                               QT_TRANSLATE_NOOP('App::Property',
                                               'Recording Clapperboard animation on or off.\n'
                                               '\n'
                                               'It is activated by the “Enable recording” button \n'
                                               'and deactivated by the “Stop recording” one.'
                                               )).Clap_04OnRec = False
        # Frames config
        if not 'Frame_01Name' in pl:
            obj.addProperty('App::PropertyString', 'Frame_01Name', 'Frames config',
                                               TIP_FRAME_NAME
                                               ).Frame_01Name = str(FreeCAD.ActiveDocument.Label)
        if not 'Frame_02Width' in pl:
            obj.addProperty('App::PropertyInteger', 'Frame_02Width', 'Frames config',
                                                TIP_FRAME_WIDTH).Frame_02Width = 800
        if not 'Frame_03Height' in pl:
            obj.addProperty('App::PropertyInteger', 'Frame_03Height', 'Frames config',
                                                TIP_FRAME_HEIGHT).Frame_03Height = 600
        if not 'Frame_04OutputPath' in pl:
            obj.addProperty('App::PropertyPath', 'Frame_04OutputPath', 'Frames config',
                                                TIP_FRAME_OUTPUT).Frame_04OutputPath = ""
        if not 'Frame_05Type' in pl:
            from MovieAnimation import VIEW_00, VIEW_01
            #from MovieCamera import VIEW_00, VIEW_01
            obj.addProperty('App::PropertyEnumeration', 'Frame_05Type', 'Frames config',
                                                TIP_FRAME_TYPE
                                                ).Frame_05Type = (f"00 - {VIEW_00}",
                                                                  f"01 - {VIEW_01}")
        if not 'Frame_06R1OnRec' in pl:
            obj.addProperty('App::PropertyBool', 'Frame_06R1OnRec', 'Frames config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                '“3D view” recording of the Clapperboard animation \n'
                                                'on or off.\n'
                                                '\n'
                                                'Indicates whether the chosen camera will record \n'
                                                'FreeCAD 3D views.\n'
                                                '\n'
                                                'It is indicative only.'
                                                )).Frame_06R1OnRec = False
        if not 'Frame_07R2OnRec' in pl:
            obj.addProperty('App::PropertyBool', 'Frame_07R2OnRec', 'Frames config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                '“Render” recording of the Clapperboard animation \n'
                                                'on or off.\n'
                                                '\n'
                                                'It indicates whether the chosen camera will record \n'
                                                'the renders images.\n'
                                                '\n'
                                                'It is indicative only.'
                                                )).Frame_07R2OnRec = False
        if not 'Frame_08R2RenderProject' in pl:
            obj.addProperty('App::PropertyString', 'Frame_08R2RenderProject', 'Frames config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                               'Render Project of the Clapperboard animation.\n'
                                               '\n'
                                               'If you are going to use images rendered by Render \n'
                                               'Workbench, indicate the internal name (not its \n'
                                               'label) of the previously created render project.'
                                               )).Frame_08R2RenderProject = "Project"
        # Video group config
        if not 'Video_01Name' in pl:
            obj.addProperty('App::PropertyString', 'Video_01Name', 'Video config',
                                               TIP_VIDEO_NAME
                                               ).Video_01Name = str(FreeCAD.ActiveDocument.Label)
        if not 'Video_02Number' in pl:
            obj.addProperty('App::PropertyInteger', 'Video_02Number', 'Video config',
                                                TIP_VIDEO_NUMBER).Video_02Number = 1
        if not 'Video_03InputFrames' in pl:
            obj.addProperty('App::PropertyPath', 'Video_03InputFrames', 'Video config',
                                                QT_TRANSLATE_NOOP('App::Property',
                                                'Input frames for the video of the Clapperboard \n'
                                                'animation.\n'
                                                '\n'
                                                'Indicate the path to the folder containing the \n'
                                                'frames for creating a video by clicking on \n'
                                                'the three dots on the right.'
                                                )).Video_03InputFrames = ""
        if not 'Video_04OutputPath' in pl:
            obj.addProperty('App::PropertyPath', 'Video_04OutputPath', 'Video config',
                                               TIP_VIDEO_OUTPUT).Video_04OutputPath = ""
        if not 'Video_05Fps' in pl:
            obj.addProperty('App::PropertyInteger', 'Video_05Fps','Video config',
                                                TIP_VIDEO_FPS).Video_05Fps = 24
        if not 'Video_06PlayVideo' in pl:
            obj.addProperty('App::PropertyBool', 'Video_06PlayVideo', 'Video config',
                                                TIP_VIDEO_PLAY).Video_06PlayVideo = False

class ClapperboardViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/ClapperboardIcon.svg'

class CreateClapperboard:

    """Creates a Clapperboard."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateClapperboardIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateClapperboard',
                                              'Clapperboard'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateClapperboard',
                                             'Create a Clapperboard to save the playback \n'
                                             'and recording settings of a MovieCamera or \n'
                                             'MovieObjects.\n'
                                             '\n'
                                             '1. Select one or more MovieCameras in sequence \n'
                                             'and click “Clapperboard”.\n'
                                             '\n'
                                             '2. You can also create an animation using only \n'
                                             'MovieObjects. Select one or more MovieObjects and \n'
                                             'click this button.\n'
                                             '\n'
                                             '3. To configure and prepare for recording, \n'
                                             'click the “Enable recording” button.\n'
                                             '\n'
                                             '4. To re-enable a Clapperboard, select one \n'
                                             'and click the “Enable an object for animation” \n'
                                             'button.'
                                             )}

    def IsActive(self):
        if Gui.ActiveDocument:
            selection = []
            selection = Gui.Selection.getSelection()
            if not selection:
                return False
            else:
                if any(condition for condition in [selection[0].Name[0:11] == 'MovieCamera',
                                                   selection[0].Name[0:12] == 'MovieObjects'
                                                  ]):
                    return True
        else:
            return False

    def Activated(self):

        global CL
        #Pre-selected objects (MovieCameras or Movieobjects)
        listObjects = []
        listObjects = Gui.Selection.getSelection()
        if not listObjects:
            FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                                   'Select at least one MovieCamera or MovieObject \n'
                                                   'to create a Clapperboard!') + '\n')
            return
        else:
            for n in range(len(listObjects)):
                if listObjects[n].Name[0:12] == 'MovieObjects' or listObjects[n].Name[0:11] == 'MovieCamera':
                    pass
                else:
                    FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                                       'To create a Clapperboard the pre-selected objects \n'
                                                       'must be MovieCamera or MovieObjects!') + '\n')
                    return
            Gui.Selection.clearSelection()
            ActivatedClapperboard(self)
            # Put MovieCamera or MovieObeject into CL.Clap_03AnimationSelection
            CL.Clap_03AnimationSelection = listObjects
            # Enable Clapperboard
            ma.enableMovieClapperboard(obj = CL)
            FreeCAD.ActiveDocument.recompute()

def ActivatedClapperboard(self):

    global CL
    default_label = translate('MovieClapperboard',
                              'Clapperboard')
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython',
                                              'Clapperboard')
    Clapperboard(folder)
    ClapperboardViewProvider(folder.ViewObject)
    CL = None
    CL = folder
    CL.Label = default_label
    FreeCAD.ActiveDocument.recompute()

# New
class EnableMovieRecord:

    """Enables a Clapperboard to save a animation (images and videos)."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableMovieRecordIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableMovieRecord',
                                              'Enable recording'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableMovieRecord',
                                             'Opens a task panel to configure the recording. \n'
                                             '\n'
                                             '1. After clicking on it, do not forget to confirm the \n'
                                             'folders to save the frames and the video in the \n'
                                             'opened task panel.\n'
                                             '\n'
                                             '2. To start recording the animations, click the \n'
                                             '“Play Forward” or “Play Backward” buttons of \n'
                                             'the “Animations tools”.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            #from MovieAnimation import CL
            if CL:
                #print(f'EnableMovieRecord, CL = {CL}')
                if CL.Name:
                    #print(f'EnableMovieRecord, CL.Name = {CL.Name}')
                    if ma.ENABLE_01 == 'Clapperboard':
                        if not CL.Clap_04OnRec:
                            return True
            #else:
                #print('EnableMovieRecord, there is no CL')

        else:
            return False

    def Activated(self):
        # --- Launching the Panel ---
        # Instantiate your panel class
        panel = RecordTaskPanel()

        # Open it inside the FreeCAD Task View panel
        Gui.Control.showDialog(panel)

class StopMovieRecord:

    """Stops the process of recording of a Clapperboard."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StopMovieRecordIcon.svg',
                'Accel': 'Ctrl+k',
                'MenuText': QT_TRANSLATE_NOOP('StopMovieRecord',
                                              'Stop recording'),
                'ToolTip': QT_TRANSLATE_NOOP('StopMovieRecord',
                                             'Stops the animation recording.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if CL.Clap_04OnRec:
                return True
        else:
            return False

    def Activated(self):
        stopMovieRecord(Clap = CL)

class RecordVideo:

    """Records a video from a sequence of images."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/RecordVideoIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('RecordVideo',
                                              'Record video'),
                'ToolTip': QT_TRANSLATE_NOOP('RecordVideo',
                                             'Creates a video from a sequence \n'
                                             'of created frames (images).\n'
                                             '\n'
                                             '1. Click this button and select the \n'
                                             'folder containing the image sequence \n'
                                             'of a created animation.\n'
                                             '\n'
                                             '2. Next, indicate the folder where the \n'
                                             'video should be saved and specify its name.\n'
                                             '\n'
                                             '3. At the end of the process, the video \n'
                                             'will play automatically.\n'
                                             '\n'
                                             '4. If you want to watch the video again, \n'
                                             'click the “Play video” button and select \n'
                                             'the corresponding file.\n'
                                             '\n'
                                             'Note: It works only with FreeCAD versions \n'
                                             'that import the cv2 module, like 1.0.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            #if not CL.Clap_04OnRec:
            #return True
            try:
                import cv2
                return True
            except Exception:
                return False
        else:
            return False

    def Activated(self):
        #if CL.Clap_04OnRec is True:
        createVideo()
        # Play video after recording
        playVideo(auto = True)
        #else:
            #return

class PlayVideo:

    """Plays a video from a file."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayVideoIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayVideo',
                                              'Play video'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayVideo',
                                             'Play an existing video by indicating its file path.\n'
                                             '\n'
                                             'Note: It works only with FreeCAD versions \n'
                                             'that import the cv2 module, like 1.0.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            try:
                import cv2
                return True
            except Exception:
                return False
        else:
            return False

    def Activated(self):
        playVideo()

#New
class RecordTaskPanel:

    """Provides a task panel for recording frames and videos."""

    def __init__(self):
        # The main widget
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle(translate('MovieClapperboard',
                                            'Recording settings'))

        # Layout
        layout = QtWidgets.QVBoxLayout(self.form)

        # Labels, Inputs, Buttons
        # Enabled Clapperboard
        global CL
        label1 = translate('MovieClapperboard','Enabled Clapperboard:')
        self.label_clapperboard1 = QtWidgets.QLabel(f'<b>{label1}<b>')
        self.label_clapperboard2 = QtWidgets.QLabel(CL.Label)
        layout.addWidget(self.label_clapperboard1)
        layout.addWidget(self.label_clapperboard2)
        # Instructions
        label2 = translate('MovieClapperboard','Instructions:')
        self.label_instructions = QtWidgets.QLabel(f'<b>{label2}<b>\n')
        layout.addWidget(self.label_instructions)
        self.label_text = QtWidgets.QLabel(translate('MovieClapperboard',
                                                      '1. Configure the animation properties below and '
                                                      'click “OK”. After this task panel closes, '
                                                      'the recording will be ready to begin.\n'
                                                      '\n'
                                                      '2. To start recording the animations, click '
                                                      'the “Play Forward” or “Play Backward” '
                                                      'buttons of the “Animations tools”. '
                                                      'Click “Pause Animation” to pause it '
                                                      'and “Stop Recording” to '
                                                      'stop the recording process.\n'
                                                      '\n'
                                                      '3. The final video will play '
                                                      'automatically if the “Save video” '
                                                      'and “Play video” checkboxes are enabled.'))
        self.label_text.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.label_text.setWordWrap(True)
        layout.addWidget(self.label_text)
        # Frames properties:
        label3 = translate('MovieClapperboard', 'Frame properties:')
        self.label_frames = QtWidgets.QLabel(f'<b>{label3}<b>\n')
        layout.addWidget(self.label_frames)
        # Type view
        self.label_type_view = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                  'Frame type:'))
        self.comboBox_view = QtWidgets.QComboBox()
        self.comboBox_view.addItem("")
        self.comboBox_view.addItem("")
        from MovieAnimation import VIEW_00, VIEW_01
        #from MovieCamera import VIEW_00, VIEW_01
        self.comboBox_view.setItemText(0, f"00 - {VIEW_00}")
        self.comboBox_view.setItemText(1, f"01 - {VIEW_01}")
        idx = int((CL.Frame_05Type)[0:2])
        if idx >= 0:
            self.comboBox_view.setCurrentIndex(idx)
        self.comboBox_view.setToolTip(TIP_FRAME_TYPE)
        self.row_type = QtWidgets.QGridLayout()
        self.row_type.addWidget(self.label_type_view, 0, 0)
        self.row_type.addWidget(self.comboBox_view, 0, 1)
        layout.addLayout(self.row_type)
        # Resolution
        self.label_resolution = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                     'Frame resolution:'))
        self.label_resolution_h = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                     'Height:'))
        self.spinBox_resolution_h = QtWidgets.QSpinBox()
        self.spinBox_resolution_h.setMaximum(10000)
        self.spinBox_resolution_h.setValue(CL.Frame_03Height)
        self.spinBox_resolution_h.setToolTip(TIP_FRAME_HEIGHT)
        self.label_resolution_w = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                     'width:'))
        self.spinBox_resolution_w = QtWidgets.QSpinBox()
        self.spinBox_resolution_w.setMaximum(10000)
        self.spinBox_resolution_w.setValue(CL.Frame_02Width)
        self.spinBox_resolution_w.setToolTip(TIP_FRAME_WIDTH)
        layout.addWidget(self.label_resolution)
        self.row_hw = QtWidgets.QGridLayout()
        self.row_hw.addWidget(self.label_resolution_h, 0, 0)
        self.row_hw.addWidget(self.spinBox_resolution_h, 0, 1)
        self.row_hw.addWidget(self.label_resolution_w, 0, 2)
        self.row_hw.addWidget(self.spinBox_resolution_w, 0, 3)
        layout.addLayout(self.row_hw)
        # Interval
        self.label_interval = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                 'Frame interval:'))
        self.label_frame_from = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                   'From frame:'))
        self.spinBox_frame_from = QtWidgets.QSpinBox()
        self.spinBox_frame_from.setMaximum(10000)
        self.spinBox_frame_from.setValue(CL.Clap_01AnimIniStep)
        print(f'TIP_ANIM_INIT = {TIP_ANIM_INIT}')
        self.spinBox_frame_from.setToolTip(TIP_ANIM_INIT)
        self.label_frame_to = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                 'to:'))
        self.spinBox_frame_to = QtWidgets.QSpinBox()
        self.spinBox_frame_to.setMaximum(10000)
        self.spinBox_frame_to.setValue(CL.Clap_03AnimEndStep)
        self.spinBox_frame_to.setToolTip(TIP_ANIM_END)
        layout.addWidget(self.label_interval)
        self.row_steps = QtWidgets.QGridLayout()
        self.row_steps.addWidget(self.label_frame_from, 0, 0)
        self.row_steps.addWidget(self.spinBox_frame_from, 0, 1)
        self.row_steps.addWidget(self.label_frame_to, 0, 2)
        self.row_steps.addWidget(self.spinBox_frame_to, 0, 3)
        layout.addLayout(self.row_steps)
        # Frame name
        self.label_frame_name = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                   'Frame names:'))
        self.lineEdit_frame_name = QtWidgets.QLineEdit(str(CL.Frame_01Name))
        self.lineEdit_frame_name.setToolTip(TIP_FRAME_NAME)
        self.row_frame_name = QtWidgets.QGridLayout()
        self.row_frame_name.addWidget(self.label_frame_name, 0, 0)
        self.row_frame_name.addWidget(self.lineEdit_frame_name, 0, 1)
        layout.addLayout(self.row_frame_name)
        # Frames output path
        self.label_output_path = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                    'Frames output folder path:'))
        self.lineEdit_output_path = QtWidgets.QLineEdit(str(CL.Frame_04OutputPath))
        self.lineEdit_output_path.setToolTip(TIP_FRAME_OUTPUT)
        self.toolButton_path = QtWidgets.QToolButton()
        self.toolButton_path.setToolTip(TIP_FRAME_OUTPUT)
        self.row1 = QtWidgets.QGridLayout()
        self.row1.addWidget(self.lineEdit_output_path, 0, 0)
        self.row1.addWidget(self.toolButton_path, 0, 1)
        layout.addWidget(self.label_output_path)
        layout.addLayout(self.row1)
        temp_dir = tempfile.gettempdir()
        if CL.Frame_04OutputPath == "" or CL.Frame_04OutputPath[0:3] == temp_dir[0:3]:
            #temporary folder
            tmp_folder = tempfile.mkdtemp()
            frames_path = tmp_folder
        else:
            frames_path = CL.Frame_04OutputPath
        self.lineEdit_output_path.setText(frames_path)
        self.toolButton_path.clicked.connect(self.open_output_path_file_dialog)
        # Video properties
        label4 = translate('MovieClapperboard','Video properties:')
        self.label_video = QtWidgets.QLabel(f'<b>{label4}<b>\n')
        # Save video
        self.checkBox_save_video = QtWidgets.QCheckBox()
        self.checkBox_save_video.setText(
                       translate('MovieClapperboard',
                                 'Save video'))
        self.checkBox_save_video.setToolTip(translate('MovieClapperboard',
                                                      'Indicate whether you also want to save \n'
                                                      'automatically the video after the frames \n'
                                                      'are produced. \n'
                                                      '\n'
                                                      'Alternatively, you can record the video \n'
                                                      'later by clicking the “Record video” \n'
                                                      'button or use external recording software \n'
                                                      'with the images generated.'))
        self.label_name = QtWidgets.QLabel(translate('MovieClapperboard',
                                                             'Video name:'))
        self.lineEdit_name = QtWidgets.QLineEdit(CL.Video_01Name)
        self.lineEdit_name.setToolTip(TIP_VIDEO_NAME)
        self.row_name = QtWidgets.QGridLayout()
        self.row_name.addWidget(self.label_name, 0, 0)
        self.row_name.addWidget(self.lineEdit_name, 0, 1)
        self.label_number = QtWidgets.QLabel(translate('MovieClapperboard',
                                                               'Video num.:'))
        self.spinBox_number = QtWidgets.QSpinBox()
        self.spinBox_number.setMaximum(1000)
        self.spinBox_number.setValue(CL.Video_02Number)
        self.spinBox_number.setToolTip(TIP_VIDEO_NUMBER)
        self.row_number = QtWidgets.QGridLayout()
        self.row_number.addWidget(self.label_number, 0, 0)
        self.row_number.addWidget(self.spinBox_number, 0, 1)
        # Fps
        self.label_fps = QtWidgets.QLabel(translate('MovieClapperboard',
                                                           'Fps:'))
        self.lineEdit_fps = QtWidgets.QLineEdit(str(CL.Video_05Fps))
        self.lineEdit_fps.setToolTip(TIP_VIDEO_FPS)
        self.row_fps = QtWidgets.QGridLayout()
        self.row_fps.addWidget(self.label_fps, 0, 0)
        self.row_fps.addWidget(self.lineEdit_fps, 0, 1)
        self.label_output_video = QtWidgets.QLabel(translate('MovieClapperboard',
                                                                     'Video output folder path:'))
        file_doc_path = os.path.abspath(FreeCAD.ActiveDocument.Name)
        folder_doc_path = os.path.dirname(file_doc_path)
        if CL.Video_04OutputPath == "":
            videos_path = folder_doc_path
        else:
            videos_path = CL.Video_04OutputPath
        self.lineEdit_output_video = QtWidgets.QLineEdit(str(videos_path))
        self.toolButton_video = QtWidgets.QToolButton()
        self.lineEdit_output_video.setToolTip(TIP_VIDEO_OUTPUT)
        self.toolButton_video.clicked.connect(self.open_output_path_video_file_dialog)
        self.lineEdit_output_video.setText(videos_path)
        self.checkBox_play_video = QtWidgets.QCheckBox()
        self.checkBox_save_video.toggled.connect(self.label_name.setEnabled)
        self.checkBox_save_video.toggled.connect(self.lineEdit_name.setEnabled)
        self.checkBox_save_video.toggled.connect(self.label_number.setEnabled)
        self.checkBox_save_video.toggled.connect(self.spinBox_number.setEnabled)
        self.checkBox_save_video.toggled.connect(self.label_fps.setEnabled)
        self.checkBox_save_video.toggled.connect(self.lineEdit_fps.setEnabled)
        self.checkBox_save_video.toggled.connect(self.label_output_video.setEnabled)
        self.checkBox_save_video.toggled.connect(self.lineEdit_output_video.setEnabled)
        self.checkBox_save_video.toggled.connect(self.toolButton_video.setEnabled)
        self.checkBox_save_video.toggled.connect(self.checkBox_play_video.setEnabled)
        self.checkBox_save_video.clicked.connect(self.checkBox_play_video_toggled)
        layout.addWidget(self.label_video)
        try:
            import cv2
            self.checkBox_save_video.setChecked(True)
            self.checkBox_play_video.setChecked(True)
        except Exception:
            self.label_cv2 = QtWidgets.QLabel(MESSAGE)
            self.label_cv2.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
            self.label_cv2.setWordWrap(True)
            layout.addWidget(self.label_cv2)
            self.checkBox_play_video.setEnabled(False)
            self.label_name.setEnabled(False)
            self.lineEdit_name.setEnabled(False)
            self.label_number.setEnabled(False)
            self.spinBox_number.setEnabled(False)
            self.label_fps.setEnabled(False)
            self.lineEdit_fps.setEnabled(False)
            self.label_output_video.setEnabled(False)
            self.lineEdit_output_video.setEnabled(False)
            self.toolButton_video.setEnabled(False)
            self.checkBox_save_video.setEnabled(False)
            self.lineEdit_output_path.setText(folder_doc_path)
        layout.addWidget(self.checkBox_save_video)
        layout.addLayout(self.row_name)
        layout.addLayout(self.row_number)
        layout.addLayout(self.row_fps)
        layout.addWidget(self.label_output_video)
        self.row2 = QtWidgets.QGridLayout()
        self.row2.addWidget(self.lineEdit_output_video, 0, 0)
        self.row2.addWidget(self.toolButton_video, 0, 1)
        layout.addLayout(self.row2)
        # Play video
        self.checkBox_play_video.setText(
                       translate('MovieClapperboard',
                       'Play video'))
        self.checkBox_play_video.setToolTip(TIP_VIDEO_PLAY)
        layout.addWidget(self.checkBox_play_video)
        print('Record panel was activated')

    def open_output_path_file_dialog(self):

        """Open output frame files dialog"""

        WindowTitle = translate('MovieClapperboard',
                                'Select the output folder for the frames.')
        OpenDir = self.lineEdit_output_path.text()
        output_path = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle, OpenDir)

        if output_path:
            self.lineEdit_output_path.setText(output_path)
            self.check_output_path() #?

    def check_output_path(self):

        """Checks the frames output path"""

        out_path1 = self.lineEdit_output_path.text()
        if not out_path1 or not os.path.isdir(out_path1):
            QtWidgets.QMessageBox.warning(
                self, translate("MovieClapperboard", "Warning"),
                translate("MovieClapperboard",
                "Indicate a output folder to save the frames before \n"
                "close the “Recording settings” task panel!")
            )
            return

    def open_output_path_video_file_dialog(self):

        """Open output video file dialog"""

        WindowTitle = translate('MovieClapperboard',
                                'Select the output folder for the video')
        OpenDir1 = self.lineEdit_output_path.text()
        output_path2 = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle, OpenDir1)

        if output_path2:
            self.lineEdit_output_video.setText(output_path2)
            self.check_video_output_path() #?

    def check_video_output_path(self):

        """Checks the video output path"""

        out_path2 = self.lineEdit_output_video.text()
        if not out_path2 or not os.path.isdir(out_path2):
            QtWidgets.QMessageBox.warning(
                self, translate("MovieClapperboard",
                                "Warning"),
                translate("MovieClapperboard",
                          "Indicate a output folder to save the video before \n"
                          "close the “Recording settings” task panel!")
            )
            return

    def checkBox_play_video_toggled(self):
        if self.checkBox_save_video.isChecked() is False:
            self.checkBox_play_video.setChecked(False)

    def accept(self):

        """Triggered automatically when the user clicks the 'OK' button."""

        global CL
        # Save Clapperboard settings
        # Interval
        CL.Clap_01AnimIniStep = self.spinBox_frame_from.value()
        CL.Clap_03AnimEndStep = self.spinBox_frame_to.value()
        # Frames
        CL.Frame_01Name = self.lineEdit_frame_name.text()
        # Resolution
        CL.Frame_02Width = self.spinBox_resolution_w.value()
        CL.Frame_03Height = self.spinBox_resolution_h.value()
        # Output path
        CL.Frame_04OutputPath = self.lineEdit_output_path.text()
        # Type view
        prefix = int(self.comboBox_view.currentText()[0:2])
        type_view_list = CL.getEnumerationsOfProperty("Frame_05Type")
        CL.Frame_05Type = type_view_list[prefix]
        # Save video
        CL.Video_01Name = self.lineEdit_name.text()
        CL.Video_02Number = self.spinBox_number.value()
        CL.Video_03InputFrames = self.lineEdit_output_path.text()
        CL.Video_04OutputPath = self.lineEdit_output_video.text()
        # Save frames
        if CL.Frame_05Type[0:2] == '00':
            startRecord3DView(auto = True)
        if CL.Frame_05Type[0:2] == '01':
            startRecordRender(auto = True)
        # Create video
        print(f'{self.checkBox_save_video.isChecked()}')
        if self.checkBox_save_video.isChecked() is True:
            print('createVideo was activated')
        # Video fps
        CL.Video_05Fps = int(self.lineEdit_fps.text())
        # Play video
        if self.checkBox_play_video.isChecked() is True:
            CL.Video_06PlayVideo = True
            print('playVideo was activated')
        # Warning
        FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                               'Recording is enabled! \n'
                                               'Click the animation playback button (forward or \n'
                                               'backward) to start recording the video. \n'
                                               'If the “Play video” option is enabled, \n'
                                               'it will play automatically at the end \n'
                                               'of the recording.') + '\n')
        # Close the task panel
        Gui.Control.closeDialog()
        return True

    def reject(self):

        """Triggered automatically when the user clicks 'Cancel'."""

        global CL
        print("Record panel was canceled.")
        # Delete tempfile?
        '''temp_dir = tempfile.gettempdir()
        frames_folder = self.lineEdit_output_path.text()
        if frames_folder [0:3] == temp_dir[0:3]:
            shutil.rmtree(frames_folder)'''
        CL.Clap_04OnRec = False
        Gui.Control.closeDialog()
        return True

    def getStandardButtons(self):

        """Defines which default FreeCAD buttons appear at the bottom."""

        return (QtWidgets.QDialogButtonBox.Ok |
                QtWidgets.QDialogButtonBox.Cancel)

'''
from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(187, 178)
        self.title = QtGui.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(10, 10, 271, 16))
        self.title.setObjectName("title")
        self.label_width = QtGui.QLabel(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

d = QtGui.QWidget()
d.ui = Ui_Dialog()
d.ui.setupUi(d)
d.show()

def warning_recording():
    d = QtGui.QWidget()
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.show()
'''
# ======================================================================================
# 2. Command functions

def getCLObject(cl = None):

    """Gets CL from another module"""

    global CL
    if cl != None:
        CL = cl

# 2.1. Frames recording commands

def startRecord3DView(auto = False):

    """Defines recording frames from a 3D view."""

    global CL
    CL.Clap_04OnRec = True
    #CL.Frame_05Type[0:2] = '00'
    CL.Frame_06R1OnRec = True
    if auto is False:
        WindowTitle = translate('MovieClapperboard',
                                'Select the folder to save the “3D view” frames')
        OpenDir = CL.Frame_04OutputPath
        CL.Frame_04OutputPath = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle, OpenDir)

def startRecordRender(auto = False):

    """Defines recording frames from a Render view."""

    global CL
    #import Render
    global START_RENDER_FRAME
    START_RENDER_FRAME = CL.Clap_02AnimCurrentStep
    #CL.Frame_05Type[0:2] = '01'
    CL.Clap_04OnRec = True
    CL.Frame_07R2OnRec = True
    if auto is False:
        WindowTitle = translate('MovieClapperboard',
                                'Select the folder to save the “Render” frames')
        OpenDir = CL.Frame_04OutputPath
        CL.Frame_04OutputPath = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle, OpenDir)

def stopMovieRecord(Clap = None):

    """Stops recording process."""

    global CL
    CL = Clap
    CL.Clap_04OnRec = False
    CL.Frame_06R1OnRec = False
    CL.Frame_07R2OnRec = False
    FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                           'Recording has been disabled!') + '\n'
                                           )

def runRecordCamera(Back = False):

    """Runs the recording process."""

    camNum = str(f'{CL.Clap_01Name:0>2}')
    takeNum = str(f'{CL.Clap_02Take:0>2}')
    #totalFrames = int(CL.Clap_03AnimEndStep - CL.Clap_01AnimIniStep)
    totalFrames = CL.Clap_03AnimEndStep - CL.Clap_01AnimIniStep + 1
    #subTotalFrames = int(CL.Clap_02AnimCurrentStep - CL.Clap_01AnimIniStep)
    subTotalFrames = CL.Clap_02AnimCurrentStep - CL.Clap_01AnimIniStep
    perFrames = str(int(subTotalFrames / totalFrames * 100)) + '%'

    if CL.Frame_06R1OnRec == True:
        if Back == False:
            frameNum = str(f'{CL.Clap_02AnimCurrentStep:0>4}')
        else:
            frameNum = str(f'{(CL.Clap_04AnimTotalSteps - CL.Clap_02AnimCurrentStep):0>4}')
        #frameFinalName = f'{CL.Frame_01Name}_{camNum}_{takeNum}_{CL.Frame_05Type}_{frameNum}.png'
        frameFinalName = f'{CL.Frame_01Name}_{camNum}_{takeNum}_{CL.Frame_05Type}_{frameNum}.jpg'
        pathAndName = CL.Frame_04OutputPath +'/' + frameFinalName
        Gui.activeDocument().activeView().saveImage(pathAndName,CL.Frame_02Width,CL.Frame_03Height,'Current')
        curFrame = int(frameNum)
        from MovieAnimation import VIEW_00
        #from MovieCamera import VIEW_00
        typeImage = VIEW_00

    if CL.Frame_07R2OnRec == True :
        if Back == False:
            frameNum = str(f'{CL.Clap_02AnimCurrentStep:0>4}')
        else:
            frameNum = str(f'{(CL.Clap_04AnimTotalSteps - CL.Clap_02AnimCurrentStep):0>4}')
        frameFinalName = f'{CL.Frame_01Name}_{camNum}_{takeNum}_{CL.Frame_05Type}_{frameNum}.png'
        project =  FreeCAD.getDocument(FreeCAD.ActiveDocument.Label).getObject(CL.Frame_08R2RenderProject)
        if CL.Clap_02AnimCurrentStep == START_RENDER_FRAME:
            output_file=project.Proxy.render(skip_meshing=False, wait_for_completion=True)
        else:
            output_file=project.Proxy.render(skip_meshing=True, wait_for_completion=True)
        #shutil.move(output_file, f'' + f'{CL.Frame_04OutputPath}/{frameFinalName}')
        shutil.move(output_file, f'{CL.Frame_04OutputPath}/{frameFinalName}')
        # Close render window
        if project.OpenAfterRender:
            Gui.runCommand('Std_CloseActiveWindow',0)
        from MovieAnimation import VIEW_01
        #from MovieCamera import VIEW_01
        typeImage = VIEW_01

    curFrame = int(frameNum)
    FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                           '{} frame {} of {} has been completed ({})'
                                            ).format(typeImage, curFrame, totalFrames, perFrames) + '\n')

# ======================================================================================
# 2.2. Create and play video commands

VIDEO_FILE = ''

def createVideo(auto = False):

    """Creates video file from a sequenced images (frames)"""

    global CL
    global VIDEO_FILE
    try:
        import cv2
    except Exception:
        FreeCAD.Console.PrintMessage(MESSAGE)
        return

    if auto is False:
        fileDocPath = os.path.abspath(FreeCAD.ActiveDocument.Name)
        folderDocPath = os.path.dirname(fileDocPath)
        openDir = None
        openDir = folderDocPath
        # Confirmation of the input frames folder to create video
        WindowTitle1 = translate('MovieClapperboard',
                                 'Select the frames folder to create video')
        inputFramesFolder = ''
        inputFramesFolder = QFileDialog.getExistingDirectory(Gui.getMainWindow(), WindowTitle1, openDir)
        if inputFramesFolder == '':
            return
        # Confirmation of the output folder to save video
        WindowTitle1 = translate('MovieClapperboard',
                                 'Select the folder to save the video')
        outputFilePath = ''
        outputFilePath = QFileDialog.getSaveFileName()[0]
        if outputFilePath == '':
            return

        pathFrames = inputFramesFolder + '/'
        frames_folder = inputFramesFolder
        fps = 24
        outVideoFullPath = outputFilePath + '.mp4'

    else:
        pathFrames = CL.Video_03InputFrames +'/'
        outVideoPath = CL.Video_04OutputPath + '/'
        CL.Video_02Number += 1
        videoNum = str(f'{CL.Video_02Number:0>2}')
        outVideoName = str(f'{CL.Video_01Name}_{CL.Clap_01Name}_{CL.Clap_02Take}_{CL.Frame_05Type}_{videoNum}.mp4')
        outVideoFullPath = outVideoPath+outVideoName
        fps = CL.Video_05Fps
        frames_folder = CL.Frame_04OutputPath

    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    inFrames = sorted(os.listdir(pathFrames))

    frames = []

    for i in inFrames:
        i = pathFrames+i
        frames.append(i)

    frame1 = cv2.imread(frames[0])
    size1 = list(frame1.shape)
    del size1[2]
    Heightframe1, Widthframe1 = size1

    # Output video name, fourcc, fps, size (height, width)
    video = cv2.VideoWriter(outVideoFullPath, cv2_fourcc, fps, (Widthframe1, Heightframe1))

    for i in range(len(frames)):
        video.write(cv2.imread(frames[i]))
        FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                               'Recording of frame {} of {} ({}%)'
                                               ).format(i+1, len(frames), int((i+1)/len(frames)*100)
                                               ) + '\n')

    video.release()
    # Delete tempfile
    temp_dir = tempfile.gettempdir()

    if frames_folder[0:3] == temp_dir[0:3]:
        shutil.rmtree(frames_folder)
    FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                           'Output video to {}').format(outVideoFullPath)+'\n')
    VIDEO_FILE = outVideoFullPath

def playVideo(auto = False):

    """Plays video files"""

    try:
        import cv2
    except Exception:
        FreeCAD.Console.PrintMessage(MESSAGE)
        return

    import time

    MovieFileFilter = '; All files (*.*)'
    WindowTitle = translate('MovieClapperboard', 'Select file to play')
    pathFile = None
    if auto is True and VIDEO_FILE != '':
        pathFile = [VIDEO_FILE]
    else:
        fileDocPath = os.path.abspath(FreeCAD.ActiveDocument.Name)
        folderDocPath = os.path.dirname(fileDocPath)
        OpenDir = folderDocPath +'/'
        pathFile = QFileDialog.getOpenFileName(Gui.getMainWindow(), WindowTitle, OpenDir, MovieFileFilter)
    if pathFile[0] == '':
        return
    else:
        Video_pathFile = pathFile[0]

    cap = cv2.VideoCapture(Video_pathFile)

    fps2 = int(cap.get(cv2.CAP_PROP_FPS))

    if cap.isOpened() == False:
        FreeCAD.Console.PrintMessage(translate('MovieClapperboard',
                                               'Error: video file not found!') + '\n')
        return

    else:
        message2 = ('Movie preview at {} fps, press q to stop the video').format(fps2)
        '''
        translate doesn't work with cv2.imshow()!
        message2 = (translate('MovieClapperboard',
                              'Movie at {} fps, press q to stop the video').format(fps2))
        '''
    while cap.isOpened():
        success, frame = cap.read()
        if success == True:
            time.sleep(1/fps2)
            cv2.imshow(message2, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    #cv2.destroyAllWindows()

# ======================================================================================
# 3. Commands

if FreeCAD.GuiUp:

    FreeCAD.Gui.addCommand('CreateClapperboard', CreateClapperboard())
    #New
    FreeCAD.Gui.addCommand('EnableMovieRecord', EnableMovieRecord())
    FreeCAD.Gui.addCommand('StopMovieRecord', StopMovieRecord())
    FreeCAD.Gui.addCommand('RecordVideo', RecordVideo())
    FreeCAD.Gui.addCommand('PlayVideo', PlayVideo())

# ======================================================================================

#https://wiki.freecad.org/Command
#https://wiki.freecad.org/Translating_an_external_workbench
