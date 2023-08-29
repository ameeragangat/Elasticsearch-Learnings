#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ameeragangat
"""

# Make sure all functions have docstrings - refer to the CAM Python Style guide on how it should look
# Decide between Options 1 or 2 below
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
update_doc_query = {
    "doc": {
        "field1": "new_value1",
        "field2": "new_value2"
        # Add more fields and values as needed
    }
}

def update_document(index, document_id, doc):
    # Update a document
    es.update(index=index, id=document_id, body=doc)
    
update_document("test_index", "31", update_doc_query)

#%% OPTION 1
def delete_field_from_document(index, document_id, field_to_delete):
    # Remove a field from a document
    doc = {
        "script": {
            "source": f"ctx._source.remove('{field_to_delete}')"
        }
    }
    es.update(index=index, id=document_id, body=doc)
            
delete_field_from_document("test_index", "31", "field1")

#%% OPTION 2
def delete_field_from_document(index, document_id, field_to_delete):
    doc = {"size": 10000, "query": {"match_all": {}}}

    obs = es.search(index=index, body=doc)

    #  Remove a field from a document according to katsdpopt
    for ob in obs["hits"]["hits"]:
        doc = ob["_source"]

        if field_to_delete in doc :
            del doc[field_to_delete]
            es.index(index=index, id=document_id, body=doc)
                
delete_field_from_document("test_index", "31", "field1")

#%% OPTION 1
def update_field_in_document(index, document_id, field_to_update, new_value):
    # Update a field in a document
    doc = {
        "script": {
           "source": f"ctx._source.{field_to_update} = '{new_value}'"
        }
    }
    es.update(index=index, id=document_id, body=doc)
    
update_field_in_document("test_index", "31", "field2", "new_value3")

#%% OPTION 2
def update_field_in_document(index, document_id, field_to_update, new_value):
    doc = {"size": 10000, "query": {"match_all": {}}}

    obs = es.search(index=index, body=doc)

    #  Update a field in a document according to katsdpopt
    for ob in obs["hits"]["hits"]:
        doc = ob["_source"]

        if field_to_update in doc :
            doc[field_to_update] = new_value
            es.index(index=index, id=document_id, body=doc)
                
update_field_in_document("test_index", "31", "field2", "new_value4")

#%% Create an element in an object field in a document - TODO

#%% Update an element in an object field in a document - TODO

#%% Delete an element in an object field in a document - TODO

#%% 
def get_document_by_id(index, document_id):
    # Get full document by ID
    res = es.get(index=index, id=document_id)
    
    if res:
        print(res["_source"])
    
get_document_by_id("test_index", "31")

#%% This function can be used if fields are specified and if left blank. Is the above function necessary?
def get_document_by_id(index, document_id, fields=None):
    # Get document by id, but only certain fields 
    fields_to_retrieve = ",".join(fields) if fields else None

    # Get the document with specified fields
    res = es.get(index=index, id=document_id, _source=fields_to_retrieve)

    if res:
        print(res["_source"])

get_document_by_id("test_index", "31", fields=["field1"])
#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"field1": "new_value1"}}
            ],
            "must_not": [
                {"term": {"field2": "must_not_match_value"}}
            ],
            "should": [
                {"match": {"field3": "should_match_value1"}}
            ]
        }
    }
}

result = search_documents_by_query("test_index", query)
print("Results:", result)

#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "query": {
    "bool": {
      "should": [
        { "match": { "field1": "new_value1" } },
        { "match": { "field2": "value2" } }
      ],
      "minimum_should_match": 1
    }
  }
}

result = search_documents_by_query("test_index", query)
print("Results:", result)

#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "query": {
    "match_all": {}
  }
}

result = search_documents_by_query("test_index", query)
print("Results:", result)

#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "query": {
    "match": {
      "field1": "new_value1"
    }
  }
}

result = search_documents_by_query("test_index", query)
print("Results:", result)

#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "query": {
    "bool": {
      "filter": {
        "term": {
          "field1": "new_value1"
        }
      }
    }
  }
}

result = search_documents_by_query("test_index", query)
print("Results:", result)

#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "query": {
    "range": {
      "numeric_field": {
        "gte": 10,
        "lte": 100
      }
    }
  }
}

result = search_documents_by_query("test_index", query)
print("Results:", result)

#%%
def search_documents_by_query(index, query):
    # Get documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "query": {
    "bool": {
      "must": [
        { "match": { "field1": "value1" } },
        { "range": { "numeric_field": { "gte": 10 } } }
      ]
    }
  }
}

result = search_documents_by_query("test_index", query)
print("Search results:", result)

#%% Update all documents by query - TODO
def search_documents_by_query(index, query):
    # First one needs to get all documents by query
    res = es.search(index=index, body=query)

    return res

query = {
  "size": 100,
  "query": {
    "match_all": {}
  }
}

result = search_documents_by_query("test_index", query)
print("Search results:", result)

#%% 
def count_documents_matching_specific_query(index, field_name, desired_value):
    # Count the number of documents that match a specific query
    query = {
        "query": {
            "match": {
                field_name: desired_value
            }
        }
    }

    res = es.count(index=index, body=query)
    print("Number of documents that match a specific query = ",res["count"])
    
count_documents_matching_specific_query("test_index", "field1", "new_value1")
#%% Get multiple documents in one request - TODO
