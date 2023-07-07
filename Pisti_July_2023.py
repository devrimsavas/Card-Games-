
import time 
from tkinter import *
import random

CARD_WIDTH=80
CARD_HEIGHT=130
symbols={'HEARTS': ['♥','red'],'DIAMONDS': ['♦','red'],'CLUBS': ['♣','black'],'SPADES': ['♠','black'] }

class Card:
    def  __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.x=0 
        self.y=0 #cards y upper coords
        self.rect=None # card rectangle 
        self.text=None # card text 
        self.card_value=None #card value in game A=1,2=2 so on
        self.card_back=None
        self.card_hide_value=None

        #hide card or show tag?
        self.hide_card=True

    def card_shape(self,canvas,x,y,**kwargs):
        global hex_color
        self.x=x #x,y start coordinates of card rectangle shape 
        self.y=y 
        #self.rect=canvas.create_rectangle(x,y,x+CARD_WIDTH,y+CARD_HEIGHT,fill='white',width=2,outline='gray',**kwargs)
        #self.hide_card=True 
       

        self.rect=canvas.create_rectangle(x,y,x+CARD_WIDTH,y+CARD_HEIGHT,activefill='gray',outline='black',**kwargs)
        #card_value is cards rank and suit text
        self.card_value=f"""\n\n\n{' ':4}{self.rank:2}  
{' ':7}{symbols[self.suit][0]:^00}
{' ':8}{self.rank:2}
"""
        self.card_hide_value_1=f"""\n\n\n\n\n          XXXXXX
          XXXXXX
          XXXXXX
          XXXXXX
          XXXXXX  
          XXXXXX
"""
        self.card_hide_value=f"""\n\n\n\n\n          ▓▓▓▓▓▓
          ▓▒▒▒▒ ▓
          ▓▒░░▒ ▓
          ▓▒░░▒ ▓
          ▓▒▒▒▒ ▓
          ▓▓▓▓▓▓
"""
        if self.hide_card:
            #text on the cards
            self.text=canvas.create_text(self.x+20,self.y+26,text=self.card_hide_value,font=('Arial',12,'bold'),fill='brown')
            
        else:
            
            self.text=canvas.create_text(self.x+20,self.y+26,text=self.card_value,font=('Arial',26,'bold'),fill=symbols[self.suit][1])

        #bind mouse to card
        canvas.tag_bind(self.rect,'<Button-1>',self.start_drag)
        canvas.tag_bind(self.text,'<Button-1>',self.start_drag)
        canvas.tag_bind(self.rect,'<B1-Motion>',self.drag)
        canvas.tag_bind(self.text,'<B1-Motion>',self.drag)
        canvas.tag_bind(self.rect,'<ButtonRelease-1>',self.end_drag)
        canvas.tag_bind(self.text,'<ButtonRelease-1>',self.end_drag)
        canvas.tag_bind(self.rect,'<Double-Button-1>',self.on_double_click)
        canvas.tag_bind(self.text,'<Double-Button-1>',self.on_double_click)

    def on_double_click(self,event): #this method will be used to choose card to throw
        card=self
        double_test(card)

    def start_drag(self,event):
        self.start_x=event.x
        self.start_y=event.y
        canvas.tag_raise(self.rect)
        canvas.tag_raise(self.text)

    def drag(self,event):
        if self.start_x is not None and self.start_y is not None:
            dx=event.x-self.start_x
            dy=event.y-self.start_y
        canvas.move(self.rect,dx,dy)
        canvas.move(self.text,dx,dy)
        self.start_x=event.x
        self.start_y=event.y
        coords=f'{event.x}- {event.y}'
        #position_label.config(text=coords)

    def end_drag(self,event):
        self.start_x=None
        self.start_y=None

    def move_card_org(self,canvas,dx,dy): #no animation 
        canvas.move(self.rect,dx,dy)
        canvas.move(self.text,dx,dy)
        self.x+=dx
        self.y+=dy

    def move_card(self, canvas, dx, dy):
        num_steps = 5  # Number of steps to move the card
        delay = 32  # Delay in milliseconds between each step

        step_x = dx / num_steps
        step_y = dy / num_steps

        for _ in range(num_steps):
            canvas.move(self.rect, step_x, step_y)
            canvas.move(self.text, step_x, step_y)
            self.x += step_x
            self.y += step_y
            canvas.update()  # Update the canvas to reflect the movement
            time.sleep(delay / 1000)  # Delay in seconds
        

    def raise_card(self,canvas):
        canvas.tag_raise(self.rect)
        canvas.tag_raise(self.text)

    def set_visibility(self,canvas,hide):
        self.hide_card=hide
        #remove the old card text
        canvas.delete(self.text)

        
        if self.hide_card:
            #text on the cards
            self.text=canvas.create_text(self.x+20,self.y+26,text=self.card_hide_value,font=('Arial',12,'bold'),fill='brown')
        else:
            self.text=canvas.create_text(self.x+20,self.y+26,text=self.card_value,font=('Arial',26,'bold'),fill=symbols[self.suit][1])

