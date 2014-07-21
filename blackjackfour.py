## A program to play Blackjack for a job interview with InsightDataEngineering
## By David L. Anderson
## Written in Python 3.4.1


""" Assumption: players already know how to play blackjack,
and do not require educating."""




"""This is just defining a deck of cards,
returning it as a list in numerical_suit order."""
card_values = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven',\
               'eight', 'nine', 'ten', 'jack', 'queen', 'king')
deck_suits = ('_clubs', '_diamonds', '_hearts', '_spades')
deckofcards = [ value+suit for value in card_values for suit in deck_suits]

"""build a dictionary of card values for the handvalue calculation"""
card_value_dictionary = {}
card_value_counter = 0
for card in card_values:
    card_value_counter = card_value_counter + 1
    if card_value_counter > 10:
        card_value_counter = 10
    card_value_dictionary[card[:3]] = card_value_counter

"""import a couple of packages that blackjack won't run without."""
import random 
import math

#A string which will be used in several places.
failuretocomply = """
Local laws forbid us from taking money from people
who can't understand our instructions.

I'm going to have to ask you to leave."""




# Naming conventions:
"""
shoedeck = the deck being dealt from at the table.
dealerdeck = the dealer's deck/hand
playerdeck = the player's deck/hand
useddeck = where the used cards go.
bet_value = how many chips the player is betting
bet_result = above, with appropriate modifiers
playerchips = the total of how many chips the player has
quittracker = a boolean noting whether the player wants to quit,
    or is getting ejected.
dealerhandvalue = the integer value of the dealer's hand.
playerhandvalue = the integer value of the player's hand.
numberofdecks = how many decks are in the shoe at the table the player is at.
playerstand = boolean set to true of the player stands

Suffix local versions of these variables with
    the initials of the function they appear in.
Don't bother with purely local variables or retries.
"""





def playgame(playerchipspg=100, quittrackerpg = False):
    """They core function that calls all others to play the game.

    Has an initial setup block.
    Then loops until the player looses all chips or quits."""
    
    print('Welcome to our casino. You have ' + str(playerchipspg) +\
          ' chips to play with.')
    numberofdeckspg, quittrackerpg = get_number_decks(quittrackerpg)
    shoedeckpg = bigdeckmaker(numberofdeckspg)
    random.shuffle(shoedeckpg)
    random.shuffle(shoedeckpg) # seems to be more thoroughly shuffled with two
    useddeckpg = []
    
    while (playerchipspg > 0 and quittrackerpg == False):
        
        bet_valuepg, quittrackerpg =\
                     get_number_bet(playerchipspg, quittrackerpg)
        
        if quittrackerpg: # eject the player for bad answers
            break
        
        bet_resultpg, shoedeckpg, useddeckpg, quittrackerpg =\
                    playhand(bet_valuepg, playerchipspg, shoedeckpg,\
                             useddeckpg, quittrackerpg)
        
        playerchipspg = playerchipspg + bet_resultpg
        print('You now have ' + str(playerchipspg) + ' chips.')
        if quittrackerpg == False:
            quittrackerpg = quit_query()
        
    print('You have ' + str(playerchipspg) + ' chips as you leave the casino.')





def playhand(bet_valueph, playerchipsph, shoedeckph,\
             useddeckph, quittrackerph):
    """Plays through a hand.

    Initializes internal control variables.
    Does an initial deal (the dealer gets one card, the player two).
    Loops through the player playing their hand.
    Loops through the dealer hitting until >= 17.
    Calls another function to calculate the result of the bet.
    Puts the cards in the hands into the used card pile."""
    
    playerdeckph=[]
    dealerdeckph=[]
    playerhandvalueph = 0
    dealerhandvalueph = 0
    playerstandph = False
    
    deckatthetable, playerdeckph, useddeckph =\
                    dealto(shoedeckph, playerdeckph, useddeckph)
    handstatement(playerdeckph, 'Your')
    deckatthetable, dealerdeckph, useddeckph =\
                    dealto(shoedeckph, dealerdeckph, useddeckph)
    handstatement(dealerdeckph, 'The dealer\'s')
    deckatthetable, playerdeckph, usedcards =\
                    dealto(shoedeckph, playerdeckph, useddeckph)
    handstatement(playerdeckph, 'Your')
    

    while ( (playerhandvalueph < 21) and (playerstandph != True)):  

        bet_valueph, playerstandph, playerhandph,\
                     shoedeckph, useddeckph, quittrackerph = \
                     playerdecision_dialog(bet_valueph, playerchipsph,\
                                           playerstandph, playerdeckph,\
                                           shoedeckph, useddeckph,\
                                           quittrackerph)

        if quittrackerph: # eject the player for bad answers
            break
        playerhandvalueph = handvalue(playerdeckph)
        handstatement(playerdeckph, 'Your')
    

    while ( dealerhandvalueph < 17) and (quittrackerph == False):

        shoedeckph, dealerdeckph, useddeckph =\
                        dealto(shoedeckph, dealerdeckph, useddeckph)

        dealerhandvalueph = handvalue(dealerdeckph)
        handstatement(dealerdeckph, 'The dealer\'s')


    bet_resultph = bet_result(bet_valueph, playerdeckph, dealerdeckph)
    useddeckph = useddeckph + playerdeckph + dealerdeckph
    
    return bet_resultph, shoedeckph, useddeckph, quittrackerph





