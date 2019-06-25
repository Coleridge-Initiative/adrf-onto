# ADRF Ontology

The focus for this repo is a mid-level ontology specification for
ADRF, managed in the `adrf.ttl` file.  

Note: that's in [*TTL*](https://www.w3.org/TR/turtle/) format
(pronounced "turtle").


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

We use the following packages:

  * [*rdflib*](https://rdflib.readthedocs.io/): load and parse the RDF input
  * [*skosify*](https://skosify.readthedocs.io/): validate our use of SKOS vocabulary

To load, parse, and validate the ontology file:

```
./onto.py adrf.ttl
```

Then review the generated `tmp.ttl` output file to make sure it
doesn't show any errors.

For more details about the *inference rules* used, see
[*SKOS-Inference*](https://github.com/NatLibFi/Skosify/wiki/SKOS-Inference).


## Roadmap

Later, we'll automated these tests.

A more comprehensive online service for validating SKOS files is
available at [*PoolParty*](https://qskos.poolparty.biz/login).

See the [wiki](https://github.com/Coleridge-Initiative/adrf-onto/wiki) for this repo for more detailed specifications.
