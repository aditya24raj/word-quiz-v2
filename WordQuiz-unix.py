from os import name
from random import choice
from time import sleep


def colored(message, color="red"):
    colors = {"red": "0;37;41"}
    return(f"\x1b[{colors[color]}m{message}\x1b[0m")
    #return message


class Dictionary:
    def __init__(self):
        self.words_list_path = ".\\words_list\\" if name == "nt" else "./words_list/"
        self.lexis = {}
        self.word_usage_index = 0

    def __words_is_used__(self, word):
        self.lexis[word[0]][0].remove(word)
        self.lexis[word[0]][1][word] = self.word_usage_index
        self.word_usage_index += 0.5

    def __lexis_maker__(self, letter):
        try:
            with open(self.words_list_path + letter) as word_file_path:
                self.lexis[letter] = list(
                    set(word_file_path.read().splitlines())), {}
        except FileNotFoundError:
            print(f"\nNecessary word lists are missing!!")
            input("Press any key to exit...")
            exit()

    def check_word(self, word):
        global start_with
        global total_lives
        global wasted_lives

        word = str(word).strip().lower()
        invalid_word_error = ""
        try:
            if not word.isalpha() or ord(word[0]) not in range(97, 123):
                invalid_word_error = "Not an alphabetic string"

            elif word[0] != start_with:
                invalid_word_error = f"String does not start with '{start_with}'"

            elif word in self.lexis[word[0]][1]:
                used_at = self.lexis[word[0]][1][word]
                invalid_word_error = f"Already used by {'You' if used_at == int(used_at) else 'Bot'} at score {int(used_at)} "

            elif word not in self.lexis[word[0]][0]:
                invalid_word_error = "Not an english word"

            if invalid_word_error:
                print(
                    f"{colored('Error')} {colored(f'{repr(word)}')} {invalid_word_error}\n{' ' * (6 + len(repr(word)))} {wasted_lives} out of {total_lives} chances wasted.\n")
                if wasted_lives == total_lives:
                    self.word_usage_index += 0.5
                    print(f"{' ' * (7 + len(repr(word)))}Passing this letter...\n")
                return False

            else:
                self.__words_is_used__(word)
                return True

        except KeyError:
            self.__lexis_maker__(word[0])
            return self.check_word(word)

    def get_word(self, letter):
        letter = str(letter).lower()
        try:
            response = choice(self.lexis[letter][0])
            self.__words_is_used__(response)
            return response

        except KeyError:
            self.__lexis_maker__(letter)
            return self.get_word(letter)

        except IndexError:
            return None  # lexis exhausted


class Player:
    def __init__(self, name, *, auto_respond=False):
        self.name = name
        self.score = 0
        self.auto_respond = auto_respond

    def respond(self):
        if self.auto_respond:
            response = my_dictionary.get_word(start_with)
            if response:
                for i in response:
                    print(i, end="", flush=True)
                    sleep(0.03)
                print("\n")
            else:
                print(":(\n")
                print("Bot exhuasted its vocabulary!")

            return response
        else:
            return input()


# starting gameplay
players = Player("You"), Player("Bot", auto_respond=True)

my_dictionary = Dictionary()

total_lives = 3
wasted_lives = 0
passed = 0
start_with = chr(choice(range(97, 123)))


def declare_winner_and_exit():
    print("\n")
    for player in players:
        print(f"{player.name} {player.score}")

    score_diff = players[0].score - players[1].score

    if score_diff < 0:
        print(f"{players[0].name} lost by {abs(score_diff)}. :(")
    elif score_diff > 0:
        print(f"{players[0].name} won by {abs(score_diff)}. :) :)")
    else:
        print("it was a tie. :)")

    input("\nPress any key to exit...")
    exit()


title = f"""\
 _ _ _           _  
| | | |___ ___ _| |  
| | | | . |  _| . |  
|_____|___|_| |___|  
 _____     _         
|     |_ _|_|___     
|  |  | | | |- _|    
|__  _|___|_|___|    
   |__|              
  """

description = f"""\
 ** Parental advisory, 
    computer uses wordlists to respond.
    wordlists contain most of the common words,
    including explicit ones.
    
 ** Wordlists are based on Google n-grams,
    used under creative commons attribution 3.0
    unported license.
"""

howto = f"""\
   
       Enter a word |   |Type word here and press
       starting with|   |enter or press enter without
       this letter  |   |typing anything to exit.
       _____________|_  |____________________________
                      |          |"""

tags = f"""\
{colored(' Player ')}   {colored(' Score ')}   {colored(' Letter ')}   {colored(' Word ')}\n"""

print(title)
print(description)
print(howto)
print(tags)
while passed < 2:
    for player in players:
        wasted_lives = 0

        while wasted_lives < total_lives:
            print(
                f" {player.name}{' '*8}{player.score}{' '*(11-len(str(player.score)))}{start_with}", end=" "*9)
            # keeps cursor from going to bottom
            print("\n"*7) # move cursor down
            print(f"\x1b[7A\x1b[0A",end="") # move cursor up
            print(f"\x1b[32C\x1b[0C",end="") # move cursor forward

            response = player.respond()
            wasted_lives += 1

            if not response:
                if player.auto_respond:
                    declare_winner_and_exit()
                else:
                    print(f"{colored(' Exit ')} {colored(' y/N ')}", end=" ")
                    if input().lower() == "y":
                        declare_winner_and_exit()
                    else:
                        wasted_lives -= 1
                        print(" resuming game..\n")
                        continue

            if not player.auto_respond:
                if my_dictionary.check_word(response):
                    pass
                else:
                    continue

            player.score += 1
            start_with = response[-1]
            break
