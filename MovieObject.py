''' Movie Workbench, Movie Object animation module '''

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

"""Creates a animation of objects to play in FreeCAD."""

import FreeCAD
import FreeCADGui as Gui
import os
import time
from PySide.QtCore import QT_TRANSLATE_NOOP
import MovieAnimation as ma

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
Gui.addLanguagePath(LanguagePath)

# ======================================================================================
# 0. Globals

MO = None
OBJ_REFRESH = False
# ======================================================================================
# 1. Classes

class MovieObjects:

    '''Class to create a group of objects to be animated'''

    def __init__(self,obj):
        obj.Proxy = self
        self.setProperties(obj)

    def setProperties(self,obj):

        """Gives the object properties to MovieObjects."""

        pl = obj.PropertiesList

        if not 'Objects' in pl:
            obj.addProperty('App::PropertyLinkList', 'Objects', 'Movie Objects',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'List of objects of this MovieObjects.'
                                                    )).Objects = []
        if not 'Names' in pl:
            obj.addProperty('App::PropertyPythonObject', 'Names').Names = []
        if not 'CenterGravityA' in pl:
            obj.addProperty('App::PropertyPythonObject', 'CenterGravityA').CenterGravityA = {}
        if not 'CenterGravityB' in pl:
            obj.addProperty('App::PropertyPythonObject', 'CenterGravityB').CenterGravityB = {}
        if not 'Pos0' in pl:
            obj.addProperty('App::PropertyPythonObject', 'Pos0').Pos0 = {} # Placement0
        if not 'PosA' in pl:
            obj.addProperty('App::PropertyPythonObject', 'PosA').PosA = {} # PlacementA
        if not 'PosB' in pl:
            obj.addProperty('App::PropertyPythonObject', 'PosB').PosB = {} # PlacementB
        if not 'ObjectAxis' in pl:
            obj.addProperty('App::PropertyPythonObject', 'ObjectAxis').ObjectAxis = {}
        if not 'PosGCAverage0' in pl:
            obj.addProperty('App::PropertyPythonObject', 'PosGCAverage0').PosGCAverage0 = []

        # Movie Objects 01 - Animation config
        if not 'Obj_01AnimIniStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Obj_01AnimIniStep', 'Movie Objects 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Initial step of the MovieObjects animation.\n'
                                                    '\n'
                                                    'Indicate the step which this section of the \n'
                                                    'animation will begin. Changes will only take \n'
                                                    'effect after MovieObjects has been re-enabled.'
                                                    )).Obj_01AnimIniStep = 1
        if not 'Obj_02AnimCurrentStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Obj_02AnimCurrentStep', 'Movie Objects 01 - Animation config',
                                                     QT_TRANSLATE_NOOP('App::Property',
                                                    'Current step of the MovieObjects animation.\n'
                                                    '\n'
                                                    'It is only indicative.'
                                                    )).Obj_02AnimCurrentStep = 1
        if not 'Obj_03AnimEndStep' in pl:
            obj.addProperty('App::PropertyInteger', 'Obj_03AnimEndStep', 'Movie Objects 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'End step of the MovieObjects animation.\n'
                                                    '\n'
                                                    'Indicate the step which this section of \n'
                                                    'the animation will finish. Changes will \n'
                                                    'only take effect after MovieObjects has \n'
                                                    'been re-enabled.'
                                                    )).Obj_03AnimEndStep = 50
        if not 'Obj_04AnimTotalSteps' in pl:
            obj.addProperty('App::PropertyInteger', 'Obj_04AnimTotalSteps', 'Movie Objects 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Total steps of MovieObjects animation.\n'
                                                    '\n'
                                                    'It is the result of the difference \n'
                                                    'between End step (“Obj_03AnimEndStep”) \n'
                                                    'and Initial step (“Obj_01AnimIniStep”).'
                                                    )).Obj_04AnimTotalSteps = 50
        if not 'Obj_05AnimFps' in pl:
            obj.addProperty('App::PropertyInteger', 'Obj_05AnimFps', 'Movie Objects 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Animation fps of the MovieObjects.\n'
                                                    '\n'
                                                    'Indicate the fps through which the \n'
                                                    'section of the animation will be performed. \n'
                                                    'It is a simulation and will depend on the \n'
                                                    'computer performance. Changes will only take \n'
                                                    'effect after MovieObjects has been re-enabled.'
                                                    )).Obj_05AnimFps = 30
        if not 'Obj_06AnimTime' in pl:
            obj.addProperty('App::PropertyString', 'Obj_06AnimTime', 'Movie Objects 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Animation time of the MovieObjects, \n'
                                                    'in in hours, minutes, and seconds. \n'
                                                    '\n'
                                                    'It is only indicative.'
                                                    )).Obj_06AnimTime = time.strftime("%H:%M:%S", time.gmtime(1.7))
        if not 'Obj_07AnimOnAnim' in pl:
            obj.addProperty('App::PropertyBool', 'Obj_07AnimOnAnim', 'Movie Objects 01 - Animation config',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'MovieObjects animation on or off. \n'
                                                    '\n'
                                                    'It should not be changed manually, \n'
                                                    'it is controlled by the animation buttons.'
                                                    )).Obj_07AnimOnAnim = False

        # Movie Objects 02 - Objects config
        if not 'Obj_01Route' in pl:
            obj.addProperty('App::PropertyBool', 'Obj_01Route', 'Movie Objects 02 - Objects config',
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route of the MovieObjects. \n'
                                                    '\n'
                                                    'Enable this so that the objects follow a route. \n'
                                                    'You have to select a single segment on route \n'
                                                    'selection (“Obj_02RouteSelection”) to use it. \n'
                                                    'With the route activated, the coordinate \n'
                                                    'settings for points A and B will be ignored, \n'
                                                    'but not deleted. \n'
                                                    '\n'
                                                    'Disable the route and the animation of \n'
                                                    'points A and B will be activated again, \n'
                                                    'if it has already been configured before.'
                                                    )).Obj_01Route = False
        if not 'Obj_02RouteSelection' in pl:
            obj.addProperty('App::PropertyLink', 'Obj_02RouteSelection', 'Movie Objects 02 - Objects config',
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Route selection of the MovieObjects.\n'
                                                    '\n'
                                                    'Choose the route through which the \n'
                                                    'objects will be animate. You have to \n'
                                                    'select a single segment such as: line, \n'
                                                    'arc, circle, ellipse, B-spline or \n'
                                                    'Bézier curve, from Sketcher or Draft \n'
                                                    'Workbenches.'
                                                    )).Obj_02RouteSelection = None

        # Movie Objects 03 - Objects rotation
        if not 'Obj_01Rotation' in pl:
            obj.addProperty('App::PropertyBool', 'Obj_01Rotation', 'Movie Objects 03 - Objects rotation',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Rotation of the MovieObjects.\n'
                                                    '\n'
                                                    'Enable this if you want to animate \n'
                                                    'the objects angles.'
                                                    )).Obj_01Rotation = False
        if not 'Obj_02RotationCG' in pl:
            obj.addProperty('App::PropertyBool', 'Obj_02RotationCG', 'Movie Objects 03 - Objects rotation',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Rotation by the centers of gravities \n'
                                                    'of the MovieObjects.\n'
                                                    '\n'
                                                    'Enable this if you want to rotate \n'
                                                    'the objects by their centers of gravity.'
                                                    )).Obj_02RotationCG = False

        # New properties
        #def updateProps(self, obj):
        if not 'PosAList' in pl:
            obj.addProperty('App::PropertyStringList', 'PosAList', 'Movie Objects',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Placements of PosA of this MovieObjects.'
                                                    )).PosAList = [] # New
        if not 'PosBList' in pl:
            obj.addProperty('App::PropertyStringList', 'PosBList', 'Movie Objects',
                                                    QT_TRANSLATE_NOOP('App::Property',
                                                    'Placements of PosB of this MovieObjects.'
                                                    )).PosBList = [] # New
        if not 'Obj_03Refresh' in pl:
            obj.addProperty('App::PropertyBool', 'Obj_03Refresh', 'Movie Objects 02 - Objects config',
                                                    QT_TRANSLATE_NOOP('App::Property', 
                                                    'Refresh on or off.\n'
                                                    '\n'
                                                    'Enable this if you need to update \n'
                                                    'at each step of the animation. \n'
                                                    'Sometimes needed in combination \n'
                                                    'with other object animation workbenches.\n'
                                                    '\n'
                                                    'Note: This decreases the performance \n'
                                                    'of object animations.'
                                                    )).Obj_03Refresh = False

class MovieObjectsViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/MovieObjectsIcon.svg'
        '''
        from MovieAnimation import ENABLE_01
        print(f'MovieObject icon, ENABLE_01 = {ENABLE_01}')
        if ENABLE_01 == 'Objects':
            return __dir__ + '/icons/EnableMovieObjectsIcon.svg'
        else:
            return __dir__ + '/icons/MovieObjectsIcon.svg'
        '''

# ======================================================================================
# 2. Command classes

class CreateMovieObjects:

    """Creates a MovieObjects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateMovieObjects',
                                              'MovieObjects'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateMovieObjects',
                                             'Objects can be animated from position A to B, \n'
                                             'follow a route, rotate around their \n'
                                             'gravity centers or a chosen axis.\n'
                                             '\n'
                                             '1. First select a group of objects \n'
                                             'you want to animate and click here.\n'
                                             '\n'
                                             '2. To animate one or more objects \n'
                                             'together from point A to B, that move \n'
                                             'and/or rotate, establish their A and B \n'
                                             'positions (see the positions A and B \n'
                                             'instructions).\n'
                                             '\n'
                                             '3. Using a path. Enable “Obj_01Route” \n'
                                             'in the properties window and specify an \n'
                                             'previous line or continuous curves under \n'
                                             '“Obj_02_Route Selection”.\n'
                                             '\n'
                                             '4. Rotating around their gravity centers. \n'
                                             'Specify the initial (PosA) and final (Pos B) \n'
                                             'rotations and enable the “Obj_Rotation CG” property.\n'
                                             '\n'
                                             '5. Rotating around chosen axis. See “Rotation \n'
                                             'axis” instruction button.\n'
                                             '\n'
                                             '6. Make finer adjustments in the properties window, \n'
                                             'if necessary.\n'
                                             '\n'
                                             '7. To view the animation, select one or more created \n'
                                             'MovieObjects (sequentially) and click the “Enable an \n'
                                             'object for animation” button. Control the animation using \n'
                                             'the “Animation tools” buttons.\n'
                                             '\n'
                                             '8. To save a video from the animation, indicate the \n'
                                             'MovieObjects on a Clapperboard, to do so, see the \n'
                                             'corresponding instructions.'
                                             )}

    def IsActive(self):
        if Gui.ActiveDocument:
            selection = []
            selection = Gui.Selection.getSelection()
            if not selection:
                return False
            else:
                if selection[0].Name[0:11] != 'MovieCamera':
                    if selection[0].Name[0:12] != 'MovieObjects':
                        if selection[0].Name[0:12] != 'Clapperboard':
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def Activated(self):
        global MO
        listObjects = []
        listObjects = Gui.Selection.getSelection()
        if not listObjects:
            FreeCAD.Console.PrintMessage(translate('MovieObjects',
                                                   'Select at least one object to create a '
                                                   'MovieObjects!') + '\n')
            return
        else:
            Gui.Selection.clearSelection()
            # Objects initial positions and angles
            ActivatedMovieObjects(self)
            MO.Objects = listObjects
            sumCG = FreeCAD.Vector(0,0,0)

            for n in range(len(listObjects)):
                #Get object names (MO.Names)
                Object = listObjects[n]
                name = Object.Name
                MO.Names.append(name)
                MO.ObjectAxis[name] = 'None' # Applies no external rotation axis to object
                #Get object placements
                vectorCenterGravity0 = listObjects[n].Shape.CenterOfGravity
                sumCG = sumCG + vectorCenterGravity0
                vectorBase0 = listObjects[n].Placement.Base
                coordBase0 = (vectorBase0[0], vectorBase0[1], vectorBase0[2])
                rotation0 = listObjects[n].Placement.Rotation.getYawPitchRoll()
                placement0 = (coordBase0, rotation0)
                MO.Pos0[name] = placement0

            # Initial vector of gravity centers average
            vectorGCAverage0 = sumCG/len(listObjects)
            MO.PosGCAverage0 = (vectorGCAverage0[0], vectorGCAverage0[1], vectorGCAverage0[2])
            # Applies an automatic initial A position
            setMOPosAB(obj = MO, position = 'A')
            setMOPosAB(obj = MO, position = 'B') #Repeat position A
            # Updates animation indicator
            ma.modifyAnimationIndicator(animation = False)
            FreeCAD.Console.PrintMessage(translate('MovieObjects',
                                                   'A MovieObject was created with the \n'
                                                   'pre-established position A!') + '\n')

def ActivatedMovieObjects(self):
    global MO

    default_label = translate('MovieObjects',
                              'MovieObjects')
    folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython',
                                              'MovieObjects')
    MovieObjects(folder)
    MovieObjectsViewProvider(folder.ViewObject)
    MO = None
    MO = folder
    MO.Label = default_label
    FreeCAD.ActiveDocument.recompute()

class SetMovieObjectsAxis:

    """Sets a MovieObjects axis."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/SetMovieObjectsAxisIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('SetMovieObjectsAxis',
                                               'Rotation axis'),
                'ToolTip': QT_TRANSLATE_NOOP('SetMovieObjectsAxis',
                                            '1. First create a MovieObjects, set their rotation A and B.\n'
                                            '\n'
                                            '2. Then, define a rotation axis for objects of a created \n'
                                            'MovieObject. The rotation axis can be a line (from Draft \n'
                                            'or Sketch) or even an object edge.\n'
                                            '\n'
                                            '3. After that, select first the objects you want to rotate, \n'
                                            'then the axis and click this button.\n'
                                            '\n'
                                            '4. To erase these settings, enable the MovieObjects and \n'
                                            'click on “Set position B” button.'
                                            )}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MO.Obj_07AnimOnAnim:
                selection = []
                selection = Gui.Selection.getSelection()
                if not selection:
                    return False
                else:
                    if selection[0].Name[0:12] == 'MovieObjects':
                        return True
        else:
            return False

    def Activated(self):
        setObjectsAxis(obj = MO)