class Deck: #Creates a deck 
    def  __init__(self):
        self.all_cards_in_deck=[] # ATTENTION ALL CARDS HERE 
        for suit in ('HEARTS', 'DIAMONDS', 'CLUBS', 'SPADES'):
            for rank in ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'):
                self.all_cards_in_deck.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.all_cards_in_deck)
    def draw(self):
        try:
            return self.all_cards_in_deck.pop()
        except IndexError:
            raise IndexError('The Deck is Empty') #add here a tkinter label center table

class Player:
    def  __init__(self,name):
        self.name=name
        self.player_cards=[] #dealt cards
        self.player_taken_cards=[] #taken cards
        self.card_position={self.name:[]} # adjust dealt card position
        self.player_box=None #holder for dealt cards
        self.taken_cards_box=None #holder for taken cards
        self.player_info_box=None #text box for players cards
        self.player_info_text=None
        self.player_taken_cards_textbox=None

        self.player_total_value=0 #players taken cards' values

        self.player_pisti=0
        self.player_grand_score=0
        
        

    def player_card_box(self,canvas,x,y,color): # player dealt cards holder
        x1=x+380 #coords and size x, 30 y,165
        y1=y+165
        self.player_box=canvas.create_rectangle(x,y,x1,y1,outline=color,fill=color,width=4)
        self.player_label=canvas.create_text(x+175,y-20,text=self.name.upper(),fill=color,font=('Arial',22))

    def player_value_box(self,canvas,x,y,color): #taken cards box
        x1=x+180
        y1=y+165 # coords and size 180,165
        self.taken_cards_box=canvas.create_rectangle(x,y,x1,y1,outline=color,width=4,fill=color)
        self.tplayer_label=canvas.create_text(x+75,y-10,text=self.name.upper(),fill='white',font=('Arial',16))

    def player_score_box(self,root,x,y,**kwargs): #score and value
        
        self.player_score_box=Text(root,width=15,height=1,fg='black',borderwidth='1',font=('Arial',14),wrap='word')
        self.player_score_box.place(x=x,y=y)

    def player_info(self,root,x,y,**kwargs): # player info taken card box
      
        
        self.player_info_box=Text(root,width=40,height=5,bg='white',borderwidth='3',font=('Arial',13),wrap='word')
        self.player_info_box.place(x=x,y=y)
        self.player_info_text=canvas.create_text(x,y+10,text=self.name.upper(),font=('Arial',14,'italic'),fill='white')

    def player_got_cards(self,card): #player taken cards maybe it must be a list????
        self.player_cards.append(card) # this method add card or cards to players' value
        
    def show_player_dealt_cards(self): #show player dealt cards
        player_name=self.name
        v=0        
        text=""
        for index,card in enumerate(self.player_cards):
            v+=card_valuation(card)
            text+=f'{index}- {card.suit},   {card.rank}, value: {v}\n'
        return f'{text}'

