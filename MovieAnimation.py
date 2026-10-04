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
STEP_POS = 'I'
ANIMATION_BACK = False

#VIEW_00 = translate("MovieCamera", "3D view")
#VIEW_01 = translate("MovieCamera", "Render")

VIEW_00 = translate('MovieAnimation', '3D view')
VIEW_01 = translate('MovieAnimation', 'Render')
print(f'VIEW_00 = {VIEW_00}')
print(f'VIEW_01 = {VIEW_01}')

TIP_CONNECTION = translate('MovieAnimation',
                           'Connection is enable, you must select \n'
                           'one connection in “Cam_07Connection“!')

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
        if selection:
            if selection[0].Name[0:11] == 'MovieCamera':
                indicateMovieSelection(obj = 'Camera')
            if selection[0].Name[0:12] == 'MovieObjects':
                indicateMovieSelection(obj = 'Objects')
            if selection[0].Name[0:12] == 'Clapperboard':
                CL = None
                CL = enableMovieClapperboard()
        FreeCAD.ActiveDocument.recompute()

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
        ENABLE_01 = 'None'
        getMessage(message = translate('MovieAnimation',
                                       'There is no movie object enabled to animate!'))
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
                                             'if record is on it will turn off.\n'
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
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
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
            #if MC.Name or MO.Name or CL.Name:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        modifyAnimationIndicator(animation = False)
        if MC != None:
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                if MC.Cam_07Connection == 'None':
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
            #if MC.Name or MO.Name or CL.Name:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ANIMATION_BACK
        ANIMATION_BACK = True
        if MC != None:
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = TIP_CONNECTION)
                    return
               else:
                   if MC.Cam_07Connection == 'ExplodedAssembly':
                       getViewProjection()
                       co.connectionPlayBackward(Selection = MC)
                       FreeCAD.ActiveDocument.recompute()
                       return
        playMovieAnimation()

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
            #if MC.Name or MO.Name or CL.Name:
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
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
               if MC.Cam_07Connection == 'None':
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
            #if MC.Name or MO.Name or CL.Name:
            if ENABLE_01 != 'None':
                if not ANIMATION:
                    return True
        else:
            return False

    def Activated(self):
        global ANIMATION_BACK
        ANIMATION_BACK = False
        if MC != None:
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = TIP_CONNECTION)
                    return
               else:
                   if MC.Cam_07Connection == 'ExplodedAssembly':
                       getViewProjection()
                       co.connectionPlay(Selection = MC)
                       FreeCAD.ActiveDocument.recompute()
                       return
        playMovieAnimation()
        if CL != None:
            try: #new
                if CL.Clap_04OnRec is True:
                    cl.createVideo(auto = True)
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
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
               if MC.Cam_07Connection == 'None':
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
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
               if MC.Cam_07Connection == 'None':
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

# ======================================================================================
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
            ENABLE_01 = 'Objects'
        if ENABLE_01 == 'Camera' or ENABLE_01 == 'Camera and objects' or ENABLE_01 == 'Camera and connection':
            mc.setMCPosB(Option = MC)

# ======================================================================================
# 2. Command functions

# 2.1. Support

def getMessage(message = 'None'):

    """Gets a repeated message"""

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
        getMessage(message = translate('MovieAnimation',
                                       'Animation off.'))
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
        getMessage(message = translate('MovieAnimation',
                                       'Animation on.'))
    FreeCAD.ActiveDocument.recompute()

def getViewProjection():

    """Move to a perspective view for a MovieCamera."""

    if MC != None:
        #if MC.Cam_06Enable == 'Camera' or MC.Cam_06Enable == 'Camera and objects' or MC.Cam_06Enable == 'Camera and connection' :
        #if MC.Cam_06Enable[0:2] == '00' or MC.Cam_06Enable[0:2] == '01' or MC.Cam_06Enable[0:2] == '03':
        if any(condition for condition in [MC.Cam_06Enable[0:2] == '00',
                                           MC.Cam_06Enable[0:2] == '01',
                                           MC.Cam_06Enable[0:2] == '03'
                                          ]):
            Gui.runCommand('Std_PerspectiveCamera',1)

