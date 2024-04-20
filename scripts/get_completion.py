import requests
import json
import os


# print("in the script")
# print(pr_diff)

pr_diff = os.environ['PR_DIFF']
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

full_prompt = ""
full_prompt += "In the following diff, please provide a brief summary of the changes made in the PR. \n\n"
full_prompt += f"```diff\n{pr_diff}\n```"

url = "https://api.openai.com/v1/chat/completions"
headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {OPENAI_API_KEY}"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": full_prompt}],
    "max_tokens": 200
}

response = requests.post(url, json=data, headers=headers)
print(response)
print(response.status_code)
try: 
    # print(response.json())
    output_data = response.json()["choices"][0]["message"]["content"]
except Exception as e: 
    print(e)
    output_data = "Error: Unable to get completion from OpenAI API"

print(output_data)

output_data = output_data.replace("\n", "\\n")
print(f"::set-output name=completion_output::{output_data}")

# print("::set-output name=completion_output::<<EOF")
# print(f"::set-output name=completion_output::{output_data}")
# print("::set-output name=completion_output::<<EOF")
# print(output_data)
# print("EOF")