#END CLASSES

#PROGRAM FUNCTIONS

def create_deck(canvas): #create a deck
    r=0
    global hex_color
    global all_cards_in_deck #all cards in the deck
    all_cards_in_deck=[]
    global my_deck #create a global deck
    global my_card # draw a card from deck
    my_deck=Deck()
    my_deck.shuffle() #shuffle deck
    #create cards graphic
    for card in my_deck.all_cards_in_deck:
        
        r+=0.3
        my_card=card
        my_card.card_shape(canvas,19+r,19+r,fill='beige',width=2)
        
        my_card.raise_card(canvas)
        
def draw_table(canvas):
    global table_x_start
    global table_y_start
    
    canvas.update() # need to get canvas width and height
    table_x_start=(canvas.winfo_width()/2)-100
    table_y_start=(canvas.winfo_height()/2)-140
    table_x_end=table_x_start+200
    table_y_end=table_y_start+200
    global card_table # defined as global to use in class methods
    card_table=canvas.create_rectangle(table_x_start,table_y_start,table_x_end,table_y_end,width=2,fill='#276862')
    global coor_card_table
    coor_card_table=canvas.bbox(card_table)
    #place for deck
    canvas.create_rectangle(5,2,100,150,width=3, fill='#276862')

def create_players(canvas): #CREATE PLAYERS
    global players_holder # players in a list
    players_holder=[]
    player_names=['Ahmet','Zeynep','Devrim','Selim']
    positions=[(500,160),(900,370),(500,700),(100,370)] #players table positions on canvas
    box_colors=['magenta','pink','brown','purple']
    for i in range(4):
        player=Player(player_names[i])
        players_holder.append(player)
        
    for index,player in enumerate(players_holder):
        
        player.card_position[player.name]=positions[index]

        #player card_box line 110
        player.player_card_box(canvas,player.card_position[player.name][0],player.card_position[player.name][1],color=box_colors[index]) 

        #player_value_box taken cards table position
        player.player_value_box(canvas,index*180,950,box_colors[index])
        

    for index,player in enumerate(players_holder):
            offset=index*110
            offset_1=index*90
            player.player_info(root,1460,50+offset)
            player.player_score_box(root,50+(offset_1)*2,1170)

def give_cards(canvas):
    global my_deck #deck 
    global all_cards_in_deck #all cards in the deck
    global my_card #draw a card
    global turn #position adjust
    global players_holder #keep all players in a list
    global player #player
    coordx=0

    for player in players_holder: #loop gives cards to player 
        for i in range(1):
            
            my_card=my_deck.draw() #draw a card from the deck
            if player.name=='Devrim':
                my_card.set_visibility(canvas,False)
            else:
                my_card.set_visibility(canvas,True)
            
            
            canvas.tag_raise(my_card.rect)
            canvas.tag_raise(my_card.text)

            player.player_got_cards(my_card) #player takes card and add to player method: self.player_cards.append(card)
            coordx,coordy=canvas.bbox(player.player_box)[:2] # take coords of player box to move cards
            dx,dy=coordx-my_card.x,coordy-my_card.y #delta distances
            my_card.move_card(canvas,dx+i*2+turn*1,dy+30) #5
            my_card.raise_card(canvas) # ADDED THIS CHECK
            player.player_info_box.delete(1.0,END)

            player.player_info_box.insert(1.0,player.show_player_dealt_cards())

            coordx+=CARD_WIDTH+20 #original=40
            
            turn=(turn+20)%320 # there is 16x between a and b f.ex= 20 320, 16 times

def double_test(card): #this routine allows player click card
    #index takes player_number
    test_card=None 
    for index,player in enumerate(players_holder):
        if card in player.player_cards:
            
            #print(f'{player.name} has clicked card {card.rank}-{card.suit} and card index={index}')
            for index_1,card_s in enumerate(player.player_cards):
                print(f'{index_1}-{card_s.rank}: {card_s.suit}')
                
            test_card=card
            throw_card(test_card) #pop the user card


