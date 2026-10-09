<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="pt-BR" sourcelanguage="en">
  <context>
    <name>App::Property</name>
    <message>
      <location filename="../MovieCamera.py" line="67"/>
      <source>Initial step of the MovieCamera animation.

Indicate the step which this section of 
the animation will begin.</source>
      <translation>Passo inicial da animação da CameraMovie.

Indique o passo em que esta seção da 
animação começará.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="75"/>
      <source>Current step of the MovieCamera animation.

It is only indicative.</source>
      <translation>Passo atual da animação da CameraMovie. 

É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="82"/>
      <source>End step of the MovieCamera animation.

Indicate the step which this section of 
the animation will finish. 

Changes will only take effect after 
MovieCamera has been re-enabled.</source>
      <translation>Passo final da animação da CameraMovie. 

Indique o passo que esta seção da animação 
terminará. 

As alterações só terão efeito depois que a 
CameraMovie for reativada.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="93"/>
      <source>Total steps of the MovieCamera animation.

It is the result of the difference between 
end step (“Cam_03AnimEndStep”) and initial 
step (“Cam_01AnimIniStep”).</source>
      <translation>Total de passos da animação CameraMovie. 

É o resultado da diferença entre o Passo final 
(“Cam_03AnimEndStep”) e o Passo inicial 
(“Cam_01AnimIniStep”).</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="102"/>
      <source>Animation fps of the MovieCamera.

Specify the value for this animation 
section.
It is a simulation and will depend on 
the computer performance. 

Changes will only take effect after 
MovieCamera has been re-enabled.</source>
      <translation>Quadros por segundo da animação da CameraMovie.

Especifique o fps da animação da seção.
É uma simulação e dependerá do desempenho 
do computador.

As alterações só terão efeito depois que a 
CameraMovie for reativada.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="115"/>
      <source>Animation time of the MovieCamera, 
in hours, minutes, and seconds. 

It is only indicative.</source>
      <translation>Tempo de animação da CameraMovie 
em horas, minutos e segundos.

É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="123"/>
      <source>MovieCamera animation on or off. 

It should not be changed manually, 
it is controlled by the animation 
buttons.</source>
      <translation>Animação da CameraMovie ativada ou desativada. 

Não deve ser alterado manualmente, é controlado 
pelos botões de animação.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="134"/>
      <source>Camera type for the MovieCamera.

Choose the camera through which this section 
of the animation will be performed: “3D view” 
for 3D views and the “Render” for adopting 
the settings of a camera from the Render 
Workbench, previously created and adjusted.</source>
      <translation>Tipo de câmera para a CameraMovie. 

Escolha a câmera através da qual esta seção 
da animação será executada: “3DView” para 
vistas 3D e a “Render” para adotar as 
configurações de uma câmera da Bancada 
Render, previamente criada e ajustada.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="146"/>
      <source>Render camera selection for the MovieCamera animation.

If you have chosen “Render” in Camera type (“Cam_01Type”), 
you have to select which one will be used in this 
section of the animation.</source>
      <translation>Seleção da câmera de render para a animação CameraMovie. 

Se você escolheu “Render” em Tipo de câmera (“Cam_01Type”), 
deverá selecionar qual será utilizada nesta seção de animação.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="155"/>
      <source>Render image width of the MovieCamera animation.

Configure the width in pixels that will compose 
the aspect ratio of the image (“AspectRatio”).</source>
      <translation>Largura da imagem renderizada da animação da CameraMovie. 

Configure a largura em píxeis que irá compor a proporção da 
imagem (“AspectRatio”).</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="163"/>
      <source>Render image height of the MovieCamera animation.

Configure the height in pixels that will compose 
the aspect ratio of the image (“AspectRatio”).</source>
      <translation>Altura da imagem renderizada da animação da CameraMovie. 

Configure a altura em píxeis que irá compor a proporção da 
imagem (“AspectRatio”).</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="171"/>
      <source>Objects selected for the MovieCamera animation.

Select the MoveObjects to animate together 
with this MovieCamera.</source>
      <translation>Objetos selecionados para a animação da CameraMovie. 

Selecione ObjetosMovie para animar com esta 
CameraMovie.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="179"/>
      <source>Enable the combinations for the MovieCamera animation.

Configure the combination of objects to animate together: 
only MovieCamera (“Camera”), MovieCamera and MovieObjects 
(“Camera and objects”), MovieCamera and connection 
(“Camera and connection”), or even just the MovieObjects 
(“Objects”) or connection (“Connection”) associated with 
this MovieCamera.

For each combination change it will be necessary to 
re-enable the MovieCamera.</source>
      <translation>Habilite as combinações para a animação da CameraMovie.

Configure a combinação de objetos para se animarem juntos: 
apenas CameraFime (“Camera”), CameraMovie e ObjetosMovie 
(“Camera and Objects”), CameraMovie e conexão 
(“Camera and Connection”), ou mesmo apenas os 
ObjetosMovie (“Objects”) ou conexão (“Connection”) 
associados a esta CameraMovie. 

Para cada alteração da combinação será necessário 
reativar a CameraMovie.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="198"/>
      <source>Connection for MovieCamera animation. 

Choose the workbench through which the 
animation will be performed together, if so.

Make sure the workbench is installed and 
that there is an animation created with it.</source>
      <translation>Conexão para a animação da CameraMovie.

Escolha a bancada de trabalho através da 
qual a animação será executada em conjunto, 
se for o caso.

Certifique-se de que a bancada 
esteja instalada e que haja uma animação 
criada com ela.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="211"/>
      <source>Target of the MovieCamera. 

If you want to use an object or point as a target, 
choose “Follow an object or point” and select one of 
them in target object selection (“Cam_02Target_ObjectSelection”), 
while for the “Follow a route” option you must use route 
selection (“Cam_02RouteSelection”).</source>
      <translation>Alvo da CameraMovie. 

Caso queira utilizar um objeto ou ponto como alvo, 
escolha “Seguir um objeto ou ponto” e selecione um 
deles em seleção de objeto alvo (“Cam_02Target_ObjectSelection”), 
enquanto para a opção “Seguir uma rota ” você deve usar a 
seleção de rota (“Cam_02RouteSelection”).</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="224"/>
      <source>Target object selection of the MovieCamera.

Select the point or object you want the 
camera to point to.</source>
      <translation>Seleção de objeto alvo da CameraMovie. 

Selecione o ponto ou objeto para o qual 
deseja que a câmera aponte.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="232"/>
      <source>Target ahead of the MovieCamera.

If you chose for the target to 
“follow a route”, in “Cam_01Target”, 
you need to specify how many steps 
this target will be ahead of the 
camera on the same route.</source>
      <translation>Alvo à frente da CameraMovie.

Se você escolheu para o alvo “seguir uma rota”, 
em “Cam_01Target”, você precisa especificar 
quantos passos esse alvo estará à frente da 
câmera na mesma rota.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="245"/>
      <source>Route of the MovieCamera animation.

Enable it so that the camera follows a route. 
You have to select a single segment on route 
selection (“Cam_02RouteSelection”) 
to use it.</source>
      <translation>Rota da animação da CameraMovie 

Habilite-o se a câmera for animada em uma rota. 
Você deve selecionar um único segmento em 
seleção da rota (“Cam_02RouteSelection”) para usá-lo.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="255"/>
      <source>Route selection for the MovieCamera animation.

Choose the route through which the camera will be 
animate. You have to select a single segment such 
as: line, arc, circle, ellipse, B-spline or Bézier 
curve, from Sketcher or Draft Workbenches.</source>
      <translation>Seleção da rota para a animação da CameraMovie. 

Escolha a rota pela qual a câmera será animada. 
Você deve selecionar um único segmento como: 
linha, arco, círculo, elipse, B-spline ou curva de 
Bézier, das Bancadas Sketcher ou Draft.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="267"/>
      <source>X movement of the MovieCamera.

