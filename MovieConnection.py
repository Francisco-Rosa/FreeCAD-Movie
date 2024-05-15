''' Movie Workbench, Connection Module '''

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

import FreeCADGui as Gui
import FreeCAD
from PySide.QtCore import QT_TRANSLATE_NOOP
import os
import time
import MovieCamera as mc
import MovieAnimation as ma
import MovieClapperboard as cl
import MovieObject as ob

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

'''INSTRUCTIONS'''
'''
This is the module to connect Movie Workbench with other object animation workbenches. 
You can add them, according to the indicated suggestions (from 01 to 08),
always making all the necessary adaptations and testing them, before finalizing the 
inclusion.
'''
# ======================================================================================
# 0. Global

EA_PRESENCE = False
VERIFIED = False

''' 01. Include here the indication of the presence of the Workbench you want to connect'''
#WN_PRESENCE = False 

def verification(Selection = None):

    global EA_PRESENCE
    global VERIFIED
    #global WN_presence
    
    MC = Selection

    if VERIFIED == False:
        pass
    else:
        return

    if MC.Cam_07Connection == 'ExplodedAssembly':
        if 'ExplodedAssembly' in FreeCAD.ActiveDocument.Content:
            EA_PRESENCE = True
            import ExplodedAssembly as ea
            ea.connectionMC(option = True)
        else:
            EA_PRESENCE = False

    '''
    if MC.Cam_07Connection == 'WorbenchName':
        if 'WorbenchName' in FreeCAD.ActiveDocument.Content:
            WN_PRESENCE = True
        else:
            WN_PRESENCE = False
    '''

    VERIFIED = True

# ======================================================================================
# 1. Connection list

'''02.Include in the connection list below the name of the Workbench you want to connect'''

connections = ['None', 'ExplodedAssembly']

# ======================================================================================
# 2. Functions

