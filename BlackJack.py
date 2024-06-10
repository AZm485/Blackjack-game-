import random, sys

HEARTS = chr(9829) 
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'

def getBet(maxBet):
    # Asks player how much they want to bet
    while True:
        print('How much do you want to bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        
        if not bet.isdecimal():
            continue
        
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet


def getDeck():
    # Return a list of (rnk, suit) tuples for all 52 cards.
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank,suit))
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    #Show the player and dealer's cards. Hide the dealer's first card if showDealerHand is False
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # Hide's the dealers first card
        displayCards([BACKSIDE] + dealerHand[1:])
    
    # Show player's cards
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    # Returns the value of the cards
    value = 0
    numberOfAces = 0

    # Add the value for the non-ace cards:
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)
    
    # Add the value for the aces
    value += numberOfAces
    for i in range(numberOfAces):
        # if another 10 can be added without busting
        if value + 10 <= 21:
            value += 10
    
    return value

def displayCards(cards):
    # Display all the cards in the cards list
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += '___  '
        if card == BACKSIDE:
            # Print a cards back
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_## | '
        else:
            # Print the cards front
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{} | '.format(rank.rjust(2, '_'))
    for row in rows:
        print(row)


def getMove(playerHand, money):
    # Asks the player for their move
    while True:
        moves = ['(H)it', '(S)tand']

        # The player can double down on their first move
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')
        
        # Get the player's move
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move

            
def main():
    print("""
          Rules:
            Try to get as close to 21 without going over.
            Kings,Queens, and Jacks are 10 points.
            Aces are worth 1 or 11 points.
            Cards 2 through 10 are worth their face value.
            (H)it to take another card.
            (S)tand to stop taking cards.
            On your first play you can (D)ouble down to increase your bet
            but must hit exactly one more time before standing.
            In case of a tie, the bet us returned to the player.
            The dealer stops hitting at 17""")
    
    money = 5000
    while True:
        # Check if the player has run out of money
        if money <= 0:
            print("You're broke!")
            print('Thanks for playing!')
            sys.exit()
        # Let the player enter their bet for this round
        print('Money: ', money)
        bet = getBet(money)

        # Give the dealer and player two cards from the deck each:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Handle player actions
        print('Bet: ', bet)
        while True: # Keeps looping until player stands or busts
            displayHands(playerHand, dealerHand, False)
            print()

            # Check if player has bust
            if getHandValue(playerHand) > 21:
                break
            
            # Get the player's move, either H, S, or D
            move = getMove(playerHand, money - bet) 

            # Handle the player action
            if move == 'D':
                # Double down
                additionalBet =getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet: ', bet)
            
            if move in ('H', 'D'):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    #Busted
                    continue

            if move in ('S', 'D'):
                # Stand or doubling down stops the players turn
                break
            
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # The dealer hits
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)
                
                if getHandValue(dealerHand) > 21:
                    break
                input('Press Enter to continue...')
                print('\n\n')

        # Show the final hands
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        #Handle whether the player won, lost, or tied
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue == dealerValue:
            print('It\'s a tie, the bet is returned to you.')

        input('Press enter to continue...')
        print('\n\n')


if __name__ == '__main__':
    main()
    