Enable this if you want to 
animate the camera in X direction.</source>
      <translation>Movimento X da CameraMovie. 

Habilite isto se quiser animar a 
câmera na direção X.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="275"/>
      <source>Y movement of the MovieCamera.

Enable this if you want to 
animate the camera in Y direction.</source>
      <translation>Movimento Y da CameraMovie 

Habilite isto se deseja animar a 
câmera na direção Y.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="283"/>
      <source>Z movement of the MovieCamera.

Enable this if you want to 
animate the camera in Z direction.</source>
      <translation>Movimento Z da CameraMovie. 

Habilite isto se desejar animar a 
câmera na direção Z.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="293"/>
      <source>Yaw of the MovieCamera.

Enable this if you want to 
animate the camera horizontal angle.</source>
      <translation>Guinada da CameraMovie. 

Habilite isto se quiser animar o ângulo 
horizontal da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="301"/>
      <source>Pitch of the MovieCamera.

Enable this if you want to 
animate the camera vertical angle.</source>
      <translation>Inclinação vertical da CameraMovie. 

Habilite isto se quiser animar o ângulo 
vertical da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="309"/>
      <source>Roll of the MovieCamera.

Enable this if you want to 
animate the camera roll angle.</source>
      <translation>Rolagem da CameraMovie. 

Habilite isto se quiser animar 
o ângulo de rotação da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="317"/>
      <source>Zoom of the MovieCamera.

Enable this if you want to 
animate the camera zoom.</source>
      <translation>Zoom da CameraFime. 

Habilite isto se quiser animar o 
zoom da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="327"/>
      <source>X of Position A of the MovieCamera.

It is set when the “Set position 
A” button is pressed, after that, 
if necessary, you can make adjustments 
to the x-value.</source>
      <translation>X da Posição A da CameraMovie. 

É definido quando o botão "Definir posição A" é pressionado, 
após isso, se necessário, você pode fazer ajustes no valor x.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="337"/>
      <source>Y of Position A of the MovieCamera.

It is set when the “Set position 
A” button is pressed, after that, 
if necessary, you can make adjustments 
to the y-value.</source>
      <translation>Y da Posição A da CameraMovie. 

É definido quando o botão "Definir posição A" 
é pressionado, após isso, se necessário, 
você pode fazer ajustes no valor y.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="347"/>
      <source>Z of Position A of the MovieCamera.

It is set when the “Set position A” button 
is pressed, after that, if necessary, 
you can make adjustments to the z-value.</source>
      <translation>Z da Posição A da CameraMovie. 

É definido quando o botão "Definir posição A" é pressionado, 
após isso, se necessário, você pode fazer ajustes no valor z.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="356"/>
      <source>X of Position B of the MovieCamera.

It is set when the “Set position B” button 
is pressed, after that, if necessary, 
you can make adjustments to the x-value.</source>
      <translation>X da Posição B da CameraMovie. 

É definido quando o botão "Definir posição B" é pressionado, 
após isso, se necessário, você pode fazer ajustes no valor x.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="365"/>
      <source>Y of Position B of the MovieCamera.

It is set when the “Set position B” button 
is pressed, after that, if necessary, 
you can make adjustments to the y-value.</source>
      <translation>Y da Posição B da CameraMovie. 

É definido quando o botão "Definir posição B" é pressionado, 
após isso, se necessário, você pode fazer ajustes no valor y.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="374"/>
      <source>Z of Position B of the MovieCamera.

It is set when the “Set position B” button 
is pressed, after that, if necessary, 
you can make adjustments to the z-value.</source>
      <translation>Z da Posição B da CameraMovie. 

É definido quando o botão "Definir posição B" é pressionado, 
após isso, se necessário, você pode fazer ajustes no valor z.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="385"/>
      <source>Yaw of Position A of the MovieCamera.

It is set when the “Set position A” button 
is pressed, after that, if necessary, 
you can make little adjustments to the 
horizontal angle value of the camera.</source>
      <translation>Guinada da Posição A da CameraMovie. 

É definido quando o botão "Definir posição A" 
é pressionado, depois disso, se necessário, 
você pode fazer pequenos ajustes no valor 
do ângulo horizontal da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="395"/>
      <source>Pitch of Position A of the MovieCamera.

It is set when the “Set position A” button 
is pressed, after that, if necessary, 
you can make little adjustments to the 
vertical angle value of the camera.</source>
      <translation>Inclinação horizontal da Posição A da CameraMovie. 

É definido quando o botão "Definir posição A" 
é pressionado, após isso, se necessário, você 
pode fazer pequenos ajustes no valor do ângulo 
vertical da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="405"/>
      <source>Roll of Position A of the MovieCamera.

It is set when the “Set position A” button 
is pressed, after that, if necessary, 
you can make little adjustments to the 
roll value of the camera.</source>
      <translation>Rolagem da Posição A da CameraMovie. 

É definido quando o botão "Definir posição A" é pressionado, 
após isso, se necessário, você pode fazer pequenos ajustes 
no valor de rotação da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="415"/>
      <source>Yaw of Position B of the MovieCamera.

It is set when the “Set position B” button 
is pressed, after that, if necessary, 
you can make little adjustments to the 
horizontal angle value of the camera.</source>
      <translation>Guinada da Posição B da CameraMovie. 

É definido quando o botão "Definir posição B" 
é pressionado, após isso, se necessário, 
você pode fazer pequenos ajustes no 
valor do ângulo horizontal da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="425"/>
      <source>Pitch of Position B of the MovieCamera.

It is set when the “Set position B” button 
is pressed, after that, if necessary, 
you can make little adjustments to the 
vertical angle value of the camera.</source>
      <translation>Inclinação da Posição B da CameraMovie. 

É definido quando o botão "Definir posição B" 
é pressionado, após isso, se necessário, 
você pode fazer pequenos ajustes no valor 
do ângulo vertical da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="435"/>
      <source>Roll of Position B of the MovieCamera.

It is set when the “Set position B” button 
is pressed, after that, if necessary, 
you can make little adjustments to the 
roll value of the camera.</source>
      <translation>Rolagem da Posição B da CameraMovie. 

É definido quando o botão "Definir posição B" é pressionado, 
após isso, se necessário, você pode fazer pequenos ajustes 
no valor de rotação da câmera.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="447"/>
      <source>Zoom of Position A of the MovieCamera.

If Zoom of the MovieCamera (“Cam_04Zoom”) 
is enabled and after the Set position A button 
is pressed, you can adjust the angle in degrees 
you want to start the camera animation. 

Decreasing the value to zoom in and increasing 
to zoom out.</source>
      <translation>Zoom da posição A da CameraMovie. 

Se o Zoom da CameraMovie("Cam_04Zoom") 
estiver habilitado e após o botão "Definir posição A" 
ser pressionado, você pode ajustar o ângulo desejado 
em graus para iniciar a animação da câmera.

Diminuindo o valor para aproximar o zoom e 
aumentando para afastar o zoom.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="460"/>
      <source>Zoom of Position B of the MovieCamera.

If Zoom of the MovieCamera (“Cam_04Zoom”) 
is enabled and after the Set position B button 
is pressed, you can adjust the angle in degrees 
you want to finish the camera animation. 

Decreasing the value to zoom in and increasing 
to zoom out.</source>
      <translation>Zoom da posição B da CameraMovie

Se o Zoom da CameraMovie ("Cam_04Zoom") estiver habilitado
e após o botão "Definir posição B" ser pressionado, você pode ajustar 
o ângulo desejado em graus para finalizar a animação da câmera.

Diminuindo o valor para aproximar o zoom e aumentando para 
afastá-lo.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="56"/>
      <source>Initial step of the Clapperboard animation.

