#!/usr/bin/env python
# encoding: utf-8

from rdflib.serializer import Serializer
import rdflib
import skosify
import sys

# see docs:
# https://semantic-web.com/2017/08/21/standard-build-knowledge-graphs-12-facts-skos/
# https://skosify.readthedocs.io/en/latest/


if __name__ == "__main__":
    # test with:
    # ./onto.py adrf.ttl rcc.ttl

    # load the graph
    ttl_paths = sys.argv[1:]
    graph = rdflib.Graph()

    for ttl_file in ttl_paths:
        print("loading TTL file: {}".format(ttl_file))
        graph.parse(ttl_file, format="n3")

    # an example lookup
    # https://github.com/Coleridge-Initiative/adrf-onto/wiki/Vocabulary#Catalog
    print(list(graph[::rdflib.Literal("ADRF Data Catalog")]))

    # enumerate the S/V/O relationships within the graph
    for subj, pred, obj in graph:
        print(subj, pred, obj)

    # transform graph into JSON-LD
    with open("tmp.json", "wb") as f:
        f.write(graph.serialize(format="json-ld", indent=2))

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

    # for the humans watching, print a note that all steps completed
    print("OK")
