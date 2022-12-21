''' Movie workbench, record and play animation videos in FreeCAD '''

# ***************************************************************************
# *   Copyright (c) 2022 Francisco Rosa                                     *   
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
import FreeCADGui
import shutil
from PySide.QtGui import QFileDialog
from PySide.QtCore import QT_TRANSLATE_NOOP

translate = FreeCAD.Qt.translate

LanguagePath = os.path.dirname(__file__) + '/translations'
FreeCADGui.addLanguagePath(LanguagePath)


# ======================================================================================

# 1. Classes
# 1.1. Clapperboard - Record Animation Configuration

class Clapperboard:
    def __init__(self, obj):
    	  # Camera group config
        obj.addProperty('App::PropertyString', 'Cam_1Name', 'Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                             'Indicate the chosen camera or view through which the recording will be performed. '
                                             'Write a short name, as this will be inserted in the nomenclature of each frame'
                                             ' created.')).Cam_1Name = 'Cam_01'
        obj.addProperty('App::PropertyString', 'Cam_2Take', 'Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                             'Indicate the take of each recording made. Write a short name, '
                                             'as this will be inserted in the nomenclature of each frame '
                                             'created.')).Cam_2Take = 'Take_01'
        obj.addProperty('App::PropertyBool', 'Cam_3OnRec', 'Camera config', QT_TRANSLATE_NOOP('App::Property', 
                                             'It indicates whether the chosen camera is recording or not.'
                                             ' It is activated by the R1 or R2 buttons and deactivated by the '
                                             'Stop Recording one.')).Cam_3OnRec = False
                                             
        # R1 3DView frames group config                                                                               

        obj.addProperty('App::PropertyString', 'R1_1FrameName', 'R1 3DView frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the main name of these frames. Write a short name, '
                                             'as this will be inserted in the nomenclature of each frame '
                                             'created.')).R1_1FrameName = str(FreeCAD.ActiveDocument.Label) + '_R1_frame'
        obj.addProperty('App::PropertyInteger', 'R1_2FrameInitial', 'R1 3DView frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the initial number of these frames (zero to first one). '
                                             'This will be inserted in the nomenclature of each frame '
                                             'created.')).R1_2FrameInitial = 0
        obj.addProperty('App::PropertyInteger', 'R1_3FrameWidth', 'R1 3DView frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Configure the width in pixels of the created frames.')).R1_3FrameWidth = 800                                             
        obj.addProperty('App::PropertyInteger', 'R1_4FrameHeight', 'R1 3DView frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Configure the heigth in pixels of the created frames.')).R1_4FrameHeight = 600
        obj.addProperty('App::PropertyPath', 'R1_5FrameOutputPath', 'R1 3DView frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'The path to R1 frames folder')).R1_5FrameOutputPath = ""                         
        obj.addProperty('App::PropertyBool', 'R1_6OnRec', 'R1 3DView frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicates whether the chosen camera is recording the FC 3D views or not.'
                                             ' Control this by the R1 and Stop Recording buttons.')).R1_6OnRec = False                                             
                                             
        # R2 Render frames group config                                         
        obj.addProperty('App::PropertyString', 'R2_1FrameName', 'R2 Render frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the main name of the rendered frames. Write a short name, '
                                             'as this will be inserted in the nomenclature of each frame '
                                             'created.')).R2_1FrameName = str(FreeCAD.ActiveDocument.Label) + '_R2_frame'
        obj.addProperty('App::PropertyInteger', 'R2_2FrameInitial', 'R2 Render frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the initial number of these frames (zero to first one). '
                                             'This will be inserted in the nomenclature of each frame created.')).R2_2FrameInitial = 0
        obj.addProperty('App::PropertyPath', 'R2_3FrameOutputPath', 'R2 Render frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'The path to R2 frames folder')).R2_3FrameOutputPath = ""                                                                                   
        obj.addProperty('App::PropertyString', 'R2_4RenderProject', 'R2 Render frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the internal name (not its label) of one of the previously created '
                                             'render projects.')).R2_4RenderProject = "Project"                                                      
        obj.addProperty('App::PropertyBool', 'R2_5OnRec', 'R2 Render frames config',  QT_TRANSLATE_NOOP('App::Property',
                                             'It indicates whether the chosen camera is recording the renders or not.'
                                             ' Control this by the R2 and Stop Recording buttons.')).R2_5OnRec = False 
                                            
        # Videos group config   
        obj.addProperty('App::PropertyString', 'Video_1Name', 'Videos',  QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the main name for the created videos. '
                                             'Chose to add the 3DViews text or Renders one, according to the origin of the '
                                             'frames.')).Video_1Name = str(FreeCAD.ActiveDocument.Label) + '_R1_frames or R2_frames'                                   
        obj.addProperty('App::PropertyPath', 'Video_2InputFrames', 'Videos',  QT_TRANSLATE_NOOP('App::Property',
                                             'Confirm the path to the folder containing the frames for creating a video '
                                             'when clicking on the create video button.')).Video_2InputFrames = ""
        obj.addProperty('App::PropertyInteger', 'Video_3Fps','Videos', QT_TRANSLATE_NOOP('App::Property',
                                             'Indicate the frames per second of the video (fps) that will be created.'
                                             )).Video_3Fps = 24                                             
        obj.addProperty('App::PropertyPath', 'Video_4OutputPath', 'Videos',  QT_TRANSLATE_NOOP('App::Property',
                                             'Set path to folder to save created videos by clicking on the button with '
                                             'the three dots on the right.')).Video_4OutputPath = ""
        obj.addProperty('App::PropertyInteger', 'Video_5Number', 'Videos',  QT_TRANSLATE_NOOP('App::Property',
                                              'Indicate the initial number of the videos (zero to first one). '
                                             'This will be inserted in the nomenclature of each one created.')).Video_5Number = 0                    
        obj.Proxy = self


class ClapperboardViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        __dir__ = os.path.dirname(__file__)
        return __dir__ + '/icons/ClapperboardIcon.svg'

def ActivatedClapperboard():
    try:
        folder = FreeCAD.ActiveDocument.Clapperboard

    except:
        folder = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'Clapperboard')
        Clapperboard(folder)
        ClapperboardViewProvider(folder.ViewObject)
            
# ======================================================================================

# 1.2. Command classes

class CreateClapperboard:
	
    def QT_TRANSLATE_NOOP(Movie, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateClapperboardIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateClapperboard', 'Clapperboard'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateClapperboard',
                                             'Creates a clapperboard with the recording camera settings. '
                                             'Once created, complete and/or modify each of its properties '
                                             'before starting to record your frames or movies.')}
 
                                      
    def Activated(self):
        ActivatedClapperboard()
        
class StartRecord3DView:
	
    def QT_TRANSLATE_NOOP(Render, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StartRecord3DViewIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('StartRecord3DView', 'Record 3DView Frames'),
                'ToolTip': QT_TRANSLATE_NOOP('StartRecord3DView', 
                                             'Triggers the recording of frames according to '
                                             'the Camera and R1 3DView settings of the clapperboard. '
                                             'After clicking on it, confirm the folder to salve the frames '
                                             'and start the animation')}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.Clapperboard.Cam_3OnRec):
                return True

        else:
            return False
                                   
    def Activated(self):
        startRecord3DView()

class StartRecordRender:
	
    def QT_TRANSLATE_NOOP(Render, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StartRecordRenderIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('StartRecordRender', 'Record Render Frames'),
                'ToolTip': QT_TRANSLATE_NOOP('StartRecordRender', 
                                             'Triggers the recording of frames according to '
                                             'the Camera and R2 Render settings of the clapperboard. '
                                             'After clicking on it, confirm the folder to salve the frames '
                                             'and start the animation')}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.Clapperboard.Cam_3OnRec):
                return True

        else:
            return False
                                   
    def Activated(self):
        startRecordRender()

