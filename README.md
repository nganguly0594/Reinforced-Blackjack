# Reinforced Blackjack

<img src="raw/AI_Blackjack.jpeg" alt="AI-generated blackjack card with armor" width="600" style="text-align: center;"> <br>
*Created using DeepAI Image Generator with the prompt: "A playing card with armor and a spear."*

This project is a comprehensive Blackjack game simulation and data analysis project built with Python. It includes the training of a reinforcement learning agent to find optimal Blackjack strategies, alongside basic and advanced strategy simulations.

## Project Statement
Blackjack is undoubtedly one of the most popular casino games in the world, among the likes of Poker and Roulette. Blackjack's popularity is based on multiple features, the first being its simplicity. The goal of the game is to beat the dealer with a series of "hitting" and "standing" actions in an effort to gain a better card total, while not exceeding a total of 21 (called a "bust"). However, arguably the more favorable reason to participate in Blackjack is the existence of strategies that allow players to reduce the casino's winning edge to a mere 0.5%.

The goal of this project is to create a robust environment to explore and learn different strategies in the game of Blackjack, ranging from basic and randomized playing, to strategies used by professional players. However, as a CS student, the larger purpose of this repository is geared towards answering this one question: can we teach a computer to play a perfect game of Blackjack from scratch?

In order to solve this question, I go through the steps of creating a blackjack simulation, exploring different strategies, and then eventually I use the ideas of Reinforcement Learning to help my computer beat the game of Blackjack.

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/nganguly0594/Reinforced-Blackjack.git
cd Reinforced-Blackjack
conda env create -f environment.yml
conda activate blackjack
```

## Usage
To explore strategy simulations and RL training, open the Jupyter notebooks in the notebooks/ directory. Make sure to activate the conda environment first:

```bash
conda activate blackjack
```

To begin a Blackjack game simulation and play against the computer, from the top directory run:

```bash
python src/main.py
```

## Project Structure
**exp/**: Area for experimental implementations and strategies.

**notebooks/**: Contains four notebooks with explanations, results, and complete data analysis from simulations.
- [Notebook 1](notebooks/1%20-%20Blackjack%20Logic.ipynb) contains a breakdown of the logic behind the blackjack game simulation.
- [Notebook 2](notebooks/2%20-%20Strategy%20Comparison.ipynb) simulates and compares the expected winnings from three different strategies.
- [Notebook 3](notebooks/3%20-%20Environment%20Setup.ipynb) goes over the process of setting up a Gymnasium environment to train and test RL algorithms.
- [Notebook 4](notebooks/4%20-%20Q-Learning%20Algorithm.ipynb) implements a reinforcement learning algorithm (Q-Learning) to iteratively find an optimal blackjack strategy.

**raw/**: Image files to display in README.md and notebooks.

**src/**: Contains the base logic for the Blackjack game, the main script to run the game simulation, and the Gymnasium environment used to train the RL algorithm.

## License
This project is licensed under the MIT License.