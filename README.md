Below is a draft **README.md** for your project based on the uploaded files (`models.py`, `pages.py`, `settings.py`, `Dockerfile`, `docker-compose.yml`).

---

# Public goods game with asymmetric endowments and punishment systems

## Summary

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

## Experimental design

### public goods game

* Group size: 4 players
* Each player receives an endowment (treatment dependent)
* Players decide how much to contribute to a public good
* Contributions are multiplied (MPCR mechanism)
* Earnings depend on own contribution and total group contribution

### Endowment Profiles

Defined in `models.py`:

* Symmetric: (30, 30, 30, 30)
* Asymmetric (moderate inequality): (40, 40, 20, 20)
* Asymmetric (high inequality): (80, 40, 20, 20)

### Punishment Stage

Depending on treatment:

* Peer punishment
* Potential central punishment
* Configurable punishment budget and cost structure

---

## Project folder structure

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

````markdown
## Getting Started

Follow the steps below to run the project locally using Docker.

### 1. Start the Docker Container

From the project root directory, run:

```bash
docker compose up -d
````

This command:

* Builds the Docker image (if not already built)
* Starts the container in detached mode
* Exposes port `8000` to your local machine

---

### 2. Enter the Container

Open a shell inside the running container:

```bash
docker compose exec python bash
```

You are now inside the container environment (`/workspace`).

---

### 3. Start the oTree Server

Inside the container, run:

```bash
otree devserver
```

The development server will start and listen on port `8000`.

---

### 4. Access the Application

Open your browser and go to:

```
http://localhost:8000
```


