## Rag Fusion - RFF Algorithm

This system is designed to enhance search results by generating `multiple queries` from a user's initial query, conducting vector-based searches, and `re-ranking` the results using the `Reciprocal Rank Fusion` (RRF) algorithm.

## Architecture

![image](https://github.com/user-attachments/assets/d33eb54d-a0eb-4be0-9811-710f2dc1b2b9)

## Workflow

1. Initial Query: User provides an initial search query.
2. Query Generation: The system generates multiple related queries using the `GPT model`.
3. Vector Search: Each generated query is used to perform a vector-based search, retrieving documents from a predefined set.
4. Reciprocal Rank Fusion: Retrieved documents are `re-ranked` based on their relevance across multiple queries using the `RRF` algorithm.
5. Final Output: A re-ranked list of documents is produced, offering the most relevant search results.

## License

For more information, please refer to the full research paper [here](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf).
