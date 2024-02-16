import pygame, csv, os, random

##########
# Appearances
##########
window_width = 700
window_height = 450

midnight = '#0C6170'
bluegreen = '#37BEB0'
tiffany = '#83BDC0'
baby = '#DBF5F0'

##########
# Get materials
##########
with open('assets/chengyu-list.csv', 'r', encoding='utf-8') as chengyu_input:
    readcy = csv.reader(chengyu_input)
    contents = [row for row in readcy]
    # This list is already ordered by frequency high to low (i.e. difficulty low to high)
    chengyu_list = [row[0] for row in contents]
    chengyu_list_normal = [row[0] for row in contents if int(row[1])>0]
    chengyu_list_hard = [row[0] for row in contents if int(row[1])==0]

with open('assets/character-rank.csv', 'r', encoding='utf-8') as char_input:
    readchar = csv.reader(char_input)
    # get a list of all characters ranked by frequency highest to lowest
    char_rank = []
    for row in readchar:
        char_rank.append(row[1])

##########
# Classes
##########
# button code from:
# https://pythonprogramming.sssaltervista.org/buttons-in-pygame/?doing_wp_cron=1685564739.9689290523529052734375
class Button:
    def __init__(self,text,width,height,pos,elevation,onclickFunction=None):
        #Core attributes 
        self.pressed = False
        self.onclickFunction = onclickFunction
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = bluegreen

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = midnight
        #text
        self.text = text
        if (glyphInFont(text, button_font)):
            self.text_surf = button_font.render(text,True,'#FFFFFF')
        else:
            self.text_surf = button_font_tr.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = tiffany
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.onclickFunction()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = bluegreen

########
# Functions
########
# wipe screen
def wipe():
    pygame.draw.rect(screen, baby, pygame.Rect(0, 0, window_width, window_height))
    pygame.display.flip()

# onclickfunctions for the start button
def start():
    global started, hard, start_button, start_button_hard
    started = True
    hard = False
    wipe()
    init_game()

def start_hard():
    global started, hard
    started = True
    hard = True
    wipe()
    init_game()

# initialise a game of 20 trials
def init_game():
    global trial_count, correct_count, chengyus, reached_end
    wipe()
    trial_count = 0
    correct_count = 0
    reached_end = False
    chengyus = []
    init_trial()

# initialise a trial
def init_trial():
    global hard, trial_count, chengyu, chengyus, selected, current_location, last_chengyu_freq, reached_end
    wipe()
    match trial_count:
        case 0:
            # if the first trial in a game, randomly select a chengyu that's easy (more than 100 per million)
            # or if hard, randomly choose one from the hard list
            chengyu = random.choice(chengyu_list_hard if hard else chengyu_list_normal[:30])
            chengyus.append(chengyu)
            #last_chengyu_freq = int(chengyu_frequency[chengyu])
        case _:
            # hard mode, just randomly choose another hard entry
            if hard:
                chengyu_list_new = [item for item in chengyu_list_hard if item not in chengyus]
                random_chengyu = random.choice(chengyu_list_new)
                chengyu = random_chengyu
                chengyus.append(chengyu)
            # normal mode, choose a chengyu that's more difficult than the last one
            else:
                # in case we reached the last entry
                if reached_end:
                    # get a random one from the most difficult ones
                    chengyu_list_new = [item for item in chengyu_list if item not in chengyus]
                    random_chengyu = random.choice(chengyu_list_new[-50:])
                    chengyu = random_chengyu
                    chengyus.append(chengyu)
                # otherwise select a chengyu that's more difficult than the previous one
                else:
                    while True:
                        random_chengyu = random.choice(chengyu_list)
                        # check if the frequency of randomly selected chengyu is smaller than or equal to the last frequency and not to infrequent immediately
                        # and check if it's not already appeared
                        if chengyu_list.index(chengyu) < chengyu_list.index(random_chengyu) < chengyu_list.index(chengyu)+50 and random_chengyu not in chengyus:
                            # if so, get the item and break out of while
                            chengyu = random_chengyu
                            chengyus.append(chengyu)
                            # mark if the last entry is selected
                            if chengyu == chengyu_list[-1]:
                                reached_end = True
                            break
    # change variables
    selected = [chengyu[0]]
    current_location = 1
    get_options(current_location)

