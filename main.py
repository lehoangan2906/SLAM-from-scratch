import env, sensors, features
import pygame
import random

def random_color():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))

FEATUREMAP = features.featuresDetection()
environment = env.buildEnvironment((600, 1200))
originalMap = environment.map.copy()

laser = sensors.LaserSensor(200, originalMap, uncertainty = (0.5, 0.01))
environment.map.fill((255, 255, 255))
environment.infomap = environment.map.copy()
originalMap = environment.map.copy()
running = True
FEATURE_DETECTION = True
BREAK_POINT_IND = 0


while running:
    environment.informap = originalMap.copy()
    FEATURE_DETECTION = True
    BREAK_POINT_IND = 0
    ENDPOINT = [0, 0]
    sensorON = False
    PREDICTED_POINTS_TO_DRAW = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_focused():
        sensorON = True

    elif not pygame.mouse.get_focused():
        sensorON = False
    
    if sensorON: 
        position = pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles()
        FEATUREMAP.laser_points_Set(sensor_data)

        while BREAK_POINT_IND < (FEATUREMAP.NP - FEATUREMAP.PMIN):
            seedseg = FEATUREMAP.seed_segment_detection(laser.position, BREAK_POINT_IND)
            
            if seedseg == False:
                break

            else:
                seedSegment = seedseg[0]
                PREDICTED_POINTS_TO_DRAW = seedseg[1]
                INDICES = seedseg[2]
                results = FEATUREMAP.seed_segment_growing(INDICES, BREAK_POINT_IND)

                if results == False:
                    BREAK_POINT_IND = INDICES[1]
                    continue

                else:
                    line_eq = results[1]
                    m, c = results[5]
                    line_seq = results[0]
                    OUTERMOST = results[2]
                    BREAK_POINT_IND = results[3]

                    ENDPOINT[0] = FEATUREMAP.projection_point2line(OUTERMOST[0], m, c)
                    ENDPOINT[1] = FEATUREMAP.projection_point2line(OUTERMOST[1], m, c)

                    COLOR = random_color()

                    for point in line_seq:
                        environment.infomap.set_at((int(point[0][0]), int(point[0][1])), (0, 255, 0))
                        pygame.draw.circle(environment.infomap, COLOR, (int(point[0][0]), int(point[0][1])), 2, 0)
                    
                    pygame.draw.line(environment.infomap, (255, 0, 0), ENDPOINT[0], ENDPOINT[1], 2)

                    environment.dataStorage(sensor_data)

    environment.map.blit(environment.infomap, (0, 0))
    pygame.display.update() 

