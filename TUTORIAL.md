### Movie Workbench Tutorial
        
#### Introduction

The Movie workbench consists of three main parts. The first, Movie Camera module, is in charge of producing camera animation in isolation or together with object animations using tools from this workbench or others. The second one, the Movie Objects module it is possible to animate objects separate or simultaneously with the Movie Camera.

The trird one, the Clapperboard module, is in charge of producing the sequences of frames that will later compose the final videos of the animations. It has tools for creating and recording and play videos of animations within FreeCAD itself.  As a “bonus” it also allows the production and playback of videos from external files. The concept of using a “Clapperboard” comes from the idea that the “action” is due to the animation (Movie Camera).

Finaly, the connection module can provide the integration with animations from others workbenches.

#### Steps for using the Movie workbench:

#### 1. Preparation

1.1. Create an animation with the Movie Workbench or with a workbench, script, or macro of FreeCAD that are prepared for using this workbench (ex. [Modified ExplodedAssembly](https://github.com/Francisco-Rosa/ExplodedAssembly)). If you want to integrated one of those to Movie Workbench, use the Connections.py module, it contains guidelines on how to establish the connection between them.

1.2. The instructions on how to create animations with the Movie Workbench are in README.md.

1.3. Configure the Render projects and cameras if you want to use them.

Install the Render Workbench and the external rendering programs, indicating them in the FC preferences, and carry out all the necessary preparations. See instructions on the Render Workbench at:
![FreeCAD-Render](ttps://github.com/FreeCAD/FreeCAD-render); [Creating renderings](https://wiki.freecadweb.org/Manual:Creating_renderings); [Engine Install](https://github.com/FreeCAD/FreeCAD-render/blob/master/docs/EngineInstall.md).

Prepare the render project(s) as per the instructions on the mentioned websites. Configure, in the properties window, that Open After Render be False and the Render Height and Width values for the final rendering images. For renderers other than POV-Ray, it is necessary to configure the value of Samples Per Pixel and it is recommended to activate the Denoiser.

Important: click on the render button to generate an image and verify that everything is installed and configured correctly.
    
It is possible to use only the “camera” of the 3D view, but the purpose of the render one is to transfer the visual configurations to the render project (see information of the Render Workbench). It's good to remember that the render camera will be moved and changed by one or more Movie Cameras. So if you are using other render cameras for isolated perspectives, don't use them in Movie Cameras, create an exclusive one for this function.

The Movie Camera will adjust, automatically, the 'Aspec Ratio' of the selected render camera to 1.77 (proportion of the resolution of 1920×1080, for example). But you will have to adjust it according to the proportion that you will use in the output images from the render projects, to have a preview of what will be produced in the renderings.
     
#### 2. Usage

2.1. After the animations tested and finished, create and configure the **Clapperboard**

Create a general animation recording configuration using the **Clapperboard**, clicking on its icon, Menu > Movie - Clapperboard or in the pop-up menu opened with the right mouse button.

Configure the **Clapperboard properties window** according to the guidelines ('tips') for each one and your needs. It comes almost completely pre-configured, however the paths for saving the generated frames and videos must be indicated before starting any recording. After creating your first video, you can complete the last property, the path to play a video.
     
2.2. Recording process

Select one or more Movie Camera in sequence and position your animation at the desired step (see more information in README.md).

Create the 3D view frames - **R1**. For a preview of the animation with frames of the 3D view, click on **R1** (or menu Movie > Record 3DView Frames). Choose or confirm the folder to salve the frames (that you've configured above)  and start the animation (from a workbench, script or macro). The animation frames will be named and saved in the folder as configured in 'R1_5FrameOutpuPath' of the Clapperboard properties window. Messages on the bottom bar of the FC will show the recording progress, to better follow the process, open the report window.

Create the video in FC. After finishing all desired animation recording steps, click on **Create Video** (or Menu > Movie > Create Video), choose or confirm the input frames folder (indicated in Video 'InputFrames' of the Clapperboard). After finishing the recording, a message in the report window will confirm the location where the file was saved. Important: it will be named and saved in the folder you configured before, respectively in Video Name and Video OutputPath of Clapperboard properties window.

Play the video in the FC or an external program. Click on **Play Video** (or Menu > Movie > Play Video or workbench pop menu) and choose the file you want to play, or directly click on the created video file to open it with your system's video playback program for confirmation of the result. If you prefer, you can also import the frames created into an external video editing program that you already know, or assemble the final video with the various partial footage from the cameras used and include the sound.

Repeat the previous items using the render frames - **R2**. Once satisfied with the result of the animation of the 3D views of the FC, you can start recording the rendered frames, according to the Render project(s) chosen and already properly configured (s). Repeat the four previous steps, but now confirming the properties corresponding to the Render in the Clapperboard properties window (mainly Render 'FrameOutputPath'), use the cameras configured for the render and activate **R2** (Record Render Frames).

Stop recording. If you need or want to interrupt the recording process, click on **Stop Recording** or type **Crtl k**. This command only interrupts the recording, for the animation use the pause animation button of the workbench, it will also stop the recording process.

#### 3. Observations

3.1. Usage of Render POV-Ray. In addition to already mentioned, you must configure for the render window not remains open after completion, deleting the '+P' in the 'Render parameters' field of the FC preferences.

For the Windows version, it will also be necessary to configure the POV-Ray Gui to close after the rendering is finished. To do so, open the POV-Ray GUI, go to the render settings (menu - Render), click 'On Completion' and enable 'Exit POV-Ray for Windows'. Also disable all sound warnings (in Render menu - 'SoundSettings...') and any message openings that may appear after each completed render.

3.2. Usage of other renderers. Still are necessary adjustments for animation, mainly the inclusion of automatic closing of the program window. If anyone knows how and wants to contribute, please post the instructions in the [FC forum topic - Movie Workbench](https://forum.freecadweb.org/viewtopic.php?f=8&t=74432).

#### 4. Installation of the Movie Workbench
    
4.1. The Movie Workbench is available at [FreeCAD-Movie](https://github.com/Francisco-Rosa/FreeCAD-Movie), but you can install it through the addon manager within the FC: Menu Tools - Addon Manager.

4.2. The ExplodedAssembly workbench modified and prepared for recording is available at: [Modified ExplodedAssembly](https://github.com/Francisco-Rosa/ExplodedAssembly)

If you have mastery over the functioning of the different python files of workbenches contained in the Mod folder of FC, you can only replace the modified file ('ExplodedAssembly.py'). But first, save the original file or rename it, adding a _orig, for example.
