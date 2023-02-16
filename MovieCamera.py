''' Movie Workbench, Movie Camera animation toolbar '''

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

import FreeCAD
import FreeCADGui as Gui
from pivy import coin
import time
import os
from math import degrees, radians
from PySide.QtCore import QT_TRANSLATE_NOOP
import RecordPlayVideo as rpv
import Connection as co

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Global

STEP_POS = 'I'
CL_presence = False

def verification():
    global CL_presence
    if 'Clapperboard' in FreeCAD.ActiveDocument.Content:
        CL_presence = True    
    else:
        CL_presence = False 

# ======================================================================================
# 1. Classes

class MovieCamera:
    '''Class to create a camera to be animated'''
       
    def __init__(self, obj):

    # Movie Camera 1 - Animation config

        obj.addProperty('App::PropertyInteger', 'Anim_1TotalSteps', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the number of steps through which the camera animation will be '
                                                    'animate in this section.')).Anim_1TotalSteps = 100
        obj.addProperty('App::PropertyInteger', 'Anim_2IniStep', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the step which this section of the animation will begin.')).Anim_2IniStep = 0
        obj.addProperty('App::PropertyInteger', 'Anim_3EndStep', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the step which this section of the animation will finish.')).Anim_3EndStep = 100         
        obj.addProperty('App::PropertyInteger', 'Anim_4CurrentStep', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'The current step of this section of the animation.')).Anim_4CurrentStep = 0
        obj.addProperty('App::PropertyInteger', 'Anim_5Fps', 'Movie Camera 01 - Animation config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Indicate the fps through the section of the animation will be '
                                                    'performed. It is a simulation and will depend on the '
                                                    'computer performance.')).Anim_5Fps = 24

    # Movie Camera 02 - Camera config

        obj.addProperty('App::PropertyEnumeration', 'Cam_1Type', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose the camera through which this section of the animation will be '
                                                    'performed.')).Cam_1Type = ('3DView', 'Render')
        obj.addProperty('App::PropertyLink', 'Cam_2Render_Selection', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'If you have chosen the render camera in Cam_1Type, you have to select '
                                                    'which one will be used in this section of the animation.'
                                                    )).Cam_2Render_Selection = None                                                    
        obj.addProperty('App::PropertyEnumeration', 'Cam_3Connection', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose the connection through which the animation will be performed together, if so.'
                                                    'Make sure the connected animation module is installed.'
                                                    )).Cam_3Connection = list(co.connections)                                         
        obj.addProperty('App::PropertyBool', 'Cam_4OnAnim', 'Movie Camera 02 - Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                                     'It only indicative whether the camera is in animation or not. '
                                                     'It should not be changed manually, it is controlled by the animations buttons.'
                                                     )).Cam_4OnAnim = False                                              
  
    # Movie Camera 03 - Target config                                                    
                                                                                                       
        obj.addProperty('App::PropertyEnumeration', 'Cam_Target', 'Movie Camera 03 - Target config', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose the type of camera target. The target object must be '
                                                    'selected in Cam_Target_Object_Selection, while in the follow a route option '
                                                    'you have to select the route in Cam_Route_Selection.'
                                                    )).Cam_Target = ('Free', 'Follow an object or point', 'Follow a route')
        obj.addProperty('App::PropertyLink', 'Cam_Target_Object_Selection', 'Movie Camera 03 - Target config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Select the point or object you want the camera to follow.'
                                                    )).Cam_Target_Object_Selection = None
        obj.addProperty('App::PropertyInteger', 'Cam_Target_Steps_Forward', 'Movie Camera 03 - Target config', QT_TRANSLATE_NOOP('App::Property', 
                                                    'If you chose that the target follows the route, indicate here how many steps '
                                                    'it will be in front of the camera on the path.'
                                                    )).Cam_Target_Steps_Forward = 10

    # Movie Camera 04 - Camera follows a path
    
        obj.addProperty('App::PropertyBool', 'Cam_Route', 'Movie Camera 04 - Camera follows a path', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose True if the camera will be animate on a route. '
                                                    'You have to select a single segment on Cam_Route_Selection to use it.'
                                                    )).Cam_Route = False
        obj.addProperty('App::PropertyLink', 'Cam_Route_Selection', 'Movie Camera 04 - Camera follows a path', 
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose the route through which the camera will be '
                                                    'animate. You have to select a single segment such as: line, arc, circle, '
                                                    'ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches.'
                                                    )).Cam_Route_Selection = None

    # Movie Camera 05 - Camera Pos A-B - pos On/Off
                                                     
        obj.addProperty('App::PropertyBool', 'Cam_XMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose True, if you want to animate the camera in x direction.'
                                                    )).Cam_XMov = False
        obj.addProperty('App::PropertyBool', 'Cam_YMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose True, if you want to animate the camera in y direction.'
                                                    )).Cam_YMov = False
        obj.addProperty('App::PropertyBool', 'Cam_ZMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off', QT_TRANSLATE_NOOP('App::Property', 
                                                    'Choose True, if you want to animate the camera in z direction.'
                                                    )).Cam_ZMov = False

    # Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off

        obj.addProperty('App::PropertyBool', 'Cam_01Yaw', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose True, if you want '
                                                    'animate the camera horizontal angle.')).Cam_01Yaw = False
        obj.addProperty('App::PropertyBool', 'Cam_02Pitch', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose True, if you want '
                                                    'animate the camera vertical angle.')).Cam_02Pitch = False
        obj.addProperty('App::PropertyBool', 'Cam_03Roll', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose True, if you want '
                                                    'animate the camera roll angle.')).Cam_03Roll = False
        obj.addProperty('App::PropertyBool', 'Cam_04Zoom', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'Choose True, if you want to animate the camera zoom.'
                                                    )).Cam_04Zoom = False

    # Movie Camera 07 - Camera Pos A-B - pos AB 

        obj.addProperty('App::PropertyFloat', 'Cam_01XPosA', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'It is set when the Save position A button is pressed, after that, if necessary, you can make '
                                                    'adjustments to the x-value.')).Cam_01XPosA = 0                                          
        obj.addProperty('App::PropertyFloat', 'Cam_02YPosA', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'It is set when the Save position A button is pressed, after that, if necessary, you can make '
                                                    'adjustments to the y-value.')).Cam_02YPosA = 0
        obj.addProperty('App::PropertyFloat', 'Cam_03ZPosA', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                     'It is set when the Save position A button is pressed, after that, if necessary, you can make '
                                                    'adjustments to the z-value.')).Cam_03ZPosA = 0
        obj.addProperty('App::PropertyFloat', 'Cam_04XPosB', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'It is set when the Save position B button is pressed, after that, if necessary, you can make '
                                                    'adjustments to the x-value.')).Cam_04XPosB = 1000.0
        obj.addProperty('App::PropertyFloat', 'Cam_05YPosB', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'It is set when the Save position B button is pressed, after that, if necessary, you can make '
                                                    'adjustments to the y-value.')).Cam_05YPosB = 1000.0
        obj.addProperty('App::PropertyFloat', 'Cam_06ZPosB', 'Movie Camera 07 - Camera Pos A-B - pos AB', QT_TRANSLATE_NOOP('App::Property', 
                                                    'It is set when the Save position B button is pressed, after that, if necessary, you can make '
                                                    'adjustments to the z-value.')).Cam_06ZPosB = 1000.0

    # Movie Camera 08 - Camera Pos A-B - angles

        obj.addProperty('App::PropertyAngle', 'Cam_01YawPosA', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'It is set when the Save position A button is pressed, after that, if '
                                                    'necessary, you can make little adjustments to the yaw value of the camera.')
                                                    ).Cam_01YawPosA = 0
        obj.addProperty('App::PropertyAngle', 'Cam_02PitchPosA', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'It is set when the Save position A button is pressed, after that, if '
                                                    'necessary, you can make little adjustments to the pitch value of the camera.'
                                                    )).Cam_02PitchPosA = 0
        obj.addProperty('App::PropertyAngle', 'Cam_03RollPosA', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'It is set when the Save position A button is pressed, after that, if '
                                                    'necessary, you can make little adjustments to the roll value of the camera.'
                                                    )).Cam_03RollPosA = 90
        obj.addProperty('App::PropertyAngle', 'Cam_04YawPosB', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'It is set when the Save position B button is pressed, after that, if '
                                                    'necessary, you can make little adjustments to the yaw value of the camera.'
                                                    )).Cam_04YawPosB = 30
        obj.addProperty('App::PropertyAngle', 'Cam_05PitchPosB', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'It is set when the Save position B button is pressed, after that, if '
                                                    'necessary, you can make little adjustments to the pitch value of the camera.'
                                                    )).Cam_05PitchPosB = 45
        obj.addProperty('App::PropertyAngle', 'Cam_06RollPosB', 'Movie Camera 08 - Camera Pos A-B - Angles', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'It is set when the Save position B button is pressed, after that, if '
                                                    'necessary, you can make little adjustments to the roll value of the camera.'
                                                    )).Cam_06RollPosB = 45

    # Movie Camera 09 - Camera Pos A-B - Zoom

        obj.addProperty('App::PropertyAngle', 'Cam_02ZoomPosA', 'Movie Camera 09 - Camera Pos A-B - Zoom', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'If Cam_04Zoom is True and after the Save position A button is pressed, '
                                                    'you can adjust the angle in degrees you want to start the '
                                                    'camera animation. Descending to zoom in, increasing to zoom out.'
                                                    )).Cam_02ZoomPosA = 50
        obj.addProperty('App::PropertyAngle', 'Cam_03ZoomPosB', 'Movie Camera 09 - Camera Pos A-B - Zoom', QT_TRANSLATE_NOOP(
                                                    'App::Property', 'If Cam_04Zoom is True and after the Save position B button is pressed, '
                                                    'you can adjust the angle in degrees you want to finish the '
                                                    'camera animation. Descending to zoom in, increasing to zoom out.'
                                                    )).Cam_03ZoomPosB = 20

        obj.Proxy = self

class MovieCameraViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/MovieCameraIcon.svg'

# ======================================================================================    
# 2. Command classes

class CreateMovieCamera:
	
    def QT_TRANSLATE_NOOP(Movie, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateMovieCameraIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateMovieCamera', 'Create a Movie Camera'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateMovieCamera', 
                                             'Create a camera that follows a previously selected path, '
                                             'goes from position A to B or keeps in a fixed base. '
                                             'Configure its corresponding necessary properties '
                                             'before starting the animation.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True

        else:
            return False

    def Activated(self):
        ActivatedMovieCamera(self)
        MovieCamera.Cam_4OnAnim = False

def ActivatedMovieCamera(self):

    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'MovieCamera')
    MovieCamera(folder)
    MovieCameraViewProvider(folder.ViewObject)
                      
# ======================================================================================

class EnableMovieCamera:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EnableMovieCameraIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EnableMovieCamera', 'Enable one or more select movie cameras'),
                'ToolTip': QT_TRANSLATE_NOOP('EnableMovieCamera', 
                                             'First, select one or more movie cameras that you want to use, '
                                             'then click in this button to activate then to perform the the animation. After that, '
                                             'if you enable a connection to another animation workbench in Cam_3Connection, '
                                             'you must re-enable the cameras.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            return True

        else:
            return False
                                   
    def Activated(self):
        enableMovieCamera()

def enableMovieCamera():
    global MC
    global CAMERAS
    global N
    Gui.runCommand('Std_PerspectiveCamera',1)
    CAMERAS = []
    CAMERAS = Gui.Selection.getSelection()
    if not CAMERAS:
        FreeCAD.Console.PrintMessage(translate('Movie', 'Select at least one '
                                                   'Movie Camera to activate') + '\n')
        return
    else:
        N = 0
        MC = CAMERAS[N]
        Gui.Selection.clearSelection()
        verification()
        MC.Cam_4OnAnim = False
        if MC.Cam_3Connection != 'None':
            co.verification()
     
# ======================================================================================

class SetMovieCameraPosA:
	
    def QT_TRANSLATE_NOOP(Movie, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMovieCameraPosAIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMovieCameraPosA', 'Set movie camera position A'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMovieCameraPosA',
                                             'Applicable for creating an animation from point A to B '
                                             '(not when the camera target is set up to follow a route). ' 
                                             'First, select and activate the Movie Camera you want to configure. '
                                             'Position the 3D view with the desired framing to be the start '
                                             'of the animation (Pos A), then click in Save the position A.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MC.Cam_4OnAnim:
                return True

        else:
            return False

    def Activated(self):
        global MC
        MC.Cam_4OnAnim = False
        setMCPosA()

class SetMovieCameraPosB:
	
    def QT_TRANSLATE_NOOP(Movie, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMovieCameraPosBIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMovieCameraPosB', 'Set movie camera position B'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMovieCameraPosB', 
                                             'Applicable for creating an animation from point A to B '
                                             '(not when the camera target is set up to follow a route). '
                                             'Select and activate the Movie Camera you want to configure (if not so). '
                                             'Position the 3D view with the desired framing to be the end '
                                             'of the animation (Pos B), then click in Save the position B.')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MC.Cam_4OnAnim:
                return True

        else:
            return False
                                            
    def Activated(self):
        global MC
        MC.Cam_4OnAnim = False
        setMCPosB()

class IniMovieAnimation:

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/IniMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('IniMovieAnimation', 'Move to the beginning'),
                'ToolTip': QT_TRANSLATE_NOOP('IniMovieAnimation', 
                                             'On the first click, it returns to the beginning of the animation '
                                             'of the current camera and resets it. On the second click, it goes '
                                             'to the end of the animation of the previous camera (if so)')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MC.Cam_4OnAnim:
                return True

        else:
            return False
                                   
    def Activated(self):
        global MC
        MC.Cam_4OnAnim = False
        recoverIniMovieCamera()       
        if MC.Cam_3Connection != 'None':
            co.connectionIni()

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
            if not MC.Cam_4OnAnim:
                return True
                    
        else:
            return False
                                   
    def Activated(self):
        prevMovieAnimation()
 
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
            if MC.Cam_4OnAnim:
                return True

        else:
            return False
                                   
    def Activated(self):
        global MC
        MC.Cam_4OnAnim = False
        if MC.Cam_3Connection != 'None':
            co.connectionPause()

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
            if not MC.Cam_4OnAnim:
                return True

        else:
            return False
                                   
    def Activated(self):
        global MC
        MC.Cam_4OnAnim = True
        FreeCAD.ActiveDocument.recompute()
        if MC.Cam_3Connection != 'None':
            if MC.Cam_Target == 'Follow a route':
                if MC.Anim_3EndStep - (MC.Anim_4CurrentStep + MC.Cam_Target_Steps_Forward) > 0:
                    pass
                else:
                    MC.Cam_4OnAnim = False
                    return          
            else:
                if MC.Anim_3EndStep - MC.Anim_4CurrentStep > 0:
                    pass
                else:
                    MC.Cam_4OnAnim = False
                    return         
            co.connectionPlay()
        else:         
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
            if not MC.Cam_4OnAnim:
                return True
        else:
            return False
                                   
    def Activated(self):
        postMovieAnimation()

class EndMovieAnimation: 

    def QT_TRANSLATE_NOOP(Movie, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/EndMovieAnimationIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('EndMovieAnimation', 'Move to the end'),
                'ToolTip': QT_TRANSLATE_NOOP('EndMovieAnimation', 
                                             'On the first click, it moves to the end of the animation of the current camera. '
                                             'On the second click, it goes to the beginning of the animation of '
                                             'the next camera (if so.)')}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MC.Cam_4OnAnim:
                return True

        else:
            return False
                                   
    def Activated(self):
        global MC
        MC.Cam_4OnAnim = False
        getEndMovieCamera()
        if MC.Cam_3Connection != 'None':
            co.connectionEnd()

# ======================================================================================  
# 3. Functions

def setMCPosA():

    global MC
    global STEP_POS

    Gui.runCommand('Std_PerspectiveCamera',1)

    if MC.Cam_Target == 'Free':
        MC.Cam_XMov = True 
        MC.Cam_YMov = True 
        MC.Cam_ZMov = True 
        MC.Cam_01Yaw = True 
        MC.Cam_02Pitch = True
        MC.Cam_03Roll = True
        MC.Cam_04Zoom = True
        
    if MC.Cam_Target == 'Follow an object or point' :    
        MC.Cam_XMov = True 
        MC.Cam_YMov = True 
        MC.Cam_ZMov = True 
        MC.Cam_01Yaw = False 
        MC.Cam_02Pitch = False
        MC.Cam_03Roll = False
        MC.Cam_04Zoom = True

    # Camera node position A
    cameraNodeA = Gui.ActiveDocument.ActiveView.getCameraNode()
    
    # Camera position A   
    vectorNodeA = FreeCAD.Vector(cameraNodeA.position.getValue()) 
    MC.Cam_01XPosA = vectorNodeA[0]
    MC.Cam_02YPosA = vectorNodeA[1]
    MC.Cam_03ZPosA = vectorNodeA[2]
        
    # Camera angles pos A
    rotNodeA = FreeCAD.Rotation(*cameraNodeA.orientation.getValue().getValue())
    anglesYawPitchRollA = rotNodeA.getYawPitchRoll()                               
    MC.Cam_01YawPosA = anglesYawPitchRollA[0]                 
    MC.Cam_02PitchPosA = anglesYawPitchRollA[1]                 
    MC.Cam_03RollPosA = anglesYawPitchRollA[2]

    # Camera zoom pos A
    MC.Cam_02ZoomPosA = degrees(float(cameraNodeA.heightAngle.getValue()))
            
    # Render camera angles and zoom pos A
    if "Camera" in FreeCAD.ActiveDocument.Content and MC.Cam_1Type == 'Render':
        if not MC.Cam_2Render_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select a render '
                                                   'camera in Cam_2Render_Selection') + '\n')
            return
        else:
            renderCameraA = MC.Cam_2Render_Selection
            renderCameraA.ViewObject.Proxy.set_camera_from_gui()  
            renderCameraA.AspectRatio = 1.77 # resolution 1920/1080
            renderCameraA.ViewportMapping = "CROP_VIEWPORT_FILL_FRAME"              
            renderCameraA.ViewObject.Proxy.set_gui_from_camera()
              
    MC.Anim_4CurrentStep = 0           
    STEP_POS = 'I'
    Gui.updateGui()

