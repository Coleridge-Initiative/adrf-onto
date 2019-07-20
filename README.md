# ADRF Ontology

Welcome to `adrf-onto` which is used to construct, validate, and
leverage the Rich Contexgt knowledge graph within the ADRF framework.

Some files of particular interest:

  * `adrf.ttl` -- a mid-level ontology specification for ADRF
  * `rcc.ttl` -- results from the [Rich Context Competition](https://coleridgeinitiative.org/richcontextcompetition), represented in a graph using the ADRF ontology
  * `onto.py` -- a brief Python script used to load and validate the graph data
  * `vocab.json` -- a JSON-LD context for [*compaction*](https://www.w3.org/TR/json-ld-api/#compaction) of the output graph files

Note that this data is represented in [*TTL*](https://www.w3.org/TR/turtle/) format
(pronounced "turtle") for the parts that humans read and write.
We use [*JSON-LD*](https://json-ld.org/) format for the parts of the graph that machines consume or produce.
A couple lines of Python convert between those two formats rather quickly.


## Dependencies

The following assumes that your Python binary is located at
`/usr/bin/python3` -- change that as needed.

To set up a virtual environment for Python 3.x using `virtualenv`:
```
virtualenv -p /usr/bin/python3 ~/venv
pip install --upgrade pip
pip install -r requirements.txt
```

Then to activate the environment:
```
source ~/venv/bin/activate
```


## Validation

A variety of "unit tests" can be performed on this ontology spec, so
that as multiple people are collaborating to develop it, we can make
sure that the committed file is consistent.

To load, parse, and validate the files used to construct the graph:

```
./onto.py adrf.ttl rcc.ttl
```

Then review the generated `tmp.ttl` output file to make sure it
doesn't show any errors.

Also, the `tmp.json` shows that same graph in JSON-LD format (machine
readable).

For more details about the *inference rules* used, see
[*SKOS-Inference*](https://github.com/NatLibFi/Skosify/wiki/SKOS-Inference).

We're using the following packages:

  * [*rdflib*](https://rdflib.readthedocs.io/): load and parse the RDF input
  * [*rdflib-jsonld*](https://github.com/RDFLib/rdflib-jsonld): read/write JSON-LD format
  * [*skosify*](https://skosify.readthedocs.io/): validate our use of SKOS vocabulary


## Roadmap

Later, we'll automated these tests.

A more comprehensive online service for validating SKOS files is
available at [*PoolParty*](https://qskos.poolparty.biz/login).

See the [wiki](https://github.com/Coleridge-Initiative/adrf-onto/wiki) for this repo for more detailed specifications.
