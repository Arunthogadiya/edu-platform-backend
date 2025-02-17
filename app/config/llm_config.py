# config/llm_config.py
LLM_CONFIG = {
    "openai": {
        "api_key": "your-api-key",
        "temperature": 0.7
    },
    "ollama": {
        "model": "llama2",
        "temperature": 0.7
    }
}

BHASHINI_CONFIG = {
    "pipeline_config_endpoint": "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline",
    "inference_endpoint": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
    "pipeline_id": "64392f96daac500b55c543cd",
    "user_id": "9e66ee1ff55b46b7b7584a6e0c04e4a6",
    "api_key": "23e623b2d2-2856-4f05-ae3d-0d090210e27a"
}

BASIC_PROMPT_TEMPLATE = """Question: {question}

Answer: Let's think step by step."""

RAG_TEMPLATE = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

<context>
{context}
</context>

Question: {question}"""