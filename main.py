#import kivy
from kivy.config import Config
#Config.set('graphics', 'width', '360')
#Config.set('graphics', 'height', '720')
Config.set('kivy', 'window_icon', 'static/knight32x32.png')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
#from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty, NumericProperty #BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from functools import partial
from copy import deepcopy
from chess import Chess
from config import odd_color, even_color, check_color, move_color, pm_color, gui_m, game_level, man_color, background
# from kivy.core.window import Window

class MainWindow(BoxLayout):
    pass

class WindowManager(ScreenManager):
    pass

class DashboardWindow(Screen):
    mycolor = StringProperty('W')
    mylevel = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_game(self):
        GameWindow.chessboard = deepcopy(Chess.board)
        GameWindow.castle = deepcopy(Chess.castle)
        GameWindow.turn = GameWindow.my_turn = self.mycolor
        GameWindow.my_promote_row, GameWindow.opp_promote_row, GameWindow.opp_turn = (0,7,'W') if self.mycolor=='B' else (7,0,'B')
        GameWindow.depth = game_level[self.mylevel]
        self.parent.current = "game_screen"
        # MyChessApp.WindowManager.current = 'game_screen'

class GameWindow(Screen):
    chessboard = castle = depth = turn = my_turn = opp_turn = my_promote_row = opp_promote_row = previous_position = None
    undo_list = []
    dead_list = []
    move_data = []
    moved_mark = []
    r_possible_moves = []
        
    def __init__(self, **kwargs):
        super().__init__()
        self.main = BoxLayout(orientation="vertical")
        self.add_widget(self.main)
        self.widget_ids = {}
        self.header_layout = self.board_layout = self.c_dead_layout = self.h_dead_layout =\
        self.footer_layout = self.undo_btn = self.new_game_btn = None
        self.button_action_enabled = True

        with self.canvas.before:
            Color(*background)  # Set the background color (RGB format)
            self.rect = Rectangle(size=self.main.size, pos=self.main.pos)
        self.main.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.main.pos
        self.rect.size = self.main.size

    def on_enter(self):
        self.header_layout = BoxLayout(orientation="horizontal", size_hint_y=.10)
        self.h_dead_layout = BoxLayout(orientation="horizontal", size_hint_y=.10)
        self.board_layout = GridLayout(rows=8, cols=8, spacing=0, padding=0, size=(100,100),\
                                        size_hint_y=.60, pos_hint={'center_x':0.5, 'center_y':0.5})
        self.c_dead_layout = BoxLayout(orientation="horizontal",size_hint_y=.10)
        self.footer_layout = BoxLayout(orientation="horizontal",size_hint_y=.10)
        
        temp_text = "Your turn" if self.turn == self.my_turn else "Computer turn"
        self.head_lbl = Label(text=temp_text, pos_hint={'center_x':0.5, 'center_y':.5}, font_size=24, halign='center', valign='middle')
        self.header_layout.add_widget(self.head_lbl)
        
        self.undo_btn = Button(text="Undo",)
        self.undo_btn.bind(on_press=self.undo_step)
        self.new_game_btn = Button(text="New Gmae" )
        self.new_game_btn.bind(on_press=self.new_game)
        self.footer_layout.add_widget(self.undo_btn)
        self.footer_layout.add_widget(self.new_game_btn)

        self.main.add_widget(self.header_layout)
        self.main.add_widget(self.h_dead_layout)
        self.main.add_widget(self.board_layout)
        self.main.add_widget(self.c_dead_layout)
        self.main.add_widget(self.footer_layout)

        arr = [str(i)+str(j) for i in range(0,8,1) for j in range(0,8,1)]
        arr.reverse() if self.turn=='W' else arr
        
        for box_id in arr:
            row = int(box_id[0]); col = int(box_id[1]);
            mark_color = even_color if (row + col)%2==0 else odd_color
            txt = gui_m[self.chessboard[box_id][0:2]] if self.chessboard[box_id] != '' else ''
            
            if txt!='': 
                font_color = man_color['W'] if self.chessboard[box_id][0]=='W' else man_color['B']
            else: font_color = man_color['W']
                
            chessbtn = Button(background_normal='' , background_color=mark_color, text=txt, font_name='static/chess_fonts/CHEQ_TT.ttf',\
                             color=font_color, font_size=32, size=(50,50), border=(0, 0, 0, 0), size_hint=(1,.6))
            chessbtn.bind(on_press=partial(self.make_move, __class__, box_id))
            self.board_layout.add_widget(chessbtn)
            self.widget_ids[box_id] = chessbtn

        # with self.canvas.before:
        #     Color(.168,.168,.168,1)  # Set the background color (RGB format)
        #     self.rect = Rectangle(size=self.board_layout.size, pos=self.board_layout.pos)
        # self.board_layout.bind(size=self.update_rect, pos=self.update_rect)
      
  
    def on_leave(self):
        self.main.clear_widgets()
        self.widget_ids = {}

    def new_game(self, instance):
        GameWindow.chessboard = GameWindow.castle = GameWindow.depth = GameWindow.turn = GameWindow.my_turn =\
        GameWindow.opp_turn = GameWindow.my_promote_row = GameWindow.opp_promote_row = GameWindow.previous_position = None
        
        GameWindow.undo_list = []
        GameWindow.dead_list = []
        GameWindow.move_data = []
        GameWindow.moved_mark = []
        GameWindow.r_possible_moves = []
        self.button_action_enabled = True
        self.parent.current = "dash_screen"

    def make_move(self, cls, box_id, instance):
        if self.button_action_enabled == False:
            return None

        row,col = int(box_id[0]), int(box_id[1])
        if cls.turn==cls.my_turn:
            dead_chessman_id = None
            #return previous background color
            if len(cls.r_possible_moves)>0:
                for box in cls.r_possible_moves:
                    self.widget_ids[box].background_color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color

            #step 1: if curent box id in possile moves    
            if box_id in cls.r_possible_moves:
                dead_chessman_id = cls.chessboard[box_id] if cls.chessboard[box_id] != '' else ''
                chessman_id = cls.chessboard[cls.previous_position]
                chessman_color = chessman_id[0]
                chessman_short_id = chessman_id[1]
                chessman_name = gui_m[chessman_id[0:2]]
                
                if row == cls.my_promote_row and chessman_short_id =='S':
                    chessman_id = chessman_id[0]+'Q'+chessman_id[2:]
                    chessman_name = gui_m[chessman_id[0:2]]
                    chessman_short_id = chessman_id[1]

                if dead_chessman_id != '':    #if killing chessman
                    cls.dead_list.append(dead_chessman_id)
                    self.c_dead_layout.add_widget(Label(text=gui_m[dead_chessman_id[0:2]], font_size=32,\
                                                font_name='static/chess_fonts/CHEQ_TT.ttf', color=man_color[cls.opp_turn]))            

                #make and remove moved mark
                if len(cls.moved_mark)>0:
                    for box in cls.moved_mark:
                        self.widget_ids[box].background_color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color
                    cls.moved_mark = []

                self.widget_ids[cls.previous_position].text = ""
                self.widget_ids[box_id].text = chessman_name
                self.widget_ids[cls.previous_position].background_color = move_color
                self.widget_ids[box_id].background_color = move_color
                self.widget_ids[box_id].color = man_color[cls.my_turn]

                cls.moved_mark.append(box_id)
                cls.moved_mark.append(cls.previous_position)
                # castle case
                if chessman_short_id=='K' and abs(int(cls.previous_position[1])-col)==2:
                    if int(cls.previous_position[1])-col==2:#left castle
                        self.widget_ids[cls.castle[cls.my_turn]['lep']].text = ''
                        self.widget_ids[cls.castle[cls.my_turn]['lboxes'][0]].text = gui_m[cls.castle[cls.my_turn]['leid'][0:2]]
                        self.widget_ids[cls.castle[cls.my_turn]['lep']].background_color = move_color
                        self.widget_ids[cls.castle[cls.my_turn]['lboxes'][0]].background_color = move_color
                        self.widget_ids[cls.castle[cls.my_turn]['lboxes'][0]].color = man_color[cls.my_turn]
                        cls.moved_mark.append(cls.castle[cls.my_turn]['lep'])
                        cls.moved_mark.append(cls.castle[cls.my_turn]['lboxes'][0])
                        
                    elif int(cls.previous_position[1])-col==-2:#right castle
                        self.widget_ids[cls.castle[cls.my_turn]['rep']].text = ''
                        self.widget_ids[cls.castle[cls.my_turn]['rboxes'][0]].text = gui_m[cls.castle[cls.my_turn]['reid'][0:2]]
                        self.widget_ids[cls.castle[cls.my_turn]['rep']].background_color = move_color
                        self.widget_ids[cls.castle[cls.my_turn]['rboxes'][0]].background_color = move_color
                        self.widget_ids[cls.castle[cls.my_turn]['rboxes'][0]].color = man_color[cls.my_turn]
                        cls.moved_mark.append(cls.castle[cls.my_turn]['rep'])
                        cls.moved_mark.append(cls.castle[cls.my_turn]['rboxes'][0])

                cls.undo_list.append((deepcopy(cls.chessboard),deepcopy(cls.castle),deepcopy(cls.dead_list)))

                if len(cls.undo_list)>5: cls.undo_list.pop(0);    
                Chess.push(cls.my_turn,cls.chessboard,cls.castle,cls.previous_position,box_id,cls.chessboard[cls.previous_position])

                temp = Chess.get_both_data(cls.my_turn,cls.chessboard,cls.castle,)
                if temp[1]['kp'] in temp[0]['all_moves']:
                    cls.moved_mark.append(temp[1]['kp'])
                    self.widget_ids[temp[1]['kp']].background_color = check_color

                if len(temp[1]['legal_moves'])==0:
                    if Chess.checkmate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                        self.stop_command("You win the game", False)
                        return None

                    elif Chess.stalemate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                        self.stop_command("You win the game", False)
                        return None
                
                if Chess.insufficient_piece(cls.chessboard):
                    self.stop_command("Game has been draw\nCause of Insufficient pieces", False);
                    return None
                    
                cls.previous_position = None
                cls.r_possible_moves.clear()
                cls.move_data = []
                
                cls.turn = cls.opp_turn
                self.stop_command("Computer turn", False)
                # Clock.schedule_interval(self.computer_move, 1.0 / 60.0)
                Clock.schedule_once(lambda dt: self.computer_move(1.0/60.0, cls))

            #step 2: if box id not in possibble moves
            else:
                if len(cls.r_possible_moves)>0:
                    cls.r_possible_moves.clear()

                if cls.chessboard[box_id] != '' and cls.chessboard[box_id][0] == cls.my_turn:
                    moving_man = cls.chessboard[box_id]
                    cls.previous_position = box_id
                    cls.possible_moves = []

                    if len(cls.move_data) == 0: cls.move_data = Chess.get_both_data(cls.my_turn,cls.chessboard,cls.castle)
                    cls.possible_moves = cls.move_data[0]['legal_moves'].get(moving_man,[])
                    #storing bg color of possible moves
                    cls.r_possible_moves = cls.possible_moves.copy()
                    for box in cls.possible_moves:
                        self.widget_ids[box].background_color = pm_color
                else:
                    cls.previous_position = None

    def computer_move(self, dt, cls):
        data,points = Chess.play(deepcopy(cls.chessboard), deepcopy(cls.castle), cls.opp_turn, cur_depth=cls.depth)
        self.stop_command("Your turn", True)
        
        if data!=None:
            chessman_name, from_, to_= data
            if len(cls.moved_mark)>0:
                for box in cls.moved_mark:
                    self.widget_ids[box].background_color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color
                cls.moved_mark = []
                    
            if chessman_name[1]=='S' and int(to_[0])==cls.opp_promote_row:
                chessman_name = chessman_name[0]+'Q'+chessman_name[2:]

            self.widget_ids[from_].text = ""
            self.widget_ids[to_].text = gui_m[chessman_name[0:2]]
            self.widget_ids[from_].background_color = move_color
            self.widget_ids[to_].background_color = move_color
            self.widget_ids[to_].color = man_color[cls.opp_turn]

            cls.moved_mark.append(from_)
            cls.moved_mark.append(to_)
            
            if cls.chessboard[to_]!='':
                cls.dead_list.append(cls.chessboard[to_])
                self.h_dead_layout.add_widget(Label(text=gui_m[cls.chessboard[to_][0:2]], font_size=32,\
                                                font_name='static/chess_fonts/CHEQ_TT.ttf', color=man_color[cls.my_turn]))            

            if chessman_name[1]=='K' and abs(int(from_[1])-int(to_[1])) == 2:   #castle case
                if int(from_[1])-int(to_[1]) == 2:#left castle
                    self.widget_ids[cls.castle[cls.opp_turn]['lep']].text = ''
                    self.widget_ids[cls.castle[cls.opp_turn]['lboxes'][0]].text = gui_m[cls.castle[cls.opp_turn]['leid'][0:2]]
                    self.widget_ids[cls.castle[cls.opp_turn]['lep']].background_color = move_color
                    self.widget_ids[cls.castle[cls.opp_turn]['lboxes'][0]].background_color = move_color
                    self.widget_ids[cls.castle[cls.opp_turn]['lboxes'][0]].color = man_color[cls.opp_turn]
                    cls.moved_mark.append(cls.castle[cls.opp_turn]['lep'])
                    cls.moved_mark.append(cls.castle[cls.opp_turn]['lboxes'][0])
                    
                elif int(from_[1])-int(to_[1]) == -2:#right castle
                    self.widget_ids[cls.castle[cls.opp_turn]['rep']].text = ''
                    self.widget_ids[cls.castle[cls.opp_turn]['rboxes'][0]].text = gui_m[cls.castle[cls.opp_turn]['reid'][0:2]]
                    self.widget_ids[cls.castle[cls.opp_turn]['rep']].background_color = move_color
                    self.widget_ids[cls.castle[cls.opp_turn]['rboxes'][0]].background_color = move_color
                    self.widget_ids[cls.castle[cls.opp_turn]['rboxes'][0]].color = man_color[cls.opp_turn]
                    cls.moved_mark.append(cls.castle[cls.opp_turn]['rep'])
                    cls.moved_mark.append(cls.castle[cls.opp_turn]['rboxes'][0])
                    
            Chess.push(cls.opp_turn,cls.chessboard,cls.castle,from_,to_,chessman_name)
            temp = Chess.get_both_data(cls.opp_turn,cls.chessboard,cls.castle)

            if temp[1]['kp'] in temp[0]['all_moves']:
                cls.moved_mark.append(temp[1]['kp'])
                self.widget_ids[temp[1]['kp']].background_color = check_color

            if len(temp[1]['legal_moves'])==0:
                if Chess.checkmate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                    self.stop_command("Computer win the game", False)
                    return None

                elif Chess.stalemate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
                    self.stop_command("Computer win the game", False)
                    return None
            
            if Chess.insufficient_piece(cls.chessboard):
                self.stop_command("Game has been draw\nCause of Insufficient pieces", False)
                return None
            
            cls.turn = cls.my_turn

    def undo_step(self, instance):
        if len(self.undo_list)>0:
            GameWindow.move_data = []
            temp = GameWindow.undo_list.pop()
            # GameWindow.chessboard = deepcopy(temp[0])
            GameWindow.castle = {}
            GameWindow.dead_list = []
            GameWindow.castle = deepcopy(temp[1])
            GameWindow.dead_list = temp[2].copy()
            for box,man in temp[0].items():
                color = even_color if (int(box[0])+int(box[1]))%2==0 else odd_color
                txt = gui_m[man[0:2]] if man!='' else ''
                font_c = man_color[man[0]] if man!='' else man_color['W']
                self.widget_ids[box].text = txt
                self.widget_ids[box].background_color = color
                self.widget_ids[box].color = font_c
                GameWindow.chessboard[box] = man

            if len(self.h_dead_layout.children)>0: self.h_dead_layout.clear_widgets();
            if len(self.c_dead_layout.children)>0: self.c_dead_layout.clear_widgets();
            
            if len(GameWindow.dead_list)>0:
                for dead in GameWindow.dead_list:
                    if dead[0]==self.my_turn:
                        self.h_dead_layout.add_widget(Label(text=gui_m[dead[0:2]], font_size=32,\
                                                font_name='static/chess_fonts/CHEQ_TT.ttf', color=man_color[self.my_turn]))
                    else:
                        self.c_dead_layout.add_widget(Label(text=gui_m[dead[0:2]], font_size=32,\
                                                font_name='static/chess_fonts/CHEQ_TT.ttf', color=man_color[self.opp_turn]))
    def stop_command(self, txt, activ):
        self.head_lbl.text = txt
        self.button_action_enabled = activ

kv = Builder.load_file('main.kv')

class MyChessApp(App):
    title = "Chess"
    def build(self):
        return kv

    
if __name__=='__main__':
    obj = MyChessApp()
    obj.run()
