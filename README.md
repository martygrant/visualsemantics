# Visual Semantics

Processes images with a neural network to detect and classify objects. The results are then added to an OWL data ontology file where reasoning rules are executed to find relationships between detected objects.

The project currently executes simple SWRL rules (leftOf, rightOf, above and below) based on 2D object coordinates.

* Vision processing is implemented in Python using the [YOLO](https://pjreddie.com/darknet/yolo/) network. 
* Adding detected objects as Individuals to the ontology data file is also implemented in Python using the [Owlready2](https://pypi.org/project/Owlready2/) library.
* The SWRL rules are applied with a Java program using the [SWRL API](https://github.com/protegeproject/swrlapi).

Requires:
* Python3
* Java 8+ to run SWRL API code. Must be Java 8 to compile and build.