def get_options(current_location):
    global chengyu, rand_options, option_buttons
    # get correct option
    options = {}
    options[chengyu[current_location]] = 'y'
    options[get_candidate(chengyu, current_location)] = 'n'
    # scramble the order of correct/incorrect options and get button objects
    rand_options = list(options.keys())
    random.shuffle(rand_options)
    option_buttons = [Button(option, 120, 70, (145+(rand_options.index(option)*290), 250), 3, select) for option in rand_options]

def get_candidate(chengyu, current_location):
    try:
        cur_char_rank = char_rank.index(chengyu[current_location])
    # if the searched character is not in the list, just give it a to-the-end number
    except ValueError:
        cur_char_rank = 14900
    found = False
    # randomly select another option that matches the correct option in character frequency (rank +- 50?), except for the current index
    candidate = random.choice(char_rank[max(cur_char_rank-50,0):cur_char_rank] + char_rank[(cur_char_rank+1):min(cur_char_rank+50,len(char_rank)-1)])
    found = any(chengyu[:current_location]+candidate in c for c in chengyu_list)
    if found:
        return get_candidate(chengyu, current_location)
    return candidate

def select():
    mouse_pos = pygame.mouse.get_pos()
    # if left button clicked
    if option_l_rect.collidepoint(mouse_pos):
        # if correct
        if rand_options[0] == chengyu[current_location]:
            correct()
        # if wrong
        else:
            wrong()
    # if right button clicked
    elif option_r_rect.collidepoint(mouse_pos):
        # if correct
        if rand_options[1] == chengyu[current_location]:
            correct()
        # if wrong
        else:
            wrong()

def correct():
    global current_location, selected, correct_count, trial_count
    # if end of chengyu, start a new trial
    if current_location == 3:
        selected.append(chengyu[current_location])
        correct_count += 1
        trial_count += 1
        # initialise another trial after some time
        start_time = pygame.time.get_ticks()
        delay = 750
        while True:
            current_time = pygame.time.get_ticks()
            # repeat what's done in main loop to prevent freezing
            for i in range(len(selected)):
                if (glyphInFont(selected[i], text_font)):
                    message = text_font.render(selected[i], True, midnight)
                    screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
                else:
                    message = text_font_tr.render(selected[i], True, midnight)
                    screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
            # print correct message
            correct = text_font_small.render('恭喜！', True, midnight)
            screen.blit(correct, correct.get_rect(center = (250, 65)))
            pygame.display.flip()
            if current_time - start_time >= delay:
                init_trial()
                break
    else:
        selected.append(chengyu[current_location])
        pygame.display.flip()
        current_location += 1
        get_options(current_location)

def wrong():
    global trial_count
    trial_count += 1
    start_time = pygame.time.get_ticks()
    delay = 1000
    while True:
        current_time = pygame.time.get_ticks()
        # repeat what's done in main loop to prevent freezing
        for i in range(len(selected)):
            if (glyphInFont(selected[i], text_font)):
                message = text_font.render(selected[i], True, midnight)
                screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
            else:
                message = text_font_tr.render(selected[i], True, midnight)
                screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
        # print wrong message
        wrong = text_font_small.render('错误…', True, midnight)
        screen.blit(wrong, wrong.get_rect(center = (250, 65)))
        # print answer
        answer = list(chengyu)[len(selected):]
        for j in range(len(answer)):
            if (glyphInFont(answer[j], text_font)):
                message = text_font.render(answer[j], True, tiffany)
                screen.blit(message, message.get_rect(center = (150+(50*(j+len(selected))), 150)))
            else:
                message = text_font_tr.render(answer[j], True, tiffany)
                screen.blit(message, message.get_rect(center = (150+(50*(j+len(selected))), 150)))
        pygame.display.flip()
        if current_time - start_time >= delay:
            init_trial()
            break

