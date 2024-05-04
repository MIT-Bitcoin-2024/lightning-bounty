import os
import dotenv
import requests


def fetch_reward():
    with open("./reward.txt", "r") as file:
            return file.read()
    
def pay_reward(
        base_url: str,
        api_key: str,
        payment_invoice: str
) -> bool:
    headers = {
        "X-Api-Key": api_key
    }

    body = {
        "out": True,
        "bolt11": payment_invoice
    }

    url = f"https://{base_url}/api/v1/payments"

    response = requests.post(url, headers=headers, json=body)

    return response.status_code == 201


class GithubException(Exception):
    pass


class GithubService:
    def __init__(self, gh_token) -> None:
        self.gh_token = gh_token

    def comment_on_pr(self, repo: str, pr_number: int, message: str):
        
        headers = {
            'Authorization': f'token {self.gh_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        api_url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'

        response = requests.post(api_url, headers=headers, json={'body': message})

        if response.status_code != 201:
            raise GithubException(f"Couldn't comment the message. Response status is {response.status_code}",
                                  api_url,
                                  response.json())
        
        print("successful comment on", api_url)


def main():
    dotenv.load_dotenv()

    # BASE_URL: str = os.getenv("WALLET_BASE_URL")
    BASE_URL = "d5aedbf627.d.voltageapp.io"
    API_KEY: str = os.getenv("WALLET_API_KEY")

    GH_TOKEN = os.getenv("GITHUB_TOKEN")
    GH_REPO = os.getenv("GITHUB_REPOSITORY")
    PR_NUMBER: int = int(os.getenv("PR_NUMBER"))

    payment_invoice = fetch_reward()
    completion = pay_reward(
        BASE_URL,
        API_KEY,
        payment_invoice
    )

    gh_service = GithubService(GH_TOKEN)
    if completion:
        gh_service.comment_on_pr(GH_REPO, PR_NUMBER, "Thank you for contribution! :)")
    else:
        gh_service.comment_on_pr(GH_REPO, PR_NUMBER, "Couldn't sent you your reward. Please contact our support.")



if __name__ == "__main__":
    main()