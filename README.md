<!--Title-->
<h1> Pomodoro Timer GUI Python Vers. </h1>

<!--Description-->
<h2> Description </h2>
  <!--Describe the project (what is a pomodoro timer?)-->
  <p> Pomodoro Timer GUI emulates the Pomodoro Technique which is a time management method that breaks work into intervals separated by short or long breaks.</p>
       
<!--Technologies and Frameworks Used-->
<h2> Technologies and Frameworks Used </h2>
  <p> Make sure to install the DearPyGUI and Playsound Modules for it to work. You can follow the installation to DearPyGUI <a href="https://github.com/hoffstadt/DearPyGui"> here </a> and Playsound <a href="https://pypi.org/project/playsound/"> here </a>.</p> 
  <p> Alternatively just do <i> pip install dearpygui==1.0.2 </i> and <i> pip install playsound==1.2.2 </i> on your terminal</p>
  <ul>
    <li> <i> PyCharm IDE </i> </li>
    <li> <i> DearPyGUI v1.0.2 (GUI Framework) </i> </li>
    <li> <i> Playsound Module v1.2.2 </i></li>
    <li> <i> Python 3.8+ </i> </li>
  </ul>

<!--Demonstration + How to Use-->
<h2> Demonstration & How to Use </h2>
  <p> You can now just run the Pomodoro Timer.exe from the dist folder </p>
  
  <!--Configuring the settings-->
  <h3> Configuring the Settings </h3>
    <p> Configured settings will be stored on local json file after starting the session </p>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/settings_example.gif"/>
  
  <!--Checking User Data-->
  <h3> Checking User Data </h3>
    <p> User can check out the total mins of focus and the total pomodoros they have done so far </p>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/check_user_data.gif"/>
    
  <!--Functional Buttons-->
  <h3> Timer Buttons </h3>
    <ul>
      <li> Pause - Pauses the timer </li>
      <li> Stop - Stops the timer, and returns user back to the setting configurations </li>
      <li> Restart - Resets the timer to the original timer and the Pomodoro Counter </li>
      <li> Resume - (only available once the user pauses the timer) Resumes the timer </li>
    </ul>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/buttons_example.gif"/>

  <!--Finished-->
  <h3> Timer Finished </h3>
    <p> Once the timer finishes, a small dialog appears that asks the user either to continue with focusing or take a break. The day's pomodoro counter will be incremented and    saved to the json file</p>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/timer_finished.gif"/>
    <p> (For Window 10 Users only) Once the timer is finished it will also display a notification </p>
    <img src="https://github.com/gnikkoch96/Python-Pomodoro-Timer-GUI/blob/master/resources/read_me%20stuff/notification_example.png"/>
    
<!--What I learned-->
<h2> What I learned </h2> 
  <ul>
    <li> When using a new framework like this, it is important to visit their communities (i.e. Discord and Reddit) for help as usually problems don't appear often in popular            sites like stackoverflow </li>
    <li> Python has a more cleaner way of setting up a GUI as opposed to in Java. </li>
    <li> Since threading was involved in counting down the timer and updating the GUI, I had to make them into daemon threads which meant that once the main thread ends it                ends the process almost immediately </li> 
    <li> If I wanted a make a thread wait for another thread, I'd have to use the join() </li> 
    <li> I found it easier to create the GUI that I wanted with DearPyGUI as opposed to Swing framework from Java. </li>
    <li> The reason why I chose DearPyGUI over other frameworks like Tkinter, QT, or Kivy is that it is open-source, I don't need to worry about the terms and conditions especially for a small project like this, and it has a very active community (Discord and Reddit). </li>
  
  </ul>

<h2> Credit and Notice </h2>
<p> The images I used for this project are not mine. You can find the sites where I got the images below </p>
<ul>
  <li> <a href="https://opengameart.org/content/little-tomato"> Tomato Character </a> </li>
  <li> <a href="https://cliparts.zone/clipart/585233"> Kid Studying </a> </li>
  <li> <a href="https://lh3.googleusercontent.com/proxy/nAzHFtxsck04b8cHE6bKLNxLwbhHRjetcP4o48rZj3dmunBCrl842cz3RKILtNaPUS1lgM7JcW3lJRl9VkGRNB3Y6k98U9RDzUSng7LnSo8AUZSWDkKpvFK8IAyvIFZMNe9MQnxNgIzc3TI"> Marathon Runner Finishing Race </a> </li>
  <li> <a href="https://www.flaticon.com/free-icon/tomato_1202125?term=tomato&page=1&position=1&page=1&position=1&related_id=1202125&origin=tag"> Tomato Icon by Pixel Perfect </a>
</ul>
