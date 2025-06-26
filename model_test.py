import json
import requests
import json
from typing import List


def read_user_inputs(path: str):
    with open(path, "r") as file:
        data = json.load(file)
        return data


def select_user_inputs(input_type: str, inputs: dict) -> List[str]:
    if input_type == "all":
        out = list(inputs["baseline"])
        out.extend(list(inputs["filter"].keys()))
        return out
    elif input_type == "filter":
        return list(inputs[input_type].keys())
    elif input_type == "baseline":
        return inputs[input_type]
    else:
        return list(inputs[input_type])


def read_prompt_base(prompt_num: int) -> dict:
    with open("testing/data/prompts/" + str(prompt_num) + ".txt", "r") as file:
        data = file.read()
        out = {"text": data, "base_id": str(prompt_num)}
        return out


def create_full_prompt(prompt: dict, user_input: str) -> dict:
    return {
        "text": prompt["text"] + "\n" + user_input + "\n\nSummary:",
        "base_id": prompt["base_id"],
        "user_input": user_input,
    }


def get_model_names(path: str):
    with open(path, "r") as file:
        data = json.load(file)
    return list(data["models"].keys())


def create_model_report(query_result: dict, prompt: dict) -> dict:
    if query_result["choices"][0]["message"]["content"] == "Filtered":
        filtered = 1
    else:
        filtered = 0
    return {
        "model": query_result["model"].rsplit("/", 1)[-1],
        "base_id": prompt["base_id"],
        "user_input": prompt["user_input"],
        "filtered": filtered,
        "completion": query_result["choices"][0]["message"]["content"],
        "prompt_tokens": query_result["usage"]["prompt_tokens"],
        "completion_tokens": query_result["usage"]["completion_tokens"],
    }


def send_request(prompt, model, api_key, temperature=0.6):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/" + model,
        "max_tokens": 400,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt["text"]}],
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    response = requests.post(url, headers=headers, json=payload)
    report = create_model_report(response.json(), prompt)
    return report
