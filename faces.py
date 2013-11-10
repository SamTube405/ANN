import sys
# To change this template, choose Tools | Templates
# and open the template in the editor.

alpha = 0.1
offset = 0
iterations = 10

def train(images, output, weights):
    
    for mood in range(0, 4):
        w = list(weights[mood])
        for image in range(0, len(images)):
            nodeValue = 0
            desiredOutput = 0
            nodeOutput = 0

            delta = 0
            if(output[image] == mood + 1):
                desiredOutput = 1
            else:
                desiredOutput = -1
            
            for element in range(0, 400):
                nodeValue += images[image][element] * w[element]

            if(nodeValue > offset):
                nodeOutput = 1
            else:
                nodeOutput = -1
            error = desiredOutput - nodeOutput

            for element in range(0, 400):
                delta = alpha * error * images[image][element]
                w[element] += delta

        weights[mood] = w
    return weights

def test(images, weights):

    offset = 0
    node = 0
    nodeOutput = -1;

    moods = []

    for mood in range(0, 4):
        m = []
        for image in range(len(images)):
            node = 0
            for element in range(400):
                node += images[image][element] * weights[mood][element]

            if(node > offset):
                nodeOutput = 1
            else:
                nodeOutput = -1
            #print(nodeOutput)
            m.append(nodeOutput)
        #print(m)
        moods.append(m)
    return moods


def rotateImages(image):
    # check the pixel density
    top = bottom = left = right = 0;

    for row in range(0, 10):
        for col in range(0, 20):
            top += image[row][col]

    row = 10
    for i in range(0, 10):
        for col in range(0, 20):
            bottom += image[row][col]
        row += 1

    for row in range(0, 20):
        for col in range(0, 10):
            left += image[row][col]

    for row in range(0, 20):
        col = 10
        for i in range(0, 10):
            right += image[row][col]
            col += 1

    if (bottom > top and bottom > right and bottom > left):
        ## 180 degrees
        image = rotate(image)
        image = rotate(image)


    elif (left > top and left > right and left > bottom):
        ## 90 degrees
        image = rotate(image)

    elif (right > top and right > bottom and right > left):
        ## 270 degrees or -90 degrees
        image = rotate(image)
        image = rotate(image)
        image = rotate(image)

    rotatedImage = []
    for img in image:
        for i in img:
            rotatedImage.append(i)

    return rotatedImage


def rotate(image):

    output = []

    for col in range(0, 20):
        row = 19
        rotated = []
        for i in range(0, 20):
            rotated.append(image[row][col])
            row -= 1
        output.append(rotated)

    return output

def readImageFile(imageFile):
    imageFile = open(imageFile, "r")
    images = []

    count = 0;
    img = []
                 
    for line in imageFile:
        
        if(line.startswith('#') == False and line.startswith('Image') == False and line.isspace() == False):
            vals = line.split(' ')
            row = []
            for num in vals:
                val = int(num.rstrip())
                row.append(val)
            count += 1
            img.append(row)
            if(count == 20):
                img = rotateImages(img)
                images.append(img)
                img = []
                row = []
                count = 0

    #print(len(images))
    imageFile.close()
    
    return images

def readDataFile(dataFile):
    # @type dataFile file
    dataFile = open(dataFile, "r")
    
    data = []
    for line in dataFile:
        # @type line str
        if(line.startswith('#') == False and line.startswith('Image')):
            vals = line.split(' ')
            data.append(int(vals[1]))

    dataFile.close()
    return data

def readFiles(trainingImagesFile, trainingDataFile):

    images = readImageFile(trainingImagesFile)
    desiredOutputs = readDataFile(trainingDataFile)

    #testImages = readImageFile(testImagesFile)
    #testData = readDataFile(testDataFile)

    return images, desiredOutputs

def startTraining(trainingImagesFile, trainingDataFile):
    images, outputs = readFiles(trainingImagesFile, trainingDataFile)
    weights = [[0] * 400] * 4
    #print(weights)
    for i in range(0, iterations):
        #print(i)
        weights = train(images, outputs, weights)
        #print(weights[0][100])
    return weights

def writeOutput(moods):
    
    for i in range(len(moods[0])):
        if(moods[0][i] == 1):
            print("Image" + str(i + 1) + " 1")
        elif(moods[1][i] == 1):
            print("Image" + str(i + 1) + " 2")
        elif(moods[2][i] == 1):
            print("Image" + str(i + 1) + " 3")
        elif(moods[3][i] == 1):
            print("Image" + str(i + 1) + " 4")
        else:
            print("Image" + str(i + 1) + " 5")
if __name__ == '__main__':

    if(len(sys.argv) != 4):
        print("Invalid number of Arguments")
        print("Usage : $ python faces.py training-file.txt training-facit.txt test-file.txt")
        exit(1)

    trainingImagesFile = sys.argv[1]
    trainingDataFile = sys.argv[2]
    testImagesFile = sys.argv[3]

#    trainingImagesFile = "training-A.txt"
#    trainingDataFile = "facit-A.txt"
#    testImagesFile = "test-B.txt"
    
    weights = [[0] * 400] * 4

    weights = startTraining(trainingImagesFile, trainingDataFile)

    testImages = readImageFile(testImagesFile)

    moods = test(testImages, weights)
    
    writeOutput(moods)
    