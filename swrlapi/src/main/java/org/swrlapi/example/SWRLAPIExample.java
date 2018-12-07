package org.swrlapi.example;

import org.checkerframework.checker.nullness.qual.NonNull;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.swrlapi.factory.SWRLAPIFactory;
import org.swrlapi.core.SWRLRuleEngine;
import java.io.File;
import java.util.Optional;

public class SWRLAPIExample {
	public static void main(String[] args) {

		long overallStartTime = System.nanoTime();

		Optional<@NonNull String> owlFilename = args.length == 0 ? Optional.<@NonNull String>empty()
				: Optional.of(args[0]);
		Optional<@NonNull File> owlFile = (owlFilename != null && owlFilename.isPresent())
				? Optional.of(new File(owlFilename.get()))
				: Optional.<@NonNull File>empty();

		try {
			// Create an OWL ontology using the OWLAPI
			OWLOntologyManager ontologyManager = OWLManager.createOWLOntologyManager();
			OWLOntology ontology = ontologyManager.loadOntologyFromOntologyDocument(owlFile.get());

			SWRLRuleEngine ruleEngine = SWRLAPIFactory.createSWRLRuleEngine(ontology);

			long endStartupTime = System.nanoTime();
			long overallStartupTime = (endStartupTime - overallStartTime) / 1000000; 

			System.out.println("SWRLAPI startup time: " + overallStartupTime + " ms");

			long inferenceStartTime = System.nanoTime();

			ruleEngine.infer();
			ontologyManager.saveOntology(ontology);

			long inferenceEndTime = System.nanoTime();
			long overallInferenceTime = (inferenceEndTime - inferenceStartTime) / 1000000; 
			System.out.println("SWRLAPI inference time: " + overallInferenceTime + " ms");
			
			long overallEndTime = System.nanoTime();
			long duration = (overallEndTime - overallStartTime) / 1000000; 

			System.out.println("SWRLAPI overall time: " + duration + " ms");
			System.out.println("SWRLAPI execution complete on: " + args[0]);

		} catch (OWLOntologyCreationException e) {
			System.err.println("Error creating OWL ontology: " + e.getMessage());
			System.exit(-1);
		} catch (OWLOntologyStorageException e) {
			System.err.println("OWLOntologyStorageException: " + e.getMessage());
			System.exit(-1);
		} catch (RuntimeException e) {
			System.err.println("Error starting application: " + e.getMessage());
			System.exit(-1);
		}
	}
}