Indicate the step and/or frame which this 
section of the animation and/or recording 
will begin.</source>
      <translation>Passo inicial da animação da Claquete. 

Indique o passo e/ou quadro em que esta 
seção da animação e/ou gravação será iniciada.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="63"/>
      <source>End step of the Clapperboard animation.

Indicate the step which this section of 
the animation will finish.</source>
      <translation>Passo final da animação da Claquete. 

Indique o passo que esta seção da animação terminará.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="68"/>
      <source>Name of frame of the Clapperboard animation.

Indicate the main name of frames. Write a 
short name, as this will be inserted in 
the nomenclature of each one created.</source>
      <translation>Nome do quadro da animação da Claquete.

Indique o nome principal destes quadros. 
Escreva um nome abreviado, pois este será 
inserido na nomenclatura de cada um criado.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="74"/>
      <source>Width of frames of the Clapperboard animation.

Configure the width in pixels of the frames.</source>
      <translation>Largura do quadro da animação da Claquete. 

Configure a largura em píxeis dos quadros criados.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="78"/>
      <source>Height of frames of the Clapperboard animation.

Configure the height in pixels of the frames.</source>
      <translation>Altura dos quadros da animação da claquete.

Configure a altura dos quadros em pixels.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="82"/>
      <source>Output path of the Clapperboard animation frames.

Confirm the folder where the animation frames 
will be saved.

If you wish to preserve the generated images 
(in the case of rendered ones, for example), 
specify a folder other than the temporary folder.</source>
      <translation>Caminho de saída dos quadros da animação da Claquete

Confirme a pasta onde os quadros da animação serão salvos.

Se desejar preservar as imagens geradas(no caso de imagens 
renderizadas, por exemplo), especifique uma pasta diferente 
da pasta temporária.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="103"/>
      <source>Name of the video of the Clapperboard animation.

Indicate the main name for the created videos. 
If you prefer, chose to add manually “3D view“ 
text or “Render” one, according to the origin 
of the frames.</source>
      <translation>Nome do vídeo da animação da Claquete.

Indique o nome principal dos vídeos criados. 
Se preferir, opte por adicionar manualmente o 
texto “Vista 3D” ou “Render”, de acordo com 
a origem dos quadros.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="110"/>
      <source>Number of the video of the Clapperboard animation.

Indicate the initial number of the videos. This will 
be inserted in the nomenclature of each one created.</source>
      <translation>Número do vídeo da animação da Claquete.

Indique o número inicial dos vídeos. Este será 
inserido na nomenclatura de cada um criado.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="115"/>
      <source>Output path for the video of the Clapperboard 
animation.

Set path to folder to save created videos by 
clicking on the button with the three dots 
on the right.</source>
      <translation>Caminho de saída do vídeo da animação da Claquete.

Defina o caminho da pasta para salvar os vídeos 
criados clicando no botão com os três pontos à direita.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="122"/>
      <source>Fps of the video of the Clapperboard animation.

Indicate the frames per second (fps) of the video 
that will be created.</source>
      <translation>Fps do vídeo da animação da Claquete. 

Indique os quadros por segundo (fps) 
do vídeo que será criado.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="127"/>
      <source>Read-only. 

Indicates whether the animation video will play 
automatically after being generated.</source>
      <translation>Somente leitura. 

Indica se o video de animação 
será reproduzido automaticamente
após ser gerado.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="79"/>
      <source>Current step of the Clapperboard animation.

It is only indicative.</source>
      <translation>Passo atual da animação da Claquete. 

É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="89"/>
      <source>Total steps of the Clapperboard animation.

Indicates the number of steps through which 
the animation and/or the recording will be 
performed in this section.

It is only indicative.</source>
      <translation>Passos totais da animação da Claquete.

Indica o número de passo pelos quais será 
realizada a animação e/ou gravação nesta seção.

É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="100"/>
      <source>Animation fps of the Clapperboard.

Indicate the fps through which the 
section of the animation will be 
performed. 

It is a simulation and will depend 
on the computer performance.</source>
      <translation>Fps da animação da Claquete.

Indique a taxa de quadros (fps) na qual a
seção da animação será executada. 

Trata-se de uma simulação e dependerá 
do desempenho do computador.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="112"/>
      <source>Animation time of the Clapperboard.

Time in hours, minutes and seconds. 
It is only indicative.</source>
      <translation>Tempo de animação desta Claquete.

Tempo em horas, minutos e segundos. 
É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="123"/>
      <source>Name for this Clapperboard.

It will indicate the Clapperboard 
through which the animation and 
the recording will be performed. 

Write a short name, as this will 
be inserted in the nomenclature 
of each frame created.</source>
      <translation>Nome para esta Claquete. 

Indicará a Claquete escolhida através da qual 
será realizada a animação e a gravação. 

Escreva um nome abreviado, pois este será 
inserido na nomenclatura de cada quadro criado.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="136"/>
      <source>Take of the Clapperboard animation.

Indicate the take of each recording 
made. Write a short name, as this 
will be inserted in the nomenclature 
of each frame created.</source>
      <translation>Tomada da animação da Claquete.

Indique a tomada de cada gravação realizada. 
Escreva um nome abreviado, pois este será 
inserido na nomenclatura de cada quadro criado.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="146"/>
      <source>Selection of the Clapperboard animation.

Select the MovieCameras and/or the MovieObjects 
to animate with this Clapperboard.</source>
      <translation>Seleção da animação da Claquete. 

Selecione as CameraMovies e/ou 
ObjetosMovies para animar com esta Claquete.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="154"/>
      <source>Recording Clapperboard animation on or off.

It is activated by the “Enable recording” button 
and deactivated by the “Stop recording” one.</source>
      <translation>Gravação de animação da Claquete ligada ou desligada. 

É ativada pelo botão “Habilitar gravação” e desativada pelo 
botão “Parar gravação”.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="182"/>
      <source>“3D view” recording of the Clapperboard animation 
on or off.

Indicates whether the chosen camera will record 
FreeCAD 3D views.

It is indicative only.</source>
      <translation>Gravação da animação da claquete na “vista 3D”
ativada ou desativada.

Indica se a câmera escolhida gravará as vistas 3D 
do FreeCAD.

É apenas informativo.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="193"/>
      <source>“Render” recording of the Clapperboard animation 
on or off.

It indicates whether the chosen camera will record 
the renders images.

It is indicative only.</source>
      <translation>Ativa ou desativa a gravação da animação da Claquete em 'Render'.

Indica se a câmera selecionada gravará as imagens renderizadas.

É somente indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="216"/>
      <source>Input frames for the video of the Clapperboard 
animation.

Indicate the path to the folder containing the 
frames for creating a video by clicking on 
the three dots on the right.</source>
      <translation>Quadros de entrada para o vídeo da animação da Claquete.

Indique o caminho para a pasta que contém os 
quadros para a criação do vídeo clicando no botão 
com três pontos à direita.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="63"/>
      <source>List of objects of this MovieObjects.</source>
      <translation>Lista de objetos deste ObjetosMovie.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="86"/>
      <source>Initial step of the MovieObjects animation.

Indicate the step which this section of the 
animation will begin. Changes will only take 
effect after MovieObjects has been re-enabled.</source>
      <translation>Passo inicial da animação do ObjetosMovie. 

Indique o passo em que esta seção da animação 
começará. As alterações só terão efeito depois 
que ObjetosMovie for reativado.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="95"/>
      <source>Current step of the MovieObjects animation.

It is only indicative.</source>
      <translation>Passo atual da animação do ObjetosMovie. 

É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="102"/>
      <source>End step of the MovieObjects animation.

Indicate the step which this section of 
the animation will finish. Changes will 
only take effect after MovieObjects has 
been re-enabled.</source>
      <translation>Passo final da animação do ObjetosMovie. 

