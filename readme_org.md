![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/banner.png?raw=true)

# GitHub Lightning Bounties ⚡️

Welcome to the **GitHub Lightning Bounties.** Lightning Bounty is a groundbreaking project that revolutionizes code collaboration and incentivizes software developers using the power of Bitcoin. By integrating with GitHub Actions, Lightning Bounties automatically pays code contributors in Bitcoin for their valuable contributions to open-source projects.

![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/projectLogo3.png?raw=true)

## Hackathon Details 🚀

**Name**: MIT Bitcoin Hackathon: Scaling Up  
**Dates**: April 19th-21st, 2024  
**Venue**: MIT / Online

## About the Project 📝

We aim to integrate LLMs for analyzing incoming pull requests (PRs) on GitHub. This will cater to various aspects such as security analysis, code quality, and completeness checks. We recognize that LLM API calls have a cost associated, which can escalate with spam PRs. Our solution is a system that employs the Bitcoin Lightning Network to require a small payment for each PR review, thereby filtering spam and covering API costs.

We also believe in rewarding contributors. Hence, payments can be refunded if PRs are accepted, with potential bonuses for merged contributions.

## Architecture Overview 🏗️

![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/gh-bounty-1.png?raw=true)

## Stack and Tools 🛠️

- **GitHub Actions**: Utilize Python and Node.js scripts.
- **LNBits / LND**: Basic Lightning node setup.
- **Lime-Green**: A Python package for LLM evaluations.
- **Bring Your Own Setup**: Open to additional tools and libraries.

## Participating in the Hackathon 🤓

- **Will Sutton**: [git](https://github.com/sutt/gha-tut)
- **Mike Abramo**: [git](https://github.com/SonnyMonroe)
- **Pavel Kononov**: [git](https://github.com/super-jaba)
- **Enrique Gamboa**: [git](https://github.com/jegamboafuentes)
- **Alex Gill**: [git](https://github.com/devopsgill)

## Key Features

- **Automatic Payments**: Contributors receive Bitcoin payments automatically upon merging their pull requests.
- **Enhanced Collaboration**: Encourages collaboration and fosters a sense of community among developers.
- **Secure Transactions**: Built-in security measures ensure safe and secure Bitcoin transactions.
- **Anti-Spam Mechanism**: Contributors are required to submit a small fee to a Lightning Network wallet, preventing spam and ensuring genuine contributions.

## What's next for Lightning Bounties?

**Customizable Bounty Payouts**:
Looking ahead, we aim to give project owners and managers greater control over the bounty payouts on the Lightning Bounty platform. This will allow them to customize the reward amounts based on factors like code quality, complexity, and overall impact of the contributions.

**Broader Language Support**:
While we initially built Lightning Bounty with English and Spanish, we're eager to make our platform as globally accessible as possible. Open source development is a collaborative effort that knows no borders. Contributors from all corners of the world should feel empowered to participate regardless of their native tongue. By increasing language availability, we hope to lower barriers to entry and cultivate an even more diverse pool of talent.

**Rewarding Code Contributions with NFTs**:
Recognizing the potential of non-fungible tokens (NFTs) to serve as digital badges of honor, we aim to integrate an NFT rewards system into the Lightning Bounty platform. This will allow open-source developers who contribute high-quality code to receive free, unique NFTs that they can showcase as proof of their valuable work. By tying these NFTs to specific code contributions, we can create a new level of recognition and ownership for developers within the open-source ecosystem.

**Expanding Cryptocurrency Payment Options**
To further empower open-source developers and increase the accessibility of the Lightning Bounty platform, we plan to integrate support for a wider range of cryptocurrency payment options beyond just Bitcoin. This will include integrating Ethereum, Polygon, & Solana.


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

 ![alt text](https://github.com/MIT-Bitcoin-2024/lightning-bounty/blob/main/assets/img/team_picture.jpg?raw=true)


