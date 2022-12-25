from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        self.title('Digital Board')
        self.geometry('1050x600')
        self.configure(background='#c4c3d0')
        self.resizable(False, False)

        # Important attributes/variables
        self._pencil_color, self._board_color = 'black', '#f8f8ff'
        self._current_x, self._current_y = 0, 0
        self._pencil_thickness = 2
        
        # Provide an icon to the app
        self._provide_icon()

        # Display the main board
        self._display_board()

        # Display the box containing colors
        self._display_colorbox()

        # Display colors in the color box
        self._display_colors()

        # Clear the board
        self._clear_board()

        # Select the color for the board
        self._select_board_color()

        # Adjust thickness of the pencil stroke
        self._adjust_thickness()
    

    def _provide_icon(self):
        icon = ImageTk.PhotoImage(Image.open('_01__DigitalBoard/blackboard.png'))
        self.iconphoto(False, icon)

    def _display_board(self):
        self._board = Canvas(self, width=1000, height=450, background=self._board_color, cursor='pencil')
        self._board.place(x=25, y=125)

        def locate_xy(e):
            self._current_x, self._current_y = e.x, e.y
        
        def draw_on_theboard(e):
            self._board.create_line((self._current_x, self._current_y), (e.x, e.y), fill=self._pencil_color, width=self._pencil_thickness)
            self._current_x, self._current_y = e.x, e.y

        self._board.bind('<Button-1>', locate_xy)
        self._board.bind('<B1-Motion>', draw_on_theboard)
    
    def _display_colorbox(self):
        self._colorbox = Canvas(self, width=178, height=90, background='#c4c3d0', borderwidth=0)
        self._colorbox.place(x=848, y=16)
    
    def _display_colors(self):
        # First Row
        id_11 = self._colorbox.create_rectangle((4, 4), (29, 29), fill='black')
        self._colorbox.tag_bind(id_11, '<Button-1>', lambda e: self._select_color('black'))

        id_12 = self._colorbox.create_rectangle((33, 4), (58, 29), fill='brown')
        self._colorbox.tag_bind(id_12, '<Button-1>', lambda e: self._select_color('brown'))

        id_13 = self._colorbox.create_rectangle((62, 4), (87, 29), fill='maroon')
        self._colorbox.tag_bind(id_13, '<Button-1>', lambda e: self._select_color('maroon'))

        id_14 = self._colorbox.create_rectangle((91, 4), (116, 29), fill='red')
        self._colorbox.tag_bind(id_14, '<Button-1>', lambda e: self._select_color('red'))

        id_15 = self._colorbox.create_rectangle((120, 4), (145, 29), fill='blue')
        self._colorbox.tag_bind(id_15, '<Button-1>', lambda e: self._select_color('blue'))

        id_16 = self._colorbox.create_rectangle((149, 4), (174, 29), fill='green')
        self._colorbox.tag_bind(id_16, '<Button-1>', lambda e: self._select_color('green'))

        # Second Row
        id_21 = self._colorbox.create_rectangle((4, 33), (29, 58), fill='yellow')
        self._colorbox.tag_bind(id_21, '<Button-1>', lambda e: self._select_color('yellow'))

        id_22 = self._colorbox.create_rectangle((33, 33), (58, 58), fill='orange')
        self._colorbox.tag_bind(id_22, '<Button-1>', lambda e: self._select_color('orange'))

        id_23 = self._colorbox.create_rectangle((62, 33), (87, 58), fill='violet')
        self._colorbox.tag_bind(id_23, '<Button-1>', lambda e: self._select_color('violet'))

        id_24 = self._colorbox.create_rectangle((91, 33), (116, 58), fill='indigo')
        self._colorbox.tag_bind(id_24, '<Button-1>', lambda e: self._select_color('indigo'))

        id_25 = self._colorbox.create_rectangle((120, 33), (145, 58), fill='purple')
        self._colorbox.tag_bind(id_25, '<Button-1>', lambda e: self._select_color('purple'))

        id_26 = self._colorbox.create_rectangle((149, 33), (174, 58), fill='darkcyan')
        self._colorbox.tag_bind(id_26, '<Button-1>', lambda e: self._select_color('darkcyan'))

        # Third Row
        id_31 = self._colorbox.create_rectangle((4, 62), (29, 87), fill='silver')
        self._colorbox.tag_bind(id_31, '<Button-1>', lambda e: self._select_color('silver'))

        id_32 = self._colorbox.create_rectangle((33, 62), (58, 87), fill='#708090')
        self._colorbox.tag_bind(id_32, '<Button-1>', lambda e: self._select_color('#708090'))

        id_33 = self._colorbox.create_rectangle((62, 62), (87, 87), fill='#696969')
        self._colorbox.tag_bind(id_33, '<Button-1>', lambda e: self._select_color('#696969'))

        id_34 = self._colorbox.create_rectangle((91, 62), (116, 87), fill='pink')
        self._colorbox.tag_bind(id_34, '<Button-1>', lambda e: self._select_color('pink'))

        id_35 = self._colorbox.create_rectangle((120, 62), (145, 87), fill='#4f666a')
        self._colorbox.tag_bind(id_35, '<Button-1>', lambda e: self._select_color('#4f666a'))

        id_36 = self._colorbox.create_rectangle((149, 62), (174, 87), fill='#ff00ff')
        self._colorbox.tag_bind(id_36, '<Button-1>', lambda e: self._select_color('#ff00ff'))

    def _select_color(self, new_color):
        self._pencil_color = new_color
    
    def _clear_board(self):
        def clear_utility():
            self._board.delete('all')
        ttk.Button(self, text='Clear Board', padding=5, command=clear_utility).place(x=750, y=56)

    def _select_board_color(self):
        color = StringVar(value='White')
        colors = ('', 'White', 'Black', 'Green')

        def utility(col):
            match(col):
                case 'White':
                    print('hhh')
                    self._board_color = '#f8f8ff'
                case 'Black':
                    self._board_color = '#242124'
                case 'Green':
                    self._board_color = '#3cb371'
            self._board.configure(background=self._board_color)

        board_colors = ttk.OptionMenu(self, color, *colors, command=lambda e: utility(e))
        board_colors.place(x=25, y=16)
        
    
    def _adjust_thickness(self):
        frame = Frame(self, background='#c4c3d0')
        frame.place(x=628, y=20)

        ttk.Label(frame, text='Adjust thickness:', background='#c4c3d0').grid(row=0, column=0)
        
        def utility(val):
            self._pencil_thickness = val.__round__(2)

        global val 
        val = DoubleVar(value=2)
        ttk.Scale(frame, from_=2, to=50, variable=val, command=lambda e: utility(val.get())).grid(row=0, column=1, padx=5)
        


if __name__ == '__main__':
    app = App()
    app.mainloop()