Indique o passo que esta seção da animação terminará. 
As alterações só terão efeito depois que ObjetosMovie for reativado.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="112"/>
      <source>Total steps of MovieObjects animation.

It is the result of the difference 
between End step (“Obj_03AnimEndStep”) 
and Initial step (“Obj_01AnimIniStep”).</source>
      <translation>Total de passos da animação do ObjetosMovie.

É o resultado da diferença entre o Passo final 
(“Cam_03AnimEndStep”) e o Passo inicial 
(“Cam_01AnimIniStep“).</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="121"/>
      <source>Animation fps of the MovieObjects.

Indicate the fps through which the 
section of the animation will be performed. 
It is a simulation and will depend on the 
computer performance. Changes will only take 
effect after MovieObjects has been re-enabled.</source>
      <translation>Fps da animação do ObjetosMovie. 

Indique o fps através do qual será realizado o trecho da animação. 
É uma simulação e dependerá do desempenho do computador. 
As alterações só terão efeito depois que o ObjetosMoviefor reativado.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="132"/>
      <source>Animation time of the MovieObjects, 
in in hours, minutes, and seconds. 

It is only indicative.</source>
      <translation>Tempo de animação do ObjetosMovie, em horas, 
minutos e segundos. 

É apenas indicativo.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="140"/>
      <source>MovieObjects animation on or off. 

It should not be changed manually, 
it is controlled by the animation buttons.</source>
      <translation>Animação da CameraMovie ativada ou desativada.

Não deve ser alterado manualmente, é controlado 
pelos botões de animação.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="150"/>
      <source>Route of the MovieObjects. 

Enable this so that the objects follow a route. 
You have to select a single segment on route 
selection (“Obj_02RouteSelection”) to use it. 
With the route activated, the coordinate 
settings for points A and B will be ignored, 
but not deleted. 

Disable the route and the animation of 
points A and B will be activated again, 
if it has already been configured before.</source>
      <translation>Rota dos ObjetosMovie. 

Habilite isto para que os objetos sigam uma rota. 
Você deve selecionar um único segmento na seleção 
de rota (“Obj_02RouteSelection“) para usá-lo. 
Com a rota ativada, as configurações de coordenadas 
dos pontos A e B serão ignoradas, mas não excluídas.

Desative a rota e a animação dos pontos A e B será 
ativada novamente, caso já tenha sido configurada 
anteriormente.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="166"/>
      <source>Route selection of the MovieObjects.

Choose the route through which the 
objects will be animate. You have to 
select a single segment such as: line, 
arc, circle, ellipse, B-spline or 
Bézier curve, from Sketcher or Draft 
Workbenches.</source>
      <translation>Seleção da rota do ObjetosMovie. 

Escolha a rota pela qual os objetos serão animados. 
Você deve selecionar um único segmento como: 
linha, arco, círculo, elipse, B-spline ou curva de 
Bézier, das Bancadas Sketcher ou Draft.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="180"/>
      <source>Rotation of the MovieObjects.

Enable this if you want to animate 
the objects angles.</source>
      <translation>Rotação do ObjetosMovie. 

Habilite isto se deseja animar 
os ângulos dos objetos.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="188"/>
      <source>Rotation by the centers of gravities 
of the MovieObjects.

Enable this if you want to rotate 
the objects by their centers of gravity.</source>
      <translation>Rotação pelos centros de gravidade do ObjetosMovie. 

Habilite isto se deseja girar os objetos 
de acordo com seus centros de gravidade.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="200"/>
      <source>Placements of PosA of this MovieObjects.</source>
      <translation>Posicionamentos da PosA deste ObjetosMovie.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="205"/>
      <source>Placements of PosB of this MovieObjects.</source>
      <translation>Posicionamentos da PosB deste ObjetosMovie.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="210"/>
      <source>Refresh on or off.

Enable this if you need to update 
at each step of the animation. 
Sometimes needed in combination 
with other object animation workbenches.

Note: This decreases the performance 
of object animations.</source>
      <translation>Atualização ativada ou desativada.

Habilite isto se precisar atualizar
a cada etapa da animação.
Às vezes, isso é necessário em conjunto
com outras bancadas de trabalho de animação de objetos.

Nota: Isso reduz o desempenho
das animações de objetos.</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="98"/>
      <source>To use images rendered by the Render Workbench, you must specify an existing Render Project!</source>
      <translation>Para usar imagens renderizadas pelo Render Workbench, você deve especificar um Projeto de Renderização existente!</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="91"/>
      <source>Type of frame of the Clapperboard animation.

Select the type of image to be generated: from 
the FreeCAD 3D view or rendered. For the latter 
option, you must specify a project already prepared 
using the Render Workbench.</source>
      <translation>Tipo de quadro da animação da Claquete.

Selecione o tipo de imagem a ser gerada: a partir
da vista 3D do FreeCAD ou renderizada. Para esta
última opção, você deve especificar um projeto já
preparado utilizando a Bancada de Trabalho Render.</translation>
    </message>
  </context>
  <context>
    <name>ContextMenu</name>
    <message>
      <location filename="../InitGui.py" line="117"/>
      <source>Cameras and Objects</source>
      <translation>Câmeras e Objetos</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="118"/>
      <source>Animation</source>
      <translation>Animação</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="119"/>
      <source>Record and Play</source>
      <translation>Gravar e Reproduzir</translation>
    </message>
  </context>
  <context>
    <name>CreateClapperboard</name>
    <message>
      <location filename="../MovieClapperboard.py" line="253"/>
      <source>Clapperboard</source>
      <translation>Claquete</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="255"/>
      <source>Create a Clapperboard to save the playback 
and recording settings of a MovieCamera or 
MovieObjects.

1. Select one or more MovieCameras in sequence 
and click “Clapperboard”.

2. You can also create an animation using only 
MovieObjects. Select one or more MovieObjects and 
click this button.

3. To configure and prepare for recording, 
click the “Enable recording” button.

4. To re-enable a Clapperboard, select one 
and click the “Enable an object for animation” 
button.</source>
      <translation>Crie uma claquete para salvar as configurações 
de reprodução e gravação de uma câmera ou
animação de objetos.

1. Selecione uma ou mais CameraMovies em sequência
e clique em "Claquete".

2. Você também pode criar uma animação usando apenas
ObjetosMovie. Selecione um ou mais e clique neste botão.

3. Para configurar e preparar a gravação, clique no botão 
"Habilitar gravação".

4. Para reativar uma Claquete, selecione uma
e clique no botão "Habilitar um objeto para animação".</translation>
    </message>
  </context>
  <context>
    <name>CreateMovieCamera</name>
    <message>
      <location filename="../MovieCamera.py" line="491"/>
      <source>MovieCamera</source>
      <translation>CameraMovie</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="493"/>
      <source>Creates a MovieCamera. 

1. Initially, a static camera is created (its positions 
A and B are identical). You can use it to control the 
display of object animations.

2. To animate an isolated camera that move e/or rotates 
establish its B position, since A has already been 
established(see the positions A and B instructions).

3. There are two ways to create a walkthrough:

Using a path. Enable “Cam_01Route” in the 
properties window and specify an previous line 
or continuous curves under “Cam_02_Route Selection”.

Using a sequence of cameras. Go to point B of the 
first created MovieCamera, then select it and click 
this button. Repeat this process until the last camera, 
then set point B for this one.

4. If you want the camera to point at an object, 
select “Follow an object or point” under 
“Cam_01_Target” and specify the object in 
“Cam_02_Target Object Selection”.

5. Make finer adjustments in the properties window, 
if necessary.

6. To view the animation, select (sequentially) one 
or more created MovieCameras and click the “Enable an 
object for animation” button. Control the animation 
using the “Animation tools” buttons.

