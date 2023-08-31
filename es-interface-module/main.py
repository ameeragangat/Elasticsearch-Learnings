#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script contains a ElasticSearch python interface module with various common
queries methods

reference: https://www.elastic.co/guide/en/elasticsearch/client/python-api/7.16/overview.html

@author: ameeragangat
"""
#imports
from elasticsearch import Elasticsearch

class ElasticsearchInterface:
    """
    A class that provides an interface to interact with Elasticsearch.

    Parameters:
        host (str): The Elasticsearch host. Default is 'localhost'.
        port (int): The Elasticsearch port. Default is 9200.
    """
    def __init__(self, host='localhost', port=9200):
        self.host = host
        self.port = port
        self.client = Elasticsearch([{'host': self.host, 'port': self.port}])


    def create_index(self, index_name):
        """
        Create an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index to create.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.indices.create(index=index_name)
            return response
        except Exception as e:
            print(f"An error occurred while creating index: {e}")
            return None

    def create_document(self, index_name, doc_id, document):
        """
        Create a document within an index.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            document (dict): The document data.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.index(index=index_name, id=doc_id, body=document)
            return response
        except Exception as e:
            print(f"An error occurred while creating document: {e}")
            return None

    def delete_index(self, index_name):
        """
        Delete an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index to delete.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.indices.delete(index=index_name)
            return response
        except Exception as e:
            print(f"An error occurred while deleting index: {e}")
            return None

    def get_document(self, index_name, doc_id):
        """
        Get a document from an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document to retrieve.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.get(index=index_name, id=doc_id)
            return response['_source']
        except Exception as e:
            print(f"An error occurred while getting document: {e}")
            return None

    def refresh_index(self, index_name):
        """
        Refresh an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index to refresh.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.indices.refresh(index=index_name)
            return response
        except Exception as e:
            print(f"An error occurred while refreshing index: {e}")
            return None

    def search_document(self, index_name, query):
        """
        Search for documents in an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index.
            query (dict): The query to search for documents.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.search(index=index_name, body=query)
            return response['hits']['hits']
        except Exception as e:
            print(f"An error occurred while searching for document: {e}")
            return None

    def update_document(self, index_name, doc_id, updated_document):
        """
        Update a document in an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document to update.
            updated_document (dict): The updated document data.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.update(index=index_name, id=doc_id, body={"doc": updated_document})
            return response
        except Exception as e:
            print(f"An error occurred while updating document: {e}")
            return None

    def delete_document(self, index_name, doc_id):
        """
        Delete a document from an Elasticsearch index.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document to delete.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.delete(index=index_name, id=doc_id)
            return response
        except Exception as e:
            print(f"An error occurred while deleting document: {e}")
            return None
        
    def create_field_in_document(self, index_name, doc_id, field_name, field_value):
        """
        Create a new field in a document.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            field_name (str): The name of the new field.
            field_value: The value of the new field.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            script = {
                "source": f"ctx._source.{field_name} = '{field_value}'"
            }
            response = self.client.update(index=index_name, id=doc_id, body={"script": script})
            return response
        except Exception as e:
            print(f"An error occurred while creating field: {e}")
            return None
        
    def delete_field_from_document(self, index_name, doc_id, field_name):
        """
        Delete a field from a document.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            field_name (str): The name of the field to delete.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            script = {
                "source": f"ctx._source.remove('{field_name}')"
            }
            response = self.client.update(index=index_name, id=doc_id, body={"script": script})
            return response
        except Exception as e:
            print(f"An error occurred while deleting field: {e}")
            return None
      
    def update_field_in_document(self, index_name, doc_id, field_name, new_field_value):
        """
        Update the value of a field in a document.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            field_name (str): The name of the field to update.
            new_field_value: The new value for the field.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            script = {
                "source": f"ctx._source.{field_name} = '{new_field_value}'"
            }
            response = self.client.update(index=index_name, id=doc_id, body={"script": script})
            return response
        except Exception as e:
            print(f"An error occurred while updating field: {e}")
            return None

    def create_element_in_object_field(self, index_name, doc_id, object_field_name, element):
        """
        Create an element in an object field of a document.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            object_field_name (str): The name of the object field.
            element: The element to create in the object field.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            script = {
                "source": f"ctx._source.{object_field_name} = '{element}'"
            }
            response = self.client.update(index=index_name, id=doc_id, body={"script": script})
            return response
        except Exception as e:
            print(f"An error occurred while creating element: {e}")
            return None
        
    def delete_element_from_object_field(self, index_name, doc_id, object_field_name, element):
        """
        Delete an element from a specified object field of a document.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            object_field_name (str): The name of the object field containing the element.
            element (str): The element to delete from the object field.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            # First, get the existing document
            existing_document = self.client.get(index=index_name, id=doc_id)

            # Update the specified object field's list by removing the specified element
            object_field = existing_document["_source"][object_field_name]
            object_field.remove(element)

            # Update the document with the modified object field
            updated_document = {"doc": {object_field_name: object_field}}
            response = self.client.update(index=index_name, id=doc_id, body=updated_document)

            return response
        except Exception as e:
            print(f"An error occurred while deleting element: {e}")
            return None
        
    def update_element_in_object_field(self, index_name, doc_id, object_field_name, old_element, new_element):
        """
        Update an element in a specified object field of a document.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            object_field_name (str): The name of the object field containing the elements.
            old_element (str): The element to be updated.
            new_element (str): The updated element.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            # First, get the existing document
            existing_document = self.client.get(index=index_name, id=doc_id)

            # Update the specified object field's list by replacing the old element with the new element
            object_field = existing_document["_source"][object_field_name]
            if old_element in object_field:
                index_of_old_element = object_field.index(old_element)
                object_field[index_of_old_element] = new_element

                # Update the document with the modified object field
                updated_document = {"doc": {object_field_name: object_field}}
                response = self.client.update(index=index_name, id=doc_id, body=updated_document)

                return response
            else:
                print(f"The specified old element '{old_element}' was not found.")
                return None
        except Exception as e:
            print(f"An error occurred while updating element: {e}")
            return None

    def get_full_document_by_id(self, index_name, doc_id):
        """
        Get the full document by its ID.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.

        Returns:
            response (dict): Elasticsearch response document data.
        """
        try:
            response = self.client.get(index=index_name, id=doc_id)
            return response['_source']
        except Exception as e:
            print(f"An error occurred while getting full document: {e}")
            return None
            
    def get_partial_document(self, index_name, doc_id, fields):
        """
        Get specific fields of a document by its ID.

        Parameters:
            index_name (str): The name of the index.
            doc_id (str): The ID of the document.
            fields (list): List of field names to retrieve.

        Returns:
            response (dict): Elasticsearch response document data.
        """
        try:
            response = self.client.get(index=index_name, id=doc_id, _source=fields)
            return response['_source']
        except Exception as e:
            print(f"An error occurred while getting partial document: {e}")
            return None
       
    def search_documents_by_query(self, index_name, query):
        """
        Search for documents using a complex query.

        Parameters:
            index_name (str): The name of the index.
            query (dict): The complex query containing combinations of must, must_not, should, etc.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            response = self.client.search(index=index_name, body=query)
            return response
        except Exception as e:
            print(f"An error occurred while searching for documents by query: {e}")
            return None
      
    def get_all_documents(self, index_name):
        """
        Retrieve all documents from an index.

        Parameters:
            index_name (str): The name of the index.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            query = {"query": {"match_all": {}}}
            response = self.client.search(index=index_name, body=query)
            return response 
        except Exception as e:
            print(f"An error occurred while retrieving all documents: {e}")
            return None
 
    def get_documents_by_field_value(self, index_name, field_name, field_value):
        """
        Retrieve documents that match a specific field and value.

        Parameters:
            index_name (str): The name of the index.
            field_name (str): The name of the field to match.
            field_value: The value to match for the field.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            query = {"query": {"match": {field_name: field_value}}}
            response = self.client.search(index=index_name, body=query)
            return response
        except Exception as e:
            print(f"An error occurred while retrieving documents by field value: {e}")
            return None
      
    def get_documents_in_field_range(self, index_name, field_name, start_range, end_range):
        """
        Retrieve documents within a specified range of values in a field.

        Parameters:
            index_name (str): The name of the index.
            field_name (str): The name of the field.
            start_range: The start of the range (inclusive).
            end_range: The end of the range (inclusive).

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            query = {"query": {"range": {field_name: {"gte": start_range, "lte": end_range}}}}
            response = self.client.search(index=index_name, body=query)
            return response
        except Exception as e:
            print(f"An error occurred while retrieving documents within field range: {e}")
            return None
        
    def combine_queries_with_boolean_logic(self, index_name, must_queries=None, must_not_queries=None, should_queries=None):
        """
        Combine multiple queries using boolean logic (AND, OR, NOT).

        Parameters:
            index_name (str): The name of the index.
            must_queries (list): List of queries that must match (AND).
            must_not_queries (list): List of queries that must not match (NOT).
            should_queries (list): List of queries where at least one should match (OR).

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            combined_query = {"bool": {}}
            
            if must_queries:
                combined_query["bool"]["must"] = must_queries
            if must_not_queries:
                combined_query["bool"]["must_not"] = must_not_queries
            if should_queries:
                combined_query["bool"]["should"] = should_queries
            
            query = {"query": combined_query}
            response = self.client.search(index=index_name, body=query)  
            return response
        except Exception as e:
            print(f"An error occurred while combining queries with boolean logic: {e}")
            return None

    def update_documents_by_query(self, index_name, query, update_script):
        """
        Update all documents that match a specific query.

        Parameters:
            index_name (str): The name of the index.
            query (dict): The query to match documents for update.
            update_script (dict): The update script to apply to matched documents.

        Returns:
            response (dict): Elasticsearch response.
        """
        try:
            update_body = {"query": query, "script": update_script}
            response = self.client.update_by_query(index=index_name, body=update_body)
            return response
        except Exception as e:
            print(f"An error occurred while updating documents by query: {e}")
            return None
    
    def count_documents_by_query(self, index_name, field_name, desired_value):
        """
        Count the number of documents that match a specific query.

        Parameters:
            field_name (str): field_name.
            desired_value (str): desired_value
        Returns:
            resppnse (int): Number of documents that match the query.
        """
        try:
            query = {
                "query": {
                    "match": {
                        field_name: desired_value
                    }
                }
            }
            response = self.client.count(index_name, body=query)
            return response['count']
        except Exception as e:
            print(f"An error occurred while counting documents by query: {e}")
            return None
        
    
    def get_multiple_documents(self, doc_ids):
        """
        Get multiple documents in one request.

        Parameters:
            doc_ids (list): List of document IDs.

        Returns:
            List of retrieved documents.
        """
        try:
            query = {"ids": {"values": doc_ids}}
            response = self.client.mget(body=query, index=self.index_name)
            return [hit['_source'] for hit in response['docs'] if hit['found']]
        except Exception as e:
            print(f"An error occurred while getting multiple documents: {e}")
            return None
