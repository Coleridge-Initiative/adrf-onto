#!/usr/bin/env python
# encoding: utf-8

import rdflib
import skosify
import sys

# see docs:
# https://semantic-web.com/2017/08/21/standard-build-knowledge-graphs-12-facts-skos/
# https://skosify.readthedocs.io/en/latest/


if __name__ == "__main__":
    # test with:
    # ./onto.py adrf.ttl

    # load the ontology graph
    onto_path = sys.argv[1]
    graph = rdflib.Graph().parse(onto_path, format="n3")

    # enumerate the S/V/O relationships within the graph
    for subj, pred, obj in graph:
        print(subj, pred, obj)

    # convert, extend, and check the SKOS vocabulary used
    config = skosify.config("skosify.cfg")
    voc = skosify.skosify(graph, **config)
    voc.serialize(destination="tmp.ttl", format="n3")

    # validate the inference rules
    skosify.infer.skos_related(graph)
    skosify.infer.skos_topConcept(graph)
    skosify.infer.skos_hierarchical(graph, narrower=True)
    skosify.infer.skos_transitive(graph, narrower=True)

    skosify.infer.rdfs_classes(graph)
    skosify.infer.rdfs_properties(graph)