def which_card(): #this is backup
    global players_holder
    global last_card
    player_throw_this=None #decided card 
    player=players_holder[turn_throw]
    temp_cards_table=[]  # [rank, suit, value] this list takes player's cards to valuadate to find correct card to hit
    temp_card_value=0

    game_events_box.delete("1.0",END)
    #print(f'{player.name} Hand: ')
    for player_card in player.player_cards:
        #print(player_card.rank,player_card.suit)
        
        temp_cards_table.append([player_card.rank,player_card.suit])

    if not table_cards_holder : #if table is empty
        
        #print('no card on the table')
        #print('Now it is turn player: ',player.name)
        for player_card in player.player_cards:
            if player_card.rank !='J':
                player_throw_this=player_card
                break
        text=f'No card on the table\nNow it is player {player.name} turn\nplayer {player.name} can hit {player_throw_this.rank} {player_throw_this.suit}'
        game_events_box.insert("1.0",text)
        
        #print(f'player {player.name} can hit {player_throw_this.rank} {player_throw_this.suit}')

    else: #it means if table_cards_holder is not empty
        last_card=table_cards_holder[-1]
        #print('There are cards on the table')
        #print(f'last card is {last_card.rank}')
        text_1=f'Player {player.name} turn\nThere are cards on the table\nThe last card is {last_card.rank}, {last_card.suit}\n'
        game_events_box.insert('1.0',text_1)
        
        for player_card in player.player_cards:
            if player_card.rank==last_card.rank:
                #print('PLAYER CAN TAKE CARDS ON THE TABLE')
                game_events_box.insert(END,'PLAYER CAN TAKE CARDS ON THE TABLE')
                player_throw_this=player_card
                #print(f'player throw this : {player_throw_this.rank}: {player_throw_this.suit}')
                break
            elif player_card.rank=='J':
                #game_events_box.insert('END',f'Player {player.name} has JOKER {check_card.rank} {check_card_.suit}\n Can take all cards')
                #print('PLAYER HAS JOKER AND CAN TAKE ALL CARDS ON THE TABLE')
                player_throw_this=player_card
                break
        if player_throw_this is None:
            player_throw_this=random.choice(player.player_cards)
            
        #print(player.name,'can hit the card',player_throw_this.rank)
        #print(f'player throw this : {player_throw_this.rank}: {player_throw_this.suit}')

    test_card=player_throw_this
    test_card.set_visibility(canvas,True)
    throw_card(test_card)
    #print(test_card.rank,'ssssssssss')


