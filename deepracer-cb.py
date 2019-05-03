# tescalon@amazon.com
# jschwenn@amazon.com
# https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html

# all_wheels_on_track
# x
# y
# distance_from_center
# is_left_of_center
# heading
# progress
# steps
# speed
# steering_angle
# track_width
# waypoints
# closest_waypoints

import math

myVal = 10

def getHeading(x1, y1, x2, y2):
    deltax = (x2 - x1)
    # Make safe for validator
    if deltax == 0:
        deltax = .0001

    degrees = math.degrees(math.atan((y2 - y1) / deltax))
    if degrees > 180:
        degrees = degrees - 360
    return degrees

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def reward_function(params):
    print('=====START PARAMS')
    global myVal
    print('myVal', myVal)
    myVal = myVal + 10
    print('all_wheels_on_track ' + str(params['all_wheels_on_track']))
    all_wheels_on_track = params['all_wheels_on_track']
    print('x ' + str(params['x']))
    x = params['x']
    print('y ' + str(params['y']))
    y = params['y']
    print('distance_from_center ' + str(params['distance_from_center']))
    distance_from_center = params['distance_from_center']
    print('is_left_of_center ' + str(params['is_left_of_center']))
    is_left_of_center = params['is_left_of_center']
    print('heading ' + str(params['heading']))
    heading = params['heading']
    print('progress ' + str(params['progress']))
    progress = params['progress']
    print('steps ' + str(params['steps']))
    steps = params['steps']
    print('speed ' + str(params['speed']))
    speed = params['speed']
    print('steering_angle ' + str(params['steering_angle']))
    steering_angle = params['steering_angle']
    print('track_width ' + str(params['track_width']))
    track_width = params['track_width']
    print('waypoints ' + str(params['waypoints']))
    waypoints = params['waypoints']
    print('closest_waypoints ' + str(params['closest_waypoints']))
    closest_waypoints = params['closest_waypoints']
    print('=====END PARAMS')

    reward = 0
    bonus = 2 * (track_width - distance_from_center) / track_width
    speedBonus = speed
    infoBonus = 0
    infoPoints = waypoints[closest_waypoints[0]: closest_waypoints[0] + 20]
    print('infoPoints: ', infoPoints)

    for idx in range(0, len(infoPoints) - 1):
        if infoPoints[idx]:
            multiplier = 1 / ((idx + 1)**1.5)
            if infoPoints[idx] and infoPoints[idx + 1]:
                xwaypoint1 = infoPoints[idx][0]
                ywaypoint1 = infoPoints[idx][1]
                xwaypoint2 = infoPoints[idx + 1][0]
                ywaypoint2 = infoPoints[idx + 1][1]
            elif infoPoints[idx] and infoPoints[idx - 1]:
                xwaypoint1 = infoPoints[idx - 1][0]
                ywaypoint1 = infoPoints[idx - 1][1]
                xwaypoint2 = infoPoints[idx][0]
                ywaypoint2 = infoPoints[idx][1]

            # headingMultiplier = 360
            headingDiff = getHeading(xwaypoint1, ywaypoint1, xwaypoint2, ywaypoint2) - heading
            # headingFactor = 10 * (headingMultiplier - abs(heading - headingDiff)) / headingMultiplier
            headingFactor = headingDiff

            # distanceMultiplier = 5 * track_width
            distanceDiff = min(getDistance(x, y, xwaypoint1, ywaypoint1), getDistance(x, y, xwaypoint2, ywaypoint2))
            # distanceFactor = 10 * (distanceMultiplier - distanceDiff) / distanceMultiplier
            distanceFactor = 10 * distanceDiff

            # infoSteering = heading + steering_angle
            # steeringFactor = steering_angle

            print("multiplier " + str(multiplier))
            print("headingDiff " + str(headingDiff))
            print("headingFactor " + str(headingFactor))
            print("distanceDiff " + str(distanceDiff))
            print("distanceFactor " + str(distanceFactor))
            reward = reward + (multiplier * (headingFactor + distanceFactor))

    print("infoBonus " + str(infoBonus))
    print("bonus " + str(bonus))
    print("speedBonus " + str(speedBonus))
    reward = infoBonus + bonus + speedBonus
    print("reward " + str(float(reward)))
    return float(reward)
