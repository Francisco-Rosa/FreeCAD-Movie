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

"""Creates a animation of cameras to play in FreeCAD."""

import FreeCAD
import FreeCADGui as Gui
from pivy import coin
import os
import time
from math import degrees, radians
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieConnection as co
import MovieAnimation as ma

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Global

MC = None

#VIEW_00 = translate("MovieCamera", "3D view")
#VIEW_01 = translate("MovieCamera", "Render")

# ======================================================================================
# 1. Classes

class MovieCamera:

    '''Class to create a camera to be animated'''

    def __init__(self,obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self,obj):

        """Gives the object properties to MovieCamera."""

        pl = obj.PropertiesList

        # Movie Camera 1 - Animation config
        if not 'Cam_01AnimIniStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_01AnimIniStep', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Initial step of the MovieCamera animation.\n'
                                                    '\n'
                                                    'Indicate the step which this section of \n'
                                                    'the animation will begin.')
                                                    ).Cam_01AnimIniStep = 1
        if not 'Cam_02AnimCurrentStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_02AnimCurrentStep', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Current step of the MovieCamera animation.\n'
                                                    '\n'
                                                    'It is only indicative.')
                                                    ).Cam_02AnimCurrentStep = 1
        if not 'Cam_03AnimEndStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_03AnimEndStep', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'End step of the MovieCamera animation.\n'
                                                    '\n'
                                                    'Indicate the step which this section of \n'
                                                    'the animation will finish. \n'
                                                    '\n'
                                                    'Changes will only take effect after \n'
                                                    'MovieCamera has been re-enabled.')
                                                    ).Cam_03AnimEndStep = 100
        if not 'Cam_04AnimTotalSteps' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_04AnimTotalSteps', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Total steps of the MovieCamera animation.\n'
                                                    '\n'
                                                    'It is the result of the difference between \n'
                                                    'end step (“Cam_03AnimEndStep”) and initial \n'
                                                    'step (“Cam_01AnimIniStep”).')
                                                    ).Cam_04AnimTotalSteps = 100
        if not 'Cam_05AnimFps' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_05AnimFps', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Animation fps of the MovieCamera.\n'
                                                    '\n'
                                                    'Specify the value for this animation \n'
                                                    'section.\n'
                                                    'It is a simulation and will depend on \n'
                                                    'the computer performance. \n'
                                                    '\n'
                                                    'Changes will only take effect after \n'
                                                    'MovieCamera has been re-enabled.')
                                                    ).Cam_05AnimFps = 30
        if not 'Cam_06AnimTime' in pl:
            obj.addProperty('App::PropertyString', 'Cam_06AnimTime', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Animation time of the MovieCamera, \n'
                                                    'in hours, minutes, and seconds. \n'
                                                    '\n'
                                                    'It is only indicative.')
                                                    ).Cam_06AnimTime = time.strftime('%H:%M:%S', time.gmtime(3.33))
        if not 'Cam_07OnAnim' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_07OnAnim', 'Movie Camera 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'MovieCamera animation on or off. \n'
                                                    '\n'
                                                    'It should not be changed manually, \n'
                                                    'it is controlled by the animation \n'
                                                    'buttons.')
                                                    ).Cam_07OnAnim = False
        # Movie Camera 02 - Camera config
        if not 'Cam_01Type' in pl:
            from MovieAnimation import VIEW_00, VIEW_01
            obj.addProperty('App::PropertyEnumeration', 'Cam_01Type', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Camera type for the MovieCamera.\n'
                                                    '\n'
                                                    'Choose the camera through which this section \n'
                                                    'of the animation will be performed: “3D view” \n'
                                                    'for 3D views and the “Render” for adopting \n'
                                                    'the settings of a camera from the Render \n'
                                                    'Workbench, previously created and adjusted.')
                                                    ).Cam_01Type = (f"00 - {VIEW_00}",
                                                                    f"01 - {VIEW_01}")
        if not 'Cam_02Render_Selection' in pl:
            obj.addProperty('App::PropertyLink', 'Cam_02Render_Selection', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Render camera selection for the MovieCamera animation.\n'
                                                    '\n'
                                                    'If you have chosen “Render” in Camera type (“Cam_01Type”), \n'
                                                    'you have to select which one will be used in this \n'
                                                    'section of the animation.')
                                                    ).Cam_02Render_Selection = None
        if not 'Cam_03RenderWidth' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_03RenderWidth', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Render image width of the MovieCamera animation.\n'
                                                    '\n'
                                                    'Configure the width in pixels that will compose \n'
                                                    'the aspect ratio of the image (“AspectRatio”).')
                                                    ).Cam_03RenderWidth = 800
        if not 'Cam_04RenderHeight' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_04RenderHeight', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Render image height of the MovieCamera animation.\n'
                                                    '\n'
                                                    'Configure the height in pixels that will compose \n'
                                                    'the aspect ratio of the image (“AspectRatio”).')
                                                    ).Cam_04RenderHeight = 600
        if not 'Cam_05ObjectsSelected' in pl:
            obj.addProperty('App::PropertyLinkList', 'Cam_05ObjectsSelected', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Objects selected for the MovieCamera animation.\n'
                                                    '\n'
                                                    'Select the MoveObjects to animate together \n'
                                                    'with this MovieCamera.')
                                                    ).Cam_05ObjectsSelected = None
        if not 'Cam_06Enable' in pl:
            obj.addProperty('App::PropertyEnumeration', 'Cam_06Enable', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Enable the combinations for the MovieCamera animation.\n'
                                                    '\n'
                                                    'Configure the combination of objects to animate together: \n'
                                                    'only MovieCamera (“Camera”), MovieCamera and MovieObjects \n'
                                                    '(“Camera and objects”), MovieCamera and connection \n'
                                                    '(“Camera and connection”), or even just the MovieObjects \n'
                                                    '(“Objects”) or connection (“Connection”) associated with \n'
                                                    'this MovieCamera.\n'
                                                    '\n'
                                                    'For each combination change it will be necessary to \n'
                                                    're-enable the MovieCamera.')
                                                    ).Cam_06Enable = ('00 - ' + translate("MovieCamera", "Camera"),
                                                                      '01 - ' + translate("MovieCamera", "Camera and objects"),
                                                                      '02 - ' + translate("MovieCamera", "Objects"),
                                                                      '03 - ' + translate("MovieCamera", "Camera and connection"),
                                                                      '04 - ' + translate("MovieCamera", "Connection"))
        if not 'Cam_07Connection' in pl:
            obj.addProperty('App::PropertyEnumeration', 'Cam_07Connection', 'Movie Camera 02 - Camera config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Connection for MovieCamera animation. \n'
                                                    '\n'
                                                    'Choose the workbench through which the \n'
                                                    'animation will be performed together, if so.\n'
                                                    '\n'
                                                    'Make sure the workbench is installed and \n'
                                                    'that there is an animation created with it.'
                                                    )).Cam_07Connection = list(co.connections)

        # Movie Camera 03 - Target config
        if not 'Cam_01Target' in pl:
            obj.addProperty('App::PropertyEnumeration', 'Cam_01Target', 'Movie Camera 03 - Target config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Target of the MovieCamera. \n'
                                                    '\n'
                                                    'If you want to use an object or point as a target, \n'
                                                    'choose “Follow an object or point” and select one of \n'
                                                    'them in target object selection (“Cam_02Target_ObjectSelection”), \n'
                                                    'while for the “Follow a route” option you must use route \n'
                                                    'selection (“Cam_02RouteSelection”).')
                                                    ).Cam_01Target = ('00 - ' + translate("MovieCamera", "Free"),
                                                                      '01 - ' + translate('MovieCamera', 'Follow an object or point'),
                                                                      '02 - ' + translate("MovieCamera", "Follow a route"))
        if not 'Cam_02TargetObjectSelection' in pl:
            obj.addProperty('App::PropertyLink', 'Cam_02TargetObjectSelection', 'Movie Camera 03 - Target config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Target object selection of the MovieCamera.\n'
                                                    '\n'
                                                    'Select the point or object you want the \n'
                                                    'camera to point to.')
                                                    ).Cam_02TargetObjectSelection = None
        if not 'Cam_03TargetStepsForward' in pl:
            obj.addProperty('App::PropertyInteger', 'Cam_03TargetStepsForward', 'Movie Camera 03 - Target config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Target ahead of the MovieCamera.\n'
                                                    '\n'
                                                    'If you chose for the target to \n'
                                                    '“follow a route”, in “Cam_01Target”, \n'
                                                    'you need to specify how many steps \n'
                                                    'this target will be ahead of the \n'
                                                    'camera on the same route.')
                                                    ).Cam_03TargetStepsForward = 10

        # Movie Camera 04 - Camera follows a path
        if not 'Cam_01Route' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_01Route', 'Movie Camera 04 - Camera follows a path',
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route of the MovieCamera animation.\n'
                                                    '\n'
                                                    'Enable it so that the camera follows a route. \n'
                                                    'You have to select a single segment on route \n'
                                                    'selection (“Cam_02RouteSelection”) \n'
                                                    'to use it.')
                                                    ).Cam_01Route = False
        if not 'Cam_02RouteSelection' in pl:
            obj.addProperty('App::PropertyLink', 'Cam_02RouteSelection', 'Movie Camera 04 - Camera follows a path',
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route selection for the MovieCamera animation.\n'
                                                    '\n'
                                                    'Choose the route through which the camera will be \n'
                                                    'animate. You have to select a single segment such \n'
                                                    'as: line, arc, circle, ellipse, B-spline or Bézier \n'
                                                    'curve, from Sketcher or Draft Workbenches.')
                                                    ).Cam_02RouteSelection = None

        # Movie Camera 05 - Camera Pos A-B - pos On/Off
        if not 'Cam_01XMov' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_01XMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'X movement of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera in X direction.'
                                                    )).Cam_01XMov = False
        if not 'Cam_02YMov' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_02YMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Y movement of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera in Y direction.')
                                                    ).Cam_02YMov = False
        if not 'Cam_03ZMov' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_03ZMov', 'Movie Camera 05 - Camera Pos A-B - pos On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Z movement of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera in Z direction.')
                                                    ).Cam_03ZMov = False

        # Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off
        if not 'Cam_01Yaw' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_01Yaw', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Yaw of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera horizontal angle.')
                                                    ).Cam_01Yaw = False
        if not 'Cam_02Pitch' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_02Pitch', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Pitch of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera vertical angle.')
                                                    ).Cam_02Pitch = False
        if not 'Cam_03Roll' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_03Roll', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Roll of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera roll angle.')
                                                    ).Cam_03Roll = False
        if not 'Cam_04Zoom' in pl:
            obj.addProperty('App::PropertyBool', 'Cam_04Zoom', 'Movie Camera 06 - Camera Pos A-B - angles, zoom - On/Off',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Zoom of the MovieCamera.\n'
                                                    '\n'
                                                    'Enable this if you want to \n'
                                                    'animate the camera zoom.')
                                                    ).Cam_04Zoom = False

        # Movie Camera 07 - Camera Pos A
        if not 'Cam_01XPosA' in pl:
            obj.addProperty('App::PropertyFloat', 'Cam_01XPosA', 'Movie Camera 07 - Camera Pos A',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'X of Position A of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position \n'
                                                    'A” button is pressed, after that, \n'
                                                    'if necessary, you can make adjustments \n'
                                                    'to the x-value.')
                                                    ).Cam_01XPosA = 0
        if not 'Cam_02YPosA' in pl:
            obj.addProperty('App::PropertyFloat', 'Cam_02YPosA', 'Movie Camera 07 - Camera Pos A',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Y of Position A of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position \n'
                                                    'A” button is pressed, after that, \n'
                                                    'if necessary, you can make adjustments \n'
                                                    'to the y-value.')
                                                    ).Cam_02YPosA = 0
        if not 'Cam_03ZPosA' in pl:
            obj.addProperty('App::PropertyFloat', 'Cam_03ZPosA', 'Movie Camera 07 - Camera Pos A',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                     'Z of Position A of the MovieCamera.\n'
                                                     '\n'
                                                     'It is set when the “Set position A” button \n'
                                                     'is pressed, after that, if necessary, \n'
                                                     'you can make adjustments to the z-value.')
                                                     ).Cam_03ZPosA = 0
        if not 'Cam_04XPosB' in pl:
            obj.addProperty('App::PropertyFloat', 'Cam_04XPosB', 'Movie Camera 08 - Camera Pos B',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'X of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position B” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make adjustments to the x-value.')
                                                    ).Cam_04XPosB = 1000.0
        if not 'Cam_05YPosB' in pl:
            obj.addProperty('App::PropertyFloat', 'Cam_05YPosB', 'Movie Camera 08 - Camera Pos B',
                                                   QT_TRANSLATE_NOOP('App::Property',
                                                    'Y of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position B” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make adjustments to the y-value.')
                                                    ).Cam_05YPosB = 1000.0
        if not 'Cam_06ZPosB' in pl:
            obj.addProperty('App::PropertyFloat', 'Cam_06ZPosB', 'Movie Camera 08 - Camera Pos B',
                                                   QT_TRANSLATE_NOOP('App::Property',
                                                    'Z of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position B” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make adjustments to the z-value.')
                                                    ).Cam_06ZPosB = 1000.0

        # Movie Camera 08 - Camera Pos B
        if not 'Cam_01YawPosA' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_01YawPosA', 'Movie Camera 09 - Camera Rot A',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Yaw of Position A of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position A” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make little adjustments to the \n'
                                                    'horizontal angle value of the camera.')
                                                    ).Cam_01YawPosA = 0
        if not 'Cam_02PitchPosA' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_02PitchPosA', 'Movie Camera 09 - Camera Rot A',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Pitch of Position A of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position A” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make little adjustments to the \n'
                                                    'vertical angle value of the camera.')
                                                    ).Cam_02PitchPosA = 0
        if not 'Cam_03RollPosA' in pl:
           obj.addProperty('App::PropertyAngle', 'Cam_03RollPosA', 'Movie Camera 09 - Camera Rot A',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Roll of Position A of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position A” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make little adjustments to the \n'
                                                    'roll value of the camera.')
                                                    ).Cam_03RollPosA = 90
        if not 'Cam_04YawPosB' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_04YawPosB', 'Movie Camera 10 - Camera Rot B',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Yaw of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position B” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make little adjustments to the \n'
                                                    'horizontal angle value of the camera.')
                                                    ).Cam_04YawPosB = 30
        if not 'Cam_05PitchPosB' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_05PitchPosB', 'Movie Camera 10 - Camera Rot B',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Pitch of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position B” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make little adjustments to the \n'
                                                    'vertical angle value of the camera.')
                                                    ).Cam_05PitchPosB = 45
        if not 'Cam_06RollPosB' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_06RollPosB', 'Movie Camera 10 - Camera Rot B',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Roll of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'It is set when the “Set position B” button \n'
                                                    'is pressed, after that, if necessary, \n'
                                                    'you can make little adjustments to the \n'
                                                    'roll value of the camera.')
                                                    ).Cam_06RollPosB = 45

        # Movie Camera 09 - Camera Pos A-B - Zoom
        if not 'Cam_02ZoomPosA' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_02ZoomPosA', 'Movie Camera 11 - Camera Zoom A-B',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Zoom of Position A of the MovieCamera.\n'
                                                    '\n'
                                                    'If Zoom of the MovieCamera (“Cam_04Zoom”) \n'
                                                    'is enabled and after the Set position A button \n'
                                                    'is pressed, you can adjust the angle in degrees \n'
                                                    'you want to start the camera animation. \n'
                                                    '\n'
                                                    'Decreasing the value to zoom in and increasing \n'
                                                    'to zoom out.')
                                                    ).Cam_02ZoomPosA = 50
        if not 'Cam_03ZoomPosB' in pl:
            obj.addProperty('App::PropertyAngle', 'Cam_03ZoomPosB', 'Movie Camera 11 - Camera Zoom A-B',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Zoom of Position B of the MovieCamera.\n'
                                                    '\n'
                                                    'If Zoom of the MovieCamera (“Cam_04Zoom”) \n'
                                                    'is enabled and after the Set position B button \n'
                                                    'is pressed, you can adjust the angle in degrees \n'
                                                    'you want to finish the camera animation. \n'
                                                    '\n'
                                                    'Decreasing the value to zoom in and increasing \n'
                                                    'to zoom out.')
                                                    ).Cam_03ZoomPosB = 20

class MovieCameraViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/MovieCameraIcon.svg'

# ======================================================================================    
# 2. Command classes

class CreateMovieCamera:

    """Creates a MovieCamera."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateMovieCameraIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateMovieCamera',
                                              'MovieCamera'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateMovieCamera',
                                              'Creates a MovieCamera. \n'
                                              '\n'
                                              '1. Initially, a static camera is created (its positions \n'
                                              'A and B are identical). You can use it to control the \n'
                                              'display of object animations.\n'
                                              '\n'
                                              '2. To animate an isolated camera that move e/or rotates \n'
                                              'establish its B position, since A has already been \n'
                                              'established(see the positions A and B instructions).\n'
                                              '\n'
                                              '3. There are two ways to create a walkthrough:\n'
                                              '\n'
                                              'Using a path. Enable “Cam_01Route” in the \n'
                                              'properties window and specify an previous line \n'
                                              'or continuous curves under “Cam_02_Route Selection”.\n'
                                              '\n'
                                              'Using a sequence of cameras. Go to point B of the \n'
                                              'first created MovieCamera, then select it and click \n'
                                              'this button. Repeat this process until the last camera, \n'
                                              'then set point B for this one.\n'
                                              '\n'
                                              '4. If you want the camera to point at an object, \n'
                                              'select “Follow an object or point” under \n'
                                              '“Cam_01_Target” and specify the object in \n'
                                              '“Cam_02_Target Object Selection”.\n'
                                              '\n'
                                              '5. Make finer adjustments in the properties window, \n'
                                              'if necessary.\n'
                                              '\n'
                                              '6. To view the animation, select (sequentially) one \n'
                                              'or more created MovieCameras and click the “Enable an \n'
                                              'object for animation” button. Control the animation \n'
                                              'using the “Animation tools” buttons.\n'
                                              '\n'
                                              '7. To save a video from the animation, indicate the \n'
                                              'MovieCameras on a Clapperboard, to do so, see the \n'
                                              'corresponding instructions.'
                                              )}

    def IsActive(self):
        if Gui.ActiveDocument:
            selection = []
            selection = Gui.Selection.getSelection()
            if not selection:
                return True
            if any(condition for condition in [selection[0].Name[0:11] == 'MovieCamera',
                                               selection[0].Name[0:12] == 'MovieObjects'
                                               ]):
                return True
            else:
                return False
        else:
            return False

    def Activated(self):
        global MC
        doc = FreeCAD.ActiveDocument
        #Create a new MovieCamera from a existing one
        selection = []
        selection = Gui.Selection.getSelection()
        if not selection:
            ActivatedMovieCamera(self)
            # Provisional AB Positions
            setMCPosA(Option = MC)
            setMCPosB(Option = MC)
            FreeCAD.Console.PrintMessage(
                            translate('MovieObjects',
                            'A static MovieCamera was created!\n'
                            'To animate the MovieCamera without a MovieObjects\n'
                            'it is necessary to reset the MovieCamera B \n'
                            'position or enable “CAm_01Route” and \n'
                            'indicate a path at “Cam_02RouteSelection”!'
                            ) + '\n')
        else:
            if selection[0].Name[0:11] == 'MovieCamera':
                oldMC = selection[0]
                seq_label = translate('MovieCamera', 'MovieCamera #')
                oldMC.Label = seq_label
                # Makes a copy of last MovieCamera
                MC = doc.copyObject(oldMC)
                # PosA = PosB
                setMCPosA(Option = MC)
                setMCPosB(Option = MC)
                MC.Label = seq_label
                FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                       'A sequenced MovieCamera was created!'
                                                       ) + '\n')
                pass
            else:
                FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                       'To create a sequenced MovieCameras, \n'
                                                       'select the last MovieCamera inserted!'
                                                       ) + '\n')
                return
        MC.Cam_07OnAnim = False
        doc.recompute()

def ActivatedMovieCamera(self):
    global MC
    default_label = translate('MovieCamera',
                              'MovieCamera')
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython',
                                              'MovieCamera')
    MovieCamera(folder)
    MovieCameraViewProvider(folder.ViewObject)
    MC = None
    MC = folder
    MC.Label = default_label
    FreeCAD.ActiveDocument.recompute()

# ======================================================================================

# 3. Functions

def enableCameraSelection(Enable = None):

    """Enables MovieCamera selected"""

    global MC
    MC = Enable

def setMCPosA(Option = None):

    """Sets the A position for a MovieCamera."""

    MC = Option
    Gui.runCommand('Std_PerspectiveCamera',1)

    #if MC.Cam_01Target == 'Free':
    if MC.Cam_01Target[0:2] == '00': # 'Free'
        MC.Cam_01XMov = True
        MC.Cam_02YMov = True
        MC.Cam_03ZMov = True
        MC.Cam_01Yaw = True
        MC.Cam_02Pitch = True
        MC.Cam_03Roll = True
        MC.Cam_04Zoom = True

    #if MC.Cam_01Target == 'Follow an object or point' :
    if MC.Cam_01Target[0:2] == '01': # 'Follow an object or point'
        MC.Cam_01XMov = True
        MC.Cam_02YMov = True
        MC.Cam_03ZMov = True
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
    #if MC.Cam_01Type == 'Render':
    if MC.Cam_01Type[0:2] == '01': # Render
        if 'Camera' in FreeCAD.ActiveDocument.Content and MC.Cam_02Render_Selection:
            renderCameraA = MC.Cam_02Render_Selection
            renderCameraA.ViewObject.Proxy.set_camera_from_gui()
            renderCameraA.AspectRatio = MC.Cam_03RenderWidth/MC.Cam_04RenderHeight
            renderCameraA.ViewportMapping = 'CROP_VIEWPORT_FILL_FRAME'
            renderCameraA.ViewObject.Proxy.set_gui_from_camera()
        else:
            FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                   'You have to select a render '
                                                   'camera in “Cam_02Render_Selection”!'
                                                   ) + '\n')
            return

    ma.modifyAnimationIndicator(animation = False, obj = MC)
    MC.Cam_02AnimCurrentStep = 0
    FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                           'MovieCamera position A has been established.'
                                           ) + '\n')
    Gui.updateGui()

def setMCPosB(Option = None):

    """Sets the B position for a MovieCamera."""

    MC = Option
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
    #if MC.Cam_01Type == 'Render':
    if MC.Cam_01Type[0:2] == '01': # Render
        if 'Camera' in FreeCAD.ActiveDocument.Content and MC.Cam_02Render_Selection:
            renderCameraB = MC.Cam_02Render_Selection
            renderCameraB.ViewObject.Proxy.set_camera_from_gui()
            renderCameraB.AspectRatio = MC.Cam_03RenderWidth/MC.Cam_04RenderHeight
            renderCameraB.ViewportMapping = 'CROP_VIEWPORT_FILL_FRAME'
            renderCameraB.ViewObject.Proxy.set_gui_from_camera()
        else:
            FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                   'You have to select a render '
                                                   'camera in “Cam_02Render_Selection”!'
                                                   ) + '\n')
            return

    ma.modifyAnimationIndicator(animation = False, obj = MC)
    MC.Cam_02AnimCurrentStep = MC.Cam_04AnimTotalSteps
    FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                           'MovieCamera position B has been established.'
                                           ) + '\n')
    Gui.updateGui()

# ======================================================================================

def getMovieCameraMobile(Selection = None):

    """Gets the positions of a MovieCamera."""

    MC = Selection
    # Getting camera node
    cameraNode = Gui.ActiveDocument.ActiveView.getCameraNode()

    # Camera node follows route
    if MC.Cam_01Route == True:
        if not MC.Cam_02RouteSelection:
            FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                   'You have to select '
                                                   'a route in “Cam_02RouteSelection”!'
                                                   ) + '\n')
            ma.modifyAnimationIndicator(animation = False, obj = MC)
            return

        route = MC.Cam_02RouteSelection.Shape.Edges[0]
        stepLength = route.Length/MC.Cam_04AnimTotalSteps
        currentStep = stepLength*MC.Cam_02AnimCurrentStep
        if currentStep > route.Length:
            currentStep = route.Length
        currentPos = route.getParameterByLength(currentStep)
        currentVector = route.valueAt(currentPos)
        cameraNode.position.setValue(currentVector)

        # Target follows the route
        #if MC.Cam_01Target == 'Follow a route':
        if MC.Cam_01Target[0:2] == '02': # 'Follow a route'

            lengthTarget  = currentStep + stepLength*MC.Cam_03TargetStepsForward
            posTarget = route.getParameterByLength(lengthTarget)
            vectorTarget = route.valueAt(posTarget)
            cameraTarget = (vectorTarget)
            cameraNode.pointAt(coin.SbVec3f(cameraTarget),
                               coin.SbVec3f( 0, 0, 1 ) )

    # Camera node for Pos AB
    else:
        xPosCamera = MC.Cam_01XPosA
        yPosCamera = MC.Cam_02YPosA
        zPosCamera = MC.Cam_03ZPosA

        if MC.Cam_01XMov == True:
            xPosCameraInc = (MC.Cam_04XPosB - MC.Cam_01XPosA)/MC.Cam_04AnimTotalSteps
            xPosCamera = MC.Cam_01XPosA + xPosCameraInc*MC.Cam_02AnimCurrentStep
        if MC.Cam_02YMov == True:
            yPosCameraInc = (MC.Cam_05YPosB - MC.Cam_02YPosA)/MC.Cam_04AnimTotalSteps
            yPosCamera = MC.Cam_02YPosA + yPosCameraInc*MC.Cam_02AnimCurrentStep
        if MC.Cam_03ZMov == True:
            zPosCameraInc = (MC.Cam_06ZPosB - MC.Cam_03ZPosA)/MC.Cam_04AnimTotalSteps
            zPosCamera = MC.Cam_03ZPosA + zPosCameraInc*MC.Cam_02AnimCurrentStep

        cameraNode.position.setValue(xPosCamera, yPosCamera, zPosCamera)

    # Camera yaw, pitch and roll for Pos AB 
    #if MC.Cam_01Target == 'Free':
    if MC.Cam_01Target[0:2] == '00': # 'Free'
        cameraYaw = MC.Cam_01YawPosA
        cameraPitch = MC.Cam_02PitchPosA
        cameraRoll = MC.Cam_03RollPosA

        if MC.Cam_01Yaw == True:
            yawInc = (MC.Cam_04YawPosB - MC.Cam_01YawPosA)/MC.Cam_04AnimTotalSteps
            cameraYaw = MC.Cam_01YawPosA + yawInc*MC.Cam_02AnimCurrentStep

        if MC.Cam_02Pitch == True:
            pitchInc = (MC.Cam_05PitchPosB - MC.Cam_02PitchPosA)/MC.Cam_04AnimTotalSteps
            cameraPitch = MC.Cam_02PitchPosA + pitchInc*MC.Cam_02AnimCurrentStep

        if MC.Cam_03Roll == True:
            rollInc = (MC.Cam_06RollPosB - MC.Cam_03RollPosA)/MC.Cam_04AnimTotalSteps
            cameraRoll = MC.Cam_03RollPosA + rollInc*MC.Cam_02AnimCurrentStep

        rotNode = FreeCAD.Rotation(*cameraNode.orientation.getValue().getValue())
        rotNode.setYawPitchRoll(cameraYaw, cameraPitch, cameraRoll)
        cameraNode.orientation.setValue(rotNode.Q)

    # Camera Pos AB zoom
    if MC.Cam_04Zoom == True:
        zoomCameraInc = (MC.Cam_03ZoomPosB - MC.Cam_02ZoomPosA)/MC.Cam_04AnimTotalSteps
        cameraHeightAngle = MC.Cam_02ZoomPosA + zoomCameraInc*MC.Cam_02AnimCurrentStep
        cameraNode.heightAngle.setValue(radians(float(cameraHeightAngle)))

    # Object or point target
    #if MC.Cam_01Target == 'Follow an object or point':
    if MC.Cam_01Target[0:2] == '01': # 'Follow an object or point'
        if not MC.Cam_02TargetObjectSelection:
            FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                   'You have to select an object or \n'
                                                   'point in “Cam_02TargetObjectSelection”!'
                                                   ) + '\n')
            ma.modifyAnimationIndicator(animation = False, obj = MC)
            return

        cameraFixedTarget = MC.Cam_02TargetObjectSelection.Placement.Base
        cameraNode.pointAt( coin.SbVec3f(cameraFixedTarget), coin.SbVec3f( 0, 0, 1 ) )

    #  Render camera
    #if MC.Cam_01Type == 'Render':
    if MC.Cam_01Type[0:2] == '01': # Render
        if not MC.Cam_02Render_Selection:
            FreeCAD.Console.PrintMessage(translate('MovieCamera',
                                                   'You have to select a render \n'
                                                   'camera in “Cam_02Render_Selection”!'
                                                   ) + '\n')
            ma.modifyAnimationIndicator(animation = False, obj = MC)
            return

        renderCamera = MC.Cam_02Render_Selection
        renderCamera.ViewObject.Proxy.set_camera_from_gui()

        if MC.Cam_01Route == True:
            renderCamera.AspectRatio = MC.Cam_03RenderWidth/MC.Cam_04RenderHeight
            renderCamera.ViewportMapping = 'CROP_VIEWPORT_FILL_FRAME'

        renderCamera.ViewObject.Proxy.set_gui_from_camera()

# ======================================================================================

# 3. Commands

if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateMovieCamera', CreateMovieCamera())

# ======================================================================================
