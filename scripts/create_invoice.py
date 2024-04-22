import os
import time

import dotenv
import requests


class Invoice:
    def __init__(self, hash: str, request: str) -> None:
        self.payment_hash = hash
        self.payment_request = request


class CreateInvoiceException(Exception):
    pass


class PaymentService:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def create_invoice(
            self,
            amount: int,
            memo: str = ""
    ) -> str:
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

        data = {
            "out": False,
            "amount": amount,
            "memo": memo,
            "unit": "sat"
        }

        url = f"https://{self.base_url}/api/v1/payments"

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise CreateInvoiceException("Couldn't create invoice")

        response_json = response.json()
        return Invoice(response_json["payment_hash"], response_json["payment_request"])

    def check_payment(
            self,
            payment_hash: str,
            attempts: int = 10,
            delay_seconds: int = 30
    ) -> bool:
        url = f"https://{self.base_url}/api/v1/payments/{payment_hash}"
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

        for i in range(attempts):
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and response.json()["paid"]:
                return True
            if i < attempts - 1:
                time.sleep(delay_seconds)

        return False
    

class GithubException(Exception):
    pass
    

class GithubService:
    def __init__(self, gh_token) -> None:
        self.gh_token = gh_token

    def comment_on_pr(self, repo: str, pr_number: int, message: str):
        # Set up the headers with the GitHub token
        headers = {
            'Authorization': f'token {self.gh_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        api_url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'

        response = requests.post(api_url, headers=headers, json={'body': message})

        # Check the response status
        if response.status_code != 201:
            raise GithubException(f"Couldn't comment the message. Response status is {response.status_code}",
                                  api_url,
                                  response.json())
        
        print("successful comment on", api_url)


def main():
    dotenv.load_dotenv()

    BASE_URL: str = os.getenv("WALLET_BASE_URL")
    API_KEY: str = os.getenv("WALLET_API_KEY")
    INVOICE_AMOUNT: int = int(os.getenv("INVOICE_AMOUNT", 10))

    GH_TOKEN = os.getenv("GITHUB_TOKEN")
    GH_REPO = os.getenv("GITHUB_REPOSITORY")
    PR_NUMBER: int = int(os.getenv("PR_NUMBER"))

    CHECK_PAYMENT_ATTEMPTS: int = int(os.getenv("CHECK_PAYMENT_ATTEMPTS", 10))
    CHECK_PAYMENT_DELAY: int = int(os.getenv("CHECK_PAYMENT_DELAY", 30))

    try:
        payment_service = PaymentService(BASE_URL, API_KEY)
        invoice: Invoice = payment_service.create_invoice(INVOICE_AMOUNT)

        gh_service = GithubService(GH_TOKEN)

        gh_service.comment_on_pr(
            GH_REPO,
            PR_NUMBER,
            message=f"Please pay the invoice: {invoice.payment_request}"
        )
    except CreateInvoiceException:
        print("Couldn't create invoice")
    except GithubException as e:
        print("Couldn't post payment request")
        return

    is_paid = payment_service.check_payment(
        invoice.payment_hash,
        CHECK_PAYMENT_ATTEMPTS,
        CHECK_PAYMENT_DELAY
    )  # May run long
    if is_paid:
        gh_service.comment_on_pr(
            GH_REPO,
            PR_NUMBER,
            message=f"Thank you for your payment!"
        )
    else:
        gh_service.comment_on_pr(
            GH_REPO,
            PR_NUMBER,
            message=f"Payment failure"
        )


if __name__ == "__main__":
    main()
