# lol-neural-net
This repository contains the tools to build and save a neural network that can predict win/loss outcomes for the popular game Legue of Legends with roughly 80% accuracy, as well as a script that allows users to give inputs and make their own predictions.

## Data
The data folder contains two files: Champion_Info (Masters+).csv and Games.csv. The first file contains the most recent information on every champion in the game, their made up ID, and their win rates on each possible role (Top, Jungle, Mid, ADC, Support). An X means we have not seen a certain champion play in that role recently. This file should be modified as the game meta changes. The second file contains the training and testing data for the neural network. Each entry in the file cotains information on the 10 players in the game, including the champion the player is using and the player's win rate on that champion. These entries will be modified and reconstructed before being sent to the network for training and testing.

## lol_model
This folder contains the saved neural network model and weights after training. The saved model in this folder has an 85% accuracy.

## lol_network.ipynb
This file details the process I used to build and train the neural network. In here, you can modify which data will be used for training and testing as well as model hyperparameters. The current configuration was shown to have the best accuracy. Note that the current configuration also uses version 1, which does not include Champion IDs as inputs to the neural network. To change this, uncomment the corresponding lines in the Get the data section, and change input_shape from 20 to 100 in the Construct the model section. 

## lol_predict.py
This file loads in the neural network from lol_model and allows users to make their own predictions. Simply run this script and respond to the input prompts. Make sure spelling is correct.

## lol_scrape_tools.py
This file contains helper functions to assist with the data scraping from Data.
