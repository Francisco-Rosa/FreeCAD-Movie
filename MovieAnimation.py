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

import os
import FreeCAD
import FreeCADGui as Gui
import time
from PySide.QtGui import QFileDialog
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

ENABLE_01 = 'None'
MC = None
MO = None
CL = None
STEP_POS = 'I'
ANIMATION_BACK = False

# Notifications

def getMessage(message = 'None'):
    FreeCAD.Console.PrintMessage(translate('Movie', message) + '\n')

# ======================================================================================
# 1. Classes

# 1.1. Movie Animation

class IniMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/IniMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('IniMovieAnimation', 'Move to the beginning'),
                'ToolTip': QT_TRANSLATE_NOOP('IniMovieAnimation', 
                                             'On the first click, it returns to the beginning of the animation '
                                             'of the current camera/objects and resets them, if record is on it '
                                             'will turn off. On the second click, it goes '
                                             'to the end of the animation of the previous camera/objects (if so)'),
                'Accel': "Ctrl+1"}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        global ANIM_CURRENT_STEP
        global STEP_POS
        modifyAnimationIndicator(Animation = False)
        if MC != None:
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
                if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
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

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PrevMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PrevMovieAnimation', 'Move one step back'),
                'ToolTip': QT_TRANSLATE_NOOP('PrevMovieAnimation', 
                                             'Moves the animation one step back')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        modifyAnimationIndicator(Animation = False)
        if MC != None:
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
                if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
                    return
                else:
                    co.connectionPrev(Selection = MC)
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        getMessage(message = 'PrevMovieAnimation '
                                   'does not work with ExplodedAssembly')
                        return
        prevMovieAnimation()

class PlayBackwardMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayBackwardMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayBackwardMovieAnimation', 'Play backward the animation'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayBackwardMovieAnimation', 
                                             'Plays backward the animation')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        global ANIMATION_BACK
        ANIMATION_BACK = True
        if MC != None:
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
                    return
               else:
                   if MC.Cam_07Connection == 'ExplodedAssembly':
                       getViewProjection()
                       co.connectionPlayBackward(Selection = MC)
                       FreeCAD.ActiveDocument.recompute()
                       return
        playMovieAnimation()

class PauseMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PauseMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PauseMovieAnimation', 'PauseMovieAnimation'),
                'ToolTip': QT_TRANSLATE_NOOP('PauseMovieAnimation', 
                                             'Pauses the animation')}

    def IsActive(self):
        if Gui.ActiveDocument:
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
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
                    return
               else:
                    co.connectionPause(Selection = MC)
                    MC.Cam_07OnAnim = False
                    FreeCAD.ActiveDocument.recompute()

class PlayMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayMovieAnimation', 'Play the animation'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayMovieAnimation', 
                                             'Plays the animation')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        global ANIMATION_BACK
        ANIMATION_BACK = False
        if MC != None:
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
                    return
               else:
                   if MC.Cam_07Connection == 'ExplodedAssembly':
                       getViewProjection()
                       co.connectionPlay(Selection = MC)
                       FreeCAD.ActiveDocument.recompute()
                       return
        playMovieAnimation()

class PostMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PostMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PostMovieAnimation', 'Move one step forward'),
                'ToolTip': QT_TRANSLATE_NOOP('PostMovieAnimation', 
                                             'Moves the animation one step forward')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        modifyAnimationIndicator(Animation = False)
        if MC != None:
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
                    return
               else:
                    co.connectionPos(Selection = MC)
                    FreeCAD.ActiveDocument.recompute()
                    if MC.Cam_07Connection == 'ExplodedAssembly':
                        getMessage(message = 'PostMovieAnimation '
                                  'does not work with ExplodedAssembly')
                        return
        postMovieAnimation()

class EndMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EndMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EndMovieAnimation', 'Move to the end'),
                'ToolTip': QT_TRANSLATE_NOOP('EndMovieAnimation', 
                                             'On the first click, it moves to the end of the animation of the current camera/objects. '
                                             'On the second click, it goes to the beginning of the animation of '
                                             'the next camera/objects (if so.)'),
                'Accel': "Ctrl+2"}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        global ANIM_CURRENT_STEP
        global STEP_POS
        modifyAnimationIndicator(Animation = False)
        if MC != None:
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
               if MC.Cam_07Connection == 'None':
                    getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
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

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMoviePosAIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMoviePosA', 'Set the A position of a camera or objects'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMoviePosA',
                                             'Applicable for creating an animation from point A to B '
                                             '(not when the Movie Camera target or Movie Objects are set up to follow a route). ' 
                                             'First, select and activate the Movie Camera or Movie Objects you want to configure. '
                                             'For Movie Cameras, position the 3D view with the desired framing to be the start '
                                             'of the animation (Pos A), then click on Set the position A.'
                                             'For Movie Objects, position, rotate and/or keep them in their current position, then '
                                             'click on this button')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        if ENABLE_01 == 'Objects':
            mo.setMOPosA(Option = MO)
        if ENABLE_01 == 'Camera' or ENABLE_01 == 'Camera and objects' or ENABLE_01 == 'Camera and connection':
            mc.setMCPosA(Option = MC)

