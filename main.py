import os
import openai
import random
import logging

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise Exception("No OpenAI API key found. Please set it as an environment variable.")

# Function to generate queries using OpenAI's ChatGPT
def generate_queries_chatgpt(original_query):
    logging.info(f"Generating queries for the original query: {original_query}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates multiple search queries based on a single input query."},
                {"role": "user", "content": f"Generate multiple search queries related to: {original_query}"},
                {"role": "user", "content": "OUTPUT (4 queries):"}
            ]
        )
        generated_queries = response.choices[0]["message"]["content"].strip().split("\n")
        logging.info(f"Generated queries: {generated_queries}")
        return generated_queries
    except Exception as e:
        logging.error(f"Error generating queries: {e}")
        return []

# Mock function to simulate vector search, returning random scores
def vector_search(query, all_documents):
    logging.info(f"Performing vector search for query: {query}")
    available_docs = list(all_documents.keys())
    random.shuffle(available_docs)
    selected_docs = available_docs[:random.randint(2, 5)]
    scores = {doc: round(random.uniform(0.7, 0.9), 2) for doc in selected_docs}
    return {doc: score for doc, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)}

# Reciprocal Rank Fusion algorithm
def reciprocal_rank_fusion(search_results_dict, k=60):
    fused_scores = {}
    logging.info("Initial individual search result ranks:")
    for query, doc_scores in search_results_dict.items():
        logging.info(f"For query '{query}': {doc_scores}")

    for query, doc_scores in search_results_dict.items():
        for rank, (doc, score) in enumerate(sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)):
            if doc not in fused_scores:
                fused_scores[doc] = 0
            previous_score = fused_scores[doc]
            fused_scores[doc] += 1 / (rank + k)
            logging.debug(f"Updating score for {doc} from {previous_score} to {fused_scores[doc]} based on rank {rank} in query '{query}'")

    reranked_results = {doc: score for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)}
    logging.info(f"Final reranked results: {reranked_results}")
    return reranked_results

# Dummy function to simulate generative output
def generate_output(reranked_results, queries):
    return f"Final output based on {queries} and reranked documents: {list(reranked_results.keys())}"

# Preprocess query
def preprocess_query(query):
    logging.info(f"Preprocessing query: {query}")
    # Example preprocessing steps (can be expanded as needed)
    query = query.lower().strip()
    return query

# Predefined set of documents related to water life and marine ecosystems
all_documents = {
    "doc1": "The impact of climate change on marine life.",
    "doc2": "Conservation efforts for endangered marine species.",
    "doc3": "The role of coral reefs in ocean biodiversity.",
    "doc4": "Effects of pollution on marine ecosystems.",
    "doc5": "Sustainable fishing practices and their importance.",
}

# Main function
if __name__ == "__main__":
    try:
        original_query = "impact of climate change on marine life"
        preprocessed_query = preprocess_query(original_query)
        generated_queries = generate_queries_chatgpt(preprocessed_query)
        
        all_results = {}
        for query in generated_queries:
            search_results = vector_search(query, all_documents)
            all_results[query] = search_results
        
        reranked_results = reciprocal_rank_fusion(all_results)
        
        final_output = generate_output(reranked_results, generated_queries)
        
        logging.info(final_output)
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
