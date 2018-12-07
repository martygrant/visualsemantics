import timeit

from vision import Detector
from semantics import reason

overallStartTime = timeit.default_timer()

# Load neural network, input image, process it and save results in a text file
networkConfig = "yolo/yolov3.cfg"
networkWeights = "yolo/yolov3.weights"
classes = "yolo/yolonames.txt"
detector = Detector(networkConfig, networkWeights, classes)   
networkTime = detector.processImage("input.png", "output.jpg")
overallVisionStopTime = timeit.default_timer()

# Load the ontology file, add new objects to it and execute SWRL rules, save results to same file
overallReasoningStartTime = timeit.default_timer()
ontology = "modified.owl"
objects = "objects.txt"
reasoningTime = reason(ontology, objects)

overallStopTime = timeit.default_timer()

print("Neural network inference:", round(networkTime, 2), "ms")
overallVisionTime = round(overallVisionStopTime - overallStartTime, 2)
print("Overall vision time (includes file handling):", overallVisionTime, "s")

print("Reasoning time:", reasoningTime, "s")
overallReasoningTime = round(overallStopTime - overallReasoningStartTime, 2)
print("Overall reasoning time (includes file handling):", overallReasoningTime, "s")

overallTime = round(overallStopTime - overallStartTime, 2)
print("Overall time (includes file handling): ", overallTime, "s")  