class SetMoviePosB:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMoviePosBIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMoviePosB', 'Set the B position of a camera or objects'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMoviePosB', 
                                             'Applicable for creating an animation from point A to B '
                                             '(not when the Movie Camera target or Movie Objects are set up to follow a route). '
                                             'Select and activate the Movie Camera or Movie Objects you want to configure (if not so). '
                                             'For Movie Cameras, position the 3D view with the desired framing to be the end '
                                             'of the animation (Pos B), then click on Set the position B.'
                                             'For Movie Objects, position and/or rotate them in the final position, then '
                                             'click on this button')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not ANIMATION:
                return True
        else:
            return False

    def Activated(self):
        if ENABLE_01 == 'Objects':
            mo.setMOPosB(Option = MO)
        if ENABLE_01 == 'Camera' or ENABLE_01 == 'Camera and objects' or ENABLE_01 == 'Camera and connection':
            mc.setMCPosB(Option = MC)

# ======================================================================================
# 2. Command functions

# 2.1. Support

def modifyAnimationIndicator(Animation = False):
    global ANIMATION
    global MC
    global MO
    if Animation == False:
        ANIMATION = False
        if MC != None:
            MC.Cam_07OnAnim = False
        if MO != None:
            MO.Obj_07AnimOnAnim = False
        getMessage(message = 'ANIMATION = False')
    if Animation == True:
        ANIMATION = True
        if MC != None:
            if MC.Cam_06Enable != 'Objects' and MC.Cam_06Enable != 'Connection':
                MC.Cam_07OnAnim = True
        if MO != None:
            MO.Obj_07AnimOnAnim = True
        getMessage(message = 'ANIMATION = True')
    FreeCAD.ActiveDocument.recompute()

def enableCameraObjects(Enable = 'None'):
    global ENABLE_01
    global MO
    if Enable == 'Camera':
        ENABLE_01 = 'Camera'
        getMessage(message = 'Camera is enabled')
    if Enable == 'Objects':
        ENABLE_01 = 'Objects'
        getMessage(message = 'Objects are enabled')
    if Enable == 'Camera and objects':
        ENABLE_01 = 'Camera and objects'
        getMessage(message = 'Camera and objects are enabled')
    if Enable == 'Camera and connection':
        ENABLE_01 = 'Camera and connection'
        getMessage(message = 'Camera and connection are enabled')
    if Enable == 'Clapperboard':
        ENABLE_01 = 'Clapperboard'
        getMessage(message = 'Clapperboard is enabled')

def getViewProjection():
    if MC != None:
        if MC.Cam_06Enable == 'Camera' or MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Camera and objects':
            Gui.runCommand('Std_PerspectiveCamera',1)

def getTimeAnimation(secs = 0):
    hours, minutes = divmod(secs, 3600)
    minutes, seconds = divmod(minutes, 60)
    TimeAnimation = f'{int(hours):0>2}:{int(minutes):0>2}:{seconds:0>5.2f}'
    return TimeAnimation

# ======================================================================================
# 2.2. Enabling commands

def enableMovieSelection(Enable = 'None'):
    global MC
    global MO
    Selection = []
    Selection = Gui.Selection.getSelection()
    for n in range(len(Selection)):
        if Enable == 'Camera':
            if not Selection[n].Name[5] == 'C':
               getMessage(message = 'Select a MovieCamera')
               return
            else:
                MC = Selection[0]
                MC.Cam_07OnAnim = False
                mc.enableCameraSelection(Enable = MC)
                if MC.Cam_06Enable == 'Camera':
                    enableCameraObjects(Enable = 'Camera')
                if MC.Cam_06Enable == 'Camera and objects':
                    enableCameraObjects(Enable = 'Camera and objects')
                if MC.Cam_06Enable == 'Objects':
                    enableCameraObjects(Enable = 'Objects')
                if MC.Cam_06Enable == 'Camera and connection':
                    enableCameraObjects(Enable = 'Camera and connection')
                if MC.Cam_06Enable == 'Connection':
                    enableCameraObjects(Enable = 'Connection')
        if Enable == 'Objects':
            if not Selection[n].Name[5] == 'O':
               getMessage(message = 'Select a MovieObjects')
               return
            else:
                enableCameraObjects(Enable = 'Objects')
                MO = Selection[0]
                mo.enableObjectsSelection(Enable = MO)
                MO.Obj_07AnimOnAnim = False
    getSelectionSteps(Content = Selection)