def setMCPosB():

    global MC
    global STEP_POS

    Gui.runCommand('Std_PerspectiveCamera',1)

    # Camera node position B
    cameraNodeB = Gui.ActiveDocument.ActiveView.getCameraNode()

    # Camera position B
    vectorNodeB = FreeCAD.Vector(cameraNodeB.position.getValue())
    MC.Cam_04XPosB = vectorNodeB[0]
    MC.Cam_05YPosB = vectorNodeB[1]
    MC.Cam_06ZPosB = vectorNodeB[2]

    # Camera angles pos B  	
    rotNodeB = FreeCAD.Rotation(*cameraNodeB.orientation.getValue().getValue())
    anglesYawPitchRollB = rotNodeB.getYawPitchRoll()                               
    MC.Cam_04YawPosB = anglesYawPitchRollB[0]                 
    MC.Cam_05PitchPosB = anglesYawPitchRollB[1]                 
    MC.Cam_06RollPosB = anglesYawPitchRollB[2]

    # Camera zoom pos B
    MC.Cam_03ZoomPosB = degrees(float(cameraNodeB.heightAngle.getValue()))
      
    # Render camera angles and zoom pos B
    if "Camera" in FreeCAD.ActiveDocument.Content and MC.Cam_1Type == 'Render':
        if not MC.Cam_2Render_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select a render '
                                                   'camera in Cam_2Render_Selection') + '\n')
            return
        else:
            renderCameraB = MC.Cam_2Render_Selection
            renderCameraB.ViewObject.Proxy.set_camera_from_gui()  
            renderCameraB.AspectRatio = 1.77 # resolution 1920/1080
            renderCameraB.ViewportMapping = "CROP_VIEWPORT_FILL_FRAME"              
            renderCameraB.ViewObject.Proxy.set_gui_from_camera()
              
    MC.Anim_4CurrentStep = MC.Anim_1TotalSteps           
    STEP_POS = 'I'
    Gui.updateGui()
 