class StopRecordCamera:
	
    def QT_TRANSLATE_NOOP(Render, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/StopRecordCameraIcon.svg',
                'Accel': 'Ctrl+k',     
                'MenuText': QT_TRANSLATE_NOOP('StopCameraRecord', 'Stop Recording'),
                'ToolTip': QT_TRANSLATE_NOOP('StopCameraRecord','Stops camera recording.')}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.Clapperboard.Cam_3OnRec):
                return False

            else:
                return True

        else:
            return False
                                      
    def Activated(self):
        stopRecordCamera()

class CreateVideo:
	
    def QT_TRANSLATE_NOOP(Movie, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/CreateVideoIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('CreateVideo', 'Create Video'),
                'ToolTip': QT_TRANSLATE_NOOP('CreateVideo', 
                                             'Creates a mp4 video. '
                                             'Configure the videos items in the clapperboard. '
                                             'After clicking on it, confirm the folder to salve the video')}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.Clapperboard.Cam_3OnRec):
                return True

        else:
            return False
                         
                                     
    def Activated(self):
        createVideo()

      
class PlayVideo:
	
    def QT_TRANSLATE_NOOP(Render, text):
        return text
	
    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        return {'Pixmap': __dir__ + '/icons/PlayVideoIcon.svg',
                'MenuText': QT_TRANSLATE_NOOP('PlayVideo', 'Play Video'),
                'ToolTip': QT_TRANSLATE_NOOP('PlayVideo', 
                                             'Plays a video file indicated in the dialog window')}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            if not(FreeCAD.ActiveDocument.Clapperboard.Cam_3OnRec):
                return True

        else:
            return False
                         
                                      
    def Activated(self):
        playVideo()
        
# ======================================================================================

# 2. Command functions
# 2.1. Frames recording commands

def startRecord3DView():
    CL = FreeCAD.ActiveDocument.Clapperboard
    CL.Cam_3OnRec = True
    CL.R1_6OnRec = True
    WindowTitle = translate('Movie', 'Select or confirm the folder to save the R1 frames')
    OpenDir = CL.R1_5FrameOutputPath
    CL.R1_5FrameOutputPath = QFileDialog.getExistingDirectory(FreeCADGui.getMainWindow(), WindowTitle, OpenDir)
    
def startRecordRender():
    import Render
    CL = FreeCAD.ActiveDocument.Clapperboard
    CL.Cam_3OnRec = True
    CL.R2_5OnRec = True
    WindowTitle = translate('Movie', 'Select or confirm the folder to save the R2 frames')
    OpenDir = CL.R2_3FrameOutputPath
    CL.R2_3FrameOutputPath = QFileDialog.getExistingDirectory(FreeCADGui.getMainWindow(), WindowTitle, OpenDir)

def stopRecordCamera():
    CL = FreeCAD.ActiveDocument.Clapperboard
    CL.Cam_3OnRec = False
    CL.R1_6OnRec = False
    CL.R2_5OnRec = False

def runRecordCamera():
    CL = FreeCAD.ActiveDocument.Clapperboard
    camNum = str(f'{CL.Cam_1Name:0>2}')
    takeNum = str(f'{CL.Cam_2Take:0>2}')
    
    if CL.R1_6OnRec == True:
        CL.R1_2FrameInitial += 1
        name = CL.R1_1FrameName   
        frameNum = str(f'{CL.R1_2FrameInitial:0>4}')
        frameFinalName = name + '_' + camNum + '_' + takeNum +'_fr' + frameNum +'.png'
        pathAndName = CL.R1_5FrameOutputPath +'/' + frameFinalName
        
        FreeCADGui.activeDocument().activeView().saveImage(pathAndName,CL.R1_3FrameWidth,CL.R1_4FrameHeight,'Current')

        FreeCAD.Console.PrintMessage(translate('Movie', 'Frame 3DView # ' + frameNum +' has been completed') + '\n')    

    if CL.R2_5OnRec == True :
        CL.R2_2FrameInitial += 1
        name = CL.R2_1FrameName
        frameNum = str(f'{CL.R2_2FrameInitial:0>4}')
        frameFinalName = name + '_' + camNum + '_' + takeNum +'_fr' + frameNum +'.png'
        project =  FreeCAD.getDocument(FreeCAD.ActiveDocument.Label).getObject(CL.R2_4RenderProject)
        
        output_file=project.Proxy.render(wait_for_completion=True)
        shutil.move(output_file, f"" + CL.R2_3FrameOutputPath +'/' + frameFinalName)
        
        # Close render window
        FreeCADGui.runCommand('Std_CloseActiveWindow',0)

        FreeCAD.Console.PrintMessage(translate('Movie','Frame Render # ' + frameNum +' has been completed') + '\n')

