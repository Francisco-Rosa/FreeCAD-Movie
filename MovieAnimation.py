''' Movie workbench, Movie Animation to play animation in FreeCAD '''

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

"""Creates a animation of objects and cameras to play in FreeCAD."""

import os
import FreeCAD
import FreeCADGui as Gui
import time
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieCamera as mc
import MovieObject as mo
import MovieConnection as co
import MovieClapperboard as cl

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Global and notifications

ENABLE_00 = 'None' #Only enabled for configuration and saving properties
ENABLE_01 = 'None' #Enabled for configuration and saving properties and animation
MC = None
MO = None
CL = None
STEP_POS = 'I' # or 'P' for ANIM_CURRENT_STEP > ANIM_INI_STEP
ANIMATION = False
ANIMATION_BACK = False
ANIM_INI_STEP = None

#New
ANIM_CURRENT_STEP = None
ANIM_FPS = None
ANIM_END_STEP = None
ANIM_TOTAL_STEPS = None
CAMERA_NAME = 'None'
OBJECTS_NAME = 'None'
SEQ_ANIM_DIC = {}

# ======================================================================================
# 1. Classes
#New
class EnableAnimation:

    """Enables the movie objects for animation."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableAnimation',
                                              'Enable an object for animation'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableAnimation',
                                             '1. Select a MovieCamera, MovieObjects or \n'
                                             'Clapperboard already set up, then click \n'
                                             'on this button to save the configurations \n'
                                             'made and activate it for the animation.\n'
                                             '\n'
                                             '1.1 It is possible to create an animated \n'
                                             'sequence of MovieCameras and/or MovieObjects \n'
                                             'by selecting them as a group in the \n'
                                             'desired order.\n'
                                             '\n'
                                             '2. After enabled, control the animation \n'
                                             'using the animation buttons.\n'
                                             '\n'
                                             '3. To disable the animation, click ”Disables \n'
                                             'any object for animation” button.'
                                             )}

    def IsActive(self):
        if Gui.ActiveDocument:
            selection = []
            selection = Gui.Selection.getSelection()
            if not selection:
                return False
            else:
                if any(condition for condition in [
                                            selection[0].Name[0:11] == 'MovieCamera',
                                            selection[0].Name[0:12] == 'MovieObjects',
                                            selection[0].Name[0:12] == 'Clapperboard'
                                            ]):
                    return True
        else:
            return False

    def Activated(self):
        global CL
        selection = []
        selection = Gui.Selection.getSelection()
        FreeCAD.Gui.runCommand('DisableAnimation')
        if selection:
            if selection[0].Name[0:11] == 'MovieCamera':
                indicateMovieSelection(obj = 'Camera')
            if selection[0].Name[0:12] == 'MovieObjects':
                indicateMovieSelection(obj = 'Objects')
            if selection[0].Name[0:12] == 'Clapperboard':
                enableAnimObjects(obj1 = 'Clapperboard')
                CL = None
                CL = enableMovieClapperboard(obj = CL, clapNew = False)
        FreeCAD.ActiveDocument.recompute()
        #print(f'EnableAnimation, selection = {selection[0].Name}')

class DisableAnimation:

    """Disables the movie objects for animation."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/DisableAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('DisableAnimation',
                                              'Disable any object for animation'),
                'ToolTip': QT_TRANSLATE_NOOP('DisableAnimation',
                                             '1. To disable the animation status, click \n'
                                             'this button.'
                                             )}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ENABLE_01
        #New
        try:
            if ENABLE_01[0:6] == 'Camera':
                #label = MC.Label
                #MC.Label = changeEnableLabel(objLabel = label, enable = False)
                if FreeCAD.GuiUp:
                    for s in range(len(SEQ_ANIM_DIC)):
                        MC = FreeCAD.ActiveDocument.getObject(SEQ_ANIM_DIC[s][0])
                        vp = mc.MovieCameraViewProvider(MC.ViewObject)
                        vp.setEnabledState(MC.ViewObject, False)
            if ENABLE_01 == 'Objects':
                #label = MO.Label
                #MO.Label = changeEnableLabel(objLabel = label, enable = False)
                if FreeCAD.GuiUp:
                    for o in range(len(SEQ_ANIM_DIC)):
                        MO = FreeCAD.ActiveDocument.getObject(SEQ_ANIM_DIC[o][3])
                        vp = mo.MovieObjectsViewProvider(MO.ViewObject)
                        vp.setEnabledState(MO.ViewObject, False)
            if ENABLE_01 == 'Clapperboard':
                #label = CL.Label
                #CL.Label = changeEnableLabel(objLabel = label, enable = False)
                if FreeCAD.GuiUp:
                    vp = cl.ClapperboardViewProvider(CL.ViewObject)
                    vp.setEnabledState(CL.ViewObject, False)
        except:
            pass
        ENABLE_01 = 'None'
        FreeCAD.Gui.runCommand('StopMovieRecord')
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                                       'The cameras and/or objects have \n'
                                       'been disabled for the animation!'))

        FreeCAD.ActiveDocument.recompute()

