import sys
import random 
from lib.box import Box 
from lib.banker import Banker
import time 
import os

banker = Banker() 

class Game:
    def __init__(self, tts=False):
        self.tts = tts 
        self.player_box = None
        self.boxes = []
        self.boxes_chosen = []
        self.box_values = [0.01, 0.10, 1, 5, 10, 1000, 2000, 4000, 5000, 10000]
        self.remaining_box_values = [] 


    def run(self):
        self.display_message('Welcome to the game!')
        self.display_message(banker.welcome())
        self.prompt_for_game_length()
        self.setup_boxes()
        self.assign_box()
        self.show_remaining_boxes()
        self.show_remaining_values() 
        self.play_round(5)
        playing = True 
        while playing:
            self.play_round(3)

    def say(self, text):
        os.system(f'say "{text}"')


    def display_message(self, message, timer=2):
        if self.tts == True:
            self.say(message)
        print(message)
        time.sleep(timer)
    def setup_boxes(self):
        random.shuffle(self.box_values)
        box_number = 0
        for value in self.box_values:
            box_number += 1
            box = Box(box_number, value) 
            self.boxes.append(box)
            self.remaining_box_values.append(value) 
        self.remaining_box_values.sort() 
    
    def assign_box(self):
        player_box = random.choice(self.boxes)
        self.player_box = player_box
        self.boxes.remove(player_box)
        self.display_message(f'You got box {self.player_box.number}')

    def show_remaining_boxes(self):
        remaining_boxes = []
        for box in self.boxes:
             box_string = f'Box {box.number}'
             remaining_boxes.append(box_string)
        remaining_boxes = '\n'.join(remaining_boxes)
        self.display_message(remaining_boxes) 

    def show_remaining_values(self):
        remaining_values = []
        for value in self.remaining_box_values:
            penny_values = [0.01, 0.05, 0.10, 0.50]
            if value in penny_values:
                remaining_values.append(f'{int(value * 100)}p')
            else: 
                remaining_values.append(f'£{value}')
        remaining_values = '\n'.join(remaining_values)
        self.display_message(remaining_values)

    def prompt_for_choice(self):
         self.display_message('Pick a box', 0)
         choice = input('Which box would you like to get rid of?')
         if choice.isalpha():
             self.display_message('Choice must e a number', 0)
             return self.prompt_for_choice()
         elif choice == '':
            self.display_message("Can't be an empty answer!")
            return self.prompt_for_choice()

         elif int(choice) > len(self.box_values):
             self.display_message('You don\'t have that many boxes!')
             return self.prompt_for_choice()
         elif int(choice) in self.boxes_chosen:
             self.display_message('You already opened that box. Choose')
             return self.prompt_for_choice()
         elif int(choice) == self.player_box.number:
             self.display_message('You can\t pick your own box!')
             return self.prompt_for_choice()
         else:
             return choice 
         
    def take_turn(self):
        choice = self.prompt_for_choice()
        selected_box = next((box for box in self.boxes if box.number == int(choice)), None)
        selected_box_value = self.format_value(selected_box.value)
        self.display_message(f'Box {selected_box.number} was worth {selected_box_value}')
        self.boxes = [box for box in self.boxes if box.number != int(choice)]
        self.remaining_box_values.remove(selected_box.value) 
        self.boxes_chosen.append(int(choice))
        self.display_message('Boxes remaining:', 0)
        self.show_remaining_boxes()
        self.display_message('Money left on the board:', 0)
        self.show_remaining_values()

    def format_value(self, value):
        penny_values = [0.01, 0.05, 0.1, 0.5]
        if value < 1:
            return f'{int(value * 100)}p'
        else:
            return f'£{int(value)}'
        
    def make_offer(self):
        last_offer, offer = banker.make_offer(self.remaining_box_values)
        self.display_message('Ring Ring')
        if last_offer is not None:
            self.display_message(f'Last time, the banker offered you {self.format_value(last_offer)}.')
        self.display_message(f'The banker would like to offer you {self.format_value(offer)} for your box')
        self.deal_or_no_deal(offer)

    def play_round(self, turns):
        turns_taken = 0
        while turns_taken < turns:
            self.take_turn()
            turns_taken+=1
        self.make_offer()
        if len(self.boxes) == 1:
            self.offer_switch()

    def deal_or_no_deal(self, offer):
        self.display_message('Deal, or no deal?', 1)
        answer = input('deal/no deal')
        if answer.lower() == 'deal':
            self.display_message("You've decided to deal. Let's find out if you've beat the banker.")
            self.display_message(f'You made a deal with the banker for {self.format_value(offer)}.')
            self.display_message('Your box was worth...', 5)
            self.display_message(f'{self.format_value(self.player_box.value)}')
            if offer > self.player_box.value:
                self.display_message('Congratulations! You beat the banker!')
                self.display_message('Thanks for playing!')
            else:
                self.display_message('The banker wins!')
                self.display_message('Better luck next time!')
            self.exit()
        elif answer.lower() == 'no deal':
            pass 
        else:
            self.display_message('Answer must be "deal" or "no deal".')
            return self.deal_or_no_deal(offer)
    

    def exit(self):
        sys.exit(0)


    def offer_switch(self):
        self.display_message("You've played all the way to the final two boxes!", 1)
        self.display_message("You now have the choice to either keep your box, or switch it with the final remaining box.", 1)
        self.display_message("What would you like to do?", 1)
        self.display_message("Would you like to switch?",0)
        prompting = True
        while prompting:
            answer = input('yes/no')
            if answer.lower() == 'yes':
                prompting = False 
                player_box = self.boxes[0]
                self.boxes[0] = self.player_box
                self.player_box = player_box
                self.switched = True
            elif answer.lower() == 'no':
                prompting = False
                self.switched = False
                pass 
            else:
                self.display_message('Must say "yes" or "no"!')
        if self.switched:
            self.display_message("You decided to switch!")
            self.display_message("Your original box was worth...", 3)
            self.display_message(f"{self.format_value(self.boxes[0].value)}")
            self.display_message("Your new box is worth...", 4)
            self.display_message(f"{self.format_value(self.player_box.value)}")
            if self.player_box.value > self.boxes[0].value:
                self.display_message("That was a good switch!")
                self.display_message("You've beaten the banker, thanks for playing!")
                self.exit()
            else:
                self.display_message("Not a great switch!")
                self.display_message("You should have kept your box! The banker is very happy you didn't take his deal!")
                self.display_message("Better luck next time!")
                self.exit() 
        else:
            self.display_message("You've chosen to keep your box. Let's find out if it was the right thing to do!")
            self.display_message("Your box was worth...", 4)
            self.display_message(f"{self.format_value(self.player_box.value)}")
            if self.player_box.value > self.boxes[0].value:
                self.display_message("Congratulations, you win! The banker is not happy!")
                self.display_message("Thanks for playing!")
                self.exit()
            else:
                self.display_message("Bad luck! The banker is very happy with you! He's glad you didn't take his deal.")
                self.display_message("Better luck next time!")
                self.exit() 

    def prompot_for_tts(self):
        self.display_message('Would yu like to play with text to speech?', 0)
        prompting = True
        while prompting:
            setting = input('yes/no').lower()
            if setting == 'yes':
                self.tts = True
                prompting = False 
            elif setting == 'no':
                self.tts = False
                prompting = False
            else:
                self.display_message('Please type yes or no.', 0)

    def prompt_for_game_length(self):
        self.display_message('Which length game would you like to play?\nShort - 10 boxes with a grand prize of £10,000\nLong - 22 boxes with a grand prize of £250,000', 0)
        prompting = True
        while prompting == True: 
            length = input('short/long').lower()
            if length == 'short':
                prompting = False            
            elif length == 'long':
                self.box_values = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000, 200000, 250000]
                prompting = False 
            else:
                self.display_message('Must be "short" or "long".', 0)

