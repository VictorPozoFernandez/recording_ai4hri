import rospy
from audio_common_msgs.msg import AudioData
from std_msgs.msg import String
import speech_recognition as sr
import numpy as np

def callback(msg):
    global audio_control
    audio_control = msg.data


def record_audio(pub):

    global audio_control
    audio_control=False

    # Initialize the recognizer and set energy and pause thresholds
    r = sr.Recognizer()
    energy_threshold = 220

    # Open the microphone with the specified sample rate and device index
       
    try:  

        # Print available microphones PC

        rospy.sleep(2)
        print("")
        for index, name in enumerate(sr.Microphone.list_microphone_names()): print(f'{index}, {name}')
        print('')
        counter = input('Choose a microphone device:')

        with sr.Microphone(sample_rate=16000,  device_index=int(counter)) as source:

            # Clear the console
            for x in range(4):
                print("")
            rospy.loginfo("Node record_node initialized. Listening...")

            complete_audio = None
            counter = 0

            # Record audio while the ROS node is running
            while not rospy.is_shutdown():
                
                audio = r.record(source, duration=1)  # Record for a small duration

                if audio_control == "RESUME":

                        # Concatenate audio chunks if any speech is detected
                    if complete_audio == None:
                        complete_audio = sr.AudioData(previous_audio.frame_data + audio.frame_data, audio.sample_rate, audio.sample_width)
                    else:
                        complete_audio = sr.AudioData(complete_audio.frame_data + audio.frame_data, audio.sample_rate, audio.sample_width)
                
                elif (audio_control == "STOP") and (complete_audio != None):              
                    
                    complete_audio = sr.AudioData(complete_audio.frame_data + audio.frame_data, audio.sample_rate, audio.sample_width)
                    wav_data = complete_audio.get_wav_data()
                    pub.publish(wav_data)
                    complete_audio = None
                    
                else:
                    previous_audio = audio
                    complete_audio = None
                
        
    except Exception as e: 
            print(e)
            print("Microphone not found")


def main():
    # Initialize the whisper ROS node and a publisher for the AI4HRI utterance topic
    rospy.init_node("audio_recorder", anonymous=True)
    pub = rospy.Publisher('/ai4hri/audio_data', AudioData, queue_size= 1)
    rospy.Subscriber("/ai4hri/audio_control", String, callback)

    record_audio(pub)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print(rospy.ROSInterruptException)
        pass
