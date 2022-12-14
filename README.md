# FreeCAD Movie Workbench
FreeCAD workbench to create and play videos of animations

<img src=./icons//ClapperboardIcon.svg height=30>
The Movie workbench icon 



### Features
* Create frames from the FreeCAD 3D views or the rendered ones   
* Create videos from them inside FreeCAD or export them to your preferred external program   
* Check the result playing the videos you have created  

### Installation
   

##### Manually install using github
  
- Download https://github.com/Francisco-Rosa/FreeCAD-Movie as a ZIP (click 'Clone or Download' button)  
- For Ubuntu and similar OS's, extract it inside */home/username/.local/share/FreeCAD/Mod*   
- For Windows, extract it inside *C: \Users\your_user_name\AppData\Roaming\FreeCAD\Mod* 
- Rename the folder to Movie  
- Launch FreeCAD

### Usage

1. Create an animation with a workbench, script or macro of FreeCAD that are already prepared for using this workbench (ex. ExplodedAssembly)
2. Open the Render Workbench and position cameras that better shows the animations
3. For using render frames, prepare render projects (see information in https://github.com/FreeCAD/FreeCAD-render)
4. Click on <img src=./icons//CreateClapperboardIcon.svg height=20>  to create the Clapperboard and <img src=./icons//ClapperboardIcon.svg height=20> to configure it (see the tips showed for each item in the property window)
5. Choose the camera or 3D view. Position your animation at the desired step
6. Click on <img src=./icons//StartRecord3DViewIcon.svg height=20> for creating 3D view frames or <img src=./icons//StartRecordRenderIcon.svg height=20> for render ones
7. Start the animation with the correspondent commands of the workbench, script or macro used
8. After the animation finished, choose the folder to salve your video and click on <img src=./icons//CreateVideoIcon.svg height=20> (create video)
9. If you need to stop recording, click on <img src=./icons//StopRecordCameraIcon.svg height=20> (stop record)
10. For playing video, choose the file and click on <img src=./icons//PlayVideoIcon.svg height=20> (play video)

 
### Documentation
For more information, see the Tutorial.txt file inside the Movie folder installed.
Wiki documentation will be available as soon as possible.
  
### Feedback 
For discussion, please use the Movie Workbench thread (https://forum.freecadweb.org/viewtopic.php?f=8&t=74432) in the FreeCAD forum.

#### License 
LGPL-2.1

#### Author
Francisco Rosa