def throw_card(test_card):
    global turn_throw
    taken_cards_text="" # text for taken cards
    global last_card
    last_card=None
    player=players_holder[turn_throw] #player turn

    new_cards=[] #this list keeps the cards when player took them. needs to be cleaned after value calculation
    
    coor_value_box=canvas.bbox(player.taken_cards_box) # coords of taken_cards_box  
    value_box_x=(coor_value_box[0]) #start x value_box
    value_box_y=(coor_value_box[1]) #start y value_box
    global pisti
    pisti=False
    
    #player hits a cards
    #card_throw=player.player_cards.pop()
    card_throw=test_card  #this hit double selected card but not pop from players card.
    #card_throw.set_visibility(canvas,True)
    card_throw.set_visibility(canvas,False)

    #AI DENEME
    #card_throw=which_card()
    player.player_cards.remove(card_throw)
    ##CARD
    center_x=(coor_card_table[0]+coor_card_table[2])//2-50
    center_y=(coor_card_table[1]+coor_card_table[3])//2-60

    dx=center_x-card_throw.x
    dy=center_y-card_throw.y

    card_throw.move_card(canvas,dx,dy)
    card_throw.set_visibility(canvas,False)
    canvas.tag_raise(card_throw.rect)
    canvas.tag_raise(card_throw.text)
    #END BLOCK

    if table_cards_holder:
        last_card=table_cards_holder[-1] #last card before player's card
        card_throw.set_visibility(canvas,False)
    table_cards_holder.append(card_throw) #player's card adds to deck
    #function below needs to check which card
    if last_card is not None:
        #print('---------------------------------------------')
        print('PLAYER=',player.name)
        print('LAST CARD = ',last_card.rank, last_card.suit)
        print('CARD THROW= ',card_throw.rank,card_throw.suit)
        print('---------------------------------------------')

        if len(table_cards_holder)==2 and card_throw.rank==last_card.rank:
            print(f'PLAYER {player.name} hit a pisti')            
            pisti=True #check pisti 

        #PLAYER TAKES CARD if condition below occurs ****************

        if card_throw.rank==last_card.rank or (card_throw.rank=='J' and len(table_cards_holder)>0):
            #put cards on the table to player taken cards
            player.player_taken_cards.extend(table_cards_holder)
            #Clear cards on the table after player got them
            table_cards_holder.clear()

            #card position calculation
            card_throw.x=canvas.bbox(card_throw.rect)[0]
            card_throw.y=canvas.bbox(card_throw.rect)[1]
            dtvx=value_box_x-card_throw.x
            dtvy=value_box_y-card_throw.y

            #MOVE CARDS BLOCK TO VALUE_BOX
            for card in player.player_taken_cards:
                dvx=value_box_x-card.x+50
                dvy=value_box_y-card.y+25
                card.move_card(canvas,dvx,dvy)
                canvas.tag_raise(card.rect)
                canvas.tag_raise(card.text)
                
                #add to new cards for correct valuation 
                new_cards.append(card)
            #routine below calculates new_cards_values
            for index,card in enumerate(new_cards):
                player.player_total_value+=card_valuation(card)
                
                #print(player.name,index,card.rank, card.suit)
                #print('value',player.player_total_value)
        if pisti:
            player.player_total_value+=10
        else:
            player.player_total_value=player.player_total_value
            new_cards.clear()
            
    #update player score box card valuation
    player.player_score_box.delete(1.0,END)
    score_text=f'S: {player.player_total_value}: A:{len(player.player_taken_cards)}'
    player.player_score_box.insert("1.0",score_text)
    
    #those 2 lines below update player info box 
    player.player_info_box.delete(1.0,END)
    player.player_info_box.insert(1.0,player.show_player_dealt_cards())
    turn_throw=(turn_throw+1)%4
    show_cards_on_table()

    #print(player.name,len(player.player_taken_cards),'CARD AMOUNT')

        #REST CARD AND CARDS AMOUNT
    card_number_label.config(text=f'CARD ON TABLE {len(my_deck.all_cards_in_deck)} ')

    turn_label.config(text=f'PLAYER TURN {players_holder[turn_throw].name}')

    #check if DECK is empty and add a routine for rest cards
    if (len(my_deck.all_cards_in_deck)==0 and len(players_holder[0].player_cards)==0 and len(players_holder[1].player_cards)==0 and
     len(players_holder[2].player_cards)==0 and len(players_holder[3].player_cards)==0):
        print('NO CARD')
        add_rest_card()
        #reset counter
        turn_throw=0

global players_grand_score_list
players_grand_score_list=[]

