from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    SemanticSettings,
    SemanticConfiguration,
    PrioritizedFields,
    SemanticField
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

def create_index():
    credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    
    index_client = SearchIndexClient(endpoint, credential)
    
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
        SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source", type=SearchFieldDataType.String),
    ]

    fields.append(
        SearchableField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,  
            vector_search_profile_name="my-vector-profile"
        )
    )

    vector_search = VectorSearch(
        profiles=[VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="my-algorithms-config"
        )],
        algorithms=[HnswAlgorithmConfiguration(
            name="my-algorithms-config"
        )]
    )

    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=PrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")],
            keywords_fields=[SemanticField(field_name="category")]
        )
    )
    
    semantic_settings = SemanticSettings(configurations=[semantic_config])

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_settings=semantic_settings
    )
    
    try:
        index_client.create_index(index)
        print(f"Index '{index_name}' created successfully")
    except Exception as ex:
        print(f"Error creating index: {ex}")