7. To save a video from the animation, indicate the 
MovieCameras on a Clapperboard, to do so, see the 
corresponding instructions.</source>
      <translation>Cria uma CameraMovie (Câmera de Animação).

1. Inicialmente, é criada uma câmera estática (suas posições
A e B são idênticas). Você pode usá-la para controlar a
exibição de animações de objetos.

2. Para animar uma câmera isolada que se move e/ou rotaciona,
defina sua posição B, uma vez que a posição A já foi
estabelecida (consulte as instruções sobre as posições A e B).

3. Existem duas maneiras de criar um percurso de animação:

Usando um caminho. Habilite "Cam_01Route" na
janela de propriedades e especifique uma linha ou
curvas contínuas em "Cam_02_Route Selection".

Usando uma sequência de câmeras. Vá até o ponto B da
primeira CameraMovie criada, selecione-a e clique
neste botão. Repita esse processo até a última câmera
e, então, defina o ponto B para esta.

4. Se quiser que a câmera aponte para um objeto,
selecione "Seguir objeto ou ponto" em
"Cam_01_Target" e especifique o objeto em
"Cam_02_Target Object Selection".

5. Faça ajustes mais precisos na janela de propriedades,
se necessário.

6. Para visualizar a animação, selecione (sequencialmente) 
uma ou mais CameraMovies criadas e clique no botão 
"Habilitar um objeto para animação". Controle a animação 
usando os botões de "Ferramentas de animação".

7. Para salvar um vídeo da animação, indique as
CameraMovies em uma Claquete; para isso,
consulte as instruções correspondentes.</translation>
    </message>
  </context>
  <context>
    <name>CreateMovieObjects</name>
    <message>
      <location filename="../MovieObject.py" line="249"/>
      <source>MovieObjects</source>
      <translation>ObjetosMovie</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="251"/>
      <source>Objects can be animated from position A to B, 
follow a route, rotate around their 
gravity centers or a chosen axis.

1. First select a group of objects 
you want to animate and click here.

2. To animate one or more objects 
together from point A to B, that move 
and/or rotate, establish their A and B 
positions (see the positions A and B 
instructions).

3. Using a path. Enable “Obj_01Route” 
in the properties window and specify an 
previous line or continuous curves under 
“Obj_02_Route Selection”.

4. Rotating around their gravity centers. 
Specify the initial (PosA) and final (Pos B) 
rotations and enable the “Obj_Rotation CG” property.

5. Rotating around chosen axis. See “Rotation 
axis” instruction button.

6. Make finer adjustments in the properties window, 
if necessary.

7. To view the animation, select one or more created 
MovieObjects (sequentially) and click the “Enable an 
object for animation” button. Control the animation using 
the “Animation tools” buttons.

8. To save a video from the animation, indicate the 
MovieObjects on a Clapperboard, to do so, see the 
corresponding instructions.</source>
      <translation>Objetos podem ser animados da posição A para a B,
seguir uma rota ou rotacionar em torno de seus
centros de gravidade ou de um eixo escolhido.

1. Primeiro, selecione um grupo de objetos
que deseja animar e clique aqui.

2. Para animar um ou mais objetos
simultaneamente do ponto A ao B, fazendo-os
mover e/ou rotacionar, defina suas posições
A e B (consulte as instruções sobre as posições A e B).

3. Usando um caminho: habilite "Obj_01Route" na 
janela de propriedades e especifique uma linha 
ou curvas contínuas previamente criadas em 
"Obj_02_Route Selection".

4. Rotacionando em torno dos centros de gravidade:
especifique as rotações inicial (PosA) e final (Pos B)
e ative a propriedade "Obj_Rotation CG".

5. Rotacionando em torno de um eixo escolhido:
consulte as instruções no botão de "Eixo de rotação".

6. Faça ajustes mais precisos na janela de propriedades,
se necessário.

7. Para visualizar a animação, selecione (sequencialmente) 
um ou mais ObjectosFilme criados e clique no
botão "Habilitar um objeto para animação". 
Controle a animação usando os botões das 
"Ferramentas de animação".

8. Para salvar um vídeo da animação, indique os 
ObjectosFilme em uma Claquete; para isso, 
consulte as instruções correspondentes.</translation>
    </message>
  </context>
  <context>
    <name>DisableAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="136"/>
      <source>Disable any object for animation</source>
      <translation>Desativar qualquer objeto para animação</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="138"/>
      <source>1. To disable the animation status, click 
this button.</source>
      <translation>1. Para desativar o status da animação, clique
neste botão.</translation>
    </message>
  </context>
  <context>
    <name>EnableAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="76"/>
      <source>Enable an object for animation</source>
      <translation>Habilitar um objeto para animação</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="78"/>
      <source>1. Select a MovieCamera, MovieObjects or 
Clapperboard already set up, then click 
on this button to save the configurations 
made and activate it for the animation.

1.1 It is possible to create an animated 
sequence of MovieCameras and/or MovieObjects 
by selecting them as a group in the 
desired order.

2. After enabled, control the animation 
using the animation buttons.

3. To disable the animation, click ”Disables 
any object for animation” button.</source>
      <translation>1. Selecione uma MovieCamera, MovieObjects ou
Clapperboard já configurados e, em seguida, clique
neste botão para salvar as configurações
realizadas e ativá-los para a animação.

1.1 É possível criar uma sequência animada
de MovieCameras e/ou MovieObjects
selecionando-os como um grupo na
ordem desejada.

2. Após ativar, controle a animação
usando os botões de animação.

3. Para desativar a animação, clique no 
botão "Desativar qualquer objeto para animação".</translation>
    </message>
  </context>
  <context>
    <name>EnableMovieRecord</name>
    <message>
      <location filename="../MovieClapperboard.py" line="342"/>
      <source>Enable recording</source>
      <translation>Habilitar gravação</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="344"/>
      <source>Opens a task panel to configure the recording. 

1. After clicking on it, do not forget to confirm the 
folders to save the frames and the video in the 
opened task panel.

2. To start recording the animations, click the 
“Play Forward” or “Play Backward” buttons of 
the “Animations tools”.</source>
      <translation>Abre um painel de tarefas para configurar a gravação.

1. Após clicar nele, não se esqueça de confirmar as
pastas para salvar os quadros e o vídeo no
painel de tarefas aberto.

2. Para iniciar a gravação das animações, clique nos
botões "Reproduzir animação" ou "Reproduzir a 
animação para trás" das "Ferramentas de animação".</translation>
    </message>
  </context>
  <context>
    <name>EndMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="443"/>
      <source>Move to the end</source>
      <translation>Mover para o fim</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="445"/>
      <source>1. On the first click, it moves to the 
end of the animation of the current 
camera/objects.

2. On the second click, it goes to the 
beginning of the animation of the 
next camera/objects (if so).</source>
      <translation>1. No primeiro clique, avança para o
final da animação da câmera/objetos
atuais.

2. No segundo clique, vai para o
início da animação da próxima
câmera/objetos (se houver).</translation>
    </message>
  </context>
  <context>
    <name>ExcludeMovieObjects</name>
    <message>
      <location filename="../MovieObject.py" line="419"/>
      <source>Exclude a MovieObjects</source>
      <translation>Excluir um ObjetosMovie</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="421"/>
      <source>Select a MovieObjects that you want to exclude, 
then click on this button. 

Objects positions and angles will revert to 
the values set when the MovieObjects were 
created.</source>
      <translation>Selecione um ObjetosMovie que você deseja excluir 
e clique neste botão.

As posições e ângulos dos objetos serão revertidos para os valores 
definidos quando o ObjetosMovie foi criado.</translation>
    </message>
  </context>
  <context>
    <name>IniMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="170"/>
      <source>Return to beginning</source>
      <translation>Retornar ao início</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="172"/>
      <source>1. On the first click, it returns to the 
beginning of the animation of the 
current camera/objects and resets them. 

