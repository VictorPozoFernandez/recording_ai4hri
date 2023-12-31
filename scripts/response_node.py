import os
from std_msgs.msg import String
import os
import rospy

PEPPER = rospy.get_param('/response/PEPPER')

if PEPPER == False: 
    try:
        from elevenlabs import generate, stream, set_api_key
        set_api_key(os.environ.get("ELEVENLABS_API_KEY"))
    except:
        pass
else:
    from nao_interaction_msgs.srv import Say


def main():

    # Initialize the agent ROS node and subscribe to utterance topic
    rospy.init_node("response_robot", anonymous=True)
    rospy.loginfo("Node response_robot initialized. Listening...")
    rospy.Subscriber("/ai4hri/response_robot", String, callback)
    
    rospy.spin()


def callback(msg):

    # Get new utterance from message and classify it
    utterance = msg.data
    rospy.sleep(1)

    if PEPPER == True:
        Send_utterance_to_Pepper(utterance) #Publish the utterance text in the tts Ros service

    else:

        try:
            audio_stream = generate( text=utterance, stream=True)
            stream(audio_stream)
        except:
            pass
    
    for i in range (3):
        rospy.sleep(1)


def Send_utterance_to_Pepper(utterance):

    rospy.wait_for_service('/naoqi_driver/tts/say')  # Replace 'say_service' with your service's name

    try:
        say_service = rospy.ServiceProxy('/naoqi_driver/tts/say', Say)  # Create a handle to the service
        say_service(utterance)  # Call the service
    
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")


if __name__ == '__main__':

    try:
        main()
    
    except rospy.ROSInterruptException:
        pass