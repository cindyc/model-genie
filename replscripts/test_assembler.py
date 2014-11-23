import composer.assemblers.neo4j_assembler as assembler

serialized = {
    "type": "Event", 
    "name": "Ballet Performance", 
    "relationships":{
        "has": [
            {"type": "Person", 
             "name": "James Bond", 
             }, 
            {"type": "Location", 
             "name": "Mountain View"
            }
        ]
    }

}

assembler.Neo4jAssembler.save(serialized)