class ExcludeMovieObjects:

    """Excludes a MovieObjects."""

    def QT_TRANSLATE_NOOP(self, text):
        return text

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/ExcludeMovieObjectsIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('ExcludeMovieObjects',
                                              'Exclude a MovieObjects'),
                'ToolTip': QT_TRANSLATE_NOOP('ExcludeMovieObjects',
                                             'Select a MovieObjects that you want to exclude, \n'
                                             'then click on this button. \n'
                                             '\n'
                                             'Objects positions and angles will revert to \n'
                                             'the values set when the MovieObjects were \n'
                                             'created.'
                                             )}

    def IsActive(self):
        if Gui.ActiveDocument:
            if not MO.Obj_07AnimOnAnim:
                selection = []
                selection = Gui.Selection.getSelection()
                if not selection:
                    return False
                else:
                    if selection[0].Name[0:12] == 'MovieObjects':
                        return True
        else:
            return False

    def Activated(self):
        excludeMovieObjects()

def excludeMovieObjects():

    """Excludes a MovieObjects."""

    global MO
    selection = []
    selection = Gui.Selection.getSelection()
    if not selection:
        FreeCAD.Console.PrintMessage(translate('MovieObjects',
                                               'Select a MovieObjects to exclude!\n'
                                               ) + '\n')
        return
    else:
        MO = selection[0]
        MO.PosA = MO.Pos0
        MO.PosB = MO.Pos0
        getMovieObjectsMobile(Selection = MO)
        MO = []
        Gui.runCommand('Std_Delete',0)