#%%
# Example usage
if __name__ == "__main__":
    #%%
    es_interface = ElasticsearchInterface()
    
    #%% create index and create document

    index_name = "example_index_1"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": "value_2"}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)
    
    #%% get a document
    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)

    #%% refreshing an index
    es_interface.refresh_index(index_name)    
   
    #%% Searching for a document
    query = {"query": {"match": {"field_1": "value_1"}}}
    search_results = es_interface.search_document(index_name, query)
    print("Search Results:", search_results)

    #%% Updating a document
    updated_document = {"field_1": "new_value_1", "field_2": "new_value_2"}
    es_interface.update_document(index_name, doc_id, updated_document)

    #%% Getting updated document
    updated_document = es_interface.get_document(index_name, doc_id)
    print("Retrieved Document:", updated_document)

    #%% Deleting a document
    es_interface.delete_document(index_name, doc_id)
    
    #%% delete an index
    es_interface.delete_index(index_name)
    
    #%% creating a field in a document
    index_name = "example_index_2"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": "value_2"}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Creating a new field in the document
    new_field_name = "author"
    new_field_value = "Ameera"
    es_interface.create_field_in_document(index_name, doc_id, new_field_name, new_field_value)
    
    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)
    
    #%% deletng field from a document
    index_name = "example_index_3"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": "value_2"}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Deleting a field from the document
    field_to_delete = "field_2"
    es_interface.delete_field_from_document(index_name, doc_id, field_to_delete)    

    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)

    #%% updating a field in a document
    index_name = "example_index_4"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": "value_2"}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Updating a field in the document
    field_to_update = "field_2"
    new_field_value = "updated value_2"
    es_interface.update_field_in_document(index_name, doc_id, field_to_update, new_field_value)

    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)

    #%% creating an element in an object field
    index_name = "example_index_5"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": {"author": "ameera"}}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Creating an element in an object field
    object_field_to_update = "field_2.author"
    new_element = "ameera new"
    es_interface.create_element_in_object_field(index_name, doc_id, object_field_to_update, new_element)

    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)

    #%% delete an element from an object field
    index_name = "example_index_6"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": ["val_1", "val_2", "val_3"]}
    
    # Creating an index
    es_interface.create_index(index_name)
    
    # Creating a document
    es_interface.create_document(index_name, doc_id, document)
    
    # Deleting an element from an object field
    object_field_to_update = "field_2"
    element_to_delete = "val_2"
    es_interface.delete_element_from_object_field(index_name, doc_id, object_field_to_update, element_to_delete)

    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)


    #%% Update an element in an object field in a document
    index_name = "example_index_7"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": ["val_1", "val_2", "val_3"]}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Updating an element in an object field
    object_field_to_update = "field_2"
    old_element = "val_3"
    new_element = "val_3_new"
    es_interface.update_element_in_object_field(index_name, doc_id, object_field_to_update, old_element, new_element)

    getting_document = es_interface.get_document(index_name, doc_id)
    print("Getting Document:", getting_document)

    #%% get full document by id
    index_name = "example_index_8"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": ["val_1", "val_2", "val_3"]}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Getting the full document by ID
    retrieved_full_document = es_interface.get_full_document_by_id(index_name, doc_id)
    print("Retrieved Full Document:", retrieved_full_document)

    #%% Get document by id, but only certain fields
    index_name = "example_index_9"
    doc_id = "1"
    document = {"field_1": "value_1", "field_2": ["val_1", "val_2", "val_3"]}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating a document
    es_interface.create_document(index_name, doc_id, document)

    # Getting specific fields of the document by ID
    fields_to_retrieve = ["field_2"]
    retrieved_partial_document = es_interface.get_partial_document(index_name, doc_id, fields_to_retrieve)
    print("Retrieved Partial Document:", retrieved_partial_document)    

    #%% Get documents by query (combination of must, must not, should, etc)
    index_name = "example_index_10"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"field1": "value1", "field2": "value2"}
    document_2 = {"title": "Example Document 2", "content": "This is an example document content 2."}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    # Searching for documents using a complex query
    complex_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"field1": "value1"}}
                ]
            }
        }
    }
    search_results = es_interface.search_documents_by_query(index_name, complex_query)
    print("Complex Query Search Results:", search_results)

    #%% retrieve all documents from an index
    index_name = "example_index_11"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"field1": "value1", "field2": "value2"}
    document_2 = {"field3": "value3", "field4": "value4"}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    # Retrieving all documents from the index
    all_documents = es_interface.get_all_documents(index_name)
    print("All Documents:", all_documents)
    
    #%% Retrieve documents that match a specific field and value
    index_name = "example_index_12"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"field1": "value1", "field2": "value2"}
    document_2 = {"field3": "value3", "field4": "value4"}
    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    # Retrieving documents that match a specific field and value
    field_to_match = "field2"
    value_to_match = "value2"
    matching_documents = es_interface.get_documents_by_field_value(index_name, field_to_match, value_to_match)
    print("Matching Documents:", matching_documents)    
    
    #%% Retrieve documents within a specified range of values in a field
    index_name = "example_index_13"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"title": "Example Document 1", "views": 150}
    document_2 = {"title": "Example Document 2", "views": 300}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    # Retrieving documents within a specified range of values in a field
    field_to_match = "views"
    start_range = 100
    end_range = 200
    matching_documents = es_interface.get_documents_in_field_range(index_name, field_to_match, start_range, end_range)
    print("Documents within Field Range:", matching_documents)

    #%% Combine multiple queries using boolean logic (AND,OR,NOT)
    index_name = "example_index_14"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"title": "Example Document 1", "content": "This is an example document content 1.", "category": "tech"}
    document_2 = {"title": "Example Document 2", "content": "This is an example document content 2.", "category": "science"}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    # Combining queries with boolean logic (AND, OR, NOT)
    must_match_query = {"match": {"category": "tech"}}
    must_not_match_query = {"match": {"content": "content 2"}}
    combined_documents = es_interface.combine_queries_with_boolean_logic(index_name, must_queries=[must_match_query], must_not_queries=[must_not_match_query])
    print("Combined Query Search Results:", combined_documents)

    #%% Update all documents by query
    index_name = "example_index_15"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"title": "Example Document 1", "views": 150}
    document_2 = {"title": "Example Document 2", "views": 300}

    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    # Updating documents using a query and script
    query_to_match = {"range": {"views": {"gte": 200}}}
    update_script = {"source": "ctx._source.views += params.value", "params": {"value": 50}}
    update_response = es_interface.update_documents_by_query(index_name, query_to_match, update_script)
    print("Update Documents by Query Response:", update_response)
    
    #%% Count the number of documents that match a specific query
    index_name = "example_index_17"
    doc_id_1 = "1"
    doc_id_2 = "2"
    document_1 = {"field1": "value1", "field2": "value2"}
    document_2 = {"field3": "value3", "field4": "value4"}
    # Creating an index
    es_interface.create_index(index_name)

    # Creating documents
    es_interface.create_document(index_name, doc_id_1, document_1)
    es_interface.create_document(index_name, doc_id_2, document_2)

    count = es_interface.count_documents_by_query(index_name,"field1", "value1")
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    










    
 