from ctypes import windll
from os import getpid, kill
from random import shuffle
from signal import SIGTERM
from threading import Thread
import tkinter as tk
import asyncio
from playsound import playsound


# Dynamic variables
player_score = 0  # player score per round
dealer_score = 0  # dealer score per round
player_score_total = 0  # player score total
dealer_score_total = 0  # dealer score total
player_name = 'ANÓNIMO'  # player name default is ANÓNIMO
player_hand = []  # player hand per round used to store the 5 cards
dealer_hand = []  # dealer hand per round used to store the 5 cards
hit_try_player = 1  # player hit try per round
hit_try_dealer = 1  # dealer hit try per round
deck_play = []  # deck used to play. refreshes every time a round starts
turn = 'player'  # turn variable used to know who's turn is it
version = '1.8'  # version of the game
wait_hit_stand = 'wait'  # wait for player to hit or stand
muted = False  # muted variable used to know if the game is muted or not

# ICO
windll.shell32.SetCurrentProcessExplicitAppUserModelID('girtim.blackjack.0')

# Fixed variables
pid = getpid()  # get process id
suits = ('S', 'H', 'D', 'C')  # suits

# deck dictionary with all the cards and their respective images
deck_dict = {('S', 1):  'cartas/1S.png',  ('S', 2):  'cartas/2S.png',  ('S', 3): 'cartas/3S.png',
             ('S', 4):  'cartas/4S.png',  ('S', 5):  'cartas/5S.png',  ('S', 6): 'cartas/6S.png',
             ('S', 7):  'cartas/7S.png',  ('S', 8):  'cartas/8S.png',  ('S', 9): 'cartas/9S.png',
             ('S', 10): 'cartas/10S.png', ('S', 11): 'cartas/11S.png', ('S', 12): 'cartas/12S.png',
             ('S', 13): 'cartas/13S.png', ('H', 1):  'cartas/1H.png',  ('H', 2):  'cartas/2H.png',
             ('H', 3):  'cartas/3H.png',  ('H', 4):  'cartas/4H.png',  ('H', 5):  'cartas/5H.png',
             ('H', 6):  'cartas/6H.png',  ('H', 7):  'cartas/7H.png',  ('H', 8):  'cartas/8H.png',
             ('H', 9):  'cartas/9H.png',  ('H', 10): 'cartas/10H.png', ('H', 11): 'cartas/11H.png',
             ('H', 12): 'cartas/12H.png', ('H', 13): 'cartas/13H.png', ('D', 1):  'cartas/1D.png',
             ('D', 2):  'cartas/2D.png',  ('D', 3):  'cartas/3D.png',  ('D', 4):  'cartas/4D.png',
             ('D', 5):  'cartas/5D.png',  ('D', 6):  'cartas/6D.png',  ('D', 7):  'cartas/7D.png',
             ('D', 8):  'cartas/8D.png',  ('D', 9):  'cartas/9D.png',  ('D', 10): 'cartas/10D.png',
             ('D', 11): 'cartas/11D.png', ('D', 12): 'cartas/12D.png', ('D', 13): 'cartas/13D.png',
             ('C', 1):  'cartas/1C.png',  ('C', 2):  'cartas/2C.png',  ('C', 3):  'cartas/3C.png',
             ('C', 4):  'cartas/4C.png',  ('C', 5):  'cartas/5C.png',  ('C', 6):  'cartas/6C.png',
             ('C', 7):  'cartas/7C.png',  ('C', 8):  'cartas/8C.png',  ('C', 9):  'cartas/9C.png',
             ('C', 10): 'cartas/10C.png', ('C', 11): 'cartas/11C.png', ('C', 12): 'cartas/12C.png',
             ('C', 13): 'cartas/13C.png'}

# sound dictionary with all the sounds and their respective values
sounds_dict = {'hit': 'sonidos/hit.wav', 'stand': 'sonidos/stand.wav', 'win_player': 'sonidos/win_player.wav',
               'blackjack': 'sonidos/blackjack.wav', 'win_dealer': 'sonidos/win_dealer.wav',
               'confirm': 'sonidos/confirm.wav', 'card_around': 'sonidos/card_around.wav',
               'card_place': 'sonidos/card_place.wav', 'shuffle': 'sonidos/shuffle.wav'}


