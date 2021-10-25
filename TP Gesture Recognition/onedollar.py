import numpy as np
import numpy.linalg as linalg

phi = 0.5 * (-1 + np.sqrt(5))
numPoints = 128


class OneDollar(object):
    """docstring for Recognizer"""

    def __init__(self, angle_range=45., angle_step=2., square_size=250.):
        super(OneDollar, self).__init__()
        self.angle_range = angle_range
        self.angle_step = angle_step
        self.square_size = square_size
        self.templates = []
        self.resampled_templates = []     #for convenience
        self.resampled_gesture = []       #for convenience
        self.labels = []



    #########################################
    # TODO 8
    #
    #########################################
    def recognize(self, points):
        #print("Début de recognize") # Debug
        template_id = -1
        label = "None"
        score = 0
        # Dans un premier temps on fait les traitement nécessaires avant la réconnaisance
        #print("Début de la réconnaisance") # Debug
        points = self.resample(list(points), numPoints)
        #print("Resample done") # Debug
        points = self.rotateToZero(points)
        #print("Rotate to zero done") # Debug
        points = self.scaleToSquare(points)
        #print("Scale to square Done") # Debug
        points = self.translateToOrigin(points)
        #print("Translate to origine Done") # Debug
        b = np.inf # Meilleur distance entre les points et les points de chaque template
        i=0
        #print("Début des calculs de distances") # Debug
        while i<len(self.templates):
            d = self.distanceAtBestAngle(points, self.templates[i], -self.angle_range, self.angle_range, self.angle_step)
            #print("Distance N°",i," : d") # Debug
            if d < b:  
                b = d
                template_id = i
                label = self.labels[i]
            i+=1
        score = 1 - b / (0.5 * np.sqrt(self.square_size**2 + self.square_size**2))
        return template_id,label,score
            


    #########################################
    # Angle values are in degrees
    #########################################
    def distanceAtBestAngle(self, points, template, angle_a, angle_b,
                            angle_step):
        x_1 = (phi * angle_a) + ( 1 - phi)*angle_b
        f_1 = self.distanceAtAngle(points, template, x_1)
        x_2 = (1- phi) * angle_a + (phi * angle_b)
        f_2 = self.distanceAtAngle(points, template, x_2)

        while (abs(angle_b-angle_a)>angle_step):
            if (f_1 < f_2) :
                angle_b = x_2
                x_2 = x_1
                f_2 = f_1
                x_1 = (phi * angle_a) + (1 - phi) * angle_b
                f_1 = self.distanceAtAngle(points, template, x_1)
            else :
                angle_a = x_1
                x_1 = x_2
                f_1 = f_2
                x_2 = (1 - phi) * angle_a + (phi * angle_b)
                f_2 = self.distanceAtAngle(points, template, x_2)

        return min(f_1, f_2)
        return min(f_1, f_2)

    ####################
    def distanceAtAngle(self, points, template, angle):
        newPoints = self.rotateBy(points, angle)
        d = pathDistance(newPoints, template)
        return d




    ####################
    def resample(self, points, n):
        # Get the length that should be between the returned points
        path_length = pathLength(points) / float(n - 1)
        newPoints = [points[0]]
        D = 0.0
        i = 1
        while i < len(points):
            point = points[i - 1]
            next_point = points[i]
            d = getDistance(point, next_point)
            if D + d >= path_length:
                delta_distance = float((path_length - D) / d)
                q = [0., 0.]
                q[0] = point[0] + delta_distance * (next_point[0] - point[0])
                q[1] = point[1] + delta_distance * (next_point[1] - point[1])
                newPoints.append(q)
                points.insert(i, q)
                D = 0.
            else:
                D += d
            i += 1
        if len(newPoints) == n - 1:  # Fix a possible roundoff error
            newPoints.append(points[0])
        return newPoints

    ####################
    def fit(self, templates, labels):
        for i, t in enumerate(templates):
            self.addTemplate(t, labels[i])
            #self.labels.append(labels[i])


    ####################
    def addTemplate(self, template, label):
        points = []
        for i in range(template.shape[0]):
            points.append([template[i,0], template[i,1]])
        points = self.resample(points, numPoints)
        self.resampled_templates.append( points )
        points = self.rotateToZero(points)
        points = self.scaleToSquare(points)
        points = self.translateToOrigin(points)
        self.templates.append(points)
        self.labels.append(label)


    #########################################
    # TODO 6
    #########################################
    def rotateToZero(self, points):
        centroid = np.mean(points, 0)     
        #remove this line, it is just for compilation
        #todo
        angle = np.arctan2(centroid[1]-points[0][1],centroid[0]-points[0][0])
        return self.rotateBy(points,-angle)

    #########################################
    # TODO 6
    #########################################
    def rotateBy(self, points, angle):
        newPoints = np.zeros((1, 2))    #initialize with a first point [0,0]
        #todo 6 update the vector newPoints
        centroid = np.mean(points,0)
        for point in points:
            q = np.array([0., 0.])
            q[0] = (point[0]-centroid[0]) * np.cos(angle) - (point[1] - centroid[1]) * np.sin(angle) + centroid[0]
            q[1] = (point[0]-centroid[0]) * np.sin(angle) + (point[1] - centroid[1]) * np.cos(angle) + centroid[1]
            newPoints = np.append(newPoints, [q], 0)
        newPoints = newPoints[1:]       #remove the first point [0,0]
        return newPoints


    #########################################
    # TODO 7
    #########################################
    def scaleToSquare(self, points):
        newPoints = np.zeros((1, 2))    #initialize with a first point [0,0]

        #todo 7
        max_x, max_y = np.max(points, 0)
        min_x, min_y = np.min(points, 0)
        b_width = max_x - min_x
        b_height = max_y - min_y
        for point in points:
            q = np.array([0., 0.])
            q[0] = point[0] * (self.square_size / b_width)
            q[1] = point[1] * (self.square_size / b_height)
            newPoints = np.append(newPoints, [q], 0)
        newPoints = newPoints[1:]      #remove the first point [0,0]
        return newPoints



    ################################
    def translateToOrigin(self, points):
        centroid = np.mean(points, 0)
        newPoints = np.zeros((1, 2))
        self.translation = centroid
        for point in points:
            q = np.array([0., 0.])
            q[0] = point[0] - centroid[0]
            q[1] = point[1] - centroid[1]
            newPoints = np.append(newPoints, [q], 0)
        return newPoints[1:]

    ################################
    def translate(self, points, vec):
        newPoints = np.zeros((1, 2))
        for point in points:
            q = np.array([0., 0.])
            q[0] = point[0] + vec[0]
            q[1] = point[1] + vec[1]
            newPoints = np.append(newPoints, [q], 0)
        return newPoints[1:]



    ####################
    # def score(self, X_test, y_test):
    #     score_ = 0
    #     n_tests = 0
    #     for i, t in enumerate(X_test):
    #         print(i)
    #         points = []
    #         for i in range(t.shape[0]):
    #             points.append([t[i,0], t[i,1]])
    #         t_data, t_id, sc = self.recognize(points)
    #         if (t_id == y_test[i]):
    #             score_ += 1
    #         n_tests += 1
    #     return score_ / n_tests


def pathDistance(path1, path2):
    ''' Calculates the distance between two paths. Fails if len(path1) != len(path2) '''
    if len(path1) != len(path2):
        raise Exception('Path lengths do not match!')
    d = 0
    for p_1, p_2 in zip(path1, path2):
        d = d + getDistance(p_1, p_2)
    return d / len(path1)


def getDistance(point1, point2):
    return linalg.norm(np.array(point2) - np.array(point1))



def pathLength(points):
    length = 0
    for (i, j) in zip(points, points[1:]):
        length += getDistance(i, j)
    return length


def pairwiseIterator(elems):
    for (i, j) in zip(elems, elems[1:]):
        yield (i, j)
    yield (elems[-1], elems[0])