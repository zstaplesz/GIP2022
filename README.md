# GIP2022
Beat detection algorithm for UoB Yr4 project: 'A wearable sensory device aid that reproduces the feeling of music as vibration for the profoundly deaf'

This code is submitted towards a Mechanical and Electrical MEng degree at the University of Bristol, for the Year 4 Group Industrial Project MENGM0061.

All files must be in same directory. The main script is the 'BeatDetectionAlgorithm', which runs the Python code to detect beats and strengths of the 
3 provided music samples. The 'PredictedBeats' script contains information on actual beat timings of the samples used in this investigation, and is not
required to be opened. The user can choose between the 3 samples by uncommenting line groups [23, 24, 25], [27, 28, 29], or [31, 32, 33]. Only one group
must be uncommented at any time. Music samples can be found on freesound.org and are as follows in the order of name used in investigation, name of sample on freesound.org, and artist (user):

'_Piano_1.wav', Piano,	Bradovic

'_Drum_1.wav', hip hop drum beat.wav, Simon_Lacelle

'_Full_Song_2_Cut.wav', Rock music.wav, Jibey-

The algorithm script contains all 3 threshold detection methods. Optimal is active by default, but the general or auto-threshold method
can be activated by uncommenting lines 73 and 74 respectively.

The beat detection can function without a connected Arduino with no changes, but the required code is present within the Python file and as an Arduino
script ('BeatDetectionArduino') to run the entire beat detection device if the resources outlined in the report are present.

