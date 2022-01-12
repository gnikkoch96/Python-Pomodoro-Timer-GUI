<!--Title-->
<h1> Pomodoro Timer GUI Python Vers. </h1>

<!--Description-->
<h2> Description </h2>
  <!--Describe the project (what is a pomodoro timer?)-->
  <p> The Pomodoro Technique is a way to manage focus time for better performance. The user has to choose a task to focus on for a set period of time, and           once that time has finished, then the user can take a small break or a long break depending on how my sessions the user has done (usually after 4 pomodoros focus                 sessions).</p>
  
  <!--Explain why you made it-->
  <p> Pomodoro Timer GUI Python Vers. is a recreation of my Pomodro Timer GUI Java Vers. Since I have had some experience creating Swing GUIs using Java, I wanted to compare
      the differences between these languages. For the most part the framework I've chosen (DearPyGUI) and the Swing framework were entirely different. For example instead
      of actionListeners, we'd have to reference a callback method for the buttons. Also, we can generate multiple windows within one frame to appear at once with DearPyGUI.           And above else I found it easier to create the GUI that I wanted with DearPyGUI as opposed to Swing. </p> 
      
  <p> The reason why I chose DearPyGUI over other frameworks like Tkinter, QT, or Kivy is that it is open-source, I don't need to worry about the terms and conditions especially       for a small project like this, and it has a very active community (Discord and Reddit). </p>
      
<!--Technologies and Frameworks Used-->
<h2> Technologies and Frameworks Used </h2>
  <p> Make sure to install the DearPyGUI and Playsound Modules for it to work. You can follow the installation to DearPyGUI <a href="https://github.com/hoffstadt/DearPyGui">           here </a>, and install Playsound <a href="https://pypi.org/project/playsound/"> here </a>.</p> 
  <p> You could always just do <i> pip install dearpygui==1.0.2 </i> and <i> pip install playsound. </i> </p>
  <p> <b> Update: </b> You can now just run the main.exe file from the dist folder </p>
  <ul>
    <li> <i> PyCharm IDE </i> - The environment used to code in Python </li>
    <li> <i> DearPyGUI Framework v1.0.2 </i> - Framework used to create the GUI for this project </li>
    <li> <i> Playsound Module v1.2.2 </i> - Imported the playsound module so that I could alert the user that their session was done </li>
    <li> <i> Python 3.8 </i> </li>
  </ul>

<!--Demonstration + How to Use-->
<h2> Demonstration & How to Use </h2>
  <!--Configuring the settings-->
  <h3> Configuring the Settings </h3>
    <ol> 
      <li> Choose how long you want to focus </li>
      <li> Choose how long your small break is going to be </li>
      <li> Choose how long your long break is going to be </li>
      <li> Click on the Start Pomodoro button </li>
    </ol>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/Settings%20to%20Timer.gif"/>
  
  <!--Functional Buttons-->
  <h3> Timer Buttons </h3>
    <ul>
      <li> Pause - Pauses the timer </li>
      <li> Stop - Stops the timer, and returns user back to the setting configurations </li>
      <li> Restart - Resets the timer to the original timer and the Pomodoro Counter </li>
      <li> Resume - (only available once the user pauses the timer) Resumes the timer </li>
    </ul>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/Functional%20Buttons.gif"/>

  <!--Finished-->
  <h3> Timer Finished </h3>
  <p> Once the timer finishes, a small dialog appears that asks the user either to continue with focusing or take a break. Also by default, if the user closes the dialog, it 
      will start another focus session. Note that the user can not give focus to other things while the dialog is still open. </p>
  <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/Timer%20Finish.gif"/>
  
  <!--What happens after 4 sessions-->
  <p> After 4 pomodoro sessions, the small break button will be replaced with a long break button. </p>
  <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/Long%20Break%20Display.png"/>
  
<!--What I learned-->
<h2> What I learned </h2> 
  <ul>
    <li> When using a new framework like this, it is important to visit their communities (i.e. Discord and Reddit) for help as usually problems don't appear often in popular            sites like stackoverflow </li>
    <li> Python has a more cleaner way of setting up a GUI as opposed to in Java. </li>
    <li> Since threading was involved in counting down the timer and updating the GUI, I had to make them into daemon threads which meant that once the main thread ends it                ends the process almost immediately </li> 
    <li> If I wanted a make a thread wait for another thread, I'd have to use the join() </li> 
  </ul>

<h2> Credit and Notice </h2>
<p> The images I used for this project are not mine. You can find the sites where I got the images below </p>
<ul>
  <li> <a href="https://opengameart.org/content/little-tomato"> Tomato Character </a> </li>
  <li> <a href="https://cliparts.zone/clipart/585233"> Kid Studying </a> </li>
  <li> <a href="https://lh3.googleusercontent.com/proxy/nAzHFtxsck04b8cHE6bKLNxLwbhHRjetcP4o48rZj3dmunBCrl842cz3RKILtNaPUS1lgM7JcW3lJRl9VkGRNB3Y6k98U9RDzUSng7LnSo8AUZSWDkKpvFK8IAyvIFZMNe9MQnxNgIzc3TI"> Marathon Runner Finishing Race </a> </li>
</ul>
