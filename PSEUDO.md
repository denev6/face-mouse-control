# main
```
Open camera  

INIT Process object  
INIT App object  

REPEAT  
  Waiting for button clicks from the sidebar  
  Run Process object  
UNTIL the user exit the program  

Close camera  
```

## Process
```
READ single frame from the camera  

Detect landmarks from the frame using Detector  

IF the sidebar is not in the paused state THEN  
  COMPUTE facial direction  
  Move cursor by facial direction  
END IF  

IF blinked for particular frames THEN  
  Click where the current cursor is  
END IF  

IF there is a command from the sidebar THEN  
  Execute the command using the Controller  
END IF  
```


# EAR Setting
```
Open camera  

REPEAT  
  GET opened eye aspect ratio from each frame  
UNTIL 150 frames are detected successfully  

REPEAT  
  GET closed eye aspect ratio from each frame  
UNTIL 150 frames are detected successfully  

Drop outliers using IQR  
COMPUTE eye aspect ratio threshold  

Close camera  
```