# ======================================================================================
# 3. Functions

#New
def setMOPosAB(obj = None,
               position = None):

    """Sets the A and B positions for a MovieObjects."""

    MO = obj
    Pos = position # A or B

    # PosA or PosB - positions, angles and centers of gravity of objects
    for n in range(len(MO.Names)):
        name = MO.Names[n]
        vectorCG = MO.Objects[n].Shape.CenterOfGravity
        coordCG = (vectorCG[0], vectorCG[1], vectorCG[2])
        vectorBase = MO.Objects[n].Placement.Base
        coordBase= (vectorBase[0], vectorBase[1], vectorBase[2])
        rotation = MO.Objects[n].Placement.Rotation.getYawPitchRoll()
        placement = (coordBase, rotation)
        if Pos == 'A':
            MO.CenterGravityA[name] = coordCG
            MO.PosA[name] = placement
        if Pos == 'B':
            MO.CenterGravityB[name] = coordCG
            MO.PosB[name] = placement

    #Save object placements
    if Pos == 'A':
        if(hasattr(MO, 'PosAList')): # New
            MO.Obj_02AnimCurrentStep = 0
            MO.PosAList = str(MO.PosA) # New
    if Pos == 'B':
        if(hasattr(MO, 'PosBList')): # New
            MO.Obj_02AnimCurrentStep = MO.Obj_04AnimTotalSteps
            MO.PosBList = str(MO.PosB) # New
    ma.modifyAnimationIndicator(animation = False, obj = MO)
    MO.Obj_01Rotation = True
    FreeCAD.Console.PrintMessage(translate('MovieObjects',
                                          ('MovieObjects position {} has been established.'
                                          ).format(Pos) + '\n'))
    FreeCAD.ActiveDocument.recompute()

