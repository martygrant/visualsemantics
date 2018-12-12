import timeit
import subprocess
from owlready2 import *

def reason(ontologyFile, objects):
	onto = get_ontology(ontologyFile)
	try:
		onto.load()
	except Exception as e:
		# Exit if ontology file was not loaded correctly/not found
		print(e)
		exit(1)

	# Associate Box class with the onotology by inheriting base Thing class
	with onto:
		class Box(Thing):
			pass

		#class isLeftOf(Box):
			#pass

	# Parse output file from the vision system, each line contains the data for a detected object
	file = tuple(open(objects, 'r'))
	print("semantics.py: Adding new individuals to:", ontologyFile)
	print("Name\tLabel\tConf\tX\tY\tWidth\tHeight")
	for line in file:
		line = [y.strip() for y in line.split(',')]
		id = line[0]
		label = line[1]
		confidence = float(line[2])
		xpos = float(line[3])
		ypos = float(line[4])
		width = int(line[5])
		height = int(line[6])
		entity = Box(name = id, namespace = onto, hasLabel = label, hasClassificationConfidence = confidence, hasPositionX = xpos, hasPositionY = ypos, hasWidth = width, hasHeight = height)
		print(id + "\t" + label + "\t" + str(confidence) + "%" + "\t(" + str(xpos) + ", " + str(ypos) + ")\t(" + str(width) + ", " + str(height) + ")")

	# Save ontology after adding new individuals
	onto.save(ontologyFile)


	"""
	print("all individuals")
	indis = onto.individuals()
	for x in indis:
		for y in x.get_properties():
			#print(y._name)
			if y._name in ["isLeftOf", "isRightOf", "above", "below"]:
				for z in y.get_relations():
					#print(z)
					print(str(z[0]) + " " + y._name + " " + str(z[1]))
	"""
	# Call the Java SWRL program to execute rules in the ontology
	startTime = timeit.default_timer()
	command = ["java", "-jar", "swrlapi-example-2.0.5-jar-with-dependencies.jar", ontologyFile]
	subprocess.call(command) 
	stopTime = timeit.default_timer()
	return round(stopTime - startTime, 2)