def dealto(shoedeckdt, deckdealtto, useddeckdt):
    """Deals a card from the shoe to the hand specified.

    This also puts the cards from the used pile back into the shoe,
    when the used deck is > 3 * shoe deck, because that's how
    real casinos do it to reduce the effectiveness of card counting."""
    if 3*len(shoedeckdt) < len(useddeckdt):
        shoedeckdt.extend(useddeckdt)
        random.shuffle(shoedeckdt)
        del useddeckdt[:]
    deckdealtto.append(shoedeckdt.pop())
    return shoedeckdt, deckdealtto, useddeckdt




def handstatement(handtoprint, userflag='user'):
    """Prints what the hand consists of and the hand's value.

    Future development: make it return proper English,
    with Oxford commas."""
    handstring = ''
    for card in range(len(handtoprint)):
        handstring = handstring + ' ' + handtoprint[card] + ','
    handvaluestring = str(handvalue(handtoprint))
    print(userflag + ' hand is ' + handstring + ' worth '+\
          handvaluestring + '.')
        



    
def playerdecision_dialog(bet_valuepd, playerchipspd, playerstandpd,\
                          playerdeckpd, shoedeckph, useddeckpd,\
                          quittrackerpd, retries=6, decideflag = False):
    """Dialog in which the player decides their next action.

    Then it implements the decision before returning to the loop in playhand.
    Also sets conditions to eject the player from the game if they
    insist on invalid responses."""
    while (retries > 0) and (decideflag == False):
        playeraction = input('Do you want to hit, stand, or double? ')
            
        if playeraction in ('h', 'hi', 'ht', 'hit'):
            shoedeckph, playerdeckpd, useddeckpd =\
                             dealto(shoedeckph, playerdeckpd, useddeckpd)
            decideflag = True
            
        elif playeraction in ('s', 'st', 'sta', 'stan', 'stand'):
            playerstandpd = True
            decideflag = True
            
        elif playeraction in ('d', 'do', 'dou', 'doub', 'doubl', 'double' ):
            if 2*bet_valuepd > playerchipspd:
                print('I\'m sorry, you can\'t bet more chips than you have.')
                retries = retries - 1
            else:
                bet_valuepd = 2*bet_valuepd
                shoedeckph, playerdeckpd, useddeckpd =\
                                 dealto(shoedeckph, playerdeckpd,\
                                        useddeckpd)
                playerstandpd = True
                decideflag = True
                
        #will need to add 'surrender' and 'split' here, if implemented
        #elif playeraction in ('surren', 'surrender'):
                # supposed to onlybe available on first decision of hand,
                #and results in quit game -> complicated
        #    playerstandpd = True
        #    bet_valuepd = bet_valuepd - int(bet_valuepd/2)
        #    decideflag = True
        #elif playeraction in ('sp', 'spl', 'spli', 'split'):
            # supposed to only be available on first decision of hand,
            #and results in two player hands -> complicated
            #decideflag = True
            
        else:
            retries = retries - 1
            print('I am sorry, I did not understand what you said.'\
                  ' Could you repeat it, please?')
    if retries <= 0:
        quittrackerpd = True
        print(failuretocomply)
        bet_valuepd = 0
    return bet_valuepd, playerstandpd, playerdeckpd,\
           shoedeckph, useddeckpd, quittrackerpd
    




def handvalue(handlist): # to compute what a hand is worth
    """Computes what a hand is worth and returns it.

    Makes use of the fact that no more than one ace will ever
    be counted as an 11."""
    handinteger = 0
    ace_present = False
    for card_in_hand in handlist:
        if card_in_hand[:3] in list(card_value_dictionary.keys()):
            handinteger = handinteger + card_value_dictionary[card_in_hand[:3]]
        if card_in_hand[:3] == 'ace':
            ace_present = True

    #The player will never wish to count more than one ace as an 11
    if (ace_present == True) and (handinteger + 10 <= 21):
        handinteger = handinteger + 10
    return handinteger
            