def setObjectsAxis(obj = None):

    """Sets a MovieObjects axis."""

    MO = obj
    listObjects = []
    listObjects = Gui.Selection.getSelection()
    if not listObjects:
        FreeCAD.Console.PrintMessage(translate('MovieObjects',
                                               'First select the objects you want \n'
                                               'to rotate then the axis of rotation.'
                                               ) + '\n')
        return
    else:
        Gui.Selection.clearSelection()
        # Last object selected will be the axis
        Object = listObjects[-1]
        AxisName = Object.Name
        # Set the external rotation axis to each object
        for n in range(len(listObjects)):
            Object = listObjects[n]
            name = Object.Name
            if name != AxisName:
                MO.ObjectAxis[name] = AxisName

    ma.modifyAnimationIndicator(animation = False, obj = MO)

def getMovieObjectsMobile(Selection = None):

    """Gets the positions of a MovieObjects."""

    global OBJ_REFRESH
    MO = Selection

    # Objects Pos AB - Angles: yaw, pitch and roll
    if MO.Obj_01Rotation == True:
        for n in range(len(MO.Objects)):
            name = MO.Names[n]
            anglesAn = MO.PosA[name][1]
            anglesBn = MO.PosB[name][1]
            # Object rotate one step
            def getIncAngle(angleA = 0, angleB = 0):
                #New
                IncAngleStep = (angleB - angleA)/MO.Obj_04AnimTotalSteps
                IncAngle1 = IncAngleStep*MO.Obj_02AnimCurrentStep
                return IncAngle1

            yawObjectn1 = getIncAngle(angleA = anglesAn[0], angleB = anglesBn[0])
            yawObjectn2 = anglesAn[0] + yawObjectn1

            pitchObjectn1 = getIncAngle(angleA = anglesAn[1], angleB = anglesBn[1])
            pitchObjectn2 = anglesAn[1] + pitchObjectn1

            rollObjectn1 = getIncAngle(angleA = anglesAn[2], angleB = anglesBn[2])
            rollObjectn2 = anglesAn[2] + rollObjectn1
            # Object Rotates around a chosen axis
            if MO.ObjectAxis[name] != 'None':
                # Reset to the PosA
                vectorA = FreeCAD.Base.Vector(MO.PosA[name][0])
                MO.Objects[n].Placement.Base = vectorA
                MO.Objects[n].Placement.Rotation.setYawPitchRoll(anglesAn[0], anglesAn[1], anglesAn[2])
                # Placement with base, rotation and axis:
                axisObject = FreeCAD.ActiveDocument.getObject(MO.ObjectAxis[name])
                objBase = axisObject.Placement.Rotation.Axis
                objRot = FreeCAD.Base.Rotation(yawObjectn1, pitchObjectn1, rollObjectn1)
                centerRot = axisObject.Placement.Base
                placement = FreeCAD.Placement(objBase, objRot, centerRot)
                MO.Objects[n].Placement = placement.multiply(MO.Objects[n].Placement)
            # Object Rotates without a chosen axis
            else:
                MO.Objects[n].Placement.Rotation.setYawPitchRoll(yawObjectn2, pitchObjectn2, rollObjectn2)

    # Objects that follow a route
    if MO.Obj_01Route == True:
        if not MO.Obj_02RouteSelection:
            FreeCAD.Console.PrintMessage(translate('MovieObjects',
                                                   'You have to select a route in “Obj_02RouteSelection”!'
                                                   ) + '\n')
            ma.modifyAnimationIndicator(animation = False, obj = MO)
            return
        # Calculating the current vector on the route
        route = MO.Obj_02RouteSelection.Shape.Edges[0]
        stepLength = route.Length/MO.Obj_04AnimTotalSteps
        currentStep = stepLength*MO.Obj_02AnimCurrentStep
        if currentStep > route.Length:
            currentStep = route.Length
        currentPos = route.getParameterByLength(currentStep)
        currentVector = route.valueAt(currentPos)

        # Transferring the route position to the bases of the objects or there centers of gravity
        # (through the average of the centers of gravity)
        VectorCGAverageXY = FreeCAD.Vector(MO.PosGCAverage0[0], MO.PosGCAverage0[1], 0)
        for n in range(len(MO.Names)):
            name = MO.Names[n]     
            # The gap1, difference between the average of the centers of gravity and the object's Pos0
            gap1 = VectorCGAverageXY - FreeCAD.Vector(MO.Pos0[name][0])
            # 1. Moving through the bases of objects:
            # The base of each object is the difference between current vector and the gap1
            vector = currentVector - gap1
            # 2. Moving through objects' centers of gravity:
            # The difference between the current center of gravity and the object's base
            gap2 = MO.Objects[n].Shape.CenterOfGravity - MO.Objects[n].Placement.Base
            # The base of object will be the difference between the center of gravity and the gap2
            vector = vector - gap2
            MO.Objects[n].Placement.Base = vector
    else:
        # Objects move one step (PosA - PosB)
        for n in range(len(MO.Names)):
            name = MO.Names[n]
            # Only the objects without a chosen axis
            if MO.ObjectAxis[name] == 'None':
                # Moving through the bases of objects
                if MO.Obj_02RotationCG == False:
                    vectorA = FreeCAD.Vector(MO.PosA[name][0])
                    vectorB = FreeCAD.Vector(MO.PosB[name][0])
                    vectorInc = (vectorB - vectorA)/MO.Obj_04AnimTotalSteps
                    vector = vectorA + vectorInc*MO.Obj_02AnimCurrentStep
                    MO.Objects[n].Placement.Base = vector
                # Moving through objects' centers of gravity
                else:
                    # The position of the center of gravity of each object
                    CGA = FreeCAD.Vector(MO.CenterGravityA[name])
                    CGB = FreeCAD.Vector(MO.CenterGravityB[name])
                    CGInc = (CGB - CGA)/MO.Obj_04AnimTotalSteps
                    CG = CGA + CGInc*MO.Obj_02AnimCurrentStep
                    # The difference between the current center of gravity and the object's base
                    gap2 = MO.Objects[n].Shape.CenterOfGravity - MO.Objects[n].Placement.Base
                    # The base of object will be the difference between the center of gravity and the gap2
                    vector = CG - gap2
                    MO.Objects[n].Placement.Base = vector

    # New - Refreshes each step of objects animation
    if OBJ_REFRESH == True:
        FreeCAD.ActiveDocument.recompute()

def enableObjectsSelection(obj2 = None):

    """Enables position A and B of MovieObjects."""

    global MO
    MO = obj2
    # New - Updating PosA and PosB
    if hasattr(MO, 'PosAList'):
        import ast
        if MO.PosAList != []:
            MO.PosA = ast.literal_eval(MO.PosAList[0])
        if MO.PosBList != []:
            MO.PosB = ast.literal_eval(MO.PosBList[0])

def enableObjectsRefresh(refres = False):

    """Refreshes each step of objects animation."""

    global OBJ_REFRESH
    if refres == True:
        OBJ_REFRESH = True
    else:
        OBJ_REFRESH = False

# ======================================================================================

# 3. Commands

if FreeCAD.GuiUp:
    FreeCAD.Gui.addCommand('CreateMovieObjects', CreateMovieObjects())
    FreeCAD.Gui.addCommand('SetMovieObjectsAxis', SetMovieObjectsAxis())
    FreeCAD.Gui.addCommand('ExcludeMovieObjects', ExcludeMovieObjects())

# ======================================================================================
