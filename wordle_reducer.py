import string

file = open("words.txt") # The file with all the Wordle words
data = file.read() # The words, in string form seperated by newlines
words = data.split("\n") # Each word, seperately


def get_possiblities(known_correct, known_incorrect, forbidden):
    """
    Summary:
        Get the possible words for the game Wordle, incorporating all known information gained through
        prevous guesses.
    
    Parameters:
        known_correct: a 5-character string. For each character, if the character is known, write it.
            Otherwise write '*'. For example, if you guess 'zonal' for your first guess and 'z' and 'l' 
            are highlighted in green by Wordle, write 'z***l'.
        forbidden: a list of 5 strings, corresponding to each character slot in the word, in order. 
        Each string contains the characters known not to go in the slot.
            
    Returns:
        A list containing all the possible words
    """

    possibilities = [] # The possible words
    
    for possible_word in words: # Iterate over every possible word
        
        add = True
        
        for char in set(known_incorrect):
            if char not in possible_word:
                add = False
                break
            
        if not add:
            continue
        
        for index in range(len(possible_word)):
            char = possible_word[index]
            known_char = known_correct[index]
            if known_char in string.ascii_lowercase and char != known_char:
                break
            if char in forbidden[index]:
                break
        
        else:
            possibilities.append(possible_word)
            
    # Return the possibilities
    return possibilities

def score_letters(possiblities):
    table = dict.fromkeys(string.ascii_lowercase, 0)
    for possibility in possiblities:
        for letter in possibility:
            table[letter] += 1
    return table

def score_possiblity(possibility, table: dict):
    score = 0
    for letter in set(possibility):
        score += table[letter]
    return score

def get_best_guess(possibilities):
    table = score_letters(possibilities)
    best_guess = ['', 0]
    for possibility in possibilities:
        score = score_possiblity(possibility, table)
        if score > best_guess[1]:
            best_guess.clear()
            best_guess.extend([possibility, score])
    return best_guess[0]

def main():
    print("Welcome to the Worlde Helper.")
    print(f"There are {len(words)} possible 5-letter words.")
    print("As you learn more, there will be less possibilites.")
    print("The Wordle Helper will help you find them.\n")
    
    INIT_MAX_LINES = 20
    
    known_correct = ['*'] * 5
    known_incorrect = []
    forbidden = [[], [], [], [], []]
    
    possibilities = get_possiblities(known_correct, known_incorrect, forbidden)
    best_guess = get_best_guess(possibilities)
    
    print(f"For your first guess, the best word to guess is '{best_guess}'.")
    print("Good luck!\n")
    
    while True:
        print("For the feedback: type 'g' if character is green highlighted,")
        print("'y' if yellow highlighted, 'd' if dark grey highlighted")
        
        #Wordle Archive 162
        word = input("\nWhat word did you guess?: ")
        feedback = input("What is the feedback?: ")
        
        for index in range(len(word)):
            feedback_char = feedback[index]
            word_char = word[index]
            
            if feedback_char == 'g':
                known_correct[index] = word_char
            elif feedback_char == 'y':
                known_incorrect.append(word_char)
                forbidden[index].append(word_char)
            else:
                for index in range(5):
                    forbidden[index].append(word_char)
        
        
        if '*' not in known_correct:
            print("You guessed the word!")
            break
        
        possibilities = get_possiblities(known_correct, known_incorrect, forbidden)
        
        print("Below are the possible words.")
        for index in range(len(possibilities)):
            if index == INIT_MAX_LINES:
                print(f"...and {len(possibilities) - index} more words.\n")
                if input("Do you want see all the words? (y/n): ")[0].lower() != "y":
                    break
                else:
                    print("\n")
            print(possibilities[index])
        print("\n")
        
        best_guess = get_best_guess(possibilities)
        print(f"Your best guess is '{best_guess}'.")
        print("Good luck!\n")
    
    return locals()
            
x = main()
                
        

            
            
            
    