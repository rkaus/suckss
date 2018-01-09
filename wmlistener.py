from boat import *
import rospy
from std_msgs.msg import String
boatsky = Boat()
def callback(data):
     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
     if data.data == 'Forward':
           boatsky.forward()
     if data.data == 'Backward':
           boatsky.backwards()
     if data.data == 'Left':
           boatsky.left()
     if data.data == 'Right':
           boatsky.right()
     if data.data == 'B':
           boatsky.stop()
     if data.data == 'Done':
           boatsky.cleanup()     
     if data.data == 'Conveyor':
           boatsky.conveyor()     

def listener():
 
     # In ROS, nodes are uniquely named. If two nodes with the same
     # node are launched, the previous one is kicked off. The
     # anonymous=True flag means that rospy will choose a unique
     # name for our 'listener' node so that multiple listeners can
     # run simultaneously.
     rospy.init_node('listener', anonymous=True)
 
     rospy.Subscriber("chatter", String, callback)
 
     # spin() simply keeps python from exiting until this node is stopped
     rospy.spin()
if __name__ == '__main__':
     listener()
