#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ameeragangat
"""

#%%
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200/")

#%%
create_index_query = {
    # Define the index settings and mappings
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
    },
    "mappings": {
        "properties": {
            "field1": {"type": "text"},
            "field2": {"type": "keyword"}
            # Add more fields and types as needed
        }
    }
}

def create_index(es, index, doc):
    # Create an index
    es.indices.create(index=index, body=doc)
    
create_index(es, "test_index", create_index_query)

#%%
custom_index_create_query = {
    "field1": {"type": "text"},
    "field2": {"type": "keyword"},
    "field3": {"type": "integer"}
    # Add more fields and types as needed
}

def create_index(index, custom_mappings, number_of_shards=3, number_of_replicas=2):
    settings = {
        "settings": {
            "number_of_shards": number_of_shards,
            "number_of_replicas": number_of_replicas
        },
        "mappings": {
            "properties": custom_mappings
        }
    }

    # Create the index
    es.indices.create(index=index, body=settings)
    
create_index("test_index_1", custom_index_create_query, number_of_shards=5, number_of_replicas=1)

#%%
def delete_index(index):
    # Delete an index
    es.indices.delete(index=index)

delete_index("test_index")

#%%
create_doc_query = {
    "field1": "value1",
    "field2": "value2"
    # Add more fields and values as needed
}

def create_document(index, doc, document_id=None):
    # Create a document in an index
    if document_id:
        es.index(index=index, id=document_id, body=doc)
    else:
        es.index(index=index, body=doc)
        
create_document("test_index", create_doc_query, "31")

#%%
def delete_document(index, document_id):
    # Delete a document in an index
    es.delete(index=index, id=document_id)
    
delete_document("test_index", "31")

#%%