2. On the second click, it goes to the 
end of the animation of the 
previous camera/objects (if so).</source>
      <translation>1. No primeiro clique, retorna ao
início da animação da
câmera/objetos atuais e os reinicia.

2. No segundo clique, vai para o
final da animação da
câmera/objetos anteriores (se houver).</translation>
    </message>
  </context>
  <context>
    <name>InitGui</name>
    <message>
      <location filename="../InitGui.py" line="40"/>
      <source>Movie</source>
      <translation>Movie </translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="41"/>
      <source>Workbench to create and visualize animations and videos in FreeCAD</source>
      <translation>Bancada para criar e visualizar animações e vídeos no FreeCAD</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="69"/>
      <source>Cameras and objects tools</source>
      <translation>Ferramentas das câmeras e objetos</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="70"/>
      <source>Cameras and Objects</source>
      <translation>Câmeras e Objetos</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="85"/>
      <source>Animation tools</source>
      <translation>Ferramentas de animação</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="86"/>
      <source>Animation</source>
      <translation>Animação</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="94"/>
      <source>Record and play tools</source>
      <translation>Ferramentas de gravação e reprodução</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="95"/>
      <source>Record and Play</source>
      <translation>Gravar e Reproduzir</translation>
    </message>
    <message>
      <location filename="../InitGui.py" line="104"/>
      <source>Movie Workbench loaded</source>
      <translation>Bancada Movie carregada</translation>
    </message>
  </context>
  <context>
    <name>MovieAnimation</name>
    <message>
      <location filename="../MovieMessages.py" line="46"/>
      <source>Connection is enable, you must select 
one connection in “Cam_07Connection“!</source>
      <translation>A conexão está habilitada, você deve selecionar 
uma conexão em “Cam_07Connection“!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="246"/>
      <source>Take a step back does not work 
with ExplodedAssembly!</source>
      <translation>Retroceder um passo não funciona 
com ExplodedAssembly!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="427"/>
      <source>Move one step forward, 
does not work with ExplodedAssembly!</source>
      <translation>Mover um passo à frente não funciona 
com ExplodedAssembly!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="626"/>
      <source>Animation off.</source>
      <translation>Animação desativa.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="642"/>
      <source>Animation on.</source>
      <translation>Animação ativa.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="683"/>
      <source>Select a MovieCamera!</source>
      <translation>Selecione uma CameraMovie!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="708"/>
      <source>Select a MovieObjects!</source>
      <translation>Selecione um ObjetosMovie!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="723"/>
      <source>To animate the objects it is necessary 
to reset the MovieObjects B position or 
enable “Obj_01Route” and indicate a path 
at “Obj_02RouteSelection”!</source>
      <translation>Para animar os objetos, é necessário
redefinir a posição B do MovieObjects ou
habilitar “Obj_01Route” e indicar um caminho
em “Obj_02RouteSelection”!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="753"/>
      <source>Select a Clapperboard!</source>
      <translation>Selecione uma Claquete!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="761"/>
      <source>To enable the Clapperboard, it must have 
at least one MovieCamera or MovieObject 
specified in its “Clap_03 Animation 
Selection” property!</source>
      <translation>Para ativar a Claquete, é necessário especificar 
pelo menos uma CameraMovie ou ObjetosMovie 
em sua propriedade "Clap_03 Animation"!</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="796"/>
      <source>MovieCamera enabled.</source>
      <translation>CameraMovie habilitada.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="800"/>
      <source>MovieCamera and MovieObjects enabled.</source>
      <translation>CameraMovie e ObjetosMovie habilitados.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="804"/>
      <source>MovieCamera and connection enabled.</source>
      <translation>CameraMovie e conexão habilitados.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="809"/>
      <source>MovieObjects enabled.</source>
      <translation>ObjetosMovie habilitado.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="814"/>
      <source>Clapperboard enabled.</source>
      <translation>Claquete habilitada.</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="902"/>
      <source>Select MovieObjects in “Cam_06Enable“!</source>
      <translation>Selecione ObjetosMovies em “Cam_06Enable“!</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="41"/>
      <source>3D view</source>
      <translation>Vista 3D</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="42"/>
      <source>Render</source>
      <translation>Render</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="155"/>
      <source>The cameras and/or objects have 
been disabled for the animation!</source>
      <translation>As câmeras e/ou os objetos foram 
desativados para a animação!</translation>
    </message>
  </context>
  <context>
    <name>MovieCamera</name>
    <message>
      <location filename="../MovieCamera.py" line="192"/>
      <source>Camera</source>
      <translation>Câmera</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="192"/>
      <source>Camera and objects</source>
      <translation>Câmera e objetos</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="192"/>
      <source>Objects</source>
      <translation>Objetos</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="192"/>
      <source>Camera and connection</source>
      <translation>Câmera e conexão</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="192"/>
      <source>Connection</source>
      <translation>Conexão</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="220"/>
      <source>Free</source>
      <translation>Livre</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="220"/>
      <source>Follow an object or point</source>
      <translation>Seguir um objeto ou ponto</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="220"/>
      <source>Follow a route</source>
      <translation>Seguir uma rota</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="570"/>
      <source>MovieCamera #</source>
      <translation>CameraMovie #</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="578"/>
      <source>A sequenced MovieCamera was created!</source>
      <translation>Uma CameraMovie sequenciada foi criada!</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="583"/>
      <source>To create a sequenced MovieCameras, 
select the last MovieCamera inserted!</source>
      <translation>Para criar uma sequência de CameraMovies,
selecione a última CameraMovie inserida!</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="593"/>
      <source>MovieCamera</source>
      <translation>CameraMovie</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="716"/>
      <source>You have to select a render camera in “Cam_02Render_Selection”!</source>
      <translation>Você deve selecionar uma câmera de renderização em 
"Cam_02Render_Selection"!</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="676"/>
      <source>MovieCamera position A has been established.</source>
      <translation>Posição A da CameraMovie foi estabelecida.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="724"/>
      <source>MovieCamera position B has been established.</source>
      <translation>Posição B da CameraMovie foi estabelecida.</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="740"/>
      <source>You have to select a route in “Cam_02RouteSelection”!</source>
      <translation>Você deve selecionar uma rota em "Cam_02RouteSelection"!</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="815"/>
      <source>You have to select an object or 
point in “Cam_02TargetObjectSelection”!</source>
      <translation>Você deve selecionar um objeto ou ponto em 
"Cam_02TargetObjectSelection"!</translation>
    </message>
    <message>
      <location filename="../MovieCamera.py" line="828"/>
      <source>You have to select a render 
camera in “Cam_02Render_Selection”!</source>
      <translation>Você deve selecionar uma câmera render em 
"Cam_02Render_Selection"!</translation>
    </message>
  </context>
  <context>
    <name>MovieClapperboard</name>
    <message>
      <location filename="../MovieMessages.py" line="50"/>
      <source>Note: 
This version of FreeCAD seems unable to import cv2!
To create or play back a video, try a different version, like 1.0, 
or use the images generated here in an external recording program.</source>
      <translation>Nota:
Esta versão do FreeCAD parece não conseguir importar o cv2!
Para criar ou reproduzir um vídeo, tente uma versão diferente, como a 1.0,
ou utilize as imagens geradas aqui em um programa de gravação externo.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="296"/>
      <source>Select at least one MovieCamera or MovieObject 
to create a Clapperboard!</source>
      <translation>Selecione pelo menos uma CameraMovie ou ObjetosMovie 
para criar uma Claquete!</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="305"/>
      <source>To create a Clapperboard the pre-selected objects 
must be MovieCamera or MovieObjects!</source>
      <translation>Para criar uma Claquete, os objetos pré-selecionados
