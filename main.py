import env, sensors
import pygame
import math

environment = env.buildEnvironment((600, 1200))
environment.originalMap = environment.map.copy() # save the original map that will be used to reset the map
laser = sensors.LaserSensor(200, environment.originalMap, uncertainty = (0.5, 0.01))

#environment.map.fill((0, 0, 0)) # Fill the map with black color
environment.infomap = environment.map.copy() # Save the map that will be used to draw the point cloud in

running = True
while running:
    sensorOn = False

    # Check if the user wants to quit the simulation
    # Check if the mouse is focused on the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if pygame.mouse.get_focused():
            sensorOn = True
        elif not pygame.mouse.get_focused():
            sensorOn = False
    
    if sensorOn:
        position = pygame.mouse.get_pos()
        laser.position = position 
        sensor_data = laser.sense_obstacles()  # (distance, angle, position)
        environment.dataStorage(sensor_data)   # convert to Cartesian coordinates and store the data
        environment.show_sensorData()  # show the sensed obstacles on the map
    
    environment.map.blit(environment.infomap, (0, 0))
    pygame.display.update()