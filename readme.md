 ![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/banner.png?raw=true)

GitHub Lightning Bounties ⚡️
============================

Welcome to the **GitHub Lightning Bounties** project, innovatively combining GitHub Actions, Lightning Network payments, and Large Language Models (LLMs) to elevate the open-source collaboration experience.

 ![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/projectLogo3.png?raw=true)

Hackathon Details 🚀
--------------------

**Name**: MIT Bitcoin Hackathon: Scaling Up  
**Dates**: April 19th-21st, 2024  
**Venue**: MIT / Online  

About the Project 📝
--------------------

**Target Project**: GitHub Lightning Bounties

We aim to integrate LLMs for analyzing incoming pull requests (PRs) on GitHub. This will cater to various aspects such as security analysis, code quality, and completeness checks. We recognize that LLM API calls have a cost associated, which can escalate with spam PRs. Our solution is a system that employs the Bitcoin Lightning Network to require a small payment for each PR review, thereby filtering spam and covering API costs.

We also believe in rewarding contributors. Hence, payments can be refunded if PRs are accepted, with potential bonuses for merged contributions.

Architecture Overview 🏗️
-------------------------

 ![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/gh-bounty-1.png?raw=true)

Stack and Tools 🛠️
-------------------

*   **GitHub Actions**: Utilize Python and Node.js scripts.
*   **LNBits / LND**: Basic Lightning node setup.
*   **Lime-Green**: A Python package for LLM evaluations.
*   **Bring Your Own Setup**: Open to additional tools and libraries.

Participating in the Hackathon 🤓
---------------------------------

*   **Will Sutton**: [git](https://github.com/sutt/gha-tut)
*   **Mike Abramo**: [git](https://github.com/SonnyMonroe)
*   **Pavel Kononov**: [git](https://github.com/super-jaba)
*   **Enrique Gamboa**: [git](https://github.com/jegamboafuentes)
*   **Alex Gill**: [git](https://github.com/devopsgill)

 ![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/team_picture.jpg?raw=true)

How to test 💻
-----------------

- Fork the repository and clone it to your local machine. 
- Modify `src/main.py` to reflect some changes
- Generate a lightning invoice and copy that string into `reward.txt`
- Add and commit your changes, submit a pull request to the base repository.
- This will kick off the GitHub action to request that 1 sat "dust" payment from you ("the contribtuor") to pay to the base repo ("the owner").
    - As noted in video, we have two superfluous automations running here, chose the second one, the one that says "Please pay the invoice: lnbc10n1..." (not the one that says "Extracted values:...").
- You'll see one of the github actions remains running (which is polling for payment confirmation) and should return with the message "Thank you for your payment!"
- Now, request a reviewer to review your PR. (Either Enrique or Will will work for this test). After a few seconds you'll see a new action running:
    - first it will say: "Payment has been recieved, sit tight, running openai query"
    - then ~30 secs later it will return with a summary of your changes + a security vulnerability analysis.
- Finally, we'll want to merge your PR and recieve your reward. Since your not a repository maintainer, you don't have this power. But we'll keep an eye out and try to merge it for you.
    - note: currently there's no check for the amt of the reward, and we're not a rich node so anything larger than 100 sats will exceed our balance. So keep it small for now.

**Alternatively:** You can copy the contents of `.github/` directory into your own repository and modify the `main.py` file and reporduce our work. Note you'll need to setup the appropriate secrets in your repository settings:
 - OPENAI_API_KEY
 - PAY_INVOICE_KEY  (admin key for LNBits)
 - WALLET_API_KEY  (invoice/read key for LNBits)
 - WALLET_BASE_URL  (url for your LNBits instance)

