# tescalon@amazon.com
# jschwenn@amazon.com
# https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html
# https://github.com/aws-samples/aws-deepracer-workshops/blob/master/Workshops/2019-AWSSummits-AWSDeepRacerService/Lab1/Readme.md

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

position_points = []
progress_point = 0

def getHeading(x1, y1, x2, y2):
    deltax = (x2 - x1)
    # Make safe for validator
    if deltax == 0:
        deltax = 0.0001

    degrees = math.degrees(math.atan((y2 - y1) / deltax))
    if degrees > 180:
        degrees = degrees - 360
    return degrees

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def reward_function(params):
    print('=====START PARAMS')
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
    global position_points
    position_points.append([x, y, distance_from_center, progress])
    print('position_points', position_points)
    global progress_point
    progressBonus = 0
    if closest_waypoints[0] > progress_point:
        progressBonus = 10 * (closest_waypoints[0] - progress_point)
        progress_point = closest_waypoints[0]
    # progressBonus = 100 * (progress - position_points[-10:][0][2])

    reward = 0
    bonus = 0
    speedBonus = speed
    edgeMultiplier = 1
    if (distance_from_center / (track_width / 2)) > 0.75:
        edgeMultiplier = 0.5
    if not all_wheels_on_track:
        edgeMultiplier = 0.1

    angleBonus = 0.5 * max((10 - steering_angle), 0)

    if closest_waypoints[0] > closest_waypoints[1]:
        headingDiff = getHeading(waypoints[closest_waypoints[0]][0], waypoints[closest_waypoints[0]][1], waypoints[closest_waypoints[1]][0], waypoints[closest_waypoints[1]][1])
    else:
        headingDiff = getHeading(waypoints[closest_waypoints[1]][0], waypoints[closest_waypoints[1]][1], waypoints[closest_waypoints[0]][0], waypoints[closest_waypoints[0]][1])
    headingDiff = abs(headingDiff - heading)
    if headingDiff > 180:
        headingDiff = 360 - headingDiff
    headingBonus = (180 - headingDiff) / 18


    infoBonus = 0
    # infoPoints = waypoints[closest_waypoints[0]:][0:10]
    # print('infoPoints: ', infoPoints)

    # for idx in range(0, len(infoPoints) - 1):
    #     if infoPoints[idx]:
    #         multiplier = 1 / ((idx + 1)**1.5)
    #         print("multiplier " + str(multiplier))

    #         if infoPoints[idx] and infoPoints[idx + 1]:
    #             xwaypoint1 = infoPoints[idx][0]
    #             ywaypoint1 = infoPoints[idx][1]
    #             xwaypoint2 = infoPoints[idx + 1][0]
    #             ywaypoint2 = infoPoints[idx + 1][1]
    #         elif infoPoints[idx] and infoPoints[idx - 1]:
    #             xwaypoint1 = infoPoints[idx - 1][0]
    #             ywaypoint1 = infoPoints[idx - 1][1]
    #             xwaypoint2 = infoPoints[idx][0]
    #             ywaypoint2 = infoPoints[idx][1]

    #         headingDiff = abs(getHeading(xwaypoint1, ywaypoint1, xwaypoint2, ywaypoint2) - heading)
    #         if headingDiff > 180:
    #             headingDiff = 360 - headingDiff
    #         headingDiff = (180 - headingDiff) / 18

    #         print("headingDiff " + str(headingDiff))
    #         infoBonus = infoBonus + (multiplier * headingDiff)

    print('angleBonus ' + str(angleBonus))
    print('progressBonus ' + str(progressBonus))
    print("infoBonus " + str(infoBonus))
    print("bonus " + str(bonus))
    print("speedBonus " + str(speedBonus))
    reward = edgeMultiplier * (infoBonus + bonus + speedBonus + progressBonus + angleBonus + headingBonus)
    print("reward " + str(float(reward)))
    return float(reward)
