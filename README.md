# FreeCAD Movie Workbench
FreeCAD workbench to create and play videos of animations


The Movie Workbench icon

<img src=./icons//CreateVideoIcon.svg height=50>
 
The Movie toolbar

<img src=./Docs/Image_MW_toolbar_2.jpg height=60>


### Features
* Create frames from the FreeCAD 3D views (**R1**) or the rendered ones (**R2**).   
* Create videos from them inside FreeCAD or export them to your preferred external program.   
* Check the result playing the videos you have created.

### Installation

##### Via Addon Manager (Recommended)

- Menu Tools > Addon Manager
- Locating Movie Worbench and installing it
- Restart FreeCAD.
   

##### Manually install using github
  
- Download the ZIP file (click 'Clone or Download' button above) 
- For Ubuntu and similar OS's, extract it inside */home/username/.local/share/FreeCAD/Mod*   
- For Windows, extract it inside *C: \Users\your_user_name\AppData\Roaming\FreeCAD\Mod*
- On macOS it is usually */Users/username/Library/Preferences/FreeCAD/Mod*
- Launch FreeCAD

### Preparation

For full using the workbench, two basic preparations are necessary:

1. Create an animation with a workbench, script or macro of FreeCAD that are prepared for using this workbench (ex. [Modified ExplodedAssembly](https://github.com/Francisco-Rosa/ExplodedAssembly)). If you want to integrated your animation workbench, script or macro to Movie Workbench, see how in the [TUTORIAL.md](https://github.com/Francisco-Rosa/FreeCAD-Movie/blob/master/TUTORIAL.md).
2. If yoy want use the rendered frames (**R2**), you must install the Render Workbench, prepare rendering projects and test them preventively to make sure everything is working correctly (see information in [FreeCAD-Render](https://github.com/FreeCAD/FreeCAD-render)). It is also recommended to take advantage and position some cameras from this workbench that better show the animation.

### Usage
After preparation done, go to Movie Workbench and:

1. Click on <img src=./icons//CreateClapperboardIcon.svg height=20>  to **create the Clapperboard** and <img src=./icons//ClapperboardIcon.svg height=20> to **configure it** (see the tips showed for each item in the property window).
2. Choose the camera and set GUI to it (recommended) or use a FreeCAD 3D View. Position your animation at the desired step.
3. Click on <img src=./icons//StartRecord3DViewIcon.svg height=20> for **record 3D view frames** or <img src=./icons//StartRecordRenderIcon.svg height=20> for **record render ones**, choose or confirm the folder to salve the frames.
4. Start the animation with the correspondent commands of the workbench, script or macro used.
5. If you need to stop recording, click on <img src=./icons//StopRecordCameraIcon.svg height=20>  **stop recording**.
6. If you need to stop the animation, use the correspondent commands of the workbench, script or macro used.
7. After the animation finished, choose the folder to salve your video and click on <img src=./icons//CreateVideoIcon.svg height=20>  **create video**, choose or confirm the input frames folder.
8. For playing video, choose the file and click on <img src=./icons//PlayVideoIcon.svg height=20> **play video**.

The Clapperboard properties

<img src=./Docs/Image_MW_toolbar_propr.jpg height=600>

The Movie menu

<img src=./Docs/Image_MW_menu.jpg height=600>

The Movie popup menu

<img src=./Docs/Image_MW_pop_menu.jpg height=600>
 
### Documentation
For more information, see the [TUTORIAL.md](https://github.com/Francisco-Rosa/FreeCAD-Movie/blob/master/TUTORIAL.md) file inside the Movie folder installed.
Wiki documentation will be available as soon as possible.
  
### Feedback 
For discussion, please use the [Movie Workbench thread](https://forum.freecadweb.org/viewtopic.php?f=8&t=74432) in the FreeCAD forum.

#### License 
LGPL-2.1

#### Author
Francisco Rosa
