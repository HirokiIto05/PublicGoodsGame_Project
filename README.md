# Summary

This project implements a **Public Goods Game (PGG)** using **oTree**, designed to study how different punishment institutions affect cooperation under symmetric and asymmetric endowment distributions.

The experimental design is inspired by:

* Nockur
* Pfattheicher
* Keller

(2021, Journal of Experimental Social Psychology)

The game allows:

* Symmetric and asymmetric endowment profiles
* Multiple punishment systems (e.g., peer punishment, central punishment)
* Flexible treatment extensions
* Multi-round interaction
* Deployment via Docker

The application is containerized using Docker and can be run locally via `docker-compose`.

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
│   │       ├── Demographics.html
│   │       ├── Introduction.html
│   │       ├── MyPage.html
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

Move to the project root directory:

cd PGG_Project

Then run:

docker compose up -d
docker compose exec python bash
otree devserver 0.0.0.0:8000

Finally, open your browser and go to:

http://localhost:8000