from leapMotionApp import *
import leapMotionApp as lm

def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    # torque enable ID1 ID2

    # initialize list
    movementX = []
    movementY = []

    while 1:
        # motorPos = readMotorPos(ID1)
        while listener.handSphereRadius < 50 and listener.handSphereRadius > 0:
            movementX.append(listener.palmPosition[0])
            movementY.append(listener.palmPosition[1])
            dx = movementX[-1] - movementX[0]
            dy = movementY[-1] - movementY[0]

            print str(dx) + " " + str(dy)
        del movementY[:]
        del movementX[:]





    '''
    while 1:
        hand_type = listener.handType
        palm_position = listener.palmPosition
        fingerNum = listener.fingerNumber
        swipeStart = listener.startPos
        palmNormal = listener.palmNormal
        tapPos = listener.tapPos
        if fingerNum == 5:
            movement.append(palm_position[0])
            # print "start: " + str(movement[0])
            # print "end: " + str(movement[-1])
            print palmNormal
            print tapPos
        else:
            del movement[:]
        # print palmPosition[0]
    '''

if __name__ == '__main__':
    main()