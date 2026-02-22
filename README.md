# Project Overview

This project extends the public goods experiment of Laila Nockur, Stefan Pfattheicher, and Johannes Keller (2021) by introducing:

* **Stronger endowment inequality**
* **Incomplete information about endowments**

The goal is to test whether extreme inequality and imperfect information change cooperation and punishment dynamics in public goods games .

---

# Design Summary

* 4 players per group (fixed groups)
* 12 rounds total

  * Rounds 1–6: Peer punishment
  * Rounds 7–12: Democratic punishment

Each round:

1. Contribution decision
2. Public good multiplication (×1.6) and redistribution
3. Punishment stage

## Endowment Profiles

* Symmetric: (30, 30, 30, 30)
* Asymmetric (small): (40, 40, 20, 20)
* Asymmetric (large): (60, 30, 20, 10)

The first two replicate the original study; the third introduces stronger inequality .

## Information Conditions

* **Complete information**: contributions + endowments visible
* **Incomplete information**: only contributions visible

---

# Main Hypotheses

* **H1**: Under incomplete information, punishment is based on absolute contributions, disadvantaging low-endowment players.
* **H2**: Low-endowment players may increase contributions over time to avoid punishment.
* **H3**: Greater inequality amplifies contribution gaps and payoff dispersion .



---

# Project folder structure

```
PublicGoodsGame_Project/
├── .devcontainer/
│   └── devcontainer.json
├── pgg_asymmetric_punishment/
│   ├── templates/
│   │   └── pgg_asymmetric_punishment/
│   │       ├── Contribute.html
│   │       ├── DemocraticVote.html
│   │       ├── Demographics.html
│   │       ├── End.html
│   │       ├── Introduction.html
│   │       ├── Instruction_democratic.html
│   │       ├── Instruction_peer.html
│   │       ├── Punish.html
│   │       └── Results.html
│   ├── __init__.py
│   ├── models.py
│   └── pages.py
│
├── docker-compose.yml
├── Dockerfile
├── README.html
├── README.md
├── requirements.txt
└── settings.py
```

---


# Getting Started

Clone the repository and move into the project folder:

git clone https://github.com/HirokiIto05/PublicGoodsGame_Project.git
cd PublicGoodsGame_Project

Start the Docker container:

docker compose up -d

Enter the container:

docker compose exec python bash

Run the oTree development server:

otree devserver 0.0.0.0:8000

Then open your browser and go to:

http://localhost:8000