def getSelectionSteps(Content = None):
    global MC
    global MO
    global CAMERA_NAME
    global OBJECTS_NAME
    global ANIM_INI_STEP
    global ANIM_CURRENT_STEP
    global ANIM_END_STEP
    global ANIM_FPS
    global SEQ_ANIM_LIB

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
    ANIM_TOTAL_STEPS = 0
    ANIM_FPS = 0

    # Animation sequence
    # Components = (CameraN, InitCameraStep, EndCameraStep, ObjectsN, InitObjectsStep, EndObjectsStep)
    Components = ()
    SEQ_ANIM_LIB = {}

    # Cameras and Objects steps goes to SEQ_ANIM_LIB
    for n in range(len(Selection)):
        # Cameras ===========================================================================
        if Selection[n].Name[5] == 'C':
            MC = Selection[n]
            CameraN = MC.Name
            # Camera-------------------------------------------------------------------------
            if MC.Cam_06Enable == 'Camera':
                InitCameraStep = NextStep
                EndCameraStep = EndCameraStep + (MC.Cam_03AnimEndStep - MC.Cam_01AnimIniStep)
                if InitCameraStep == 0:
                    EndCameraStep -= 1
                #MC.Cam_04AnimTotalSteps = MC.Cam_03AnimEndStep
                if MC.Cam_01Target == 'Follow a route':
                    MC.Cam_04AnimTotalSteps = MC.Cam_03AnimEndStep + MC.Cam_03TargetStepsForward

                # Getting camera time animation
                t = (MC.Cam_03AnimEndStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
                MC.Cam_06AnimTime = getTimeAnimation(secs = t)

                # Cameras steps goes to SEQ_ANIM_LIB
                Components = (CameraN, InitCameraStep, EndCameraStep, 'None', InitCameraStep, EndCameraStep)
                for s1 in range(MC.Cam_03AnimEndStep + 1):
                    stepCamera = InitCameraStep + s1
                    SEQ_ANIM_LIB[stepCamera] = Components

                # Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            # Camera and Objects ----------------------------------------------------------------
            if MC.Cam_06Enable == 'Camera and objects' or MC.Cam_06Enable == 'Objects':
                #1 Verifying
                if MC.Cam_05ObjectsSelected != None:
                    Objects = MC.Cam_05ObjectsSelected
                    pass
                else:
                    getMessage(message = 'Select MovieObjects in Cam_06Enable')
                    return

                #2 Setting Init and End camera steps
                InitCameraStep = NextStep
                interval0 = MC.Cam_04AnimTotalSteps - MC.Cam_03AnimEndStep
                MC.Cam_04AnimTotalSteps = 0
                for n1 in range(len(Objects)):
                    MO = Objects[n1]
                    interval1 = MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep
                    MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + interval1
                MC.Cam_03AnimEndStep = MC.Cam_04AnimTotalSteps - interval0
                if MC.Cam_01Target == 'Follow a route':
                    MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + MC.Cam_03TargetStepsForward

                # Getting camera time animation
                t = (MC.Cam_03AnimEndStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
                MC.Cam_06AnimTime = getTimeAnimation(secs = t)

                # Total camera steps adds to EndCameraStep
                EndCameraStep = EndCameraStep + MC.Cam_03AnimEndStep

                #3 Setting Init and End objects step
                EndObjectsStep = NextStep
                for n2 in range(len(Objects)):
                    MO = Objects[n2]
                    # Getting time animation of each MovieObjects
                    t = (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep) / MO.Obj_05AnimFps
                    MO.Obj_06AnimTime = getTimeAnimation(secs = t)

                    # Objects key steps
                    InitObjectsStep = NextStep
                    EndObjectsStep = EndObjectsStep + (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep)
                    NextStep = EndObjectsStep + 1

                    #4 Camera and objects key steps goes to SEQ_ANIM_LIB
                    ObjectsN = MO.Name
                    Components = (CameraN, InitCameraStep, EndCameraStep, ObjectsN, InitObjectsStep, EndObjectsStep)
                    for s2 in range(MO.Obj_03AnimEndStep + 1):
                        stepObjects = InitObjectsStep + s2
                        SEQ_ANIM_LIB[stepObjects] = Components

                #5 Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            # Camera and connection -----------------------------------------------------------
            if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
                InitCameraStep = NextStep
                Values = []
                if MC.Cam_07Connection == 'None':
                     getMessage(message = 'Connection is enable, you have select one connection in Cam_07Connection')
                     return
                else:
                    # Camera and connection objects steps goes to SEQ_ANIM_LIB
                    co.verification(Selection = MC)
                    Values = co.connectionSteps(v0 = InitObjectsStep, v1 = EndObjectsStep, 
                                                v2 = InitCameraStep, v3 = EndCameraStep, v4 = NextStep,
                                                 v5 = SEQ_ANIM_LIB, Selection = MC)
                EndCameraStep = Values[0]
                SEQ_ANIM_LIB = Values[1]

                # Adding total camera steps to total animation
                ANIM_END_STEP = EndCameraStep
                NextStep = ANIM_END_STEP + 1

            AnimCameraFps = MC.Cam_05AnimFps
            #FreeCAD.Console.PrintMessage(translate('Movie', f'MC: {MC.Name}') + '\n')

        # Objects ===========================================================================
        if Selection[n].Name[5] == 'O':
            MO = Selection[n]
            # Getting objects time animation
            t = (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep) / MO.Obj_05AnimFps
            MO.Obj_06AnimTime = getTimeAnimation(secs = t)

            # Object key steps goes to SEQ_ANIM_LIB
            InitObjectsStep = NextStep
            EndObjectsStep = EndObjectsStep + (MO.Obj_03AnimEndStep - MO.Obj_01AnimIniStep)
            ObjectsN = MO.Name
            Components = ('None', None, None, ObjectsN, InitObjectsStep, EndObjectsStep)
            for s4 in range(MO.Obj_03AnimEndStep + 1):
                stepObjects1 = InitObjectsStep + s4
                SEQ_ANIM_LIB[stepObjects1] = Components
            Anim_ObjectsFps = MO.Obj_05AnimFps
            #FreeCAD.Console.PrintMessage(translate('Movie', f'MO: {MO.Name}') + '\n')

            # Adding total camera steps to total animation
            ANIM_END_STEP = EndObjectsStep
            NextStep = ANIM_END_STEP + 1

    # Defining the remaining animation elements
    modifyAnimationIndicator(Animation = False)
    CAMERA_NAME = 'None'
    OBJECTS_NAME = 'None'

    if not AnimCameraFps:
        ANIM_FPS = Anim_ObjectsFps
    else:
        ANIM_FPS = AnimCameraFps

    #FreeCAD.Console.PrintMessage(translate('Movie', f'EndObjectsStep e {EndObjectsStep}') + '\n')
    #FreeCAD.Console.PrintMessage(translate('Movie', f'ANIM_END_STEP: {ANIM_END_STEP}') + '\n')
    #FreeCAD.Console.PrintMessage(translate('Movie', f'SEQ_ANIM_LIB: {SEQ_ANIM_LIB}') + '\n')

def enableMovieClapperboard():
    global CL
    global ANIM_FPS
    global ANIM_INI_STEP
    global ANIM_END_STEP

    ClapSelection = None
    ClapSelection = Gui.Selection.getSelection()
    if not ClapSelection[0].Name[0] == 'C':
        getMessage(message = 'Select a Clapperboard')
        return
    CL = ClapSelection[0]
    Selection = []
    Selection = CL.Clap_03AnimationSelection
    if not Selection:
        getMessage(message = 'Select at least one Movie Camera or Movie Object to enable')
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
    t = (CL.Clap_03AnimEndStep - CL.Clap_01AnimIniStep) / CL.Clap_05AnimFps
    CL.Clap_06AnimTime = getTimeAnimation(secs = t)

    # Defining the remaining animation elements
    enableCameraObjects(Enable = 'Clapperboard')
    ANIM_FPS = CL.Clap_05AnimFps
    return CL
    #FreeCAD.Console.PrintMessage(translate('Movie', f'Clapperboard: {CL.Name}') + '\n')

# ======================================================================================
# 2.3. Animation commands

def recoverIniMovieAnimation():
    global STEP_POS
    global CL
    global ANIM_INI_STEP
    global ANIM_CURRENT_STEP

    if ENABLE_01 == 'Clapperboard':
        cl.stopRecordCamera(Clap = CL)

    if ANIM_CURRENT_STEP > ANIM_INI_STEP:
        STEP_POS = 'P'
        if ANIM_CURRENT_STEP > SEQ_ANIM_LIB[ANIM_CURRENT_STEP][4]:
            ANIM_CURRENT_STEP = SEQ_ANIM_LIB[ANIM_CURRENT_STEP][4]
        else:
            ANIM_CURRENT_STEP = SEQ_ANIM_LIB[ANIM_CURRENT_STEP - 1][4]
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
    else:
        ANIM_CURRENT_STEP = ANIM_INI_STEP
        return

    #FreeCAD.Console.PrintMessage(translate('Movie', f'STEP_POS e {STEP_POS}') + '\n')
    getViewProjection()
    getMovieMobile()
    Gui.updateGui()

def prevMovieAnimation():
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
    modifyAnimationIndicator(Animation = False)

def playMovieAnimation():
    global STEP_POS
    global ANIM_CURRENT_STEP
    global CL
    global ANIM_INI_STEP
    global ANIM_END_STEP
    global ANIM_FPS

    modifyAnimationIndicator(Animation = True)
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

    modifyAnimationIndicator(Animation = False)
    if ENABLE_01 == 'Clapperboard':
        cl.stopRecordCamera(Clap = CL)

def getMovieMobile():
    global MC
    global MO
    global CO
    global CAMERA_NAME
    global OBJECTS_NAME

    CameraN = SEQ_ANIM_LIB[ANIM_CURRENT_STEP][0]
    ObjectsN = SEQ_ANIM_LIB[ANIM_CURRENT_STEP][3]

    if ObjectsN != 'None':
        if ObjectsN[5] == 'O':
            if OBJECTS_NAME != ObjectsN:
                Gui.Selection.clearSelection()
                if MO != None:
                    MO.Obj_07AnimOnAnim = False
                OBJECTS_NAME = ObjectsN
                #FreeCAD.Console.PrintMessage(translate('Movie', f'Objects e {ObjectsN}') + '\n')
                MO = FreeCAD.ActiveDocument.getObject(ObjectsN)
                #FreeCAD.Console.PrintMessage(translate('Movie', f'Objects e {MO.Name}') + '\n')
                Gui.Selection.addSelection(MO)
                MO.Obj_07AnimOnAnim = True
            MO.Obj_02AnimCurrentStep = (ANIM_CURRENT_STEP - SEQ_ANIM_LIB[ANIM_CURRENT_STEP][4]) + MO.Obj_01AnimIniStep
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
            #FreeCAD.Console.PrintMessage(translate('Movie', f'Camera e {MC.Name}') + '\n')
            Gui.Selection.addSelection(MC)
            MC.Cam_07OnAnim = True
        MC.Cam_02AnimCurrentStep = (ANIM_CURRENT_STEP - SEQ_ANIM_LIB[ANIM_CURRENT_STEP][1]) + MC.Cam_01AnimIniStep
        if MC.Cam_06Enable == 'Objects' or MC.Cam_06Enable == 'Connection':
            enableCamera = False
        if enableCamera != False:
            # Getting camera time animation
            t = (MC.Cam_02AnimCurrentStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
            MC.Cam_06AnimTime = getTimeAnimation(secs = t)
            # Getting camera pos animation
            mc.getMovieCameraMobile(Selection = MC)
        if MC.Cam_06Enable == 'Camera and connection' or MC.Cam_06Enable == 'Connection':
            if MC.Cam_07Connection != 'None' and MC.Cam_07Connection != 'ExplodedAssembly':
                if ANIMATION_BACK == False:
                    co.connectionPos(Selection = MC)
                else:
                    co.connectionPrev(Selection = MC)

def postMovieAnimation():
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
    global ANIM_CURRENT_STEP
    global STEP_POS

    if ANIM_CURRENT_STEP < ANIM_END_STEP:
        STEP_POS = 'P'
        if ANIM_CURRENT_STEP < SEQ_ANIM_LIB[ANIM_CURRENT_STEP][5]:
            ANIM_CURRENT_STEP = SEQ_ANIM_LIB[ANIM_CURRENT_STEP][5]
        else:
            if ANIM_CURRENT_STEP + 1 < ANIM_END_STEP:
                ANIM_CURRENT_STEP = SEQ_ANIM_LIB[ANIM_CURRENT_STEP + 1][5]
        if ENABLE_01 == 'Clapperboard':
            CL.Clap_02AnimCurrentStep = ANIM_CURRENT_STEP
        #FreeCAD.Console.PrintMessage(translate('Movie', f'ANIM_CURRENT_STEP e {ANIM_CURRENT_STEP}') + '\n')
        #FreeCAD.Console.PrintMessage(translate('Movie', f'ANIM_END_STEP e {ANIM_END_STEP}') + '\n')

    else:
        return
    #FreeCAD.Console.PrintMessage(translate('Movie', f'STEP_POS e {STEP_POS}') + '\n')
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
