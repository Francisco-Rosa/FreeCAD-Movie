# FreeCAD Movie Workbench
FreeCAD workbench to create and play videos of animations

<img src=./icons//CreateVideoIcon.svg height=30>
The Movie workbench icon 



### Features
* Create frames from the FreeCAD 3D views or the rendered ones   
* Create videos from them inside FreeCAD or export them to your preferred external program   
* Check the result playing the videos you have created  

### Installation
   

##### Manually install using github
  
- Download the ZIP file (click 'Clone or Download' button above) 
- For Ubuntu and similar OS's, extract it inside */home/username/.local/share/FreeCAD/Mod*   
- For Windows, extract it inside *C: \Users\your_user_name\AppData\Roaming\FreeCAD\Mod* 
- Rename the folder to Movie  
- Launch FreeCAD

### Preparation

Before using the workbench, some preparations are necessary:

1. Create an animation with a workbench, script or macro of FreeCAD that are prepared for using this workbench (ex. ExplodedAssembly: https://github.com/Francisco-Rosa/ExplodedAssembly).
2. If you want to integrated your animation workbench, script or macro to Movie Workbench, see how to in the TUTORIAL.txt file.
3. For using render frames, you must install the Render Workbench and prepare rendering projects (see information in https://github.com/FreeCAD/FreeCAD-render).
4. Open the Render Workbench and position cameras that better show the animation (recommended).

### Usage
After preparation done, go to Movie Workbench and:

1. Click on <img src=./icons//CreateClapperboardIcon.svg height=20>  to **create the Clapperboard** and <img src=./icons//ClapperboardIcon.svg height=20> to **configure it** (see the tips showed for each item in the property window).
2. Choose the camera and set GUI to it (recommended) or use a FreeCAD 3D View. Position your animation at the desired step.
3. Click on <img src=./icons//StartRecord3DViewIcon.svg height=20> for **record 3D view frames** or <img src=./icons//StartRecordRenderIcon.svg height=20> for **record render ones**.
4. Start the animation with the correspondent commands of the workbench, script or macro used.
5. If you need to stop recording, click on <img src=./icons//StopRecordCameraIcon.svg height=20>  **stop recording**.
6. If you need to stop the animation, use the correspondent commands of the workbench, script or macro used.
7. After the animation finished, choose the folder to salve your video and click on <img src=./icons//CreateVideoIcon.svg height=20>  **create video**.
8. For playing video, choose the file and click on <img src=./icons//PlayVideoIcon.svg height=20> **play video**.

 
### Documentation
For more information, see the TUTORIAL.txt file inside the Movie folder installed.
Wiki documentation will be available as soon as possible.
  
### Feedback 
For discussion, please use the Movie Workbench thread (https://forum.freecadweb.org/viewtopic.php?f=8&t=74432) in the FreeCAD forum.

#### License 
LGPL-2.1

#### Author
Francisco Rosa