def recoverIniMovieCamera():

    global MC
    global CAMERAS
    global STEP_POS

    if MC.Anim_4CurrentStep - MC.Anim_2IniStep > 0:              
        MC.Anim_4CurrentStep = MC.Anim_2IniStep              

    else:
        global N
        if N> 0:
            N -= 1
            MC = CAMERAS[N]
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(MC)
            if MC.Cam_Target == 'Follow a route':
                MC.Anim_4CurrentStep = MC.Anim_3EndStep - MC.Cam_Target_Steps_Forward
            else: 
                MC.Anim_4CurrentStep = MC.Anim_3EndStep
        else:
            return
                
    STEP_POS = 'I'
    Gui.runCommand('Std_PerspectiveCamera',1)     
    getMovieCameraMobile()
    Gui.updateGui()

def prevMovieAnimation():
    global MC
    if MC.Anim_4CurrentStep - MC.Anim_2IniStep > 0:
        MC.Anim_4CurrentStep -= 1                  
        Gui.runCommand('Std_PerspectiveCamera',1)
        getMovieCameraMobile()
        Gui.updateGui()
    else:
        return

def playMovieAnimation():

    global MC
    global STEP_POS
    global CAMERAS
    global N
    global CL_presence

    Gui.runCommand('Std_PerspectiveCamera',1)

    leftCameras = len(CAMERAS) - N

    for c in range(leftCameras):

        MC = CAMERAS[N]
        Gui.Selection.addSelection(MC)
        MC.Cam_4OnAnim = True           	  
        pauseTime = MC.Anim_1TotalSteps/(MC.Anim_5Fps*1000) # meter (*1000)
          
        if STEP_POS == 'I':      
            MC.Anim_4CurrentStep = MC.Anim_2IniStep
            
        steps = MC.Anim_3EndStep - MC.Anim_4CurrentStep
        
        if MC.Cam_Target == 'Follow a route':
            steps = steps - MC.Cam_Target_Steps_Forward
            
        STEP_POS = 'P'
                   
        for p in range (steps):
            
            getMovieCameraMobile()           
            Gui.updateGui()
            time.sleep(pauseTime)           

            if CL_presence == True:
                CL = FreeCAD.ActiveDocument.Clapperboard
                if CL.Cam_3OnRec == True:
                    rpv.runRecordCamera() 

            if MC.Cam_4OnAnim == False:
                break

            MC.Anim_4CurrentStep += 1
            
        time.sleep(pauseTime)
        if MC.Cam_4OnAnim == False:
            break
        
        Gui.Selection.clearSelection()
        MC.Cam_4OnAnim = False
        if leftCameras > 1 :
            N += 1

    if CL_presence == True:
        CL = FreeCAD.ActiveDocument.Clapperboard
        CL.Cam_3OnRec = False