'''Go to the beginning of the animation'''
def connectionIni(Selection = None):

    MC = Selection
    '''ExplodedAssembly Workbench'''
    if MC.Cam_07Connection == 'ExplodedAssembly':
        if EA_PRESENCE == True :
            Gui.runCommand('GoToStart',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly Workbench first!') + '\n')
            return

    '''03. Include here the instructions for the Workbench you want to connect'''
    '''For example:'''
    '''
    'WorkbenchName Workbench'
    if MC.Cam_07Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('GoToStart WorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first!') + '\n')
            return
    '''
# ======================================================================================

'''Move the animation one step back'''
def connectionPrev(Selection = None):

    MC = Selection

    '''04. Include here the instructions for the Workbench you want to connect'''
    '''For example:'''
    '''
    'WorkbenchName Workbench'

    if MC.Cam_07Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('PrevWorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first!') + '\n')
            return
    '''
# ======================================================================================
'''Pause the animation'''
def connectionPause(Selection = None):

    MC = Selection
    '''ExplodedAssembly Workbench'''
    if MC.Cam_07Connection == 'ExplodedAssembly':
        if EA_PRESENCE == True :
            Gui.runCommand('StopAnimation',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly Workbench first!') + '\n')
            return

    '''05. Include here the instructions for the Workbench you want to connect'''
    '''For example:'''
    '''
    'WorkbenchName Workbench'
    if MC.Cam_07Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('PauseAnimationWorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first!') + '\n')
            return
    '''
# ======================================================================================
'''Move the animation one step forward'''
def connectionPos(Selection = None):

    MC = Selection

    '''06. Include here the instructions for the Workbench you want to connect'''
    '''For example:'''
    '''
    'WorkbenchName Workbench'

    if MC.Cam_07Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('PosWorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first!') + '\n')
            return
    '''
# ======================================================================================
'''Go to the end of the animation'''
def connectionEnd(Selection = None):

    MC = Selection
    '''ExplodedAssembly Workbench'''
    if MC.Cam_07Connection == 'ExplodedAssembly':
        if EA_PRESENCE == True :
            Gui.runCommand('GoToEnd',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the ExplodedAssembly Workbench first!') + '\n')
            return

    '''07. Include here the instructions for the Workbench you want to connect'''
    '''For example:'''
    '''
    'WorkbenchName Workbench'
    if MC.Cam_07Connection == 'WorkbenchName':
        if WN_PRESENCE == True:
            Gui.runCommand('GoToEndWorkbenchName',0)
        else:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation of '
                                                   'the WorkbenchName Workbench first!') + '\n')
            return
    '''
# ======================================================================================

'''Setting the number of steps of the animation of the workbench connected'''
def connectionSteps(v0 = None, v1 = None, v2 = None, v3 = None, v4 = None,
                    v5 = None, Selection = None):
    Values = []
    InitObjectsStep = v0
    END_OBJECTS_STEP = v1
    InitCameraStep = v2
    END_CAMERA_STEP = v3
    NextStep = v4
    Components = ()
    CameraN = 'None'
    ObjectsN = 'None'
    SEQ_ANIM_LIB = v5

    MC = Selection
    CameraN = MC.Name
    if MC.Cam_07Connection == 'ExplodedAssembly':
        EA = FreeCAD.ActiveDocument.ExplodedAssembly
        CoObjects = EA.Group

    '''08. Include here the instructions for the Workbench you want to connect'''
    '''For example:'''
    '''
    if MC.Cam_07Connection == 'WorkbenchName':
        WN = FreeCAD.ActiveDocument.WorkbenchName
        CoObjects = WN.Group
    '''

    # Setting camera steps
    MC.Cam_01AnimIniStep = 0
    MC.Cam_04AnimTotalSteps = 0
    for n5 in range(len(CoObjects)):
        ObjectsN = CoObjects[n5].Name
        MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + CoObjects[n5].AnimationSteps
    if InitObjectsStep == 0:
        MC.Cam_04AnimTotalSteps -= 1
    MC.Cam_03AnimEndStep = MC.Cam_04AnimTotalSteps
    # Getting camera time animation
    t = (MC.Cam_02AnimCurrentStep - MC.Cam_01AnimIniStep) / MC.Cam_05AnimFps
    MC.Cam_06AnimTime = ma.getTimeAnimation(secs = t)
    # Total camera steps adds to END_CAMERA_STEP
    END_CAMERA_STEP = END_CAMERA_STEP + MC.Cam_04AnimTotalSteps
    if InitCameraStep > 0:
        END_CAMERA_STEP += 1

    if MC.Cam_01Target == 'Follow a route':
        MC.Cam_04AnimTotalSteps = MC.Cam_04AnimTotalSteps + MC.Cam_03TargetStepsForward

    for n3 in range(len(CoObjects)):
        ObjectsN = CoObjects[n3].Name
        InitObjectsStep = NextStep
        END_OBJECTS_STEP = END_OBJECTS_STEP + CoObjects[n3].AnimationSteps
        if n3 == 0:
            END_OBJECTS_STEP -= 1
        NextStep = END_OBJECTS_STEP + 1

        # Setting SEQ_ANIM_LIB
        Components = (CameraN, InitCameraStep, END_CAMERA_STEP, 
                      ObjectsN, InitObjectsStep, END_OBJECTS_STEP)
        for s3 in range(CoObjects[n3].AnimationSteps):
            stepCo = InitObjectsStep + s3
            SEQ_ANIM_LIB[stepCo] = Components

    Values = [END_CAMERA_STEP, SEQ_ANIM_LIB]
    return Values

# ======================================================================================

'''Only for ExplodedAssembly Workbench'''

CL = None
def setClapperboardSelection(Clap = None):
    global CL
    CL = Clap

'''Play the animation backward'''
def connectionPlayBackward(Selection = None):
    global MC
    global ANIMATION_BACK

    ANIMATION_BACK = True
    ma.modifyAnimationIndicator(Animation = True)
    MC = Selection

    '''ExplodedAssembly Workbench'''

    if EA_PRESENCE == True:
        if CL != None:
            if CL.Clap_04OnRec == True:
                cl.runRecordCamera()
        Gui.runCommand('PlayBackward',0)
        ma.modifyAnimationIndicator(Animation = False)
        if CL != None:
            CL.Clap_04OnRec = False
    else:
        FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation from '
                                                   'the ExplodedAssembly workbench first!') + '\n')
        return

'''Play the animation'''
def connectionPlay(Selection = None):
    global MC
    global ANIMATION_BACK

    ANIMATION_BACK = False
    ma.modifyAnimationIndicator(Animation = True)
    MC = Selection

    '''ExplodedAssembly Workbench'''

    if EA_PRESENCE == True:
        if CL != None:
            if CL.Clap_04OnRec == True:
                cl.runRecordCamera()
        Gui.runCommand('PlayForward',0)
        ma.modifyAnimationIndicator(Animation = False)
        if CL != None:
            CL.Clap_04OnRec = False
    else:
        FreeCAD.Console.PrintMessage(translate('Movie', 'You must have an animation from '
                                                   'the ExplodedAssembly Workbench first!') + '\n')
        return

'''Playing the animation from the ExplodedAssembly Workbench'''
def connectionEA():

    EA = FreeCAD.ActiveDocument.ExplodedAssembly

    if MC.Cam_07Connection == 'ExplodedAssembly' and MC.Cam_07OnAnim == True:
        mc.getMovieCameraMobile(Selection = MC)
        if ANIMATION_BACK == False:
            MC.Cam_02AnimCurrentStep += 1
        else:
            if MC.Cam_02AnimCurrentStep > MC.Cam_01AnimIniStep:
                MC.Cam_02AnimCurrentStep -= 1
        if MC.Cam_07OnAnim == False:
            EA.InAnimation = False
        if CL != None:
            CL.Clap_02AnimCurrentStep = MC.Cam_02AnimCurrentStep
            if CL.Clap_04OnRec == True:
                cl.runRecordCamera()
            if EA.InAnimation == False:
                cl.stopRecordCamera()

# ======================================================================================              
