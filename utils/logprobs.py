import openai
import json

openai_config = json.loads(open("openai.config").read())
openai.api_key = openai_config["api_key"]
openai.organization = openai_config["organization"]


def write_doc(text, file, model):
    doc = "<|endoftext|>" + text
    response = openai.Completion.create(
        model=model,
        prompt=(" ".join(doc.split()[:1000])).strip(),
        max_tokens=0,
        echo=True,
        logprobs=1,
    )

    subwords = response["choices"][0]["logprobs"]["tokens"][1:]
    subprobs = response["choices"][0]["logprobs"]["token_logprobs"][1:]

    gpt2_map = {"\n": "Ċ", "\t": "ĉ", " ": "Ġ"}

    for i in range(len(subwords)):
        for k, v in gpt2_map.items():
            subwords[i] = subwords[i].replace(k, v)

    to_write = ""
    for _, (w, p) in enumerate(zip(subwords, subprobs)):
        to_write += f"{w} {-p}\n"

    with open(file, "w") as f:
        f.write(to_write)