# SPLASH SCREEN ASKS PLAYER NAME
def initialize_game():
    # GREETING WINDOW
    root = tk.Tk()
    root.resizable(False, False)
    root.overrideredirect(True)
    root.config(relief="flat", bd=0)
    root.attributes("-topmost", True)
    w = 400
    h = 600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # SET BACKGROUND IMAGE
    bg = tk.PhotoImage(file="img/cover.png")
    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.create_image(0, 0, image=bg, anchor="nw")

    # create greeting text
    canvas.create_text(100, 420, text="NOMBRE:", fill="white", font=("Monoid", 12, "bold"),
                       justify="center")

    # create entry
    entry = tk.Entry(root, width=15, font=("Monoid", 16), justify="center", bd=2, bg="#000000", fg="white")
    entry.insert(0, "Anónimo")
    entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))
    entry.place(x=100, y=435)

    # create button
    button = tk.Button(root, text="EMPEZAR", font=("Monoid", 14, "bold"), command=lambda: get_data(), bd=2, bg="#000000", fg="white")
    button.place(x=145, y=485)

    # ASK FOR PLAYER NAME AND CLOSE WINDOW, THEN START GAME
    def get_data():
        global player_name

        # get player name from entry. If empty, set to 'Anónimo'. If too long, set to first 10 characters.
        # Make it uppercase and remove trailing spaces
        player_name = (entry.get().upper()[:10]).strip()

        if player_name == "":
            player_name = "ANÓNIMO"

        root.destroy()

        main_window()

    root.mainloop()


