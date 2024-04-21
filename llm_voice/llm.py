import replicate

MODEL_LLM = "meta/meta-llama-3-8b-instruct"

ARGS = {
    "top_k": 50,
    "top_p": 0.9,
    "max_tokens": 512,
    "min_tokens": 0,
    "temperature": 0.6,
    "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant"
    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>"
    "assistant<|end_header_id|>\n\n",
    "presence_penalty": 1.15,
    "frequency_penalty": 0.2,
}


def call_llm(prompt):
    prediction = replicate.stream(MODEL_LLM, input={"prompt": prompt, **ARGS})
    output_text = ""
    for event in prediction:
        output_text += str(event)
    return output_text


if __name__ == "__main__":
    user_prompt = "Who are you?"
    _prediction = call_llm(user_prompt)
    print(_prediction)