def add_rest_card(): #handle rest cards 
    card_amount_list=[] #table rest cards' amount
    rest_cards_value=0 #value in rest cards
    
    for player in players_holder:
        #print(f'{player.name}: {len(player.player_taken_cards)}')
        card_amount_list.append((player,len(player.player_taken_cards))) #all players cards amount 

    #SHOW REST CARDS
    for card in table_cards_holder:
        print(card.rank)

    amount_rest_cards=len(table_cards_holder) #REST CARDS AMOUNT

    for card in card_amount_list: #this is just to check card_amount list 
        print(card[0].name,card[1])

    #Find who took the most cards of the deck.
    max_card_owner=max(card_amount_list,key=lambda item:item[1])
    #add cards and values . no need to calculate whole cards again
    #calculate rest cards value
    for card in table_cards_holder:
        rest_cards_value+=card_valuation(card)

    print(f'REST CARD VALUES {rest_cards_value}')

    #add rest cards value to players_value
    max_card_owner[0].player_total_value+=rest_cards_value #add rest cards' values to winner 

    #print(f'player {max_card_owner[0].name} cards value AFTER taken last card= {max_card_owner[0].player_total_value}')
    #add table cards to player
    coor_value_box=canvas.bbox(max_card_owner[0].taken_cards_box) # coords of taken_cards_box  
    value_box_x=(coor_value_box[0]) #start x value_box
    value_box_y=(coor_value_box[1]) #start y value_box

    for card in table_cards_holder:
        dvx=value_box_x-card.x+50
        dvy=value_box_y-card.y+25
        card.move_card(canvas,dvx,dvy)
        canvas.tag_raise(card.rect)
        canvas.tag_raise(card.text)

    max_card_owner[0].player_score_box.delete(1.0,END)
    score_text=f'S: {max_card_owner[0].player_total_value}: A:{len(max_card_owner[0].player_taken_cards)+amount_rest_cards}'
    max_card_owner[0].player_score_box.insert("1.0",score_text)

    #Winner
    compare_scores=[]
    for winner in players_holder:
        print(winner.name,winner.player_total_value)
        compare_scores.append((winner.name,winner.player_total_value))
        winner.player_grand_score+=winner.player_total_value
        
    winner_person=max(compare_scores,key=lambda item:item[1])
    print(winner.player_grand_score)

    print(winner_person)

    table_cards_holder.clear()
    show_cards_on_table()

    score_table(compare_scores)



def score_table(whole_scores):
    title='SCORE TABLE'
    score_table_text=""
    if whole_scores:
        whole_scores.sort(key=lambda x: x[1], reverse=True) #or sorted_scores=sorted(whole_score,key=lambda x: x[1], reverse=True)
        for index, player_rank in enumerate(whole_scores):
            score_table_text+=f'{index}- {player_rank[0]}- {player_rank[1]}\n'
        print(title)
        print(score_table_text)
        canvas.create_text(table_x_start+90,table_y_start+80,text=score_table_text,font=('Arial',16),fill='white')
    else:
        return 
    
global pisti
pisti=False
    
def card_valuation(card):
    global pisti
    if pisti==True:
        print('PISTI')
    value=0
    
    if card.rank=='J' or  card.rank=='A':
        value= 1
    elif card.rank=='2' and card.suit=='CLUBS':
        value= 2
    elif card.rank=='10' and card.suit=='DIAMONDS':
        value= 3
    else:
        value= 0
    return value
   
def show_cards_on_table():
    table_info_box.delete('1.0',END)
    
    table_text=""
    for card in table_cards_holder:
        table_text+=f'{card.rank}  {card.suit} {symbols[card.suit][0]} \n'
        
    table_info_box.insert('1.0',table_text)

def start_game(canvas):
    global last_card
    turn_throw=0
    last_card=None 
    canvas.delete('all')
    draw_table(canvas)
    
    create_players(canvas) #create players
    create_deck(canvas) #create a new deck
    for i in range(4): #since there are 4 players
        give_cards(canvas)
    turn_throw=0
#init tkinter

root=Tk()
root.geometry('1450x1350') #1850x1350')
root.title('PISTI V1')
global players_holder #list for all players
global turn #turn 
turn=0
global table_text
global card_number
card_number=0
global table_text
table_text=""
global player_turn
player_turn=0
global my_card
global total_cards_value
total_cards_value=0
global turn_throw
turn_throw=0
global table_cards_holder
table_cards_holder=[] #cards on table 

