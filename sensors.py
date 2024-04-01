import math
import pygame
import numpy as np


def uncertainty_add(distance, angle, sigma):
    """
    Add uncertainty to the distance and angle measurements
    
    Parameters
    ----------
    distance : float
        The distance measurement
    angle : float
        The angle measurement
    sigma : list
        The standard deviation of the distance and angle measurements
    
    Returns
    -------
    list
        The distance and angle measurements with added uncertainty
    """

    mean = np.array([distance, angle])
    covariance = np.diag(sigma ** 2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance, 0)
    angle = max(angle, 0)
    return [distance, angle]


class LaserSensor:

    def __init__ (self, Range, map, uncertainty):
        self.Range = Range # Range of the sensor
        self.speed = 4 # Speed of the laser sensor rotation (rounds per second)
        self.sigma = np.array([uncertainty[0], uncertainty[1]])

        self.position = (0, 0) # initial position of the robot
        self.map = map # Map of the environment
        self.W, self.H = pygame.display.get_surface().get_size() # Get the dimensions of the map
        self.sensedObstacles = [] # List to store the sensed obstacles


    def distance(self, ObstaclePosition):
        # calculate the distance between the robot and the obstacle using Euclidean distance
        px = (ObstaclePosition[0] - self.position[0])**2
        py = (ObstaclePosition[1] - self.position[1])**2
        return math.sqrt(px + py)
    

    def sense_obstacles(self):
        """
        Function to sense the obstacles in the environment

        - Rotate the sensor 360 degrees
        - Calculate the sensor line end-points for each angle using the sensor range and the robot position
        - Split the sensor range into small segments
        - Check if in the range of the sensor line, are there any points that appear to be black (obstacles)
        - If there are, add them to the list of sensed obstacles
        - If not, assume that it is obstacle-free in the sensor range
        """

        data = [] # List to store the sensed obstacles
        x1, y1 = self.position[0], self.position[1] # Get the position of the robot

        for angle in np.linspace(0, 2 * math.pi, 60, False): # Rotate the sensor 360 degrees
            x2, y2 = (x1 + self.Range * math.cos(angle), y1 - self.Range * math.sin(angle)) # Get the end point coordinate of the sensor range

            for i in range(0, 100):
                # Segment the sensor range into small samples and check if they are lying on the obstacles
                u = i/100 
                x = int(x2 * u + x1 * (1 - u)) 
                y = int(y2 * u + y1 * (1 - u))

                if 0 < x < self.W and 0 < y < self.H:
                    color = self. map.get_at((x, y)) # Get the color of the pixel 

                    if (color[0], color[1], color[2]) == (0, 0, 0): # if the color of that segment pixel is black - it is an obstacle
                        distance = self.distance((x, y)) # calculate the distance between the obstacle and the robot
                        output = uncertainty_add(distance, angle, self.sigma) # Add uncertainty to the distance and angle measurements
                        output.append(self.position) # Add the position of the robot

                        # store the measurements
                        data.append(output)

                        # break the loop if an obstacle is found
                        break
        
        # when the sensor is done rotating, store the sensed obstacles
        if len(data) > 0:
            return data
        else:
            return False
        


