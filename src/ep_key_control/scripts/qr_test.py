#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from robomaster import robot
import cv2
import pyzbar.pyzbar as pyzbar

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded_qr_codes = pyzbar.decode(gray)

    for qr_code in decoded_qr_codes:
        print("QR code data: ", qr_code.data.decode())

        # Publish QR code data as a string
        pub.publish(qr_code.data.decode())

    cv2.imshow("QR Code Reader", gray)
    print("success to get frame")
    cv2.waitKey(1)
    return True


if __name__ == '__main__':
    rospy.init_node("qr_code")
    pub = rospy.Publisher('/qr_code_data', String, queue_size=10)
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="rndis")
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream(display=False)

    try:
        while not rospy.is_shutdown():
            img = ep_camera.read_cv2_image(strategy="newest")
            if process_frame(img):
                pass    
            else:
                print("Failed to read frame")
                break
    except KeyboardInterrupt:
        print("Shutting down")

    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()

    ep_robot.close()