# ======================================================================================

# 2.2. Create and play video commands

def createVideo():
    import cv2
    CL = FreeCAD.ActiveDocument.Clapperboard
    
    # Confirmation of the input frames folder to create video
    WindowTitle1 = translate('Movie', 'Select or confirm the input frames folder to create video')
    OpenDir = CL.R1_5FrameOutputPath
    CL.Video_2InputFrames = QFileDialog.getExistingDirectory(FreeCADGui.getMainWindow(), WindowTitle1, OpenDir) 
      
    pathFrames = CL.Video_2InputFrames +'/'
    outVideoPath = CL.Video_4OutputPath + '/'
    CL.Video_5Number += 1
    videoNum = str(f'{CL.Video_5Number:0>2}')
    outVideoName = CL.Video_1Name + '_'+ CL.Cam_1Name +'_'+ CL.Cam_2Take +'_'+ videoNum + '.mp4'
    outVideoFullPath = outVideoPath+outVideoName
	
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
	
    fps = CL.Video_3Fps

    video = cv2.VideoWriter(outVideoFullPath, cv2_fourcc, fps, (Widthframe1, Heightframe1)) #output video name, fourcc, fps, size (heigth, width)

    for i in range(len(frames)):
        video.write(cv2.imread(frames[i]))
        message = str('frame ' + str(i+1) + ' of ' + str(len(frames)))
        FreeCAD.Console.PrintMessage(translate('Movie', message) + '\n')

    video.release()
    FreeCAD.Console.PrintMessage(translate('Movie','outputed video to '+ outVideoPath)+'\n')


def playVideo():
    import cv2
    import time
   	
    CL = FreeCAD.ActiveDocument.Clapperboard

    MovieFileFilter = '; All files (*.*)'
    WindowTitle = translate('Movie', 'Select file to play')
    OpenDir = CL.Video_4OutputPath + '/'
    PathAndFile = QFileDialog.getOpenFileName(FreeCADGui.getMainWindow(), WindowTitle, OpenDir, MovieFileFilter)    
    
    Video_PathAndFile = PathAndFile[0]
    
    cap = cv2.VideoCapture(Video_PathAndFile)
    
    fps2 = int(cap.get(cv2.CAP_PROP_FPS))
    
    if cap.isOpened() == False:
        FreeCAD.Console.PrintMessage(translate('Movie','Error: video file not found!'))
        
    else:
        message2 = 'Movie at '+ str(fps2) + ' fps,' + ' press q to stop the video'
        FreeCAD.Console.PrintMessage(translate('Movie', message2) + '\n')    	
    
    while cap.isOpened():
        sucess, frame = cap.read()
        if sucess == True:
            time.sleep(1/fps2)
            cv2.imshow('Video', frame)
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
    FreeCAD.Gui.addCommand('StartRecord3DView', StartRecord3DView())
    FreeCAD.Gui.addCommand('StartRecordRender', StartRecordRender())
    FreeCAD.Gui.addCommand('StopRecordCamera', StopRecordCamera())
    FreeCAD.Gui.addCommand('CreateVideo', CreateVideo())
    FreeCAD.Gui.addCommand('PlayVideo', PlayVideo())
    
# ======================================================================================

#https://wiki.freecad.org/Command
#https://wiki.freecad.org/Translating_an_external_workbench

