import pandas as pd
import numpy as np
import sys

num_to_role={0:'Top',1:'Jungle',2:'Mid',3:'ADC',4:'Support'} #index to role converter

def champToInfo(champions_df,version=1):
    '''Creates a dictionary that maps each champion to its properties

    The function will take in a pandas dataframe containing champion names and their properties (ID, Win Rate)
    and put them into a dictionary data structure. The keys will be the champion names, and the values will
    be the champion properties. Changing version from 1 to 2 will include ID to the champion properties.

    Args:
    champions_df: pandas dataframe object containing champions and its properties
    version: integer indicating which version of the dictionary to return

    Returns:
    champ_to_info: dictionary mapping champion name to win rates (and champion id if version=2)
    '''
    champions=champions_df['Champion'].values.tolist()

    win_rates=champions_df['Win Rate'].values.tolist()
    for wr in range(len(win_rates)):
        win_rate=win_rates[wr].split()
        for r in range(len(win_rate)):
            if win_rate[r]!='X':
                win_rate[r]=float(win_rate[r])
        win_rates[wr]=win_rate

    if version==2: #include champion ID to the dictionary keys

        champ_ids=champions_df['ID'].values.tolist()
        for ci in range(len(champ_ids)):
            id=int(champ_ids[ci])
            binary_id=bin(id)[2:]
            while len(binary_id)!=8:
                binary_id='0'+binary_id
            binary_id=list(binary_id)
            for bi in range(len(binary_id)):
                binary_id[bi]=int(binary_id[bi])
            champ_ids[ci]=binary_id

        champ_to_info={}
        for c in range(len(champions)):
            champ_to_info[champions[c]]=(win_rates[c],champ_ids[c])

        return champ_to_info
    
    champ_to_info={} #does not include champion id
    for c in range(len(champions)):
        champ_to_info[champions[c]]=win_rates[c]

    return champ_to_info

def joinNames(game):
    '''Updates the elements of game to join champion names

    The function will take in a list of strings containing champion names, player win rates, and outcome, 
    then updates it so that champions with 2+ more words in their names will be conjoined

    Ex. ['Miss','Fortune']->['Miss Fortune']

    Args:
    game: a list of strings with elements alternating from champion name and player win rate and outcome
          as the last element

    Returns: None
    '''
    done=False #flag variable

    while not done:
        for index in range(len(game)-1): #find first instance of names needed to be joined
            if game[index][0] not in ['0','1'] and game[index+1][0] not in ['0','1']:
                game[index]+=' '+game[index+1]
                game.pop(index+1)
                break
        check=0
        for index in range(len(game)-1): #check to see if still needs more
            if game[index][0] not in ['0','1'] and game[index+1][0] not in ['0','1']:
                check+=1
                break
        if check==0: #no more names needed to be joined
            done=True

def getData(data_df,inputs,outputs,champ_to_info,version=1):
    '''Prepares the inputs and the outputs of the data for the neural network

    The function will take in a a pandas dataframe of the game data, predefined empty input and output
    numpy arrays and the champion to information dictionary converter, and will then fill in the
    corresponding values for the inputs and outputs to the neural network. Changing the version from
    1 to 2 will also include the champion ID as an input to the neural network.

    Example NN input (version 1): [0.5114, 0.52, 0.5275, 0.619, 0.5074, 0.727, 0.4999, 0.517, 0.5187, 
                                   0.659, 0.5034, 0.0, 0.5005, 0.5, 0.4448, 0.257, 0.5065, 0.286, 0.5199, 0.544]

    Example NN input (version 2): [0.     1.     1.     0.     0.     0.     1.     0.     0.4845 0.47
                                   1.     0.     0.     1.     1.     0.     0.     1.     0.4828 0.25
                                   0.     0.     1.     1.     1.     1.     1.     1.     0.4662 0.56
                                   0.     1.     0.     0.     0.     1.     0.     0.     0.5057 0.43
                                   0.     1.     0.     0.     0.     0.     0.     1.     0.4802 0.4
                                   0.     0.     0.     0.     0.     0.     0.     0.     0.4641 0.53
                                   0.     0.     0.     1.     1.     1.     0.     1.     0.5429 0.53
                                   0.     0.     0.     0.     0.     0.     0.     1.     0.5235 0.77
                                   0.     1.     1.     0.     0.     1.     1.     1.     0.5148 0.57
                                   0.     1.     0.     1.     0.     0.     0.     0.     0.5208 0.6   ]

    Args:
    data_df: pandas dataframe object containing game data
    inputs: 2D empty numpy array
    outputs: 1D empty numpy array
    champ_to_info: dictionary mapping champion name to win rates (and champion id if version=2)
    version: integer indicating which version of inputs to initialize

    Returns:
    inputs: 2D numpy array of input values for the neural network
    outputs: 1D numpy array of output values for the neural network
    '''
    games=data_df['Game'].values.tolist()

    for g in range(len(games)): 
        game=games[g].split() #game is a list of strings

        joinNames(game) #make it so champions with 2+ words in their names become one element in the list

        input=[]
        champ_index=0 #used to indicate champion role (0: top, 1:jg, 2:mid, 3:adc, 4:sup)

        if version==2: #includes champion ID as a binary into the input

            for e in range(len(game)-1): #get all elements of game except for last which is the result
                if e%2==0: #if game[e] is a champion
                    if champ_to_info[game[e]][0][champ_index]=='X': #exception
                        sys.exit('Error: No win rate found for %s for role %s!' % (game[e],num_to_role[champ_index]))
                    for val in champ_to_info[game[e]][1]: #append champion id using dictionary
                        input.append(val)
                    input.append(champ_to_info[game[e]][0][champ_index]) #append champion win rate using dictionary
                    champ_index+=1
                    if champ_index>4:
                        champ_index=0 #reset back to 0 for the second team
                else: #if game[e] is player win rate
                    input.append(float(game[e]))

            inputs[g]=np.asarray(input)
            outputs[g]=float(game[-1]) #last element of of game is the result

        else:

            for e in range(len(game)-1): #get all elements of game except for last which is the result
                if e%2==0: #if game[e] is a champion
                    if champ_to_info[game[e]][champ_index]=='X': #exception
                        sys.exit('Error: No win rate found for %s for role %s!' % (game[e],num_to_role[champ_index]))
                    input.append(champ_to_info[game[e]][champ_index]) #append champion win rate using dictionary
                    champ_index+=1
                    if champ_index>4:
                        champ_index=0 #reset back to 0 for the second team
                else: #if game[e] is player win rate
                    input.append(float(game[e]))

            inputs[g]=np.asarray(input)
            outputs[g]=float(game[-1]) #last element of of game is the result
    
    return inputs,outputs