devem ser CameraMovie ou ObjetosMovie!</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="320"/>
      <source>Clapperboard</source>
      <translation>Claquete</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="502"/>
      <source>Recording settings</source>
      <translation>Configurações de gravação</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="509"/>
      <source>Enabled Clapperboard:</source>
      <translation>Claquete habilitada:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="513"/>
      <source>Instructions:</source>
      <translation>Instruções:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="515"/>
      <source>1. Configure the animation properties below and click “OK”. After this task panel closes, the recording will be ready to begin.

2. To start recording the animations, click the “Play Forward” or “Play Backward” buttons of the “Animations tools”. Click “Pause Animation” to pause it and “Stop Recording” to stop the recording process.

3. The final video will play automatically if the “Save video” and “Play video” checkboxes are enabled.</source>
      <translation>1. Configure as propriedades da animação abaixo e clique em "OK". Após o fechamento do painel de tarefas, a gravação estará pronta para começar.

2. Para iniciar a gravação das animações, clique nos botões "Reproduzir animação" ou "Reproduzir animação para trás" nas "Ferramentas de animação". Clique em "Pausar animação" para pausá-la e em "Parar gravação" para encerrar o processo de gravação.

3. O vídeo final será reproduzido automaticamente se as caixas de seleção "Salvar vídeo" e "Reproduzir vídeo" estiverem ativadas.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="541"/>
      <source>Frame properties:</source>
      <translation>Propriedades dos quadros:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="544"/>
      <source>Frame type:</source>
      <translation>Tipo do quadro:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="591"/>
      <source>Frame resolution:</source>
      <translation>Resolução do quadro:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="611"/>
      <source>Frame interval:</source>
      <translation>Intervalo dos quadros:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="613"/>
      <source>From frame:</source>
      <translation>Do quadro:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="620"/>
      <source>to:</source>
      <translation>ao:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="632"/>
      <source>Frame names:</source>
      <translation>Nomes dos quadros:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="640"/>
      <source>Frames output folder path:</source>
      <translation>Caminho da pasta de saída dos quadros:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="660"/>
      <source>Video properties:</source>
      <translation>Propriedades do vídeo:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="664"/>
      <source>Save video</source>
      <translation>Salvar vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="667"/>
      <source>Indicate whether you also want to save 
automatically the video after the frames 
are produced. 

Alternatively, you can record the video 
later by clicking the “Record video” 
button or use external recording software 
with the images generated.</source>
      <translation>Indique se você também deseja salvar automaticamente
o vídeo após a geração dos quadros.

Alternativamente, você pode gravar o vídeo mais tarde
clicando no botão "Gravar vídeo" ou utilizar
um software de gravação externo com as imagens
geradas.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="676"/>
      <source>Video name:</source>
      <translation>Nome do vídeo:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="683"/>
      <source>Video num.:</source>
      <translation>Vídeo nº:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="693"/>
      <source>Fps:</source>
      <translation>Quadros por segundo (fps):</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="700"/>
      <source>Video output folder path:</source>
      <translation>Caminho da pasta de saída de vídeo:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="753"/>
      <source>Play video</source>
      <translation>Reproduzir vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="844"/>
      <source>Select the output folder for the frames.</source>
      <translation>Selecione a pasta de saída para os quadros.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="886"/>
      <source>Warning</source>
      <translation>Aviso</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="871"/>
      <source>Select the output folder for the video</source>
      <translation>Selecione a pasta de destino do vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="951"/>
      <source>Recording is enabled! 
Click the animation playback button (forward or 
backward) to start recording the video. 
If the “Play video” option is enabled, 
it will play automatically at the end 
of the recording.</source>
      <translation>A gravação está ativada!
Clique no botão de reprodução da animação (avançar ou
retroceder) para iniciar a gravação do vídeo.
Se a opção “Reproduzir vídeo” estiver ativada,
o vídeo será reproduzido automaticamente ao final
da gravação.</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1096"/>
      <source>Select the folder to save the “3D view” frames</source>
      <translation>Selecione a pasta para salvar os quadros da “vista 3D”</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1112"/>
      <source>Select the folder to save the “Render” frames</source>
      <translation>Selecione a pasta para salvar os quadros renderizados</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1126"/>
      <source>Recording has been disabled!</source>
      <translation>A gravação foi desativada!</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1173"/>
      <source>{} frame {} of {} has been completed ({})</source>
      <translation>Quadro {}  {} de {} foi concluído ({})</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1201"/>
      <source>Select the frames folder to create video</source>
      <translation>Selecione a pasta de quadros para criar o vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1211"/>
      <source>Select the folder to save the video</source>
      <translation>Selecione a pasta para salvar o vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1253"/>
      <source>Recording of frame {} of {} ({}%)</source>
      <translation>Gravando quadro {} de {} ({}%)</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1265"/>
      <source>Output video to {}</source>
      <translation>Vídeo enviado para {}</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1284"/>
      <source>Select file to play</source>
      <translation>Selecione o arquivo para reproduzir</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1307"/>
      <source>Error: video file not found!</source>
      <translation>Erro: arquivo de vídeo não encontrado!</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="593"/>
      <source>Height:</source>
      <translation>Altura:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="599"/>
      <source>width:</source>
      <translation>largura:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="886"/>
      <source>Indicate a output folder to save the video before 
close the “Recording settings” task panel!</source>
      <translation>Indique uma pasta de destino para salvar o vídeo 
antes de fechar o painel da tarefa "Configurações 
de gravação"!</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="859"/>
      <source>Indicate a output folder to save the frames before 
close the “Recording settings” task panel!</source>
      <translation>Indique uma pasta de destino para salvar os 
quadros antes de fechar o painel de tarefas 
"Configurações de gravação"!</translation>
    </message>
    <message>
      <location filename="../MovieMessages.py" line="101"/>
      <source>Select a Render Project</source>
      <translation>Selecione um projeto de renderização</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="560"/>
      <source>Render Project:</source>
      <translation>Projeto de Render:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="566"/>
      <source>None</source>
      <translation>Nenhum</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="577"/>
      <source>Note:</source>
      <translation>Nota:</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="834"/>
      <source>The selected object is not a Render Project!</source>
      <translation>O objeto selecionado não é um Projeto de Renderização!</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="999"/>
      <source>Render Projects</source>
      <translation>Projetos de Render</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1000"/>
      <source>Type</source>
      <translation>Tipo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="1006"/>
      <source>Confirm</source>
      <translation>Confirmar</translation>
    </message>
  </context>
  <context>
    <name>MovieConnection</name>
    <message>
      <location filename="../MovieConnection.py" line="54"/>
      <source>You must have an animation of the 
ExplodedAssembly Workbench first!</source>
      <translation>Você deve ter uma animação da
Bancada de Trabalho ExplodedAssembly primeiro!</translation>
    </message>
  </context>
  <context>
    <name>MovieObjects</name>
    <message>
      <location filename="../MovieCamera.py" line="559"/>
      <source>A static MovieCamera was created!
To animate the MovieCamera without a MovieObjects
it is necessary to reset the MovieCamera B 
position or enable “CAm_01Route” and 
indicate a path at “Cam_02RouteSelection”!</source>
      <translation>Uma CameraMovie estática foi criada!
Para animar a CameraMovie sem ObjectosMovie,
é necessário redefinir a posição B da CameraMovie
ou habilitar "CAm_01Route" e indicar um caminho 
em "Cam_02RouteSelection"!</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="315"/>
      <source>Select at least one object to create a MovieObjects!</source>
      <translation>Selecione pelo menos um objeto para criar um ObjetosMovie!</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="349"/>
      <source>A MovieObject was created with the 
pre-established position A!</source>
      <translation>Um ObjetosMovie foi criado com a 
posição A pré-estabelecida!</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="356"/>
      <source>MovieObjects</source>
      <translation>ObjetosMovie</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="454"/>
      <source>Select a MovieObjects to exclude!
