import numpy as np
import math
from fractions import Fraction
from scipy.odr import *


class featuresDetection:
    def __init__(self):
        # variables definition
        self.EPSILON = 10
        self.DELTA = 501
        self.SNUM = 6
        self.PMIN = 20
        self.GMAX = 20
        self.SEED_SEGMENTS = []
        self.LINE_SEGMENTS = []
        self.LASERPOINTS = []
        self.LINE_PARAMS = None
        self.NP = len(self.LASERPOINTS) - 1
        self.LMIN = 20 # minimum length of a line segment
        self.LR = 0 # real length of a line segment
        self.PR = 0 # the number of laser points contained in a line segment


    # Euclidean distance from point1 to point2
    def dist_point2point(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    

    # Distance from a point to a line
    def dist_point2line(self, params, point):
        A, B, C = params # A, B, C are the coefficients of the line equation Ax + By + C = 0
        distance = abs(A * point[0] + B * point[1] + C) / math.sqrt(A ** 2 + B ** 2)
        return distance
    

    # Extract two points from a line equation under the slope intercepts form
    def line_2points(self, m, b):
        x = 5
        y = m * x + b
        x2 = 2000
        y2 = m * x2 + b
        return [(x, y), (x2, y2)]
    

    # General form to slope-intercept
    def lineForm_G2SI(self, A, B, C):
        m = -A/B
        b = -C/B
        return m, b
    

    # Slope-intercept to general form
    def lineForm_SI2G(self, m, b):
        A, B, C = -m, 1, -B 
        if A < 0:
            A, B, C = -A, -B, -C
        den_a = Fraction(A).limit_denominator(1000).as_integer_ratio()[1]
        den_c = Fraction(C).limit_denominator(1000).as_integer_ratio()[1]

        gcd = np.gcd(den_a, den_c)
        lcm = den_a * den_c / gcd

        A = A * lcm
        B = B * lcm
        C = C * lcm
        return A, B, C
    

    def line_intersection_general(self, params1, params2):
        a1, b1, c1 = params1
        a2, b2, c2 = params2
        x = (c1 * b2 - b1 * c2) / (b1 * a2 - a1 * b2)
        y = (a1 * c2 - a2 * c1) / (b1 * a2 - a1 * b2)

        return x , y
    

    def point_2line(self, point1, point2):
        m, b = 0, 0
        if point2[0] == point1[0]:
            pass
        else:
            m = (point2[1] - point1[1]) / (point2[0] - point1[0])
            b = point2[1] - m * point2[0]
        return m, b
    

    def projection_point2line(self, point, m, b):
        x, y = point
        m2 = -1/m
        c2 = y - m2 * x
        intersection_x = - (b - c2) / (m - m2)
        intersection_y = m2 * intersection_x + c2
        return intersection_x, intersection_y
    

    def AD2pos(self, distance, angle, robot_position):
        x = distance * math.cos(angle) + robot_position[0]
        y = -distance * math.sin(angle) + robot_position[1]
        return (int(x), int(y))
    

    def laser_points_Set(self, data):
        self.LASERPOINTS = []
        if not data:
            pass
        else:
            for point in data:
                coordinates = self.AD2pos(point[0], point[1], point[2])
                self.LASERPOINTS.append([coordinates, point[1]])
        self.NP = len(self.LASERPOINTS) - 1


    # Define a function (quadratic in this case) to fit the data width
    def lineaer_func(self, p, x):
        m, b = p 
        return m * x + b 
    

    def odr_fit(self, laser_points):odr_dit
        x = np.array([i[0][0] for i in laser_points])
        y = np.array([i[0][1] for i in laser_points])

        # Create a model for fitting
        linear_model = Model(self.linear_func)

        # Create a RealData object using our initiated data from above
        data = RealData(x, y)

        # Set up ODR with the model and data
        odr_model = ODR(data, linear_model, beta0 = [0., 0.])

        # Run the regression
        out = odr_model.run()
        m, b = out.beta
        return m, b
    

    def predictPoint(self, line_params, sensed_point, robotpos):
        m,b = self.point_2line(robotpos, sensed_point)
        params1 = self.lineForm_SI2G(m, b)
        predx, predy = self.line_intersection_general(params1, line_params)
        return predx, predy
    

    def seed_segment_detection(self, robot_position, break_point_ind):
        flag = True
        self.NP = max(0, self.NP)
        self.SEED_SEGMENTS = []
        for i in range(break_point_ind, (self.NP - self.PMIN)):
            predicted_points_to_draw = []
            j = i + self.SNUM
            m, c = self.odr_fit(self.LASERPOINTS[i:j])

            params = self.lineForm_SI2G(m, c)

            for k in range(i, j):
                predicted_point = self.predictPoint