def bet_result(bet_valuebr, playerdeckbr, dealerdeckbr):
    """Calculates whether the bet is gained or lost by the player.

    An initial block to set some local variables for convenience.
    Then a bunch of conditions to determine whether the player or
    dealer wins (so is the bet + or -).
    Finally, modifies the bet if there is a blackjack for the player."""
    
    playerblackjackbr = black_jack_check(playerdeckbr)
    playerhandvaluebr = handvalue(playerdeckbr)
    dealerblackjackbr = black_jack_check(dealerdeckbr)
    dealerhandvaluebr = handvalue(dealerdeckbr)
    
    if playerhandvaluebr > 21:
        betmodifier = -1
        
    elif dealerhandvaluebr > 21 and playerhandvaluebr <= 21:
        betmodifier = 1
        
    elif dealerhandvaluebr <= 21 and playerhandvaluebr <= 21:
        if playerhandvaluebr > dealerhandvaluebr:
            betmodifier = 1
        elif playerhandvaluebr < dealerhandvaluebr:
            betmodifier = -1
        elif playerhandvaluebr == dealerhandvaluebr:
            if (playerblackjackbr == True) and  (dealerblackjackbr == False):
                betmodifier = 1
            elif (playerblackjackbr == False) and  (dealerblackjackbr == True):
                betmodifier = -1
            else:
                betmodifier = 0

    if playerblackjackbr == True:
        betmodifier = (3/2)*betmodifier
                
    bet_resultbr = int(betmodifier * bet_valuebr)
    return bet_resultbr





def black_jack_check(handtocheckbjc, isblackjack = False):
    """Returns a boolean on whether the hand is a blackjack.

    Creates a list of ten and face cards, then checks that the
    hand consists of one of these and an ace."""

    tenfacelist = []
    for cardvaluebjc in card_values[8:12]:
        tenfacelist = tenfacelist + [cardvaluebjc[:3]]

    if len(handtocheckbjc) == 2:
        
        if (handtocheckbjc[0][:3] in ['ace']) and\
           (handtocheckbjc[1][:3] in tenfacelist):
            isblackjack = True
            
        elif (handtocheckbjc[1][:3] in ['ace']) and\
             (handtocheckbjc[0][:3] in tenfacelist):
            isblackjack = True                    

    return isblackjack





def bigdeckmaker(numberofdecksbdm, loopdeck=deckofcards):
    """Returns the giant deck that gets put in the shoe.

    Uses the number chosen by the player and the already defined
    deckofcards."""
    makedeck = []
    while numberofdecksbdm > 0:
        makedeck.extend(loopdeck[:])
        numberofdecksbdm = numberofdecksbdm -1
    return makedeck






def get_number_from_player(maxchoicegnfp, maxstringgnfp, inputstringgnfp,\
                           minstringgnfp, quittrackergnfp, retries=6):
    """Dialog asking player to choose an integer.

    Used for both making bets and picking the size of the shoe."""
    while (retries > 0) :
        playerchoice = input(inputstringgnfp)
        if len(playerchoice) < 1:
            playerchoice='user input error'
        elif playerchoice[0] in [ str(range(10)[i]) for i in range(10)]:
            playerchoice_int = int(playerchoice)
            if (playerchoice_int <= maxchoicegnfp) and (playerchoice_int >0):
                return playerchoice_int, quittrackergnfp
            elif playerchoice_int < 1:
                print(minstringgnfp+' Try again.')
            else:
                print(maxstringgnfp + str(maxchoicegnfp) + '. Try again.')
        else:            
            print('Please enter an integer.')
        retries = retries - 1
        if retries <= 0:    
            print(failuretocomply)
            quittrackergnfp = True
            return 0, quittrackergnfp
            

def get_number_bet(playerchipsgnb, quittrackergnb):
    """A function to make calling get_number_from_player more convenient.

    Returns the number of chips bet, and whether the player needs to be
    ejected for bad answers."""
    maxstringgnb = 'You may bet at most '
    inputstringgnb = 'Please type how many chips would you like to bet: '
    minstringgnb = 'You must bet at least one.'
    bet_valuegnb, quittrackergnb =\
                   get_number_from_player(playerchipsgnb, maxstringgnb,\
                                          inputstringgnb, minstringgnb,\
                                          quittrackergnb)
    return bet_valuegnb, quittrackergnb 

def get_number_decks(quittrackergnd):
    """A function to make calling get_number_from_player more convenient.

    Returns the number of decks, and whether the player needs to be ejected
    for bad answers."""
    maxstringgnd = 'You may choose at most '
    inputstringgnd = 'Please choose how many decks your table is using: '
    minstringgnd = 'You can\'t play with less than one deck of cards.'
    numberofdecksgnd, quittrackergnd =\
                      get_number_from_player(8, maxstringgnd,\
                                             inputstringgnd, minstringgnd,\
                                             quittrackergnd)
    return numberofdecksgnd, quittrackergnd





def quit_query(retries=4):
    while (retries > 0):
        ok = input('Do you want to keep playing, Yes or No? ')
        if ok in ('y', 'ye', 'yes'):
            return False
        if ok in ('n', 'no', 'nop', 'nope'):
            return True
        retries = retries - 1
        if retries < 0:
            print(failuretocomply)
        print('Yes or no, please!')


"""
Future developments (aka a bit of the sausage making):

Write a function to print failuretocomply, set quittracker,
    and eject the player from the game.

Put the quittracker at the beginning of all functions, so that
    get_number_decks can be improved by future implementation of
    variable max number of decks.

Combine the betting and quitting dialog, which will require splitting off
    from the shoesize dialog.

Turn this into a package with one or a few closely related functions in
    each file, instead of this giant one.
"""



if __name__ == "__main__":
    playgame()







