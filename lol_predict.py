from lol_scrape_tools import *
import tensorflow as tf
from tensorflow import keras

#import resources
lol_model=keras.models.load_model('lol_model')
champions_df=pd.read_csv('Data/Champion_Info (Masters+).csv')
champ_to_info=champToInfo(champions_df)

#prepare nn input
inputs=np.zeros([1,20])
inp=[]

#TEAM 1 DATA
champ1=input('Enter Top Lane Champion for Team 1: ')
if champ_to_info[champ1][0]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ1,num_to_role[0]))
inp.append(champ_to_info[champ1][0])
player1=float(input('Enter Team 1 Player 1 Win Rate on %s: ' % (champ1)))
inp.append(player1)

champ2=input('Enter Jungle Lane Champion for Team 1: ')
if champ_to_info[champ2][1]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ2,num_to_role[1]))
inp.append(champ_to_info[champ2][1])
player2=float(input('Enter Team 1 Player 2 Win Rate on %s: ' % (champ2)))
inp.append(player2)

champ3=input('Enter Mid Lane Champion for Team 1: ')
if champ_to_info[champ3][2]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ3,num_to_role[2]))
inp.append(champ_to_info[champ3][2])
player3=float(input('Enter Team 1 Player 3 Win Rate on %s: ' % (champ3)))
inp.append(player3)

champ4=input('Enter ADC Lane Champion for Team 1: ')
if champ_to_info[champ4][3]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ4,num_to_role[3]))
inp.append(champ_to_info[champ4][3])
player4=float(input('Enter Team 1 Player 4 Win Rate on %s: ' % (champ4)))
inp.append(player4)

champ5=input('Enter Support Lane Champion for Team 1: ')
if champ_to_info[champ5][4]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ5,num_to_role[4]))
inp.append(champ_to_info[champ5][4])
player5=float(input('Enter Team 1 Player 5 Win Rate on %s: ' % (champ5)))
inp.append(player5)

#TEAM 2 DATA
champ1=input('Enter Top Lane Champion for Team 2: ')
if champ_to_info[champ1][0]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ1,num_to_role[0]))
inp.append(champ_to_info[champ1][0])
player1=float(input('Enter Team 1 Player 1 Win Rate on %s: ' % (champ1)))
inp.append(player1)

champ2=input('Enter Jungle Lane Champion for Team 2: ')
if champ_to_info[champ2][1]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ2,num_to_role[1]))
inp.append(champ_to_info[champ2][1])
player2=float(input('Enter Team 1 Player 2 Win Rate on %s: ' % (champ2)))
inp.append(player2)

champ3=input('Enter Mid Lane Champion for Team 2: ')
if champ_to_info[champ3][2]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ3,num_to_role[2]))
inp.append(champ_to_info[champ3][2])
player3=float(input('Enter Team 1 Player 3 Win Rate on %s: ' % (champ3)))
inp.append(player3)

champ4=input('Enter ADC Lane Champion for Team 2: ')
if champ_to_info[champ4][3]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ4,num_to_role[3]))
inp.append(champ_to_info[champ4][3])
player4=float(input('Enter Team 1 Player 4 Win Rate on %s: ' % (champ4)))
inp.append(player4)

champ5=input('Enter Support Lane Champion for Team 2: ')
if champ_to_info[champ5][4]=='X': #exception
    sys.exit('Error: No win rate found for %s for role %s!' % (champ5,num_to_role[4]))
inp.append(champ_to_info[champ5][4])
player5=float(input('Enter Team 1 Player 5 Win Rate on %s: ' % (champ5)))
inp.append(player5)

print()

#make prediction
inputs[0]=np.asarray(inp)
prediction=lol_model.predict(inputs[:1])[0]
print('There is a %.2f percent chance that Team 1 will win (%.2f percent chance that Team 2 will win)!' % (prediction[0]*100,prediction[1]*100))
