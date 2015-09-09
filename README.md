ModelGenie
=============
Turn unstructured data into structured data.

What does it do?
===============
Model-genie does multi-way conversions and persistence for models.
- Define a model in json and turn it into a ModelDefinition
- Define an ORM model (i.e. django, schematics, sqlalchemy) and turn it into a
ModelDefinition
- Define a ModelDefinition and serialize it to json
- Define a ModelDefinition and turn it into an ORM model
- Define a model in json and turn it into an ORM model
- Add parsers as plugins to turn raw text data into models
- Training system to coerce raw data into model definitions


Why use it?  
===========
- New models can be defined dynamically (even by user) by calling the rest API with model
definition json
- ModelDefintions can be serialized to json and persisted to database or the filesystem, they can then be queried and be turned into ORM model on-demand
- The rest APIs provide an universal interface to define models. 
- Different ORM systems are supported through plugins
