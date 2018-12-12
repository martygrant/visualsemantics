import cv2 as cv
import numpy as np

# Container object to hold data about detected objects
class Entity:
	def __init__(self, id, name, confidence, x, y, width, height):
		self.id = id
		self.name = name
		self.confidence = confidence
		self.x = x
		self.y = y 
		self.width = width
		self.height = height

	def __str__(self):
		return "Entity #" + str(self.id) + " - " + self.name + " - " + str(self.confidence) + " - (" + str(self.x) + ", " + str(self.y) + ")" + " - (" + str(self.width) + ", " + str(self.height) + ")"

# Visual detection code originally from: https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/
class Detector:
	def __init__(self, networkConfig, networkWeights, classLabels):
		self.networkConfig = networkConfig
		self.networkWeights = networkWeights
		self.classLabels = classLabels
		self.classes = None
		self.network = None
		# defaults 0.5 and 0.4
		self.confThreshold = 0.8
		self.nmsThreshold = 0.4
		self.inpWidth = 416
		self.inpHeight = 416
		self.loadNetwork()
		
	def loadNetwork(self):
		self.network = cv.dnn.readNetFromDarknet(self.networkConfig, self.networkWeights)
		self.network.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
		self.network.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

		# Network detection labels
		with open(self.classLabels, 'rt') as f:
			self.classes = f.read().rstrip('\n').split('\n')

	def processImage(self, inputImage, outputImage):
		# Open input image
		frame = cv.imread(inputImage)

		# Get a blob from the input image
		blob = cv.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)

		# Pass this to the network
		self.network.setInput(blob)

		# Forward propgate and get the network output
		out = self.network.forward(self.getOutputsNames())

		# Mark the detected objects on the actual image (boxes, labels). Build a list of Entity container objects
		entities = []
		self.postprocess(frame, out, entities)

		print("vision.py: Vision processing results:")
		for x in entities:
			print(x)

		# Get the performance time of the network 
		t, _ = self.network.getPerfProfile()
		time = (t * 1000.0 / cv.getTickFrequency())
		label = 'Inference time: %.2f ms' % time
		cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
		#print(label)

		# Write the results to a new image
		print("vision.py: Processed image saved to:", outputImage)
		cv.imwrite(outputImage, frame)

		# Create a simple text file that contains data about detected objects to be loaded into an ontology later
		self.writeDetectionsToFile(entities)

		return time

	def postprocess(self, frame, outs, entities):
		frameHeight = frame.shape[0]
		frameWidth = frame.shape[1]
	
		classIds = []
		confidences = []
		boxes = []
		# Scan through all the bounding boxes output from the network and keep only the
		# ones with high confidence scores. Assign the box's class label as the class with the highest score.
		classIds = []
		confidences = []
		boxes = []
		for out in outs:
			for detection in out:
				scores = detection[5:]
				classId = np.argmax(scores)
				confidence = scores[classId]
				if confidence > self.confThreshold:
					center_x = int(detection[0] * frameWidth)
					center_y = int(detection[1] * frameHeight)
					width = int(detection[2] * frameWidth)
					height = int(detection[3] * frameHeight)
					left = int(center_x - width / 2)
					top = int(center_y - height / 2)
					classIds.append(classId)
					confidences.append(float(confidence))
					boxes.append([left, top, width, height])
	
		# Perform non maximum suppression to eliminate redundant overlapping boxes with lower confidences.
		indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
		for i in indices:
			i = i[0]
			box = boxes[i]
			left = box[0]
			top = box[1]
			width = box[2]
			height = box[3]
			self.drawPred(frame, i, classIds[i], confidences[i], left, top, left + width, top + height)

			id = i
			name = self.classes[classIds[i]]
			confidence = round(confidences[i], 3)
			x = left + (width/2)
			y = top + (height/2)
			newEntity = Entity(id, name, confidence, x ,y, width, height)
			entities.append(newEntity)
		
	# Get the names of the output layers
	def getOutputsNames(self):
		# Get the names of all the layers in the network
		layersNames = self.network.getLayerNames()
		# Get the names of the output layers, i.e. the layers with unconnected outputs
		return [layersNames[i[0] - 1] for i in self.network.getUnconnectedOutLayers()]

	def drawPred(self, frame, id, classId, conf, left, top, right, bottom):
		# Draw a bounding box.
		cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
		
		label = '%.2f' % conf
			
		# Get the label for the class name and its confidence
		if self.classes:
			assert(classId < len(self.classes))
			label = '%s,%s,%s' % (id, self.classes[classId], label)

		#Display the label at the top of the bounding box
		labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
		top = max(top, labelSize[1])
		cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
		cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0))

	# Create a text file with data about each detected object per line
	def writeDetectionsToFile(self, entities):
		outputFile = "objects.txt"
		# Entities will be named like "keyboard2" the number does not mean it is the 2nd detected keyboard but the 2nd detected entity
		# This is to simply differentiate between objects in Protege of the same class
		with open(outputFile, 'w') as file:
			for entity in entities:
				line = entity.name
				line += str(entity.id)
				line += ","
				line += entity.name
				line += ","
				line += str(entity.confidence)
				line += ","
				line += str(entity.x)
				line += ","
				line += str(entity.y)
				line += ","
				line += str(entity.width)
				line += ","
				line += str(entity.height)
				line += "\n"
				file.write(line)
			print("vision.py: Vision results written to:", outputFile)