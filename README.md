model-genie
=============

What does it do?
===============
Model-genie does multi-way conversions and persistence for models.
- Define a model in json and turn it into a ModelDefinition
- Define an ORM model (i.e. django, schematics, sqlalchemy) and turn it into a
ModelDefinition
- Define a ModelDefinition and serialize it to json
- Define a ModelDefinition and turn it into an ORM model
- Define a model in json and turn it into an ORM model


Why use it?  
===========
- New models can be defined dynamically (even by user) by calling the rest API with model
definition json
- ModelDefintions can be serialized to json and persisted to database or the filesystem, they can then be queried and be turned into ORM model on-demand
- The rest APIs provide an universal interface to define models. 
- Different ORM systems are supported through plugins
- Raw data can be parsed by ModelDefinition parsers and turn into different model types
