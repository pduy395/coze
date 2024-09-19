from llama_cpp import Llama

from transformers import pipeline


llm = Llama (model_path='C://Users//llm_intern//.cache//huggingface//hub//models--lmstudio-ai--gemma-2b-it-GGUF//snapshots//a0b140bfb922a743f89dd0682a24a17516071ab9//gemma-2b-it-q4_k_m.gguf',             
             n_ctx=2024,
             n_gpu_layers=-1,
             main_gpu=0,
             
             )

res = llm.create_chat_completion(
		messages = [
			{
				"role": "user",
				"content": "What is the capital of France"
			}
		],
)
print(res)

