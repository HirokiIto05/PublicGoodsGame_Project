Understood — here is a **clear, structured, and concise README** with a logical hierarchy and minimal redundancy.

---

# Public Goods Game (oTree Implementation)

## 1. Project Summary

This project implements a **Public Goods Game (PGG)** in oTree with:

* Symmetric and asymmetric endowments
* Peer punishment
* Democratic punishment
* Extended inequality treatments

The experiment studies how punishment mechanisms affect cooperation under resource inequality.

---

# 2. Experimental Structure

## 2.1 Group Setup

* 4 players per group
* Fixed groups across rounds
* Player IDs reshuffled for display each round

```
PLAYERS_PER_GROUP = 4
NUM_ROUNDS = 3
```

---

## 2.2 Endowment Treatments

Endowments are fixed per participant across rounds.

```python
ENDOWMENT_PROFILES = {
    'sym_30': [30, 30, 30, 30],
    'asym_40_40_20_20': [40, 40, 20, 20],
    'asym_80_40_20_20': [80, 40, 20, 20],
}
```

Each participant receives:

* A fixed endowment
* A status label stored in `participant.vars`

---

## 2.3 Public Goods Mechanism

### Stage 1 — Contribution

Each player chooses:

```
0 ≤ contribution ≤ endowment
```

### Stage 2 — Redistribution

Total contributions are multiplied and equally redistributed:

[
individual_return = \frac{total_contribution \times 1.6}{4}
]

```
MULTIPLIER = 1.6
```

### Stage 3 — Payoff Before Punishment

```
payoff_before_punishment
= endowment - contribution + individual_return
```

---

# 3. Punishment Systems

Configured via:

```python
PUNISHMENT_SYSTEMS = [0, 1, 2]
```

---

## 3.1 No Punishment (0)

Final payoff:

```
payoff = payoff_before_punishment
```

---

## 3.2 Peer Punishment (1)

Each player:

* Can assign punishment to others
* Has a total budget of 9 MUs

```
MAX_PUNISHMENT_BUDGET = 9
PUNISHMENT_COST_PER_MU = 1
PUNISHMENT_FINE_PER_MU = 2
```

For each punishment point:

* Punisher pays 1 MU
* Target loses 2 MUs

Final payoff:

```
payoff = payoff_before_punishment
         - punishment_received*2
         - punishment_cost
```

---

## 3.3 Democratic Punishment (2)

Two-stage punishment system:

### Stage A — Proposal

Players propose punishment points (same structure as peer punishment).

### Stage B — Voting

For each target:

* Other 3 players vote
* If ≥ 2 vote YES → punishment executed
* If < 2 vote YES → no punishment

If executed:

* Target loses 2 × proposed points
* Proposers pay 1 × proposed points

If rejected:

* No cost
* No fine

---

# 4. Data Collected

## Behavioral Variables

* Contribution
* Relative contribution
* Punishment assigned
* Punishment received
* Payoff
* Status

## Demographics

* Age
* Gender
* Nationality (via `pycountry`)

---

# 5. Running the Project with Docker

## 5.1 Requirements

* Docker installed
* Project directory containing a Dockerfile

Check installation:

```bash
docker --version
```

---

## 5.2 Build Image

From the project root:

```bash
docker build -t pgg-otree .
```

---

## 5.3 Run Server

```bash
docker run -p 8000:8000 pgg-otree
```

Access in browser:

```
http://localhost:8000
```

---

## 5.4 Development Mode

To run oTree devserver:

```bash
docker run -it -p 8000:8000 pgg-otree otree devserver
```

---

## 5.5 Stop Container

```bash
docker ps
docker stop <container_id>
```

Or press:

```
CTRL + C
```

---

# 6. Session Configuration Example

In `settings.py`:

```python
SESSION_CONFIGS = [
    dict(
        name='pgg_demo',
        app_sequence=['pgg_diff_punishment'],
        num_demo_participants=4,
        punishment_system=1,
        endowment_profile='asym_40_40_20_20',
    ),
]
```

---

# 7. Project Structure

```
pgg_diff_punishment/
│
├── models.py
├── pages.py
├── templates/
│   └── pgg_diff_punishment/
│
├── settings.py
├── Dockerfile
```

---

# 8. Customization

You can modify:

* Endowment structures
* Punishment parameters
* Number of rounds
* Treatment conditions via session configs

---