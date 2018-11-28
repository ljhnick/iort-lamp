import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    handType = ""
    handSphereRadius = 0
    fingerNumber = 0
    palmPosition = []
    palmNormal = []
    keyTapPosition = []
    swipeStartPos = []

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        self.fingerNumber = len(frame.fingers)
        for hand in frame.hands:
            # mutex.request()
            # mutex.release()
            self.handType = "Left hand" if hand.is_left else "Right hand"
            self.palmPosition = hand.palm_position
            self.palmNormal = hand.palm_normal
            self.handSphereRadius = hand.sphere_radius
            #print self.handSphereRadius

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                self.keyTapPosition = keytap.position
    '''
    def getHandType(self):
        hand_type = self.handType
        return hand_type

    def getPalmPosition(self):
        palmPosition = self.palmPosition
        return palmPosition
    '''



def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)


        # print "Press Enter to quit"


    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)




if __name__ == "__main__":
    main()

