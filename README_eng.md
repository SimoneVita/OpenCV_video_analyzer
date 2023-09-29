# OpenCV_video_analyzer
Чтобы посмотреть Readme на русском - [нажми сюда](https://github.com/SimoneVita/OpenCV_video_analyzer/blob/main/README.md)
_________________________________________________
## Description
Video analyzing app, which detects actions and save frames and activity log.

### OpenCV_video_analyzer - features:

- Analyzes video of any format.
- Saves frames with contour of action persons/things.
- Specifies the time of action - start and finish.
- Can analyse more, than 1 video at once (look for 'Specific' in 'Technical description').
- Frames of different videos sorts to different directories.
 
_____________________________________________________

## Technical description

### Specific:
The app can analyze a number of videos and it's efficiency is not monitored and controlled now. Tested on M1 Pro chip without cores limitation. Experimentally analyziong of 10 simultaneous videos (each lasts 1.5 hours) was successful.

### Applyed technologies:
 > opencv-python==4.8.0.76
 > numpy==1.26

### How to lounch the app:

Clone the repository via terminal:

```
git clone git@github.com:SimoneVita/OpenCV_video_analyzer.git
```

Make the directory for unanalyzed videos:
```
mkdir videos
```

Put videos to analyze in the 'videos/' directory

It's possible to assign any other convenient directory by changing the constant ```path_to_vid``` in main.py

Create and activate a virtual environment:

```
python3 -m venv venv
```

```
source venv/bin/activate
```
Install dependencies from requirements.txt:
```
pip install -r requirements.txt
```
Start the app:
```
python3 main.py
```

______________________________________
### Author
Vitaly Simonenko (https://github.com/SimoneVita)

### License
BSD 3-Clause License
