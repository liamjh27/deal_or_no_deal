import random

class Banker:
    def __init__(self):
        self.last_offer = None 
        self.welcome_messages = [
            'The banker is hoping you have a terrible game.',
            'The banker is looking forward to making his day by ruining yours.',
            'The banker wants your box for as cheap as possible.'
        ]
    

    def welcome(self):
        return random.choice(self.welcome_messages)
    
    def make_offer(self, remaining_boxes):
        offer = sum(remaining_boxes) / len(remaining_boxes)
        previous_offer = self.last_offer 
        self.last_offer = offer 
        return previous_offer, offer 