
# Overview

* https://github.com/rohansb/knurld-apis are accessed and implemented to do the audio verification of a user based on
 the audio .wav file uploaded by user.

* To run the app, you may clone my repository and just do - `python knurld/index.py` from command line.
 Then you can go to browser and hit - http://127.0.0.1:5000/ Please use username "kramer" and password "knurld" to do
 log in attempts.

    user_pass = {'kramer': 'knurld',
                'elaine': 'knurld',
                'jerry': 'knurld',
                'geroge': 'knurld'}

    hosted .wav files:
    
     kramer: http://audiofiles2.jerryseinfeld.nl/kramer_theassman.wav (knurld verification-id: not created)
     
     elaine: http://audiofiles2.jerryseinfeld.nl/hooker.wav (knurld verification-id: a67a3f337823e2d56ec264f8c30c9375)
     
     jerry: http://audiofiles2.jerryseinfeld.nl/icaniple.wav (knurld verification-id: not created)


* At this point only use 'elaine' has a verification-id in the system and she should be able to log-in while other's wont,
 even though their login username and password are correct. Please use externally hosted audio verification files
 from mentioned above.

Please reference the code for implementation details
