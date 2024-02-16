import pygame, csv, os, random

# Set working directory to the location of this .py file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

##########
# Appearances
##########
window_width = 700
window_height = 450

rose = '#F0E1DE'
scallop = '#F7C9B6'
grotto = '#549BAD'
midnight = '#0C6170'
bluegreen = '#37BEB0'
tiffany = '#83BDC0'
baby = '#DBF5F0'

##########
# Get materials
##########
with open('assets/chengyu-list.csv', 'r', encoding='utf-8') as chengyu_input:
    readcy = csv.reader(chengyu_input)
    # This list is already ordered by frequency though
    chengyu_list = [row[0] for row in readcy]
    # But let's get a frequency dict anyway, key = chengyu, value = frequency (num per million)
    chengyu_input.seek(0)
    chengyu_frequency = {}
    for row in readcy:
        chengyu_frequency[row[0]] = row[1]

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
        self.text_surf = button_font.render(text,True,'#FFFFFF')
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

# onclickfunction for the start button
def start():
    global started
    wipe()
    started = True
    init_game()

# initialise a game of 20 trials
def init_game():
    global trial_count, correct_count, chengyus
    trial_count = 0
    correct_count = 0
    chengyus = []
    init_trial()

# initialise a trial
def init_trial():
    global trial_count, chengyu, chengyus, selected, current_location, text_font, last_chengyu_freq
    wipe()
    match trial_count:
        case 0:
            # if the first trial in a game, randomly select a chengyu that's relatively easy
            chengyu = random.choice(chengyu_list[:141])
            chengyus.append(chengyu)
            last_chengyu_freq = chengyu_frequency[chengyu]
        case _:
            # otherwise select a chengyu that's more difficult than the previous one
            while chengyu_frequency:
                random_chengyu = random.choice(chengyu_list)
                random_freq = chengyu_frequency.pop(random_chengyu)
                # check if the frequency of randomly poped chengyu is smaller than or equal to the last frequency
                # and check if it's not already appeared
                if random_freq <= last_chengyu_freq and random_chengyu not in chengyus:
                    # if so, get the item and break out of while
                    last_chengyu_freq = random_freq
                    chengyu = random_chengyu
                    chengyus.append(chengyu)
                    # put this back so that we don't run out in later games
                    chengyu_frequency[random_chengyu] = random_freq
                    break
                else:
                    # if the frequency is not smaller or equal, put the entry back to the dictionary
                    chengyu_frequency[random_chengyu] = random_freq
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
    option_buttons = [Button(option, 120, 90, (145+(rand_options.index(option)*290), 250), 3, select) for option in rand_options]

def get_candidate(chengyu, current_location):
    cur_char_rank = char_rank.index(chengyu[current_location])
    found = False
    # randomly select another option that matches the correct option in character frequency (rank +- 30?)
    candidate = random.choice(char_rank[max(cur_char_rank-30,0):min(cur_char_rank+30,len(char_rank)-1)])
    # check if identical
    if char_rank.index(candidate) == cur_char_rank:
        get_candidate(chengyu, current_location)
    else:
        # check if the other candidate makes sense in the chengyu
        found = any(chengyu[:current_location]+candidate in c for c in chengyu_list)
        if found:
            get_candidate(chengyu, current_location)
        else:
            return candidate

def select():
    global chengyu, current_location, rand_options, selected, correct_count
    global option_l_rect, option_r_rect
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
    global chengyu, current_location, selected, correct_count, trial_count
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
                message = text_font.render(selected[i], True, midnight)
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
    global chengyu, selected, text_font_small, trial_count
    trial_count += 1
    start_time = pygame.time.get_ticks()
    delay = 1000
    while True:
        current_time = pygame.time.get_ticks()
        # repeat what's done in main loop to prevent freezing
        for i in range(len(selected)):
            message = text_font.render(selected[i], True, midnight)
            screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
        # print wrong message
        correct = text_font_small.render('错误…', True, midnight)
        screen.blit(correct, correct.get_rect(center = (250, 65)))
        # print answer
        answer = list(chengyu)[len(selected):]
        for j in range(len(answer)):
            message = text_font.render(answer[j], True, tiffany)
            screen.blit(message, message.get_rect(center = (150+(50*(j+len(selected))), 150)))
        pygame.display.flip()
        if current_time - start_time >= delay:
            init_trial()
            break

##########
# Main game
##########
def main():
    global screen, icon, clock, button_font, text_font, text_font_small
    global started, selected, current_location, option_buttons, option_l_rect, option_r_rect
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('成语迷宫 Chengyu Maze')
    screen.fill(baby)
    text_font_small = pygame.font.Font('assets/MaShanZheng-Regular.ttf',28)
    text_font = pygame.font.Font('assets/MaShanZheng-Regular.ttf',50)
    button_font = pygame.font.Font('assets/MaShanZheng-Regular.ttf',40)

    # game variables
    started = False

    # buttons
    start_button = Button('开始', 120, 50, (290, 320), 3, start)
    restart_button = Button('再来一局', 180, 50, (260, 300), 3, start)
    option_l_rect = pygame.Rect(145, 250, 120, 90)
    option_r_rect = pygame.Rect(435, 250, 120, 90)

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if not started:
            message1 = text_font.render('欢迎来到成语迷宫!', True, midnight)
            message2 = text_font.render('Welcome to Chengyu Maze!', True, midnight)
            message3 = text_font_small.render('在两个选项当中选择能够组成成语的选项。', True, midnight)
            screen.blit(message1, message1.get_rect(center = (350, 85)))
            screen.blit(message2, message2.get_rect(center = (350, 145)))
            screen.blit(message3, message3.get_rect(center = (350, 220)))
            start_button.draw()
        elif trial_count == 20:
            wipe()
            message1 = text_font.render('游戏结束！', True, midnight)
            message2 = text_font_small.render('本局得分：'+str(correct_count)+'/20', True, midnight)
            screen.blit(message1, message1.get_rect(center = (350, 145)))
            screen.blit(message2, message2.get_rect(center = (350, 220)))
            restart_button.draw()
        else:
            for i in range(len(selected)):
                message = text_font.render(selected[i], True, midnight)
                screen.blit(message, message.get_rect(center = (150+(i*50), 150)))
            score = text_font_small.render('得分：'+str(correct_count)+'/20', True, midnight)
            screen.blit(score, score.get_rect(center = (550, 65)))
            for option in option_buttons:
                option.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()