class IniMovieAnimation:

    """Returns the movie objects to the beginning of the animation."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/IniMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('IniMovieAnimation',
                                              'Return to beginning'),
                'ToolTip': QT_TRANSLATE_NOOP('IniMovieAnimation',
                                             '1. On the first click, it returns to the \n'
                                             'beginning of the animation of the \n'
                                             'current camera/objects and resets them. \n'
                                             '\n'
                                             '2. On the second click, it goes to the \n'
                                             'end of the animation of the \n'
                                             'previous camera/objects (if so).'),
                                             'Accel': "Ctrl+1"}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ANIM_CURRENT_STEP
        global STEP_POS
        modifyAnimationIndicator(animation = False)
        if MC != None:
            # 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    co.connectionIni(Selection = MC)
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        ANIM_CURRENT_STEP = ANIM_INI_STEP
                        STEP_POS = 'I'
                        if ENABLE_01 == 'Clapperboard':
                            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
                        getMovieMobile()
                        Gui.updateGui()
                        return
        recoverIniMovieAnimation()

class PrevMovieAnimation:

    """Moves the animation of movie objects one step back."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PrevMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PrevMovieAnimation',
                                              'Take a step back'),
                'ToolTip': QT_TRANSLATE_NOOP('PrevMovieAnimation',
                                             'Moves the animation one step back.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        modifyAnimationIndicator(animation = False)
        if MC != None:
            # 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    co.connectionPrev(Selection = MC)
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        getMessage(message = translate('MovieAnimation',
                                                       'Take a step back does not work \n'
                                                       'with ExplodedAssembly!'))
                        return
        prevMovieAnimation()

class PlayBackwardMovieAnimation:

    """Plays backward the animation of movie objects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayBackwardMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayBackwardMovieAnimation',
                                              'Play backward the animation'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayBackwardMovieAnimation',
                                             'Plays backward the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ANIMATION_BACK
        ANIMATION_BACK = True
        if MC != None:
            # 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        getViewProjection()
                        co.connectionPlayBackward(Selection = MC)
                        FreeCAD.ActiveDocument.recompute()
                        return
        playMovieAnimation()
        #new
        if CL != None:
            try:
                if CL.Clap_04OnRec is True:
                    cl.createVideo(auto = True)
                    #Open Report view
                    openReportView()
                    if CL.Frame_05Type[0:2] == '01':
                        try:
                            projectRender = CL.Frame_08RenderProject
                            projectRender.OpenAfterRender = True
                        except:
                            pass
                    if CL.Video_06PlayVideo is True:
                        cl.playVideo(auto = True)
                    CL.Clap_04OnRec = False
            except:
                pass

class PauseMovieAnimation:

    """Pause the animation of movie objects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PauseMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PauseMovieAnimation',
                                              'Pause the animation'),
                'ToolTip': QT_TRANSLATE_NOOP('PauseMovieAnimation',
                                             'Pauses the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global MC
        global ANIMATION_BACK
        ANIMATION_BACK = False
        pauseMovieAnimation()
        FreeCAD.ActiveDocument.recompute()
        if MC != None:
            # 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    co.connectionPause(Selection = MC)
                    MC.Cam_07OnAnim = False
                    FreeCAD.ActiveDocument.recompute()

class PlayMovieAnimation:

    """Plays forward the animation of movie objects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayMovieAnimation',
                                              'Play the animation'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayMovieAnimation',
                                             'Plays the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ANIMATION_BACK
        ANIMATION_BACK = False
        if MC != None:
            # 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        getViewProjection()
                        co.connectionPlay(Selection = MC)
                        FreeCAD.ActiveDocument.recompute()
                        return
        playMovieAnimation()
        #new
        if CL != None:
            try:
                if CL.Clap_04OnRec is True:
                    cl.createVideo(auto = True)
                    #Open Report view
                    openReportView()
                    if CL.Frame_05Type[0:2] == '01':
                        try:
                            projectRender = CL.Frame_08RenderProject
                            projectRender.OpenAfterRender = True
                        except:
                            pass
                    if CL.Video_06PlayVideo is True:
                        cl.playVideo(auto = True)
                    CL.Clap_04OnRec = False
            except:
                pass

class PostMovieAnimation:

    """Moves the animation of movie objects one step forward."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PostMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PostMovieAnimation',
                                              'Move one step forward'),
                'ToolTip': QT_TRANSLATE_NOOP('PostMovieAnimation',
                                             'Moves the animation one step forward.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        modifyAnimationIndicator(animation = False)
        if MC != None:
            #i 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    co.connectionPos(Selection = MC)
                    FreeCAD.ActiveDocument.recompute()
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        getMessage(message = translate('MovieAnimation',
                                                       'Move one step forward, \n'
                                                       'does not work with ExplodedAssembly!'))
                        return
        postMovieAnimation()

class EndMovieAnimation:

    """Moves the movie objects animation to its end."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EndMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EndMovieAnimation',
                                              'Move to the end'),
                'ToolTip': QT_TRANSLATE_NOOP('EndMovieAnimation',
                                             '1. On the first click, it moves to the \n'
                                             'end of the animation of the current \n'
                                             'camera/objects.\n'
                                             '\n'
                                             '2. On the second click, it goes to the \n'
                                             'beginning of the animation of the \n'
                                             'next camera/objects (if so).'),
                'Accel': "Ctrl+2"}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ANIM_CURRENT_STEP
        global STEP_POS
        modifyAnimationIndicator(animation = False)
        if MC != None:
            # 'Camera and connection' or 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                    co.connectionEnd(Selection = MC)
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        ANIM_CURRENT_STEP = ANIM_END_STEP
                        STEP_POS = 'I'
                        if ENABLE_01 == 'Clapperboard':
                            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
                        getMovieMobile()
                        Gui.updateGui()
                        return
        getEndMovieAnimation()

# 1.2. Movie common tools

class SetMoviePosA:

    """Sets the A position for a MovieCamera or MovieObjects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMoviePosAIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMoviePosA',
                                              'Set position A'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMoviePosA',
                                             'Applicable for creating an animation from \n'
                                             'point A to B (not when the MovieCamera \n'
                                             'target or MovieObjects are set up to \n'
                                             'follow a route).\n'
                                             '\n'
                                             '1. First, select and activate the \n'
                                             'MovieCamera or MovieObjects you want \n'
                                             'to configure.\n'
                                             '\n'
                                             '2. For MovieCameras, position the 3D \n'
                                             'view with the desired framing to be the start \n'
                                             'of the animation (position A), then click on \n'
                                             'Set position A.\n'
                                             '\n'
                                             '3. For MovieObjects, position, rotate \n'
                                             'or keep them in their current position, \n'
                                             'then click on this button.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_00 != 'None': # Only enabled for configuration
                if not ANIMATION:
                    selection = []
                    selection = Gui.Selection.getSelection()
                    if not selection:
                        return False
                    else:
                        if selection[0].Name[0:11] == 'MovieCamera' or selection[0].Name[0:12] == 'MovieObjects':
                            return True
        else:
            return False

    def Activated(self):
        if ENABLE_00 == 'Objects':
            mo.setMOPosAB(obj = MO, position = 'A')
        if ENABLE_01 == 'Camera' or ENABLE_01 == 'Camera and objects' or ENABLE_01 == 'Camera and connection':
            mc.setMCPosA(Option = MC)

class SetMoviePosB:

    """Sets the B position for a MovieCamera or MovieObjects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMoviePosBIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMoviePosB',
                                              'Set position B'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMoviePosB',
                                             'Applicable for creating an animation from \n'
                                             'point A to B (not when the MovieCamera \n'
                                             'target or MovieObjects are set up to \n'
                                             'follow a route).\n'
                                             '\n'
                                             '1. Select and activate the MovieCamera \n'
                                             'or MovieObjects you want to configure.\n'
                                             '\n'
                                             '2. For MovieCameras, position the 3D \n'
                                             'view with the desired framing to be \n'
                                             'the end of the animation (position B), \n'
                                             'then click on Set position B.\n'
                                             '\n'
                                             '3. For MovieObjects, position and/or \n'
                                             'rotate them to the final position, then \n'
                                             'click on this button.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if ENABLE_00 != 'None': # Only enabled for configuration
                if not ANIMATION:
                    selection = []
                    selection = Gui.Selection.getSelection()
                    if not selection:
                        return False
                    else:
                        if selection[0].Name[0:11] == 'MovieCamera' or selection[0].Name[0:12] == 'MovieObjects':
                            return True
        else:
            return False

    def Activated(self):
        global ENABLE_01
        if ENABLE_00 == 'Objects':
            mo.setMOPosAB(obj = MO, position = 'B')
            if ANIM_INI_STEP:
                ENABLE_01 = 'Objects'
        if ENABLE_01 == 'Camera' or ENABLE_01 == 'Camera and objects' or ENABLE_01 == 'Camera and connection':
            mc.setMCPosB(Option = MC)

# ======================================================================================
# 2. Command functions

# 2.1. Support

#New
def openReportView():

    """Opens Report view"""

    from PySide import QtGui
    r = Gui.getMainWindow().findChild(QtGui.QDockWidget, "Report view")
    if r.isVisible() is False:
        r.show()
    r.raise_()

def getMessage(message = 'None'):

    """Opens the Report view and show a message"""

    #Open Report view
    openReportView()
    FreeCAD.Console.PrintMessage(('{}').format(message) + '\n')

def modifyAnimationIndicator(animation = False, obj = None):

    """Modify the animation indicator of a movie object."""

    global ANIMATION
    global MC
    global MO

    if obj == MC:
        MC = obj
    if obj == MO:
        MO = obj

    if animation == False:
        ANIMATION = False
        if MC != None:
            try: #new
                MC.Cam_07OnAnim = False
            except:
                pass
        if MO != None:
            try:#new
                MO.Obj_07AnimOnAnim = False
            except:
                pass
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                                       'Animation off.') + '\n')
    if animation == True:
        ANIMATION = True
        if MC != None:
            try: #new
                #if MC.Cam_06Enable != 'Objects' and MC.Cam_06Enable != 'Connection':
                if MC.Cam_06Enable[0:2] != '02' and MC.Cam_06Enable[0:2] != '04':
                    MC.Cam_07OnAnim = True
            except:
                pass
        if MO != None:
            try: #new
                MO.Obj_07AnimOnAnim = True
            except:
                pass
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                                       'Animation on.') + '\n')
    FreeCAD.ActiveDocument.recompute()

def getViewProjection():

    """Move to a perspective view for a MovieCamera."""

    if MC != None:
        #if MC.Cam_06Enable == 'Camera' or MC.Cam_06Enable == 'Camera and objects' or MC.Cam_06Enable == 'Camera and connection' :
        if any(condition for condition in [MC.Cam_06Enable[0:2] == '00',
                                           MC.Cam_06Enable[0:2] == '01',
                                           MC.Cam_06Enable[0:2] == '03'
                                          ]):
            Gui.runCommand('Std_PerspectiveCamera',1)

# ======================================================================================
# 2.2. Enabling commands

def indicateMovieSelection(obj = 'None'):

    """Indicates the movie objects selected."""

    global MC
    global MO
    global ENABLE_00
    global ENABLE_01
    #global ANIM_INI_STEP
    #global ANIM_END_STEP
    Selection = []
    Selection = Gui.Selection.getSelection()
    for n in range(len(Selection)):
        if obj == 'Camera':
            if not Selection[n].Name[5] == 'C':
               getMessage(message = translate('MovieAnimation',
                                              'Select a MovieCamera!'))
               return
            else:
                MC = None
                MC = Selection[0]
                MC.Cam_07OnAnim = False
                mc.enableCameraSelection(Enable = MC)
                ENABLE_00 = 'Camera' # Only enabled for configuration
                if MC.Cam_06Enable[0:2] == '00': # 'Camera'
                    enableAnimObjects(obj1 = 'Camera')
                if MC.Cam_06Enable[0:2] == '01': # 'Camera and objects'
                    enableAnimObjects(obj1 = 'Camera and objects')
                if MC.Cam_06Enable[0:2] == '02': # 'Objects'
                    enableAnimObjects(obj1 = 'Objects')
                if MC.Cam_06Enable == '03': # 'Camera and connection':
                    enableAnimObjects(obj1 = 'Camera and connection')
                if MC.Cam_06Enable[0:2] == '04': # 'Connection'
                    enableAnimObjects(obj1 = 'Connection')
                #New change laber
                #label = MC.Label
                #MC.Label = changeEnableLabel(objLabel = label, enable = True)

        if obj == 'Objects':
            mes1 = translate('MovieAnimation',
                             'Select a MovieObjects!')
            if len(Selection[n].Name) < 5:
                getMessage(message = mes1)
                return
            if not Selection[n].Name[5] == 'O':
                getMessage(message = mes1)
                return
            else:
                MO = None
                MO = Selection[0]
                mo.enableObjectsSelection(obj2 = MO)
                ENABLE_00 = 'Objects' # Only enabled for configuration
                if MO.Obj_01Route is False:
                    if MO.PosB == MO.PosA:
                        #Open Report view
                        openReportView()
                        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                                        'To animate the objects it is necessary \n'
                                        'to reset the MovieObjects B position or \n'
                                        'enable “Obj_01Route” and indicate a path \n'
                                        'at “Obj_02RouteSelection”!'
                                        ) + '\n')
                        ENABLE_01 = 'None' #Not ready for animation
                        return
                enableAnimObjects(obj1 = 'Objects')
                #New change label
                #label = MO.Label
                #MO.Label = changeEnableLabel(objLabel = label, enable = True)

    getSelectionSteps(Content = Selection)

def enableAnimObjects(obj1 = 'None'):

    """Enables a movie objects for animation."""

    global ENABLE_01

    # MovieCamera
    if obj1 == 'Camera':
        ENABLE_01 = 'Camera'
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                            'MovieCamera enabled.') + '\n')
    if obj1 == 'Camera and objects':
        ENABLE_01 = 'Camera and objects'
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                            'MovieCamera and MovieObjects enabled.') + '\n')
    if obj1 == 'Camera and connection':
        ENABLE_01 = 'Camera and connection'
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                            'MovieCamera and connection enabled.') + '\n')
    # MovieObjects
    if obj1 == 'Objects':
        ENABLE_01 = 'Objects'
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                            'MovieObjects enabled.') + '\n')
    # Clapperboard
    if obj1 == 'Clapperboard':
        ENABLE_01 = 'Clapperboard'
        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                            'Clapperboard enabled.') + '\n')

#New
def changeEnableLabel(objLabel = '',
                      enable = False
                      ):

    """Change obj label to enabled for anmation or not"""

    if enable is True:
        label = objLabel
        signalEnabled = '*'
        objLabel = label + signalEnabled
    else:
        if objLabel[-1:] == '*':
            objLabel = objLabel[:-1]
    return objLabel

def enableMovieClapperboard(obj = None, clapNew = False):

    """Enables a Clapperboard"""

    global CL
    global ANIM_FPS
    global ANIM_INI_STEP
    global ANIM_END_STEP
    global ENABLE_01

    if obj != None:
        CL = obj
    else:
        ClapSelection = None
        ClapSelection = Gui.Selection.getSelection()
        if not ClapSelection[0].Name[0] == 'C':
            getMessage(message = translate('MovieAnimation',
                                           'Select a Clapperboard!'))
            return
        CL = ClapSelection[0]
        cl.getCLObject(cl = CL)
    Selection = []
    if hasattr(CL, 'Clap_03AnimationSelection'):
        #Selection = CL.Clap_03AnimationSelection # Outdated
        getMessage(message = translate('MovieAnimation',
                                       'It seems the clapperboard \n'
                                       'is an obsolete version. Please \n'
                                       'try replacing it \n'
                                       'with a new one. \n'
                                       'Clapperboard disabled.'))
        ENABLE_01 = 'None' #Not ready for animation
        return
    Selection = CL.Group # New
    if not Selection:
        getMessage(message = translate('MovieAnimation',
                                       'To enable the Clapperboard, it must have \n'
                                       'at least one MovieCamera or MovieObject \n'
                                       'specified in its “Group” property!\n'
                                        ))
        ENABLE_01 = 'None' #Not ready for animation
        return
    try:
        CL.Frame_09RenderCamera
    except Exception:
        getMessage(message = translate('MovieAnimation',
                                       'It appears that the existing Clapperboard \n'
                                       'is an outdated version, as the Frame_09RenderCamera \n'
                                       'property could not be found. \n'
                                       'Try replacing the Clapperboard \n'
                                       'with a new one. \n'
                                       'Clapperboard disabled.'))
        return
    if CL.Frame_05Type[0:2] == '01': #Render
        #Verify Render Project selection
        if cl.checkRenderProjectSelection(
        selection = CL.Frame_08RenderProject) is False:
            ENABLE_01 = 'None'
            return

    CL.setEditorMode('Frame_10RenderCrop', 1)
    if not CL.Frame_09RenderCamera:
        mess = translate('MovieAnimation',
                         'To enable 3D view cropping, you must have a \n'
                         'render camera specified in the Clapperboard!')
        if CL.Frame_10RenderCrop is True:
            getMessage(message = mess + '\n')
            CL.Frame_10RenderCrop = False
    else:
        if not CL.Frame_09RenderCamera.Name[0:6] == 'Camera':
            if CL.Frame_10RenderCrop is True:
                getMessage(message = mess + '\n')
                CL.Frame_10RenderCrop = False
        else:
            CL.setEditorMode('Frame_10RenderCrop', 0)
            cl.getRenderCameraZoom(obj = CL)
    for n4 in range(len(Selection)):
        if Selection[n4].Name[5] == 'C':
            MC = Selection[n4]
            if MC.Cam_07Connection == 'ExplodedAssembly':
               co.setClapperboardSelection(Clap = CL)

    # Getting the elements of animation
    getSelectionSteps(Content = Selection)
    # Updating the elements of animation
    CL.Clap_04AnimTotalSteps = ANIM_TOTAL_STEPS
    if clapNew is True:
        CL.Clap_01AnimIniStep = ANIM_INI_STEP
        CL.Clap_03AnimEndStep = ANIM_END_STEP
    else:
        ANIM_INI_STEP = CL.Clap_01AnimIniStep
        ANIM_END_STEP = CL.Clap_03AnimEndStep
    if CL.Clap_03AnimEndStep > CL.Clap_04AnimTotalSteps:
        CL.Clap_03AnimEndStep = CL.Clap_04AnimTotalSteps
    ANIM_FPS = CL.Clap_05AnimFps
    # Getting clapperboard time animation
    CL.Clap_06AnimTime = getAnimTime(objIniStep =  CL.Clap_01AnimIniStep,
                                    objEndStep = CL.Clap_03AnimEndStep,
                                    objFps = CL.Clap_05AnimFps
                                    )
    # Defining the remaining animation elements
    #New change label
    #label = CL.Label
    #CL.Label = changeEnableLabel(objLabel = label, enable = True)
    if FreeCAD.GuiUp:
        vp = cl.ClapperboardViewProvider(CL.ViewObject)
        vp.setEnabledState(CL.ViewObject, True)
    return CL

def getSelectionSteps(Content = None):

    """Gets the step configuration of an animation."""

    global MC
    global MO
    global CAMERA_NAME
    global OBJECTS_NAME
    global ANIM_INI_STEP
    global ANIM_CURRENT_STEP
    global ANIM_END_STEP
    global ANIM_TOTAL_STEPS
    global ANIM_FPS
    global SEQ_ANIM_DIC
    global ENABLE_01

    # Selection
    Selection = []
    Selection = Content
    MC = None
    MO = None

    # Camera and objects steps
    CameraN = 'None'
    ObjectsN = 'None'
    InitCameraStep = 0
    EndCameraStep = 0
    AnimCameraFps = 0
    InitObjectsStep = 0
    EndObjectsStep = 0
    Anim_ObjectsFps = 0

    # Animation steps
    ANIM_INI_STEP = 0 # ?
    ANIM_CURRENT_STEP = 0 # ?
    NextStep = 0
    ANIM_END_STEP = 0
    ANIM_TOTAL_STEPS = 0
    ANIM_FPS = 0

    # Animation sequence
    # Components = (CameraN, InitCameraStep, EndCameraStep,
                  # ObjectsN, InitObjectsStep, EndObjectsStep)
    Components = ()
    SEQ_ANIM_DIC = {}

    # Cameras and Objects steps goes to SEQ_ANIM_DIC
    for n in range(len(Selection)):
        # Cameras ===========================================================================
        if Selection[n].Name[5] == 'C':
            MC = Selection[n]

            # Camera-------------------------------------------------------------------------
            if MC.Cam_06Enable[0:2] == '00': # 'Camera'
                # Verification of MC properties
                if MC.Cam_01Target[0:2] == '01': # 'Follow an object or point'
                    #Verify target selection
                    if mc.checkTargetSelection() is False:
                        ENABLE_01 = 'None'
                        return
                if MC.Cam_01Target[0:2] == '02': # 'Follow a route'
                    #Verify route selection
                    if mc.checkRouteSelection() is False:
                        ENABLE_01 = 'None'
                        return
                    MC.Cam_04AnimTotalSteps = MC.Cam_03AnimEndStep + MC.Cam_03TargetStepsForward
                if MC.Cam_01Route == True:
                    #Verify route selection
                    if mc.checkRouteSelection() is False:
                        ENABLE_01 = 'None'
                        return
                # Resetting obj end step
                if MC.Cam_03AnimEndStep > MC.Cam_04AnimTotalSteps:
                    MC.Cam_03AnimEndStep = MC.Cam_04AnimTotalSteps
                #1. Cameras steps goes to SEQ_ANIM_DIC
                #New change icon
                if FreeCAD.GuiUp and ENABLE_00 == 'Camera' and ENABLE_01 != 'Clapperboard':
                    vp = mc.MovieCameraViewProvider(MC.ViewObject)
                    vp.setEnabledState(MC.ViewObject, True)
                CameraN = MC.Name
                initEndSteps = getInitEndStep(nextStep = NextStep,
                                            objIniStep =  MC.Cam_01AnimIniStep,
                                            objEndStep = MC.Cam_03AnimEndStep
                                            )
                InitCameraStep = initEndSteps[0]
                EndCameraStep = initEndSteps[1]
                Components = (CameraN,
                              InitCameraStep,
                              EndCameraStep,
                              'None', # ObjectsN
                              InitCameraStep, # InitObjectsStep
                              EndCameraStep) # EndObjectsStep
                getStepComponents(objTotalSteps = MC.Cam_04AnimTotalSteps,
                                                 initStep = initEndSteps[0],
                                                 components = Components,
                                                 dicStep = SEQ_ANIM_DIC
                                                 )
                # Getting obj time animation
                MC.Cam_06AnimTime = getAnimTime(objIniStep =  MC.Cam_01AnimIniStep,
                                                objEndStep = MC.Cam_03AnimEndStep,
                                                objFps = MC.Cam_05AnimFps
                                                )
                #2. Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            # Camera and Objects ----------------------------------------------------------------
            #'Camera and objects' or 'Objects':
            if MC.Cam_06Enable[0:2] == '01' or MC.Cam_06Enable[0:2] == '02':
                #1. Verifying
                messag1 = translate('MovieAnimation',
                                        'You must select at least one MovieObjects in “Group”!')
                if hasattr(MC, 'Cam_05ObjectsSelected'): # Outdated
                    if MC.Cam_05ObjectsSelected != []:
                        Objects = MC.Cam_05ObjectsSelected
                    else:
                        #Open Report view
                        openReportView()
                        getMessage(message = translate('MovieAnimation',
                        'You must select at least one MovieObjects in “Cam_05ObjectsSelected”!'))
                        ENABLE_01 = 'None'
                        return
                else:
                    if MC.Group != []: #New
                        Objects = MC.Group
                    else:
                        #Open Report view
                        openReportView()
                        getMessage(message = messag1)
                        ENABLE_01 = 'None'
                        return
                #Verify MO selection
                for o in range(len(Objects)):
                    if Objects[o].Name[0:12] != 'MovieObjects':
                        #Open Report view
                        openReportView()
                        getMessage(message = messag1)
                        ENABLE_01 = 'None'
                        return
                    #Verify objects route selection
                    if Objects[o].Obj_01Route == True and mc.checkObjRouteSelection() is False:
                        ENABLE_01 = 'None'
                        return
                #New change icon
                if FreeCAD.GuiUp and ENABLE_00 == 'Camera' and ENABLE_01 != 'Clapperboard':
                    vp = mc.MovieCameraViewProvider(MC.ViewObject)
                    vp.setEnabledState(MC.ViewObject, True)
                CameraN = MC.Name
                #2. Setting End and Total camera steps
                InitCameraStep = NextStep
                # Saving original interval from MC
                interval0 = MC.Cam_04AnimTotalSteps - MC.Cam_03AnimEndStep
                # Getting total and end steps from MOs
                MC.Cam_04AnimTotalSteps = 0
                #Getting total steps from each MovieObjects
                for n1 in range(len(Objects)):
                    MO = Objects[n1]
                    #interval1 = (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep) + 1
                    interval1 = MO.Obj_04AnimTotalSteps + 1
                    MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + interval1
                MC.Cam_04AnimTotalSteps -=1 #Discounting step zero
                MC.Cam_03AnimEndStep = MC.Cam_04AnimTotalSteps - interval0
                if MC.Cam_01Target[0:2] == '02': # 'Follow a route':
                    MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + MC.Cam_03TargetStepsForward #?
                # Resetting MC end step
                if MC.Cam_03AnimEndStep > MC.Cam_04AnimTotalSteps:
                    MC.Cam_03AnimEndStep = MC.Cam_04AnimTotalSteps
                # Getting camera time animation
                MC.Cam_06AnimTime = getAnimTime(objIniStep =  MC.Cam_01AnimIniStep,
                                                objEndStep = MC.Cam_03AnimEndStep,
                                                objFps = MC.Cam_05AnimFps
                                                )
                # Total camera steps adds to EndCameraStep
                #EndCameraStep = EndCameraStep + MC.Cam_03AnimEndStep
                EndCameraStep = EndCameraStep + MC.Cam_04AnimTotalSteps
                #3. Setting Init and End objects step
                EndObjectsStep = NextStep
                for n2 in range(len(Objects)):
                    MO = Objects[n2]
                    # Updating time animation of each MovieObjects
                    MO.Obj_06AnimTime = getAnimTime(objIniStep =  MO.Obj_01AnimIniStep,
                                                    objEndStep = MO.Obj_03AnimEndStep,
                                                    objFps = MO.Obj_05AnimFps
                                                    )
                    # Objects key steps
                    InitObjectsStep = NextStep
                    #EndObjectsStep = NextStep + (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep)
                    EndObjectsStep = NextStep + MO.Obj_04AnimTotalSteps
                    NextStep = EndObjectsStep + 1
                #4. Camera and objects key steps goes to SEQ_ANIM_DIC
                    ObjectsN = MO.Name
                    Components = (CameraN,
                                 InitCameraStep,
                                 EndCameraStep,
                                 ObjectsN,
                                 InitObjectsStep,
                                 EndObjectsStep
                                 )
                    getStepComponents(objTotalSteps = MO.Obj_04AnimTotalSteps,
                                      initStep = InitObjectsStep,
                                      components = Components,
                                      dicStep = SEQ_ANIM_DIC
                                      )
                #5. Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            # Camera and connection -----------------------------------------------------------
            # 'Camera and connection' or 'Connection'
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                InitCameraStep = NextStep
                Values = []
                if MC.Cam_07Connection == 'None':
                    from MovieMessages import TIP_CONNECTION
                    getMessage(message = TIP_CONNECTION)
                    return
                else:
                #1. Camera and connection objects steps goes to SEQ_ANIM_DIC
                    co.verification(Selection = MC)
                    Values = co.connectionSteps(v0 = InitObjectsStep, v1 = EndObjectsStep, 
                                                v2 = InitCameraStep, v3 = EndCameraStep, v4 = NextStep,
                                                 v5 = SEQ_ANIM_DIC, Selection = MC)
                EndCameraStep = Values[0]
                SEQ_ANIM_DIC = Values[1]

                #2. Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            AnimCameraFps = MC.Cam_05AnimFps

        # Objects ===========================================================================
        if Selection[n].Name[5] == 'O':
            MO = Selection[n]
            #Verify objects route selection
            if MO.Obj_01Route == True and mo.checkObjRouteSelection() is False:
                ENABLE_01 = 'None'
                return
            # Resetting obj end step
            if MO.Obj_03AnimEndStep > MO.Obj_04AnimTotalSteps:
                MO.Obj_03AnimEndStep = MO.Obj_04AnimTotalSteps
            #1. Object key steps goes to SEQ_ANIM_DIC
            #New change icon
            if FreeCAD.GuiUp and ENABLE_00 == 'Objects' and ENABLE_01 != 'Clapperboard':
                vp = mo.MovieObjectsViewProvider(MO.ViewObject)
                vp.setEnabledState(MO.ViewObject, True)
            MO.Obj_07AnimOnAnim = False
            ObjectsN = MO.Name
            initEndSteps = []
            initEndSteps = getInitEndStep(nextStep = NextStep,
                                         objIniStep =  MO.Obj_01AnimIniStep,
                                         objEndStep = MO.Obj_03AnimEndStep
                                         )
            InitObjectsStep = initEndSteps[0]
            EndObjectsStep = initEndSteps[1]
            Components = ('None', # CameraN
                           None, # InitCameraStep
                           None, # EndCameraStep
                           ObjectsN,
                           InitObjectsStep,
                           EndObjectsStep
                           )
            getStepComponents(objTotalSteps = MO.Obj_04AnimTotalSteps,
                                             initStep = initEndSteps[0],
                                             components = Components,
                                             dicStep = SEQ_ANIM_DIC
                                             )
            # Getting objects time animation
            MO.Obj_06AnimTime = getAnimTime(objIniStep =  MO.Obj_01AnimIniStep,
                                            objEndStep = MO.Obj_03AnimEndStep,
                                            objFps = MO.Obj_05AnimFps
                                            )
            Anim_ObjectsFps = MO.Obj_05AnimFps
            #2. Adding total camera steps to total animation
            ANIM_END_STEP = EndObjectsStep
            NextStep = ANIM_END_STEP + 1

    # Getting total steps
    #print(f'getSelectionSteps, SEQ_ANIM_DIC = {SEQ_ANIM_DIC}')
    ANIM_TOTAL_STEPS = len(SEQ_ANIM_DIC) - 1
    #print(f'getSelectionSteps, ANIM_END_STEP = {ANIM_END_STEP}')
    #print(f'getSelectionSteps, ANIM_TOTAL_STEPS = {ANIM_TOTAL_STEPS}')
    if ANIM_END_STEP > ANIM_TOTAL_STEPS:
        ANIM_END_STEP = ANIM_TOTAL_STEPS
    #print(f'getSelectionSteps, ANIM_END_STEP = {ANIM_END_STEP}')

    # Defining the remaining animation elements
    modifyAnimationIndicator(animation = False)
    CAMERA_NAME = 'None'
    OBJECTS_NAME = 'None'

    if not AnimCameraFps:
        ANIM_FPS = Anim_ObjectsFps
    else:
        ANIM_FPS = AnimCameraFps

# ======================================================================================
#New
def getInitEndStep(nextStep = 0,
                objIniStep =  None,
                objEndStep = None
                ):

    """Gets initial and end steps"""

    initStep = nextStep
    endStep = nextStep + (objEndStep - objIniStep)
    return initStep, endStep

def getAnimTime(objIniStep =  None,
                objEndStep = None,
                objFps = None
                ):

    """Get the time animation."""

    secs = (objEndStep - objIniStep) / objFps
    hours, minutes = divmod(secs, 3600)
    minutes, seconds = divmod(minutes, 60)
    animTime = f'{int(hours):0>2}:{int(minutes):0>2}:{seconds:0>5.2f}'
    return animTime

def getStepComponents(objTotalSteps = None,
                      initStep = None,
                      components = None,
                      dicStep = None
                      ):

    """Gets a dictionary of key step components: (CameraN,
                              InitCameraStep,
                              EndCameraStep,
                              ObjectsN,
                              InitObjectsStep,
                              EndObjectsStep
                              )"""
    objStep = 0
    for n in range(objTotalSteps + 1):
        objStep = initStep + n
        dicStep[objStep] = components
    return dicStep

# ======================================================================================

# 2.3. Animation commands

def recoverIniMovieAnimation():

    """Recovers the start of the animation"""

    global STEP_POS
    global CL
    global ANIM_INI_STEP
    global ANIM_CURRENT_STEP

    if ANIM_CURRENT_STEP > ANIM_INI_STEP:
        STEP_POS = 'P'
        if ANIM_CURRENT_STEP > SEQ_ANIM_DIC[ANIM_CURRENT_STEP][4]:
            ANIM_CURRENT_STEP = SEQ_ANIM_DIC[ANIM_CURRENT_STEP][4]
        else:
            ANIM_CURRENT_STEP = SEQ_ANIM_DIC[ANIM_CURRENT_STEP - 1][4]
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
    else:
        ANIM_CURRENT_STEP = ANIM_INI_STEP
        return

    getViewProjection()
    getMovieMobile()
    Gui.updateGui()

def prevMovieAnimation():

    """Moves the movie objects animation one step back."""

    global ANIM_CURRENT_STEP
    global CL

    if ANIM_CURRENT_STEP > ANIM_INI_STEP:
        ANIM_CURRENT_STEP -= 1
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
    else:
        return
    getViewProjection()
    getMovieMobile()
    Gui.updateGui()

def pauseMovieAnimation():

    """Pauses the movie objects animation."""

    modifyAnimationIndicator(animation = False)

def playMovieAnimation():

    """Plays forward the movie objects animation."""

    global STEP_POS
    global ANIM_CURRENT_STEP
    global CL
    global ANIM_INI_STEP
    global ANIM_END_STEP
    global ANIM_FPS

    modifyAnimationIndicator(animation = True)
    getViewProjection()

    if ENABLE_01 == 'Clapperboard':
        CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
    if STEP_POS == 'I':
        ANIM_CURRENT_STEP = ANIM_INI_STEP
    if ANIMATION_BACK == False:
        Steps = ANIM_END_STEP - ANIM_CURRENT_STEP
    else:
        Steps = ANIM_CURRENT_STEP - ANIM_INI_STEP
    pauseTime = 1/(ANIM_FPS)
    STEP_POS = 'P'
    for n in range(Steps + 1):
        getMovieMobile()
        Gui.updateGui()
        time.sleep(pauseTime)
        if ENABLE_01 == 'Clapperboard':
           if CL.Clap_04OnRec == True:
               if CL.Clap_02AnimCurrentStep >= CL.Clap_01AnimIniStep:
                   cl.runRecordCamera(Back = ANIMATION_BACK)
        if ANIMATION_BACK == False:
            if ANIM_CURRENT_STEP < ANIM_END_STEP:
                ANIM_CURRENT_STEP += 1
        else:
            if ANIM_CURRENT_STEP > ANIM_INI_STEP:
                ANIM_CURRENT_STEP -= 1
            else:
                break
        if ANIMATION == False:
            break
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
            CL.Clap_06AnimTime = getAnimTime(objIniStep =  CL.Clap_01AnimIniStep,
                                            objEndStep = CL.Clap_02AnimCurrentStep,
                                            objFps = CL.Clap_05AnimFps
                                            )
    modifyAnimationIndicator(animation = False)
    if ENABLE_01[0:6] == 'Camera':
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(MC)
    if ENABLE_01 == 'Clapperboard':
        CL.Frame_06R1OnRec = False
        CL.Frame_07R2OnRec = False
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(CL)

def getMovieMobile():

    """Gets and establishes the step movie objects animation."""

    global MC
    global MO
    global CO
    global CAMERA_NAME
    global OBJECTS_NAME
    global ENABLE_01

    try:
        CameraN = SEQ_ANIM_DIC[ANIM_CURRENT_STEP][0]
        ObjectsN = SEQ_ANIM_DIC[ANIM_CURRENT_STEP][3]
    except Exception:
        #Open Report view
        openReportView()
        getMessage(message = translate('MovieAnimation',
            'It seems the number of steps has momentarily \n'
            'exceeded the total limit. Try re-enabling the \n'
            'animation again to fix this.'))
        ENABLE_01 = 'None'
        pauseMovieAnimation()
        return

    if ObjectsN != 'None':
        if ObjectsN[5] == 'O':
            if OBJECTS_NAME != ObjectsN:
                Gui.Selection.clearSelection()
                if MO != None:
                    MO.Obj_07AnimOnAnim = False
                OBJECTS_NAME = ObjectsN
                MO = FreeCAD.ActiveDocument.getObject(ObjectsN)
                Gui.Selection.addSelection(MO)
                MO.Obj_07AnimOnAnim = True
                # New - Refreshes each step of objects animation
                if(hasattr(MO, 'Obj_03Refresh')) and MO.Obj_03Refresh == True: # New
                    mo.enableObjectsRefresh(refres = True) # New
                else: # New
                    mo.enableObjectsRefresh(refres = False) # New
            MO.Obj_02AnimCurrentStep = (ANIM_CURRENT_STEP - SEQ_ANIM_DIC[ANIM_CURRENT_STEP][4]) + MO.Obj_01AnimIniStep
            # Getting objects time animation
            MO.Obj_06AnimTime = getAnimTime(objIniStep =  MO.Obj_01AnimIniStep,
                                            objEndStep = MO.Obj_02AnimCurrentStep,
                                            objFps = MO.Obj_05AnimFps
                                            )
            # Getting objects pos animation
            mo.getMovieObjectsMobile(Selection = MO)

    if CameraN != 'None':
        enableCamera = True
        if CAMERA_NAME != CameraN:
            Gui.Selection.clearSelection()
            if MC != None:
                MC.Cam_07OnAnim = False
            CAMERA_NAME = CameraN
            MC = FreeCAD.ActiveDocument.getObject(CameraN)
            Gui.Selection.addSelection(MC)
            MC.Cam_07OnAnim = True
        MC.Cam_02AnimCurrentStep = (ANIM_CURRENT_STEP - SEQ_ANIM_DIC[ANIM_CURRENT_STEP][1]) + MC.Cam_01AnimIniStep
        # 'Objects' or 'Connection':
        if MC.Cam_06Enable[0:2] == '02' or MC.Cam_06Enable[0:2] == '04':
            enableCamera = False
        if enableCamera != False:
            # Getting camera time animation
            MC.Cam_06AnimTime = getAnimTime(objIniStep =  MC.Cam_01AnimIniStep,
                                            objEndStep = MC.Cam_02AnimCurrentStep,
                                            objFps = MC.Cam_05AnimFps
                                            )
            # Getting camera pos animation
            mc.getMovieCameraMobile(Selection = MC)
        # Camera and connection' or 'Connection':
        if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
            if MC.Cam_07Connection != 'None' and MC.Cam_07Connection != 'ExplodedAssembly':
                if ANIMATION_BACK == False:
                    co.connectionPos(Selection = MC)
                else:
                    co.connectionPrev(Selection = MC)

def postMovieAnimation():

    """Moves the movie objects animation one step forward."""

    global ANIM_CURRENT_STEP

    if ANIM_END_STEP > ANIM_CURRENT_STEP:
        ANIM_CURRENT_STEP += 1
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
    else:
        return
    getViewProjection()
    getMovieMobile()
    Gui.updateGui()

def getEndMovieAnimation():

    """Moves the animation movie objects to its end."""

    global ANIM_CURRENT_STEP
    global STEP_POS

    if ANIM_CURRENT_STEP < ANIM_END_STEP:
        STEP_POS = 'P'
        if ANIM_CURRENT_STEP < SEQ_ANIM_DIC[ANIM_CURRENT_STEP][5]:
            ANIM_CURRENT_STEP = SEQ_ANIM_DIC[ANIM_CURRENT_STEP][5]
        else:
            if ANIM_CURRENT_STEP + 1 < ANIM_END_STEP:
                ANIM_CURRENT_STEP = SEQ_ANIM_DIC[ANIM_CURRENT_STEP + 1][5]
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP

    else:
        return

    getMovieMobile()
    getViewProjection()
    Gui.updateGui()

# ======================================================================================
# 3. Commands

if FreeCAD.GuiUp:

    FreeCAD.Gui.addCommand('IniMovieAnimation', IniMovieAnimation())
    FreeCAD.Gui.addCommand('PrevMovieAnimation', PrevMovieAnimation())
    FreeCAD.Gui.addCommand('PlayBackwardMovieAnimation', PlayBackwardMovieAnimation())
    FreeCAD.Gui.addCommand('PauseMovieAnimation', PauseMovieAnimation())
    FreeCAD.Gui.addCommand('PlayMovieAnimation', PlayMovieAnimation())
    FreeCAD.Gui.addCommand('PostMovieAnimation', PostMovieAnimation())
    FreeCAD.Gui.addCommand('EndMovieAnimation', EndMovieAnimation())
    FreeCAD.Gui.addCommand('SetMoviePosA', SetMoviePosA())
    FreeCAD.Gui.addCommand('SetMoviePosB', SetMoviePosB())
    #New
    FreeCAD.Gui.addCommand('EnableAnimation', EnableAnimation())
    FreeCAD.Gui.addCommand('DisableAnimation', DisableAnimation())
    #FreeCAD.Gui.addCommand('MovieAnimationGroup', MovieAnimationGroup())
