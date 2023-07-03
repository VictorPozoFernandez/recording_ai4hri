import rospy
from pynput import keyboard
from std_msgs.msg import String

audio_control = "STOP"
keyword = 'p'

def on_press(key):
    global audio_control
    try:
        if key.char == keyword:
            audio_control = "RESUME"
            msg = String()
            msg.data = audio_control
            pub.publish(msg)
    except AttributeError:
        pass  # Ignore special keys like ctrl, alt, etc.

def on_release(key):
    global audio_control
    try:
        if key.char == keyword:
            audio_control = "STOP"
            msg = String()
            msg.data = audio_control
            pub.publish(msg)
    except AttributeError:
        pass  # Ignore special keys like ctrl, alt, etc.

def audio_control_publisher():
    global pub
    rospy.init_node('audio_control_publisher', anonymous=True)
    pub = rospy.Publisher('/ai4hri/audio_control', String, queue_size=10)
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == "__main__":
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            audio_control_publisher()
    except rospy.ROSInterruptException:
        pass