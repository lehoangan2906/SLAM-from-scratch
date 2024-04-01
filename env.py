import math
import pygame

class buildEnvironment:
    def __init__(self, MapDimensions):
        pygame.init()
        self.pointCloud=[]  # List to store the points in the environment since the environment is in 2D
        self.externalMap=pygame.image.load('map.png') # Load the map image
        self.maph, self.mapw = MapDimensions # Get the dimensions of the map
        self.MapWindowName = "RRT Path Planning" 
        pygame.display.set_caption(self.MapWindowName) 
        self.map = pygame.display.set_mode((self.mapw, self.maph)) # Set the dimensions of the map
        self.map.blit(self.externalMap, (0,0))

        # Define the colors
        self.black = (0, 0, 0)
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0) 
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)


    # build the point cloud of the environment
    def AD2pos(self, distance, angle, robot_position):
        # function to convert the polar coordinates to Cartesian coordinates
        x = distance * math.cos(angle) + robot_position[0]
        y = -distance * math.sin(angle) + robot_position[1]
        return (int(x), int(y))
    

    def dataStorage(self, data):
        # Store the sensed obstacles in the point cloud
        print(len(self.pointCloud))
        for element in data:
            point = self.AD2pos(element[0], element[1], element[2])
            if point not in self.pointCloud:
                self.pointCloud.append(point)


    def show_sensorData(self):
        # Display the sensed obstacles on the map
        self.informap = self.map.copy()
        for point in self.pointCloud:
            self.infomap.set_at((int(point[0]), int(point[1])), (255, 0, 0))