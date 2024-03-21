# BASALT Algorithm Simulation

## Overview

This project simulates the BASALT algorithm, a decentralized network optimization strategy focused on dynamic peer selection and network sampling. BASALT stands for Balanced Selection and Adaptive Learning Technique, aiming to enhance network performance by periodically adjusting node connections based on a ranking function.

## Features

- **Dynamic View Management:** Each node maintains a view of a subset of the network, optimizing its connections based on network conditions.
- **Adaptive Sampling:** Nodes periodically update their views with new samples, selecting peers that offer the best match according to a hash-based ranking function.
- **Malicious Node Detection:** Implements a basic heuristic to identify nodes that may behave maliciously, based on the variance in their interaction hits.

## Implementation Details

- **Node Initialization:** Each `BasaltNode` is initialized with a unique ID, the total number of nodes in the system, and a specified view size. The node's initial view is a random sample of peers.
- **Ranking Function:** Utilizes a simple hash-based function to rank nodes, facilitating the selection of optimal peers for communication and view updates.
- **Peer Selection:** Nodes select peers for pull/push updates based on the lowest interaction hits, aiming to balance the load and ensure fairness.
- **Seed Refreshing:** To maintain adaptivity and resilience to network changes, nodes periodically refresh their seeds used for peer ranking.

## Usage

The simulation is designed as a script that can be executed directly. It initializes a set of nodes with predefined parameters and simulates the exchange process over a specified number of intervals.

1. **Initialize Nodes:** Create a list of `BasaltNode` objects, each representing a node in the network.
2. **Simulate Exchanges:** Iterate over a set number of time intervals, during which nodes select peers for pull/push updates and adjust their views accordingly.
3. **Identify Malicious Nodes:** After the simulation, apply a heuristic to flag nodes with abnormal interaction patterns as potentially malicious.

## Example Output

The script prints initial node states, their evolution after applying the BASALT algorithm, and finally, lists nodes identified as potentially malicious.

## Requirements

- Python 3.x
- Modules: `random`, `hashlib`

## Running the Simulation

Execute the script using Python:

```bash
python basalt_simulation.py