#create canvas
canvas=Canvas(root,bg='#747869',width=1350,height=1100,borderwidth=5,border=1,relief='ridge') #relief=flat,raised,sunken,groove,rigde
canvas.place(x=50,y=50)
draw_table(canvas) # draw card table

start_button=Button(root,text='START',width=10,bg='green',font=('Arial',16,'bold'),command=lambda:start_game(canvas))
start_button.place(x=50,y=1250)


create_deck_button=Button(root,text='CREATE DECK',width=14,bg='green',font=('Arial',16,'bold'),command=lambda:create_deck(canvas))
create_deck_button.place(x=200,y=1250)

create_players_button=Button(root,text='CREATE PLAYERS',width=16,bg='green',font=('Arial',16,'bold'),command=lambda:create_players(canvas))
create_players_button.place(x=400,y=1250)

give_cards_button=Button(root,text='DEAL CARDS', width=16,bg='green',font=('Arial',16,'bold'),command=lambda:give_cards(canvas))
give_cards_button.place(x=625,y=1250)

#check_value_button=Button(root,text='HIT CARD',width=16,bg='green',font=('Arial',16,'bold'),command=lambda:throw_card(test_card))
#check_value_button.place(x=850,y=1250)

#AI BUTTON

ai_button=Button(root,text='TURN', width=16,bg='blue',font=('Arial',16,'bold'),command=lambda:which_card())
ai_button.place(x=850,y=1250)

#text box shows cards on the table

table_info_box=Text(root,width=33,height=10,wrap='word',font=('Arial',14),bg='white')
table_info_box.place(x=1460,y=515)

#GAME EVENTS
game_events_box=Text(root,width=33,height=15,wrap='word',font=('Arial',14),bg='white')
game_events_box.place(x=1460,y=750)

card_number_label=Label(root,text="CARDS",font=('Arial',16,'bold'),bg='#747869')
card_number_label.place(x=250,y=70)


#the label below shows card's position
#position_label=Label(root,text="position",font=('Arial',12),fg='black')
#position_label.place(x=850,y=1200)

def change(scale_value):
    global hex_color
    r=r_vertical.get()
    g=g_vertical.get()
    b=b_vertical.get()
    rgb_color=(r,g,b)
    hex_color='#{:02x}{:02x}{:02x}'.format(*rgb_color)
    canvas.config(bg=hex_color)
    turn_label.config(bg=hex_color)
    card_number_label.config(bg=hex_color)
    root.config(bg=hex_color)
    
#RGB COLOR SLIDER FOR CANVAS
global hex_color 

hex_color=(0,154,0)

rgb_holder=LabelFrame(root,text='RGB COLORS',fg='blue',width=140,height=140,borderwidth=4)
rgb_holder.place(x=1460,y=1100)
r_vertical=Scale(rgb_holder,from_=255, to=0,command=change)
r_vertical.place(x=0,y=5)
g_vertical=Scale(rgb_holder,from_=255, to=0,command=change)
g_vertical.place(x=40,y=5)
b_vertical=Scale(rgb_holder,from_=255,to=0,command=change)
b_vertical.place(x=80,y=5)

turn_label=Label(root,text="PLAYER TURN:",bg='#747869',fg='white',font=('Arial',12,'bold'))
turn_label.place(x=650,y=680)

#EXPEND TABLE Button
global play_table_extender
play_table_extender=0


def resize_play_table():
    global play_table_extender
    play_table_extender=1-play_table_extender
    
    if play_table_extender==False:
        root.geometry('1450x1350') #original 1850x1350
        expend_button.config(text='>')
    else:
        root.geometry('1850x1350')
        expend_button.config(text='<')
    
expend_button=Button(root,text='>',bg='gray',font=('Arial',14,'bold'),command=lambda:resize_play_table())
expend_button.place(x=1412,y=500)

root.mainloop()
    
