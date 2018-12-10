# Visual Semantics

Processes images with a neural network to detect and classify objects. The results are then added to an OWL data ontology file where reasoning rules are executed to find relationships between detected objects.

The project currently executes simple SWRL rules (leftOf, rightOf, above and below) based on 2D object coordinates.

How it works:
* An input image is processed by the [YOLO](https://pjreddie.com/darknet/yolo/) object detection network, any detected objects are written to a simple text file with a name, label, detection confidence and the coordinates and size of its 2D bounding box.
* The detected objects are then added to an ontology data file as Individuals using [Owlready2](https://pypi.org/project/Owlready2/).
* The ontology is then passed to a Java program using the [SWRL API](https://github.com/protegeproject/swrlapi) where SWRL rules will be executed to find relationships between the individuals.

Requires:
* Python (atleast 3.5.2)
	* [Owlready2](https://pypi.org/project/Owlready2/)
	* [OpenCV](https://pypi.org/project/opencv-python/)
	* [Numpy](https://pypi.org/project/numpy/)
* Java 8+ to run SWRL API code. Must be Java 8 to compile and build.
  * [SWRL API](https://github.com/protegeproject/swrlapi)