def getTimeAnimation(secs = 0):

    """Get the time animation."""

    hours, minutes = divmod(secs, 3600)
    minutes, seconds = divmod(minutes, 60)
    TimeAnimation = f'{int(hours):0>2}:{int(minutes):0>2}:{seconds:0>5.2f}'
    return TimeAnimation

# ======================================================================================
# 2.2. Enabling commands

def indicateMovieSelection(obj = 'None'):

    """Indicates the movie objects selected."""

    global MC
    global MO
    global ENABLE_00
    global ENABLE_01
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
                #if MC.Cam_06Enable == 'Camera':
                if MC.Cam_06Enable[0:2] == '00':
                    enableAnimObjects(obj1 = 'Camera')
                #if MC.Cam_06Enable == 'Camera and objects':
                if MC.Cam_06Enable[0:2] == '01':
                    enableAnimObjects(obj1 = 'Camera and objects')
                #if MC.Cam_06Enable == 'Objects':
                if MC.Cam_06Enable[0:2] == '02':
                    enableAnimObjects(obj1 = 'Objects')
                #if MC.Cam_06Enable == 'Camera and connection':
                if MC.Cam_06Enable == '03':
                    enableAnimObjects(obj1 = 'Camera and connection')
                #if MC.Cam_06Enable == 'Connection':
                if MC.Cam_06Enable[0:2] == '04':
                    enableAnimObjects(obj1 = 'Connection')
                ENABLE_00 = 'Camera' # Only enabled for configuration
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
                        FreeCAD.Console.PrintMessage(translate('MovieAnimation',
                                                            'To animate the objects it is necessary \n'
                                                            'to reset the MovieObjects B position or \n'
                                                            'enable “Obj_01Route” and indicate a path \n'
                                                            'at “Obj_02RouteSelection”!'
                                                            ) + '\n')
                        ENABLE_01 = 'None' #Not ready for animation
                        return
                enableAnimObjects(obj1 = 'Objects')
                MO.Obj_07AnimOnAnim = False

    getSelectionSteps(Content = Selection)

#New
def enableMovieClapperboard(obj = None):

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
    Selection = CL.Clap_03AnimationSelection
    if not Selection:
        getMessage(message = translate('MovieAnimation',
                                       'To enable the Clapperboard, it must have \n'
                                       'at least one MovieCamera or MovieObject \n'
                                       'specified in its “Clap_03 Animation \n'
                                       'Selection” property!'))
        ENABLE_01 = 'None' #Not ready for animation
        return
    for n4 in range(len(Selection)):
        if Selection[n4].Name[5] == 'C':
            MC = Selection[n4]
            if MC.Cam_07Connection == 'ExplodedAssembly':
               co.setClapperboardSelection(Clap = CL)
    # Getting the elements of animation
    getSelectionSteps(Content = Selection)
    # Saving the elements of animation
    CL.Clap_04AnimTotalSteps = ANIM_END_STEP
    CL.Clap_03AnimEndStep = CL.Clap_04AnimTotalSteps
    ANIM_FPS = CL.Clap_05AnimFps
    # Getting clapperboard time animation
    t = (CL.Clap_03AnimEndStep - CL.Clap_01AnimIniStep + 1) / CL.Clap_05AnimFps
    CL.Clap_06AnimTime = getTimeAnimation(secs = t)
    # Defining the remaining animation elements
    enableAnimObjects(obj1 = 'Clapperboard')
    ANIM_FPS = CL.Clap_05AnimFps
    return CL

def enableAnimObjects(obj1 = 'None'):

    """Enables a movie objects for animation."""

    global ENABLE_01

    # MovieCamera
    if obj1 == 'Camera':
        ENABLE_01 = 'Camera'
        getMessage(message = translate('MovieAnimation',
                                       'MovieCamera enabled.'))
    if obj1 == 'Camera and objects':
        ENABLE_01 = 'Camera and objects'
        getMessage(message = translate('MovieAnimation',
                                       'MovieCamera and MovieObjects enabled.'))
    if obj1 == 'Camera and connection':
        ENABLE_01 = 'Camera and connection'
        getMessage(message = translate('MovieAnimation',
                                       'MovieCamera and connection enabled.'))
    # MovieObjects
    if obj1 == 'Objects':
        ENABLE_01 = 'Objects'
        getMessage(message = translate('MovieAnimation',
                                       'MovieObjects enabled.'))
    # Clapperboard
    if obj1 == 'Clapperboard':
        ENABLE_01 = 'Clapperboard'
        getMessage(message = translate('MovieAnimation',
                                       'Clapperboard enabled.'))