# I know the Cognitive Complexity is high, but I don't want to change it at this moment in time
# MAIN WINDOW
def main_window():
    global dealer_score
    global player_score
    global dealer_points_show
    global player_points_show
    global center_text
    global player_name
    global back
    global spot
    global deck_dict
    global deck_play
    global hit_try_player
    global player_hand
    global dealer_hand
    global player_score_total
    global dealer_score_total
    global muted

    # CREATE WINDOW
    root = tk.Tk()
    root.title(f"BLACKJACK! {' '*10} || Puntaje: {dealer_score_total} - {player_score_total} || {' '*10} Hola {player_name.capitalize()}!")
    root.resizable(False, False)
    root.config(relief="flat", bd=0)
    root.attributes("-topmost", True)
    w = 800
    h = 700
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # kill pid on window close
    root.protocol("WM_DELETE_WINDOW", lambda: kill_pid())  # Kill pid on window close

    # Kill pid function
    def kill_pid():
        global pid
        kill(pid, SIGTERM)
        root.destroy()

    # SET ICON
    icon = tk.PhotoImage(file='img/icon.png')
    root.wm_iconphoto(False, icon)

    # SET BACKGROUND IMAGE
    bg = tk.PhotoImage(file="img/bg.png")
    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.create_image(0, 0, image=bg, anchor="nw")

    # FIXED DECORATORS AND OUTPUTS
    # black rectangles for dealer and player round scores
    canvas.create_rectangle(20, 260, 120, 335, fill="#000000", outline="blue", width=2)
    canvas.create_rectangle(680, 260, 780, 335, fill="#000000", outline="blue", width=2)

    # dealer and player names in front of their respective hands
    canvas.create_text(70, 350, text="DEALER", fill="red", font=("Arial", 14, "bold"), justify="center")
    canvas.create_text(730, 350, text=player_name, fill="lime", font=("Arial", 14, "bold"), justify="center")

    # dealer and player names under round scores
    canvas.create_text(400, 15, text="DEALER", fill="red", font=("Monoid", 14, "bold"), justify="center")
    canvas.create_text(400, 590, text=player_name, fill="lime", font=("Monoid", 14, "bold"), justify="center")

    # dealer and player round scores values
    dealer_points_show = canvas.create_text(70, 300, text=dealer_score, fill="red", font=("Monoid", 48),
                                            justify="center")
    player_points_show = canvas.create_text(730, 300, text=player_score, fill="lime", font=("Monoid", 48),
                                            justify="center")

    # black rectangle for dealer and player total scores
    canvas.create_rectangle(580, 620, 740, 688, fill="#000000", outline="pink", width=2)

    # division in said rectangle
    canvas.create_line(665, 620, 665, 688, fill="pink", width=2)

    # dealer and player total scores values
    dealer_score_total_w = canvas.create_text(620, 655, text=dealer_score_total, fill="red", font=("Monoid", 42, "bold"), justify="left")
    player_score_total_w = canvas.create_text(700, 655, text=player_score_total, fill="lime", font=("Monoid", 42, "bold"), justify="right")

    # build number
    canvas.create_text(20, 13, text=f"{version}v", fill="gray", font=("Console", 11, "bold"), justify="center")

    # CREATE IMAGES
    spot = tk.PhotoImage(file='img/spot.png')  # placeholder spot for cards image
    back = tk.PhotoImage(file='img/back.png')  # back of cards image

    # ADD PLACEHOLDER IN THE 10 CARD SPOTS
    dealer_card1 = canvas.create_image(121, 130, image=spot, anchor="center")
    dealer_card2 = canvas.create_image(261, 130, image=spot, anchor="center")
    dealer_card3 = canvas.create_image(398, 130, image=spot, anchor="center")
    dealer_card4 = canvas.create_image(538, 130, image=spot, anchor="center")
    dealer_card5 = canvas.create_image(676, 130, image=spot, anchor="center")

    player_card1 = canvas.create_image(121, 465, image=spot, anchor="center")
    player_card2 = canvas.create_image(261, 465, image=spot, anchor="center")
    player_card3 = canvas.create_image(398, 465, image=spot, anchor="center")
    player_card4 = canvas.create_image(538, 465, image=spot, anchor="center")
    player_card5 = canvas.create_image(676, 465, image=spot, anchor="center")

    # blackjack image for when player gets blackjack. It's hidden by default
    blackjack_img = tk.PhotoImage(file="img/blackjack.png")
    blackjack_splash = canvas.create_image(400, 300, image=blackjack_img, anchor="center", state='hidden')

    # mute button image states
    muted_img = tk.PhotoImage(file="img/muted.png")
    unmuted_img = tk.PhotoImage(file="img/unmuted.png")

    # mute button itself
    mute_button = tk.Button(root, image=unmuted_img, command=lambda: Thread(target=lambda: toggle_mute()).start(),
                            borderwidth=0, highlightthickness=0, bg="#000000", activebackground="#000000")
    mute_button.place(x=750, y=13)

    # toggle mute function
    def toggle_mute():
        global muted

        if muted:
            muted = False
            mute_button.config(image=unmuted_img)
            root.update()

        else:
            muted = True
            mute_button.config(image=muted_img)
            root.update()

    # center button
    center_button = tk.Button(root, text="JUGAR", font=("Monoid", 14, "bold"),
                              command=lambda: [(center_button.config(text="JUGAR", state="disabled")),
                                               (root.update()),
                                               (Thread(asyncio.run(start_game())).start())],
                              bg="#000000", fg="lime", bd=0, justify="center", anchor="center")
    center_button.place(x=300, y=630, width=200, height=50)

    # center text for updates and win/lose messages
    center_text = canvas.create_text(400, 355, text="", fill="black", font=("Monoid", 20, "bold"),
                                     justify="center")

    # hit button
    hit_button = tk.Button(root, text="HIT", font=("Monoid", 14, "bold"), bg="#000000", fg="cyan", bd=0,
                           justify="center", anchor="center", state="disabled", cursor="hand2")
    hit_button.place(x=30, y=635, width=100, height=40)

    # stand button
    stand_button = tk.Button(root, text="STAND", font=("Monoid", 14, "bold"), bg="#000000", fg="cyan", bd=0,
                             justify="center", anchor="center", state="disabled", cursor="hand2")
    stand_button.place(x=150, y=635, width=100, height=40)

    # run this function when the program starts so as to associate the images themselves to their respective cards
    for key, value in deck_dict.items():
        deck_dict[key] = tk.PhotoImage(file=value)

    # hit button command to run when clicked
    hit_button.config(command=lambda: hit_stand_press('hit'))

    # stand button command to run when clicked
    stand_button.config(command=lambda: hit_stand_press('stand'))

    # start game runs asyncronously to start a new round
    async def start_game():
        global turn

        # the wait statements in the function are to make the game feel more natural and fake
        # the time it takes to deal the cards and the time it takes to show the dealer's first card

        asyncio.create_task(play_sound_if('confirm'))  # these are sound calls to play sounds

        # button updates to show status of game
        center_button.config(text="Preparando...", state="disabled")
        root.update()  # these are called a lot to update the gui
        await restart_board()  # restarts the board to prepare for a new round
        root.update()
        await asyncio.sleep(1)  # these tell the async function to wait for a certain amount of time before continuing

        center_button.config(text="Mezclando...", state="disabled")
        root.update()
        await populate_deck_play()  # populates the deck with cards
        root.update()
        await asyncio.sleep(1)

        center_button.config(text="Repartiendo...", state="disabled")
        root.update()
        await asyncio.sleep(.3)
        await populate_player_hand()  # populates the player's hand with ALL 5 cards
        await populate_dealer_hand()  # populates the dealer's hand with ALL 5 cards
        root.update()

        await deal_cards()  # deals the cards to the player and dealer respectively
        root.update()

        await asyncio.sleep(.2)

        center_button.config(text="Contando...", state="disabled")
        root.update()
        await asyncio.sleep(.5)
        await count_points_player()  # counts the points of the player's hand (2 cards at this point)
        await count_points_dealer()  # counts the points of the dealer's hand (2 cards at this point)
        root.update()

        proceed = await calculate_outcome()  # calculates the outcome of the round and how to proceed
        root.update()

        # check if the game is over already. If not then make the hit and stand buttons clickable
        player_continues = await hit_stand_check(proceed)
        root.update()

        dealer_continues = False  # this is set to false by default. It will be changed to true if the dealer has to hit

        # if game continues, enter a loop to allow the player to hit or stand as long as they don't bust, and
        # they don't stand or have hit 4 times already which is the max amount of hits allowed in this game.
        while player_continues:
            hit_confirmed = await hit_stand()  # this is a function that waits for the player to hit or stand

            if hit_confirmed:  # if the player hits, then run here
                await player_hit()  # this function runs the hit animation and adds the card to the player's hand
                root.update()

                await asyncio.sleep(.2)

                proceed = await calculate_outcome()  # calculate the outcome of the round
                root.update()

                player_continues = await hit_stand_check(proceed)  # check if the player can continue hitting or not
                root.update()

            else:  # if the player stands, then run here
                player_continues = False
                dealer_continues = True

            if hit_try_player == 4:  # if the player has hit 4 times, then run here to end the player's turn
                player_continues = False
                dealer_continues = True

        turn = 'dealer'  # set the turn to the dealer's turn

        # change the main button to show status. dealer's turn
        center_button.config(text="Dealer...", state="disabled")

        # if the player has not busted and the player has not gotten blackjack, then the dealer will hit
        while dealer_continues:  # this loop is the same as the player's loop, but for the dealer (which is simpler)
            proceed = await calculate_outcome()  # calculate the outcome of the round
            root.update()

            if proceed == "continue":  # if the dealer can continue, then run here
                await dealer_hit()  # this function runs the hit animation and adds the card to the dealer's hand
                root.update()

                await asyncio.sleep(.2)  # wait for a bit

            else:  # if the dealer can't continue, then run here to end the dealer's turn
                dealer_continues = False

        if proceed != "continue":  # if the dealer can't continue, then run here to end the dealer's turn
            # change the main button to allow the player to play again
            center_button.config(text="OTRA VEZ", state="normal", fg="#E845FF")

        root.update()  # update the gui

    # this function is called when the player clicks the hit or stand button
    def hit_stand_press(what_to_do):
        global wait_hit_stand

        wait_hit_stand = what_to_do  # this is a global variable that is used to tell the hit_stand function what to do

    # this function is called when the player clicks the hit button
    async def dealer_hit():  # this function is called when the dealer hits
        global hit_try_dealer
        global dealer_score
        global turn

        asyncio.create_task(play_sound_if('hit'))  # play the hit sound

        await asyncio.sleep(.5)

        turn = "dealer"  # set the turn to the dealer's turn just in case
        hit_try_dealer += 1  # add 1 to the dealer's hit counter

        await deal_cards()  # deal the card to the dealer
        await count_points_dealer()  # count the points of the dealer's hand

    # this function is called when the player clicks the hit button
    async def player_hit():
        global wait_hit_stand
        global hit_try_player
        global turn

        asyncio.create_task(play_sound_if('hit'))  # play the hit sound

        await asyncio.sleep(.5)

        turn = "player"  # set the turn to the player's turn just in case
        hit_try_player += 1  # add 1 to the player's hit counter
        wait_hit_stand = 'wait'  # set the wait_hit_stand variable to wait so the hit_stand function knows to wait

        await deal_cards()  # deal the card to the player
        await count_points_player()  # count the points of the player's hand

    # this function checks if the player can continue hitting or not
    async def hit_stand_check(proceed):
        global player_name
        global hit_try_player

        # if the player has not busted and the player has not gotten blackjack.
        # this if the player has not hit 4 times already, then the player can continue hitting
        if proceed == 'continue' and hit_try_player < 4:
            center_button.config(text="¿HIT o STAND?", state="disabled")

            # enable the hit and stand buttons
            hit_button.config(state="normal")
            stand_button.config(state="normal")

            return True  # return true to continue the loop

        else:

            asyncio.create_task(play_sound_if('stand'))  # play the stand sound

            await asyncio.sleep(.5)

            return False  # return false to end the loop

    # this function waits in a loop for the player to hit or stand
    async def hit_stand():
        global wait_hit_stand

        # run in a loop until the player hits or stands
        while True:
            if wait_hit_stand == 'hit':  # if the player hits, then run here
                # set the wait_hit_stand variable to wait so the hit_stand function knows to wait
                wait_hit_stand = 'wait'

                # disable the hit and stand buttons
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")

                return True  # return true to continue the loop

            elif wait_hit_stand == 'stand':  # if the player stands, then run here
                # set the wait_hit_stand variable to wait so the hit_stand function knows to wait
                wait_hit_stand = 'wait'

                # disable the hit and stand buttons
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")

                return False  # return false to end the loop

            else:  # if the player has not hit or stood, then run here to wait for a bit
                await asyncio.sleep(0.2)
                root.update()

    # this function calculates the outcome of the round and returns a string to tell the program what to do next
    async def calculate_outcome():
        global player_score
        global dealer_score
        global player_score_total
        global dealer_score_total
        global hit_try_dealer
        global hit_try_player
        global turn

        # if anybody has blackjack, then run here
        if player_score == 21 or dealer_score == 21:
            if player_score == 21 and dealer_score != 21:  # if the player has blackjack, then run here
                await blackjack_toast()  # show the blackjack toast celebration

            # if both the player and the dealer have blackjack, then run here
            if player_score == 21 and dealer_score == 21:
                await draw_toast()  # show the draw toast celebration

                # draw means they both get a point
                player_score_total += 1
                dealer_score_total += 1

                # update the score labels
                canvas.itemconfig(player_score_total_w, text=player_score_total)
                canvas.itemconfig(dealer_score_total_w, text=dealer_score_total)

                asyncio.create_task(play_sound_if('win_dealer'))  # play the dealer win sound as a draw alternative

                return 'draw'  # return draw to end the round

            # if the player has blackjack, then run here
            elif player_score == 21:
                # the player win toast is not player because the blackjack toast is being player already.

                # the player gets a point
                player_score_total += 1

                # update the score label
                canvas.itemconfig(player_score_total_w, text=player_score_total)

                # do not run the player win sound here as the blackjack sound is already being played.

                return 'player'  # return player to end the round

            # if the dealer has blackjack, then run here
            elif dealer_score == 21:
                await dealer_win_toast()  # show the dealer win toast

                # the dealer gets a point
                dealer_score_total += 1

                # update the score label
                canvas.itemconfig(dealer_score_total_w, text=dealer_score_total)

                asyncio.create_task(play_sound_if('win_dealer'))  # play the dealer win sound

                return 'dealer'  # return dealer to end the round

        # if the player and dealer have busted, then run here (this is impossible, but just in case)
        if player_score > 21 and dealer_score > 21:
            await draw_toast()  # show the draw toast celebration

            # draw means they both get a point
            player_score_total += 1
            dealer_score_total += 1

            # update the score labels
            canvas.itemconfig(player_score_total_w, text=player_score_total)
            canvas.itemconfig(dealer_score_total_w, text=dealer_score_total)

            asyncio.create_task(play_sound_if('win_dealer'))  # play the dealer win sound as a draw alternative

            return 'draw'  # return draw to end the round

        # if the player has busted and the dealer hasn't, then run here
        elif player_score > 21 and dealer_score <= 21:
            await dealer_win_toast()  # show the dealer win toast

            # the dealer gets a point
            dealer_score_total += 1

            # update the score label
            canvas.itemconfig(dealer_score_total_w, text=dealer_score_total)

            asyncio.create_task(play_sound_if('win_dealer'))  # play the dealer win sound

            return 'dealer'  # return dealer to end the round

        # if the dealer has busted and the player hasn't, then run here first
        elif player_score <= 21 and dealer_score > 21:
            await player_win_toast()  # show the player win toast

            # the player gets a point
            player_score_total += 1

            # update the score label
            canvas.itemconfig(player_score_total_w, text=player_score_total)

            asyncio.create_task(play_sound_if('win_player'))  # play the player win sound

            return 'player'  # return player to end the round

        # IN THE DEALER'S TURN
        # if the player and dealer has beaten the player, then run here (dealer bust is in the previous if statement)
        if turn == 'dealer' and dealer_score > player_score:
            await dealer_win_toast()  # show the dealer win toast

            # the dealer gets a point
            dealer_score_total += 1

            # update the score label
            canvas.itemconfig(dealer_score_total_w, text=dealer_score_total)

            asyncio.create_task(play_sound_if('win_dealer'))  # play the dealer win sound

            return 'dealer'  # return dealer to end the round

        # if the player has beaten the dealer, then run here
        elif turn == 'dealer' and dealer_score == player_score:
            await draw_toast()  # show the draw toast celebration

            # draw means they both get a point
            player_score_total += 1
            dealer_score_total += 1

            # update the score labels
            canvas.itemconfig(player_score_total_w, text=player_score_total)
            canvas.itemconfig(dealer_score_total_w, text=dealer_score_total)

            asyncio.create_task(play_sound_if('win_dealer'))  # play the dealer win sound as a draw alternative

            return 'draw'  # return draw to end the round

        # if the player has beaten the dealer, then run here. (dealer is out of hit tries)
        elif turn == 'dealer' and hit_try_dealer == 5 and dealer_score < player_score:
            await player_win_toast()  # show the player win toast

            # the player gets a point
            player_score_total += 1

            # update the score label
            canvas.itemconfig(player_score_total_w, text=player_score_total)

            asyncio.create_task(play_sound_if('win_player'))  # play the player win sound

            return 'player'  # return player to end the round

        # if nobody won yet, then run here. hit tries are not 5 yet if this runs.
        if player_score < 21 and dealer_score < 21:
            return 'continue'  # return continue to continue the round

    # this function is called when there is a draw. it just changes the center label to draw.
    # the idea is to maybe add a draw animation here in the future if i have time.
    async def draw_toast():
        canvas.itemconfig(center_text, text="EMPATE")

    # this function is called when the player wins. it just changes the center label to player win.
    # the idea is to maybe add a player win animation here in the future if i have time.
    async def player_win_toast():
        canvas.itemconfig(center_text, text=f"{player_name} GANA")

    # this function is called when the dealer wins. it just changes the center label to dealer win.
    # the idea is to maybe add a dealer win animation here in the future if i have time.
    async def dealer_win_toast():
        canvas.itemconfig(center_text, text="DEALER GANA")

    # this function animates the deal itself. all the possibilities are covered here.
    async def deal_cards():
        global hit_try_dealer
        global hit_try_player
        global turn
        global muted

        # if the player has blackjack, then run here
        if hit_try_player == 1 and hit_try_dealer == 1:
            canvas.itemconfig(dealer_card1, image=back)  # deal first dealer card face down
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

            await asyncio.sleep(.4)  # wait a bit

            canvas.itemconfig(dealer_card2, image=back)  # deal second dealer card face down
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

            await asyncio.sleep(.4)  # wait a bit

            canvas.itemconfig(player_card1, image=back)  # deal first player card face down
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

            await asyncio.sleep(.4)  # wait a bit

            canvas.itemconfig(player_card2, image=back)  # deal second player card face down
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

            await asyncio.sleep(.8)  # wait a bit

            canvas.itemconfig(dealer_card1, image=deck_dict[dealer_hand[0]])  # flip the first dealer card
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

            await asyncio.sleep(.5)  # wait a bit

            canvas.itemconfig(dealer_card2, image=deck_dict[dealer_hand[1]])  # flip the second dealer card
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

            await asyncio.sleep(.6)  # wait a bit

            canvas.itemconfig(player_card1, image=deck_dict[player_hand[0]])  # flip the first player card
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

            await asyncio.sleep(.5)  # wait a bit

            canvas.itemconfig(player_card2, image=deck_dict[player_hand[1]])  # flip the second player card
            root.update()  # update the canvas

            asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

            await asyncio.sleep(.2)  # wait a bit

            return  # return to end the function if this runs as it marks the end of the first deal

        # if it's the player's turn, then run here
        if turn == 'player':
            if hit_try_player == 2:  # if it's the second hit, then run here. first one is already dealt at the start
                canvas.itemconfig(player_card3, image=back)  # deal the third player card face down
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

                await asyncio.sleep(.8)  # wait a bit

                canvas.itemconfig(player_card3, image=deck_dict[player_hand[2]])  # flip the third player card
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

                await asyncio.sleep(.5)  # wait a bit

            # if it's the third hit, then run here.
            elif hit_try_player == 3:
                canvas.itemconfig(player_card4, image=back)  # deal the fourth player card face down
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

                await asyncio.sleep(.8)  # wait a bit

                canvas.itemconfig(player_card4, image=deck_dict[player_hand[3]])  # flip the fourth player card
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

                await asyncio.sleep(.5)  # wait a bit

            # if it's the fourth hit, then run here.
            elif hit_try_player == 4:
                canvas.itemconfig(player_card5, image=back)  # deal the fifth player card face down
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

                await asyncio.sleep(.8)  # wait a bit

                canvas.itemconfig(player_card5, image=deck_dict[player_hand[4]])  # flip the fifth player card
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

                await asyncio.sleep(.5)  # wait a bit

        # if it's the dealer's turn, then run here
        elif turn == 'dealer':
            if hit_try_dealer == 2:  # if it's the second hit, then run here. first one is already dealt at the start
                canvas.itemconfig(dealer_card3, image=back)  # deal the third dealer card face down
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

                await asyncio.sleep(.8)  # wait a bit

                canvas.itemconfig(dealer_card3, image=deck_dict[dealer_hand[2]])  # flip the third dealer card
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

                await asyncio.sleep(.5)  # wait a bit

            # if it's the third hit, then run here.
            elif hit_try_dealer == 3:
                canvas.itemconfig(dealer_card4, image=back)  # deal the fourth dealer card face down
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

                await asyncio.sleep(.8)  # wait a bit

                canvas.itemconfig(dealer_card4, image=deck_dict[dealer_hand[3]])  # flip the fourth dealer card
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

                await asyncio.sleep(.5)  # wait a bit

            # if it's the fourth hit, then run here.
            elif hit_try_dealer == 4:
                canvas.itemconfig(dealer_card5, image=back)  # deal the fifth dealer card face down
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_place'))  # play the card place sound

                await asyncio.sleep(.8)  # wait a bit

                canvas.itemconfig(dealer_card5, image=deck_dict[dealer_hand[4]])  # flip the fifth dealer card
                root.update()  # update the canvas

                asyncio.create_task(play_sound_if('card_around'))  # play the card turn around sound

                await asyncio.sleep(.5)  # wait a bit

    # this function is used to make the deck from scratch at the start of the game
    async def populate_deck_play():
        global deck_play
        global suits

        asyncio.create_task(play_sound_if('shuffle'))  # play the shuffle sound

        deck_play = []  # clear the deck_play list
        for this_value in range(1, 13):  # loop through the values
            for suit in suits:  # loop through the suits
                deck_play.append((suit, this_value))  # add the card to the deck_play list

    # this function is used to deal the 5 cards to the player at the start of the game
    async def populate_player_hand():
        global player_hand
        global deck_play

        player_hand = []  # clear the player's hand
        for i in range(5):  # loop through 5 times
            await shuffle_deck()  # shuffle the deck before dealing every time it loops
            player_hand.append(deck_play.pop(i))  # add the card to the player's hand

    # this function is used to deal the 5 cards to the dealer at the start of the game
    async def populate_dealer_hand():
        global dealer_hand
        global deck_play

        dealer_hand = []  # clear the dealer's hand
        for i in range(5):  # loop through 5 times
            await shuffle_deck()  # shuffle the deck before dealing every time it loops
            dealer_hand.append(deck_play.pop(i))  # add the card to the dealer's hand

    # this function is used to count the player's hand per turn. it's used to determine the value of the hand
    async def count_points_player():
        global player_hand
        global player_score
        global hit_try_player

        cards_to_calculate = hit_try_player + 1  # this is used to determine how many cards to calculate

        # aces can take values of 1 and 11. this is used to determine if the player has an ace in their hand
        # and if so, then the value of the ace will be determined
        if cards_to_calculate == 2:  # if it's the first two cards, then run here
            if player_hand[0][1] == 1:  # if the first card is an ace, then run here
                if player_score + 11 > 21:  # if the score plus 11 is greater than 21, then run here
                    player_score += 1  # add 1 to the score
                else:  # if the score plus 11 is less than or equal to 21, then run here
                    player_score += 11  # add 11 to the score
            elif player_hand[0][1] > 10:  # if the first card is a face card, then run here
                player_score += 10  # add 10 to the score
            else:  # if the first card is a number card, then run here
                player_score += player_hand[0][1]  # add the value of the card to the score

            # this does the same for the second card
            if player_hand[1][1] == 1:
                if player_score + 11 > 21:
                    player_score += 1
                else:
                    player_score += 11
            elif player_hand[1][1] > 10:
                player_score += 10
            else:
                player_score += player_hand[1][1]

        # this does the same for the third card
        elif cards_to_calculate == 3:
            if player_hand[2][1] == 1:
                if player_score + 11 > 21:
                    player_score += 1
                else:
                    player_score += 11
            elif player_hand[2][1] > 10:
                player_score += 10
            else:
                player_score += player_hand[2][1]

        # this does the same for the fourth card
        elif cards_to_calculate == 4:
            if player_hand[3][1] == 1:
                if player_score + 11 > 21:
                    player_score += 1
                else:
                    player_score += 11
            elif player_hand[3][1] > 10:
                player_score += 10
            else:
                player_score += player_hand[3][1]

        # this does the same for the fifth card
        elif cards_to_calculate == 5:
            if player_hand[4][1] == 1:
                if player_score + 11 > 21:
                    player_score += 1
                else:
                    player_score += 11
            elif player_hand[4][1] > 10:
                player_score += 10
            else:
                player_score += player_hand[4][1]

        # this updates the player score of the round
        canvas.itemconfig(player_points_show, text=player_score)

    # this function is used to count the dealer's hand per turn. it's used to determine the value of the hand
    # it's similar to the player's hand
    async def count_points_dealer():
        global dealer_hand
        global dealer_score
        global hit_try_dealer

        cards_to_calculate = hit_try_dealer + 1

        if cards_to_calculate == 2:
            if dealer_hand[0][1] == 1:
                if dealer_score + 11 > 21:
                    dealer_score += 1
                else:
                    dealer_score += 11
            elif dealer_hand[0][1] > 10:
                dealer_score += 10
            else:
                dealer_score += dealer_hand[0][1]

            if dealer_hand[1][1] == 1:
                if dealer_score + 11 > 21:
                    dealer_score += 1
                else:
                    dealer_score += 11
            elif dealer_hand[1][1] > 10:
                dealer_score += 10
            else:
                dealer_score += dealer_hand[1][1]

        elif cards_to_calculate == 3:
            if dealer_hand[2][1] == 1:
                if dealer_score + 11 > 21:
                    dealer_score += 1
                else:
                    dealer_score += 11
            elif dealer_hand[2][1] > 10:
                dealer_score += 10
            else:
                dealer_score += dealer_hand[2][1]

        elif cards_to_calculate == 4:
            if dealer_hand[3][1] == 1:
                if dealer_score + 11 > 21:
                    dealer_score += 1
                else:
                    dealer_score += 11
            elif dealer_hand[3][1] > 10:
                dealer_score += 10
            else:
                dealer_score += dealer_hand[3][1]

        elif cards_to_calculate == 5:
            if dealer_hand[4][1] == 1:
                if dealer_score + 11 > 21:
                    dealer_score += 1
                else:
                    dealer_score += 11
            elif dealer_hand[4][1] > 10:
                dealer_score += 10
            else:
                dealer_score += dealer_hand[4][1]

        canvas.itemconfig(dealer_points_show, text=dealer_score)

    # this function is used to shuffle the deck using the random module
    async def shuffle_deck():
        global deck_play

        shuffle(deck_play)

    # BLACKJACK TOAST
    async def blackjack_toast():
        asyncio.create_task(play_sound_if('blackjack'))  # play the blackjack sound
        canvas.itemconfig(blackjack_splash, state='normal')  # show the blackjack splash
        root.update()  # update the root

        await asyncio.sleep(2)  # wait 2 seconds

        canvas.itemconfig(blackjack_splash, state='hidden')  # hide the blackjack splash again
        root.update()  # update the root

    # this function is used to restart the board after a round
    async def restart_board():
        global dealer_score
        global player_score
        global player_hand
        global dealer_hand
        global hit_try_player
        global hit_try_dealer
        global deck_play
        global turn
        global wait_hit_stand

        # Score resets, turn resets. the player and dealer hands are cleared.
        dealer_score = 0
        player_score = 0
        player_hand = []
        dealer_hand = []
        hit_try_player = 1
        hit_try_dealer = 1
        deck_play = []
        turn = 'player'
        wait_hit_stand = 'wait'

        # set placeholder again for all cards
        canvas.itemconfig(dealer_card1, image=spot)
        canvas.itemconfig(dealer_card2, image=spot)
        canvas.itemconfig(dealer_card3, image=spot)
        canvas.itemconfig(dealer_card4, image=spot)
        canvas.itemconfig(dealer_card5, image=spot)

        canvas.itemconfig(player_card1, image=spot)
        canvas.itemconfig(player_card2, image=spot)
        canvas.itemconfig(player_card3, image=spot)
        canvas.itemconfig(player_card4, image=spot)
        canvas.itemconfig(player_card5, image=spot)

        # hide the dealer's second card
        canvas.itemconfig(center_text, text="", fill="black")

        # disable the hit and stand buttons again
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")

        # update both round scores to 0
        canvas.itemconfig(player_points_show, text=player_score)
        canvas.itemconfig(dealer_points_show, text=dealer_score)

        # if total scores are too big to fit in the scoreboard, make them smaller
        if dealer_score_total > 99:
            canvas.itemconfig(dealer_points_show, font=("Arial", 32))
        elif player_score_total > 99:
            canvas.itemconfig(player_points_show, font=("Arial", 32))

        # update the title with new values
        root.title(f"BLACKJACK! {' ' * 26} GIRTIM™ {' ' * 42} || Puntaje: {dealer_score_total} - {player_score_total} || {' ' * 30} Hola {player_name.capitalize()}!")

        root.update() # update the root

    # this function is used to play sounds in threads so as to not stop the main loop
    async def play_sound_if(sound):
        global muted
        global sounds_dict

        if not muted:
            Thread(target=lambda: playsound(sounds_dict.get(sound))).start()

    # this function updates the window evert 300ms. It sometimes gets stuck in my experience so I set some manually
    def update():

        root.update()

        root.after(300, update)

    root.after(1000, update)

    root.mainloop()


# run the script from here
if __name__ == "__main__":
    initialize_game()  # initialize the game


# EOF