def getMovieCameraMobile():

    global MC
    
    # Getting camera node
    cameraNode = Gui.ActiveDocument.ActiveView.getCameraNode()
    
    # Camera node follows route  
    if MC.Cam_Route == True:
        if not MC.Cam_Route_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select '
                                                   'a route in Cam_Route_Selection') + '\n')
            MC.Cam_4OnAnim = False
            return
  
        route = MC.Cam_Route_Selection.Shape.Edges[0]
        stepLength = route.Length/MC.Anim_1TotalSteps
        currentStep = stepLength*MC.Anim_4CurrentStep      
        currentPos = route.getParameterByLength(currentStep)
        currentVector = route.valueAt(currentPos)                  
        cameraNode.position.setValue(currentVector)

        # Target follows the route
        if MC.Cam_Target == 'Follow a route':     	
        	
            lengthTarget  = currentStep + stepLength*MC.Cam_Target_Steps_Forward
            posTarget = route.getParameterByLength(lengthTarget)
            vectorTarget = route.valueAt(posTarget)
            cameraTarget = (vectorTarget)
            cameraNode.pointAt(coin.SbVec3f(cameraTarget), coin.SbVec3f( 0, 0, 1 ) )

    # Camera node for Pos AB        
    else:
        
        xPosCamera = MC.Cam_01XPosA
        yPosCamera = MC.Cam_02YPosA
        zPosCamera = MC.Cam_03ZPosA
        
        if MC.Cam_XMov == True:
            xPosCameraInc = (MC.Cam_04XPosB - MC.Cam_01XPosA)/MC.Anim_1TotalSteps 
            xPosCamera = MC.Cam_01XPosA + xPosCameraInc*MC.Anim_4CurrentStep
        if MC.Cam_YMov == True:
            yPosCameraInc = (MC.Cam_05YPosB - MC.Cam_02YPosA)/MC.Anim_1TotalSteps 
            yPosCamera = MC.Cam_02YPosA + yPosCameraInc*MC.Anim_4CurrentStep
        if MC.Cam_ZMov == True:
            zPosCameraInc = (MC.Cam_06ZPosB - MC.Cam_03ZPosA)/MC.Anim_1TotalSteps 
            zPosCamera = MC.Cam_03ZPosA + zPosCameraInc*MC.Anim_4CurrentStep

        cameraNode.position.setValue(xPosCamera, yPosCamera, zPosCamera)
        
    # Camera Pos AB yaw, pitch and roll
    if MC.Cam_Target == 'Free':

        cameraYaw = MC.Cam_01YawPosA
        cameraPitch = MC.Cam_02PitchPosA
        cameraRoll = MC.Cam_03RollPosA

        if MC.Cam_01Yaw == True:          
            yawInc = (MC.Cam_04YawPosB - MC.Cam_01YawPosA)/MC.Anim_1TotalSteps
            cameraYaw = MC.Cam_01YawPosA + yawInc*MC.Anim_4CurrentStep          

        if MC.Cam_02Pitch == True:
            pitchInc = (MC.Cam_05PitchPosB - MC.Cam_02PitchPosA)/MC.Anim_1TotalSteps
            cameraPitch = MC.Cam_02PitchPosA + pitchInc*MC.Anim_4CurrentStep

        if MC.Cam_03Roll == True:
            rollInc = (MC.Cam_06RollPosB - MC.Cam_03RollPosA)/MC.Anim_1TotalSteps
            cameraRoll = MC.Cam_03RollPosA + rollInc*MC.Anim_4CurrentStep

        rotNode = FreeCAD.Rotation(*cameraNode.orientation.getValue().getValue())
        rotNode.setYawPitchRoll(cameraYaw, cameraPitch, cameraRoll)
        cameraNode.orientation.setValue(rotNode.Q)
    
    # Camera Pos AB zoom   
    if MC.Cam_04Zoom == True:
        zoomCameraInc = (MC.Cam_03ZoomPosB - MC.Cam_02ZoomPosA)/MC.Anim_1TotalSteps
        cameraHeightAngle = MC.Cam_02ZoomPosA + zoomCameraInc*MC.Anim_4CurrentStep
        cameraNode.heightAngle.setValue(radians(float(cameraHeightAngle)))

    # Object or point target
    if MC.Cam_Target == 'Follow an object or point':
        if not MC.Cam_Target_Object_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select an '
                                                   'object or point in Cam_Target_Object_Selection') + '\n')
            MC.Cam_4OnAnim = False            
            return
            
        cameraFixedTarget = MC.Cam_Target_Object_Selection.Placement.Base
        cameraNode.pointAt( coin.SbVec3f(cameraFixedTarget), coin.SbVec3f( 0, 0, 1 ) )
            
    #  Render camera
    if MC.Cam_1Type == 'Render':
        if not MC.Cam_2Render_Selection:
            FreeCAD.Console.PrintMessage(translate('Movie', 'You have to select '
                                                   'a render camera in Cam_2Render_Selection') + '\n')
            MC.Cam_4OnAnim = False
            return
            
        renderCamera = MC.Cam_2Render_Selection   
        renderCamera.ViewObject.Proxy.set_camera_from_gui()

        if MC.Cam_Route == True:
            renderCamera.AspectRatio = 1.77 # resolution 1920/1080
            renderCamera.ViewportMapping = "CROP_VIEWPORT_FILL_FRAME"

        renderCamera.ViewObject.Proxy.set_gui_from_camera()