</source>
      <translation>Selecione um ObjetosMovie para excluir!</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="518"/>
      <source>First select the objects you want 
to rotate then the axis of rotation.</source>
      <translation>Primeiro selecione os objetos que deseja 
girar e depois o eixo de rotação.</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="585"/>
      <source>You have to select a route in “Obj_02RouteSelection”!</source>
      <translation>Você deve selecionar uma rota em 
"Cam_02RouteSelection"!</translation>
    </message>
  </context>
  <context>
    <name>PauseMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="312"/>
      <source>Pause the animation</source>
      <translation>Pausar animação</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="314"/>
      <source>Pauses the animation.</source>
      <translation>Pausa animação.</translation>
    </message>
  </context>
  <context>
    <name>PlayBackwardMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="262"/>
      <source>Play backward the animation</source>
      <translation>Reproduzir animação para trás</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="264"/>
      <source>Plays backward the animation.</source>
      <translation>Reproduz a animação de trás para frente.</translation>
    </message>
  </context>
  <context>
    <name>PlayMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="352"/>
      <source>Play the animation</source>
      <translation>Reproduzir animação</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="354"/>
      <source>Plays the animation.</source>
      <translation>Reproduz a animação.</translation>
    </message>
  </context>
  <context>
    <name>PlayVideo</name>
    <message>
      <location filename="../MovieClapperboard.py" line="460"/>
      <source>Play video</source>
      <translation>Reproduzir vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="462"/>
      <source>Play an existing video by indicating its file path.

Note: It works only with FreeCAD versions 
that import the cv2 module, like 1.0.</source>
      <translation>Reproduza um vídeo existente indicando o caminho do arquivo.

Nota: Funciona apenas com versões do FreeCAD
que importam o módulo cv2, como a 1.0.</translation>
    </message>
  </context>
  <context>
    <name>PostMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="402"/>
      <source>Move one step forward</source>
      <translation>Mover um passo à frente</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="404"/>
      <source>Moves the animation one step forward.</source>
      <translation>Move a animação um passo à frente.</translation>
    </message>
  </context>
  <context>
    <name>PrevMovieAnimation</name>
    <message>
      <location filename="../MovieAnimation.py" line="222"/>
      <source>Take a step back</source>
      <translation>Retroceder um passo</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="224"/>
      <source>Moves the animation one step back.</source>
      <translation>Move a animação um passo para trás.</translation>
    </message>
  </context>
  <context>
    <name>RecordVideo</name>
    <message>
      <location filename="../MovieClapperboard.py" line="408"/>
      <source>Record video</source>
      <translation>Gravar vídeo</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="410"/>
      <source>Creates a video from a sequence 
of created frames (images).

1. Click this button and select the 
folder containing the image sequence 
of a created animation.

2. Next, indicate the folder where the 
video should be saved and specify its name.

3. At the end of the process, the video 
will play automatically.

4. If you want to watch the video again, 
click the “Play video” button and select 
the corresponding file.

Note: It works only with FreeCAD versions 
that import the cv2 module, like 1.0.</source>
      <translation>Cria um vídeo a partir de uma sequência
de quadros (imagens) gerados.

1. Clique neste botão e selecione a
pasta que contém a sequência de imagens
de uma animação criada.

2. Em seguida, indique a pasta onde o
vídeo deve ser salvo e especifique o nome dele.

3. Ao final do processo, o vídeo
será reproduzido automaticamente.

4. Se quiser assistir ao vídeo novamente,
clique no botão "Reproduzir vídeo" e selecione
o arquivo correspondente.

Nota: Funciona apenas com versões do FreeCAD
que importam o módulo cv2, como a 1.0.</translation>
    </message>
  </context>
  <context>
    <name>SetMovieObjectsAxis</name>
    <message>
      <location filename="../MovieObject.py" line="377"/>
      <source>Rotation axis</source>
      <translation>Eixo de rotação</translation>
    </message>
    <message>
      <location filename="../MovieObject.py" line="379"/>
      <source>1. First create a MovieObjects, set their rotation A and B.

2. Then, define a rotation axis for objects of a created 
MovieObject. The rotation axis can be a line (from Draft 
or Sketch) or even an object edge.

3. After that, select first the objects you want to rotate, 
then the axis and click this button.

4. To erase these settings, enable the MovieObjects and 
click on “Set position B” button.</source>
      <translation>1. Primeiro, crie ObjectosMoviee defina suas rotações A e B.

2. Em seguida, defina um eixo de rotação para os objetos
de um ObjetosMovie criado. O eixo de rotação pode ser
uma linha (do Draft ou Sketch) ou até mesmo uma aresta de um objeto.

3. Depois disso, selecione primeiro os objetos que deseja rotacionar,
em seguida o eixo e clique neste botão.

4. Para apagar essas configurações, selecione o ObjectosMovie e
clique no botão "Definir posição B".</translation>
    </message>
  </context>
  <context>
    <name>SetMoviePosA</name>
    <message>
      <location filename="../MovieAnimation.py" line="497"/>
      <source>Set position A</source>
      <translation>Definir posição A</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="499"/>
      <source>Applicable for creating an animation from 
point A to B (not when the MovieCamera 
target or MovieObjects are set up to 
follow a route).

1. First, select and activate the 
MovieCamera or MovieObjects you want 
to configure.

2. For MovieCameras, position the 3D 
view with the desired framing to be the start 
of the animation (position A), then click on 
Set position A.

3. For MovieObjects, position, rotate 
or keep them in their current position, 
then click on this button.</source>
      <translation>Aplicável para criar uma animação do
ponto A ao B (não quando o alvo da
MovieCamera ou os MovieObjects estiverem
configurados para seguir uma rota).

1. Primeiro, selecione e ative a
CameraMovie ou os ObjetosMovie que
você deseja configurar.

2. Para CameraMovie, posicione a
vista 3D com o enquadramento desejado
para o início da animação (posição A) e,
em seguida, clique em "Definir posição A".

3. Para ObjetosMovie, posicione-os,
roteacione-os ou mantenha-os na posição
atual e, depois, clique neste botão.</translation>
    </message>
  </context>
  <context>
    <name>SetMoviePosB</name>
    <message>
      <location filename="../MovieAnimation.py" line="548"/>
      <source>Set position B</source>
      <translation>Definir posição B</translation>
    </message>
    <message>
      <location filename="../MovieAnimation.py" line="550"/>
      <source>Applicable for creating an animation from 
point A to B (not when the MovieCamera 
target or MovieObjects are set up to 
follow a route).

1. Select and activate the MovieCamera 
or MovieObjects you want to configure.

2. For MovieCameras, position the 3D 
view with the desired framing to be 
the end of the animation (position B), 
then click on Set position B.

3. For MovieObjects, position and/or 
rotate them to the final position, then 
click on this button.</source>
      <translation>Aplicável para criar uma animação do
ponto A ao B (não quando o alvo da
CameraMovie ou os ObjetosMovie estiverem
configurados para seguir uma rota).

1. Selecione e ative a CameraMovie 
ou os ObjetosMovie que deseja configurar.

2. Para CameraMovie, posicione a
visualização 3D com o enquadramento
desejado para o final da animação
(posição B) e, em seguida, clique em
"Definir posição B".

3. Para ObjetosMovie, posicione-os e/ou
rotacione-os para a posição final e,
em seguida, clique neste botão.</translation>
    </message>
  </context>
  <context>
    <name>StopMovieRecord</name>
    <message>
      <location filename="../MovieClapperboard.py" line="383"/>
      <source>Stop recording</source>
      <translation>Parar gravação</translation>
    </message>
    <message>
      <location filename="../MovieClapperboard.py" line="385"/>
      <source>Stops the animation recording.</source>
      <translation>Interrompe a gravação da animação.</translation>
    </message>
  </context>
</TS>
