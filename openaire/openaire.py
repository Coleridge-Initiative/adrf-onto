#!/usr/bin/env python
# encoding: utf-8

from rdflib import Graph, plugin
from rdflib.plugin import register, Parser, Serializer
from urllib import parse
import csv
import hashlib
import json
import pyld
import sys
import urllib.request
import xml.etree.ElementTree as et


API_URI = "http://api.openaire.eu/search/publications?title="

NS = {
    "oaf": "http://namespace.openaire.eu/oaf"
    }

TTL_HEADER = """
@base <https://github.com/Coleridge-Initiative/adrf-onto/wiki/Vocabulary> .
@prefix cito:   <http://purl.org/spar/cito/> .
@prefix dct:    <http://purl.org/dc/terms/> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
"""

PUB_TEMPLATE = """
:{}
  rdf:type :ResearchPublication ;
  dct:title "{}"@en ;
  dct:identifier "{}" ;
  dct:language "en" ;
  foaf:page "{}"^^xsd:anyURI ;
  .
"""


def iter_pub (filename):
    with open(filename) as f:
        for row in csv.reader(f, delimiter=","):
            dataset, doi, journal, title = row[:4]
            yield doi, journal, title


def get_hash (doi, journal, title):
    m = hashlib.blake2b(digest_size=10)
    m.update(doi.encode("utf-8"))
    m.update(journal.encode("utf-8"))
    m.update(title.encode("utf-8"))
    return m.hexdigest()


def load_uri (uri):
    with urllib.request.urlopen(uri) as response:
        html = response.read()
        return html.decode("utf-8")


def extract_pub_uri (xml):
    root = et.fromstring(xml)
    result = root.findall("./results/result[1]/metadata/oaf:entity/oaf:result", NS)

    if len(result) > 0:
        url_list = result[0].findall("./children/instance/webresource/url")

        if len(url_list) > 0:
            pub_url = url_list[0].text
            return pub_url

    return None


def lookup_pub_uris (iter, debug=False):
    for doi, journal, title in iter:
        if debug:
            print(doi, journal, title)

        xml = load_uri(API_URI + parse.quote(title))

        if debug:
            print(xml)

        pub_url = extract_pub_uri(xml)

        if pub_url:
            pub_id = "publication-{}".format(get_hash(doi, journal, title))
            yield doi, pub_id, pub_url, journal, title


if __name__ == "__main__":
    DEBUG = False # True

    filename = sys.argv[1]
    iter = iter_pub(filename)

    if DEBUG:
        iter = [["foo", "Does a Nutritious Diet Cost More in Food Deserts?"]]


    # pull results from the API
    results = [ row for row in lookup_pub_uris(iter, debug=DEBUG) ]
    print(json.dumps(results, indent=2))


    # format as JSON_LD
    with open("../vocab.json", "r") as f:
        CONTEXT = json.load(f)

    frags = [TTL_HEADER]

    for doi, pub_id, pub_url, journal, title in results:
        frags.append(PUB_TEMPLATE.format(pub_id, title, doi, pub_url))

    g = Graph()
    g.parse(data="\n".join(frags), format="n3")

    jsonld = json.loads(g.serialize(format="json-ld", context=CONTEXT))
    jsonld = pyld.jsonld.compact(jsonld, CONTEXT)

    print(json.dumps(jsonld, indent=2))