# a function to check whether a symbol is supported by the main font, by: https://stackoverflow.com/a/64397652
def glyphInFont( glyph, font ):
    """ Given a glyph and a font, use a pixel-finding heuristic to determine
        if the glyph renders to something other than an "empty border" non-existant
        font symbol.  Returns True if it renders to something. """
    result = False
    WHITE  = ( 255, 255, 255 )   # can be any colour pair with constrast
    BLACK  = (   0,   0,   0 )
    try:
        text_image = font.render( glyph, True, WHITE, BLACK )
        text_rect  = text_image.get_rect()
        x_centre = text_rect.width // 2
        y_centre = text_rect.height // 2
        # On Linux at least, non-renderable glyphs have a border.
        # work out a 50% search box, centred inside the gluph
        box_top    = y_centre - ( text_rect.height // 4 )
        box_bottom = y_centre + ( text_rect.height // 4 )
        box_left   = x_centre - ( text_rect.width // 4 )
        box_right  = x_centre + ( text_rect.width // 4 )
        # Trace a Horizontal line through the middle of the bitmap 
        # looking for non-black pixels
        for x in range( box_left, box_right ):
            if ( text_image.get_at( ( x, y_centre ) ) != BLACK ):
                result = True
                break
        # If not found already, trace a line vertically
        if ( result == False ):
            for y in range( box_top, box_bottom ):
                if ( text_image.get_at( ( x_centre, y ) ) != BLACK ):
                    result = True
                    break
        # If still not found, check every pixel in the centre-box
        if ( result == False ):
            for y in range( box_top, box_bottom ):
                for x in range( box_left, box_right ):
                    if ( text_image.get_at( ( x, y ) ) != BLACK ):
                        result = True
                        break
    except UnicodeError as uce:
        # Glyph-ID not supported
        pass  # False goes through
    return result

##########
# Main game
##########
def main():
    global screen, icon, clock, button_font, text_font, text_font_small, button_font_tr, text_font_tr
    global started, hard, selected, current_location, option_buttons, option_l_rect, option_r_rect
    # Set working directory to the location of this .py file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('成语迷宫 Chengyu Maze')
    screen.fill(baby)
    text_font_small = pygame.font.Font('assets/zcool-yuyang-3.ttf',28)
    text_font = pygame.font.Font('assets/zcool-yuyang-3.ttf',50)
    text_font_tr = pygame.font.Font('assets/SimSun.ttf',50)
    button_font = pygame.font.Font('assets/zcool-yuyang-4.ttf',40)
    button_font_tr = pygame.font.Font('assets/SimSun.ttf',40)

    # game variables
    started = False
    hard = False

    # buttons
    start_button = Button('普通', 120, 50, (170, 330), 3, start)
    start_button_hard = Button('困难', 120, 50, (410, 330), 3, start_hard)
    option_l_rect = pygame.Rect(145, 250, 120, 90)
    option_r_rect = pygame.Rect(435, 250, 120, 90)

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if not started:
            message1 = text_font.render('欢迎来到成语迷宫!', True, midnight)
            message2 = text_font_small.render('Welcome to Chengyu Maze!', True, midnight)
            message3 = text_font_small.render('在两个选项当中选择能够组成成语的选项。', True, midnight)
            message4 = text_font_small.render('开始游戏：', True, midnight)
            screen.blit(message1, message1.get_rect(center = (350, 85)))
            screen.blit(message2, message2.get_rect(center = (350, 145)))
            screen.blit(message3, message3.get_rect(center = (350, 200)))
            screen.blit(message4, message4.get_rect(center = (350, 275)))
            start_button.draw()
            start_button_hard.draw()
        elif trial_count == 20:
            pygame.draw.rect(screen, baby, pygame.Rect(0, 0, window_width, window_height))
            message1 = text_font.render('游戏结束！', True, midnight)
            message2 = text_font_small.render('本局得分：'+str(correct_count)+'/20', True, midnight)
            message3 = text_font_small.render('再来一局：', True, midnight)
            screen.blit(message1, message1.get_rect(center = (350, 145)))
            screen.blit(message2, message2.get_rect(center = (350, 220)))
            screen.blit(message3, message3.get_rect(center = (350, 280)))
            start_button.draw()
            start_button_hard.draw()
        else:
            # hide the start buttons
            pygame.draw.rect(screen, baby, pygame.Rect(170, 325, 140, 60))
            pygame.draw.rect(screen, baby, pygame.Rect(410, 325, 140, 60))
            for i in range(len(selected)):
                if (glyphInFont(selected[i], text_font)):
                    message = text_font.render(selected[i], True, midnight)
                    screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
                else:
                    message = text_font_tr.render(selected[i], True, midnight)
                    screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
            score = text_font_small.render('得分：'+str(correct_count)+'/20', True, midnight)
            screen.blit(score, score.get_rect(center = (550, 65)))
            for option in option_buttons:
                option.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()