def postMovieAnimation():

    global MC
    
    if MC.Cam_Target == 'Follow a route':
        if MC.Anim_3EndStep - (MC.Anim_4CurrentStep + MC.Cam_Target_Steps_Forward) > 0:
            MC.Anim_4CurrentStep += 1
        else:
            return
            
    else:
        if MC.Anim_3EndStep - MC.Anim_4CurrentStep > 0:
            MC.Anim_4CurrentStep += 1
        else:
            return

    Gui.runCommand('Std_PerspectiveCamera',1)  
    getMovieCameraMobile()
    Gui.updateGui()        
   
def getEndMovieCamera():

    global MC
    global CAMERAS
    global STEP_POS
    global N

    if MC.Cam_Target == 'Follow a route':
        if MC.Anim_3EndStep - (MC.Anim_4CurrentStep + MC.Cam_Target_Steps_Forward) > 0:
            MC.Anim_4CurrentStep = MC.Anim_3EndStep - MC.Cam_Target_Steps_Forward
            
        else: 
            if N < (len(CAMERAS)- 1):
                N += 1
                MC = CAMERAS[N]
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(MC)
                MC.Cam_4OnAnim = False
                STEP_POS = 'I'
            else:
                return
    else:
        if MC.Anim_3EndStep - MC.Anim_4CurrentStep > 0:
            MC.Anim_4CurrentStep = MC.Anim_3EndStep

        else:
            if N < (len(CAMERAS)- 1):
                N += 1
                MC = CAMERAS[N]
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(MC)
                MC.Cam_4OnAnim = False
                STEP_POS = 'I'
            else:
                return

    Gui.runCommand('Std_PerspectiveCamera',1)  
    getMovieCameraMobile()
    Gui.updateGui()

# ======================================================================================

# 3. Commands

if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateMovieCamera', CreateMovieCamera())
    FreeCAD.Gui.addCommand('EnableMovieCamera', EnableMovieCamera())
    FreeCAD.Gui.addCommand('SetMovieCameraPosA', SetMovieCameraPosA())
    FreeCAD.Gui.addCommand('SetMovieCameraPosB', SetMovieCameraPosB())
    FreeCAD.Gui.addCommand('IniMovieAnimation', IniMovieAnimation())
    FreeCAD.Gui.addCommand('PrevMovieAnimation', PrevMovieAnimation())
    FreeCAD.Gui.addCommand('PauseMovieAnimation', PauseMovieAnimation())
    FreeCAD.Gui.addCommand('PlayMovieAnimation', PlayMovieAnimation())
    FreeCAD.Gui.addCommand('PostMovieAnimation', PostMovieAnimation())
    FreeCAD.Gui.addCommand('EndMovieAnimation', EndMovieAnimation())

# ======================================================================================