def getSelectionSteps(Content = None):

    """Gets the step configuration of an animation."""

    global MC
    global MO
    global CAMERA_NAME
    global OBJECTS_NAME
    global ANIM_INI_STEP
    global ANIM_CURRENT_STEP
    global ANIM_END_STEP
    global ANIM_FPS
    global SEQ_ANIM_DIC

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
    ANIM_INI_STEP = 0
    ANIM_CURRENT_STEP = 0
    NextStep = 0
    ANIM_END_STEP = 0
    #ANIM_TOTAL_STEPS = 0
    ANIM_FPS = 0

    # Animation sequence
    # Components = (CameraN, InitCameraStep, EndCameraStep, ObjectsN, InitObjectsStep, EndObjectsStep)
    Components = ()
    SEQ_ANIM_DIC = {}

    # Cameras and Objects steps goes to SEQ_ANIM_DIC
    for n in range(len(Selection)):
        # Cameras ===========================================================================
        if Selection[n].Name[5] == 'C':
            MC = Selection[n]
            CameraN = MC.Name
            # Camera-------------------------------------------------------------------------
            #if MC.Cam_06Enable == 'Camera':
            if MC.Cam_06Enable[0:2] == '00':
                InitCameraStep = NextStep
                EndCameraStep = NextStep + (MC.Cam_03AnimEndStep - MC.Cam_01AnimIniStep)
                #if MC.Cam_01Target == 'Follow a route':
                if MC.Cam_01Target[0:2] == '02':
                    MC.Cam_04AnimTotalSteps = MC.Cam_03AnimEndStep + MC.Cam_03TargetStepsForward

                # Getting camera time animation
                t = (MC.Cam_03AnimEndStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
                MC.Cam_06AnimTime = getTimeAnimation(secs = t)

                #1. Cameras steps goes to SEQ_ANIM_DIC
                Components = (CameraN,
                              InitCameraStep,
                              EndCameraStep,
                              'None',
                              InitCameraStep,
                              EndCameraStep)
                for s1 in range(MC.Cam_03AnimEndStep + 1):
                    stepCamera = InitCameraStep + s1
                    SEQ_ANIM_DIC[stepCamera] = Components

                #2. Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            # Camera and Objects ----------------------------------------------------------------
            #if MC.Cam_06Enable == 'Camera and objects' or MC.Cam_06Enable == 'Objects':
            if MC.Cam_06Enable[0:2] == '01' or MC.Cam_06Enable[0:2] == '02':
                #1. Verifying
                if MC.Cam_05ObjectsSelected != None:
                    Objects = MC.Cam_05ObjectsSelected
                    pass
                else:
                    getMessage(message = translate('MovieAnimation',
                                                   'Select MovieObjects in “Cam_06Enable“!'))
                    return

                #2. Setting Init and End camera steps
                InitCameraStep = NextStep
                interval0 = MC.Cam_04AnimTotalSteps - MC.Cam_03AnimEndStep
                MC.Cam_04AnimTotalSteps = 0
                for n1 in range(len(Objects)):
                    MO = Objects[n1]
                    interval1 = (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep) + 1
                    MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + interval1
                MC.Cam_04AnimTotalSteps -=1
                MC.Cam_03AnimEndStep = MC.Cam_04AnimTotalSteps - interval0
                #if MC.Cam_01Target == 'Follow a route':
                if MC.Cam_01Target[0:2] == '02':
                    MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + MC.Cam_03TargetStepsForward

                # Getting camera time animation
                t = (MC.Cam_03AnimEndStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
                MC.Cam_06AnimTime = getTimeAnimation(secs = t)

                # Total camera steps adds to EndCameraStep
                EndCameraStep = EndCameraStep + MC.Cam_03AnimEndStep

                #3. Setting Init and End objects step
                EndObjectsStep = NextStep
                for n2 in range(len(Objects)):
                    MO = Objects[n2]
                    # Getting time animation of each MovieObjects
                    t = (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep) / MO.Obj_05AnimFps
                    MO.Obj_06AnimTime = getTimeAnimation(secs = t)

                    # Objects key steps
                    InitObjectsStep = NextStep
                    EndObjectsStep = NextStep + (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep)
                    NextStep = EndObjectsStep + 1

                #4. Camera and objects key steps goes to SEQ_ANIM_DIC
                    ObjectsN = MO.Name
                    Components = (CameraN, InitCameraStep, EndCameraStep, ObjectsN, InitObjectsStep, EndObjectsStep)
                    for s2 in range(MO.Obj_03AnimEndStep + 1):
                        stepObjects = InitObjectsStep + s2
                        SEQ_ANIM_DIC[stepObjects] = Components

                #5. Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            # Camera and connection -----------------------------------------------------------
            #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_06Enable[0:2] == '03' or MC.Cam_06Enable[0:2] == '04':
                InitCameraStep = NextStep
                Values = []
                if MC.Cam_07Connection == 'None':
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
            # Getting objects time animation
            t = (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep) / MO.Obj_05AnimFps
            MO.Obj_06AnimTime = getTimeAnimation(secs = t)

            #1. Object key steps goes to SEQ_ANIM_DIC
            InitObjectsStep = NextStep
            EndObjectsStep = NextStep + (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep)
            ObjectsN = MO.Name
            Components = ('None', None, None, ObjectsN, InitObjectsStep, EndObjectsStep)
            for s4 in range(MO.Obj_03AnimEndStep + 1):
                stepObjects1 = InitObjectsStep + s4
                SEQ_ANIM_DIC[stepObjects1] = Components
            Anim_ObjectsFps = MO.Obj_05AnimFps

            #2. Adding total camera steps to total animation
            ANIM_END_STEP = EndObjectsStep
            NextStep = ANIM_END_STEP + 1

    # Defining the remaining animation elements
    modifyAnimationIndicator(animation = False)
    CAMERA_NAME = 'None'
    OBJECTS_NAME = 'None'

    if not AnimCameraFps:
        ANIM_FPS = Anim_ObjectsFps
    else:
        ANIM_FPS = AnimCameraFps

# ======================================================================================
# 2.3. Animation commands

def recoverIniMovieAnimation():

    """Recovers the start of the animation"""

    global STEP_POS
    global CL
    global ANIM_INI_STEP
    global ANIM_CURRENT_STEP

    if ENABLE_01 == 'Clapperboard':
        cl.stopMovieRecord(Clap = CL)

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
        ANIM_INI_STEP = CL.Clap_01AnimIniStep
        ANIM_END_STEP = CL.Clap_03AnimEndStep
        ANIM_FPS = CL.Clap_05AnimFps
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
            # Getting clapperboard time animation
            t = (CL.Clap_02AnimCurrentStep - CL.Clap_01AnimIniStep) / CL.Clap_05AnimFps
            CL.Clap_06AnimTime = getTimeAnimation(secs = t)

    modifyAnimationIndicator(animation = False)
    if ENABLE_01 == 'Clapperboard':
        CL.Frame_06R1OnRec = False
        CL.Frame_07R2OnRec = False

def getMovieMobile():

    """Gets and establishes the step movie objects animation."""

    global MC
    global MO
    global CO
    global CAMERA_NAME
    global OBJECTS_NAME

    CameraN = SEQ_ANIM_DIC[ANIM_CURRENT_STEP][0]
    ObjectsN = SEQ_ANIM_DIC[ANIM_CURRENT_STEP][3]

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
            t = (MO.Obj_02AnimCurrentStep - MO.Obj_01AnimIniStep) / MO.Obj_05AnimFps
            MO.Obj_06AnimTime = getTimeAnimation(secs = t)
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
        #if MC.Cam_06Enable == 'Objects' or MC.Cam_06Enable == 'Connection':
        if MC.Cam_06Enable[0:2] == '02' or MC.Cam_06Enable[0:2] == '04':
            enableCamera = False
        if enableCamera != False:
            # Getting camera time animation
            t = (MC.Cam_02AnimCurrentStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
            MC.Cam_06AnimTime = getTimeAnimation(secs = t)
            # Getting camera pos animation
            mc.getMovieCameraMobile(Selection = MC)
        #if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
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
