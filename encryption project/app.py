from tkinter import *
import caesarcipher
import vernamcipher
import enigmacipher
import rsacipher
import ciphercracker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Application:
    def __init__(self, master):
        self.master = master
        master.configure(bg = 'ivory2')
        master.title("My cipher")
        master.option_add('*Font', 'Georgia 12')
        master.option_add('*Background', 'ivory2')
        master.option_add('*Label.Font', 'helvetica 14')
        master.geometry('900x500+800+100')

        menubar = Menu(master) #menu bar
        master.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0) #add file tab
        menubar.add_cascade(label='File', menu=file_menu) 
        file_menu.add_command(label = 'Home', command=self.raise_home)
        file_menu.add_command(label = 'Info', command=self.raise_info)
        file_menu.add_command(label='Back', command=self.return_page)
        file_menu.add_command(label = 'Close', command=master.quit)

        cipher_menu = Menu(menubar, tearoff=0) #add cipher tab
        menubar.add_cascade(label='Cipher', menu=cipher_menu)
        cipher_menu.add_command(label='Caesar', command=self.raise_caesar)
        cipher_menu.add_command(label='Vernam', command=self.raise_vernam)
        cipher_menu.add_command(label='Enigma', command=self.raise_enigma)
        cipher_menu.add_command(label='RSA', command=self.raise_rsa)

        cracking_menu = Menu(menubar, tearoff=0) #add cracking tab
        menubar.add_cascade(label='Crack', menu=cracking_menu)
        cracking_menu.add_command(label='Analysis', command=self.analysis)



        self.choice = StringVar(value = 'encrypt') #state known to every page though the container
        self.container = Frame(master) #this cointainer is the page upon which all other pages rest upon and are raised to the top when the user selects them
        self.container.pack(fill='both', expand=True)

        self.pages = {}

        self.caesar_page = CaesarFrame(self.container, self)
        self.vernam_page = VernamFrame(self.container, self)
        self.enigma_page = EnigmaFrame(self.container, self)
        self.rsa_page = RsaFrame(self.container, self)
        self.analysis_page = AnalysisFrame(self.container, self)
        self.info_page = InfoFrame(self.container, self)
        self.home_page = HomeFrame(self.container, self)

        self.page_stack = [] #stack data structure to hold the most recent page visited at the top - FIFO
        self.page_stack.append(self.home_page)


    def raise_home(self): #all the raising functions
        self.home_page.tkraise()
        self.page_stack.append(self.home_page)
    def raise_caesar(self):
        self.caesar_page.set_init()
        self.caesar_page.tkraise()
        self.page_stack.append(self.caesar_page)
    def raise_vernam(self):
        self.vernam_page.set_init()
        self.vernam_page.tkraise()
        self.page_stack.append(self.vernam_page)
    def raise_enigma(self):
        self.enigma_page.tkraise()
        self.page_stack.append(self.enigma_page)
    def raise_rsa(self):
        self.rsa_page.set_init()
        self.rsa_page.tkraise()
        self.page_stack.append(self.rsa_page)
    def raise_info(self):
        self.info_page.tkraise()
        self.page_stack.append(self.info_page)
    def analysis(self):
        self.analysis_page.tkraise()
        self.page_stack.append(self.analysis_page)

    def return_page(self): #for the back button
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            page = self.page_stack[len(self.page_stack) - 1]
            page.tkraise()

class HomeFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.place(relheight=1, relwidth=1)
        label1 = Label(self, text = 'Welcome, please select a cipher to use')
        label1.pack(side=TOP, padx = 10, pady = 30)

        home1 = Frame(self, padx = 10, pady = 10)
        home1.bind('<Configure>', self.update_wrap)
        home1.pack(fill = 'both', expand = True)
        home1.rowconfigure(0, weight=1)
        home1.rowconfigure(1, weight=1)
        home1.rowconfigure(2, weight=1)
        home1.rowconfigure(3, weight=1)
        home1.columnconfigure(0, weight=1)
        home1.columnconfigure(1, weight=1)
        home1.columnconfigure(2, weight=1)
        home1.columnconfigure(3, weight=1)

        frame1_1 = Frame(home1)
        frame1_1.grid(column=1, row=0, columnspan=2)
        encrypt_choice = Radiobutton(frame1_1, text='Encrypt', variable=self.controller.choice, value='encrypt')
        decrypt_choice = Radiobutton(frame1_1, text='Decrypt', variable=self.controller.choice, value='decrypt')
        encrypt_choice.pack(side=LEFT)
        decrypt_choice.pack(side=RIGHT)

        self.btn1 = Button(home1, text='Caesar', command = self.controller.raise_caesar)
        self.btn2 = Button(home1, text='Vernam', command = self.controller.raise_vernam)
        self.btn3 = Button(home1, text='Enigma', command = self.controller.raise_enigma)
        self.btn4 = Button(home1, text='RSA', command = self.controller.raise_rsa)
        self.btn1.grid(row = 1, column = 0, padx = 10, pady = 10)
        self.btn2.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.btn3.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.btn4.grid(row = 1, column = 3, padx = 10, pady = 10)
        self.lbl1 = Label(home1, text='The caesar cipher shifts letters along the alphabet')
        self.lbl2 = Label(home1, text='The vernam cipher applies an xor operation on each letter')
        self.lbl3 = Label(home1, text='The enigma cipher performs a deep shift on letters')
        self.lbl4 = Label(home1, text='The RSA cipher utilizes prime factorization')
        self.lbl1.grid(row = 2, column = 0)
        self.lbl2.grid(row = 2, column = 1)
        self.lbl3.grid(row = 2, column = 2)
        self.lbl4.grid(row = 2, column = 3)
    
    def update_wrap(self, event): #this helps with the pages dimensions if the user were to resize it
        column_width = event.width // 4 -5
        self.lbl1.config(wraplength=column_width)
        self.lbl2.config(wraplength=column_width)
        self.lbl3.config(wraplength=column_width)
        self.lbl4.config(wraplength=column_width)

class CaesarFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.place(relheight=1, relwidth=1)
        label = Label(self, text = 'Caesar cipher')
        label.pack(side = TOP, pady = 10)

        frame1 = Frame(self, bg = 'ivory2') #set up grids
        frame1.pack(fill='both', expand = True)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)
        frame1.rowconfigure(2, weight=1)

        frame1_1 = Frame(frame1) #input
        frame1_1.grid(column=0, row=0)
        self.input_txt = Text(frame1_1, height=5, width=20)
        self.lbl1 = Label(frame1_1)
        self.lbl1.config(text = 'Plain Text')

        frame1_2 = Frame(frame1) #key
        frame1_2.grid(column=2, row=0)
        self.key = Text(frame1_2, height=5, width=20)
        lbl2 = Label(frame1_2)
        lbl2.config(text='Key')

        self.generate_btn = Button(frame1, height=2, width=15, font=('Arial', 16), command=self.caesar_cipher) #generate button

        frame1_3 = Frame(frame1) #output
        frame1_3.grid(column=1, row=1)
        self.output = Text(frame1_3, height=5, width=20)
        self.lbl3 = Label(frame1_3)
        self.lbl3.config(text='Cipher Text')

        frame1_4 = Frame(frame1) #switch between encrypt and decrypt button
        frame1_4.grid(column=0, row=1)
        self.switch_btn = Button(frame1_4, command=self.switch)
        if controller.choice.get() == 'encrypt':
            self.switch_btn.config(text = 'Switch to decrypt')
        else:
            self.switch_btn.config(text = 'Switch to encrypt')

        img = PhotoImage(file='photos/clipboard.gif').subsample(20)
        self.copy_btn = Button(frame1_3, image = img, text='copy', compound='top', command=self.copy)
        self.copy_btn.image = img
        self.copy_btn.pack(side=RIGHT, padx = (10, 0))

        frame1_5 = Frame(frame1)
        frame1_5.grid(column=2, row=1)
        self.gen_rng_key_btn = Button(frame1_5, text='Generate a random key', wraplength=100, command=self.gen_rng_key)
        self.gen_rng_key_btn.pack()


        #packing everything
        self.lbl1.pack(side=TOP)
        self.input_txt.pack()
        self.lbl3.pack(side=TOP)
        self.output.pack()
        self.generate_btn.grid(column=1, row=0)
        lbl2.pack(side=TOP)
        self.key.pack()
        self.switch_btn.pack()

    def caesar_cipher(self):
        if self.controller.choice.get() == 'encrypt':
            out = caesarcipher.encrypt(self.input_txt.get('1.0', 'end-1c'), int(self.key.get('1.0', 'end-1c')))
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', out)
        else:
            out = caesarcipher.decrypt(self.input_txt.get('1.0', 'end-1c'), int(self.key.get('1.0', 'end-1c')))
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', out)

    def switch(self):
        if self.controller.choice.get() == 'encrypt':
            self.generate_btn.config(text='Decrypt')
            self.switch_btn.config(text='Switch to encrypt')
            self.controller.choice.set('decrypt')
            self.lbl1.config(text='Cipher text')
            self.lbl3.config(text='Plain text')
        elif self.controller.choice.get() == 'decrypt':
            self.generate_btn.config(text='Encrypt')
            self.switch_btn.config(text='Switch to decrypt')
            self.controller.choice.set('encrypt')
            self.lbl1.config(text='Plain text')
            self.lbl3.config(text='Cipher text')
    
    def set_init(self):
        if self.controller.choice.get() == 'decrypt': #this line is differrent with the line in switch() since this coordinates the page when rising
            self.generate_btn.config(text='Decrypt')
            self.switch_btn.config(text='Switch to encrypt')
            self.controller.choice.set('decrypt')
            self.lbl1.config(text='Cipher text')
            self.lbl3.config(text='Plain text')
        elif self.controller.choice.get() == 'encrypt':
            self.generate_btn.config(text='Encrypt')
            self.switch_btn.config(text='Switch to decrypt')
            self.controller.choice.set('encrypt')
            self.lbl1.config(text='Plain text')
            self.lbl3.config(text='Cipher text')

    def copy(self):
        self.controller.master.clipboard_clear()
        self.controller.master.clipboard_append(self.output.get('1.0', 'end-1c'))

    def gen_rng_key(self):
        rng_key = caesarcipher.gen_rng_key()
        self.key.delete('1.0', 'end')
        self.key.insert('1.0', rng_key)

class VernamFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.place(relheight=1, relwidth=1)
        label = Label(self, text = 'Vernam cipher')
        label.pack(side = TOP, pady = 10)

        frame1 = Frame(self, bg = 'ivory2') #set up grids
        frame1.pack(fill='both', expand = True)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)
        frame1.rowconfigure(2, weight=1)

        frame1_1 = Frame(frame1) #input
        frame1_1.grid(column=0, row=0)
        self.input_txt = Text(frame1_1, height=5, width=20)
        self.lbl1 = Label(frame1_1)
        self.lbl1.config(text = 'Plain Text')

        frame1_2 = Frame(frame1) #key
        frame1_2.grid(column=2, row=0)
        self.key = Text(frame1_2, height=5, width=20)
        lbl2 = Label(frame1_2)
        lbl2.config(text='Key')

        self.generate_btn = Button(frame1, height=2, width=15, font=('Arial', 16), command=self.vernam_cipher) #generate button

        frame1_3 = Frame(frame1) #output
        frame1_3.grid(column=1, row=1)
        self.output = Text(frame1_3, height=5, width=20)
        self.lbl3 = Label(frame1_3)
        self.lbl3.config(text='Cipher Text')

        frame1_4 = Frame(frame1) #switch between encrypt and decrypt button
        frame1_4.grid(column=0, row=1)
        self.switch_btn = Button(frame1_4, command=self.switch)
        if controller.choice.get() == 'encrypt':
            self.switch_btn.config(text = 'Switch to decrypt')
        else:
            self.switch_btn.config(text = 'Switch to encrypt')

        img = PhotoImage(file='photos/clipboard.gif').subsample(20)
        self.copy_btn = Button(frame1_3, image = img, text='copy', compound='top', command=self.copy)
        self.copy_btn.image = img
        self.copy_btn.pack(side=RIGHT, padx = (10, 0))

        frame1_5 = Frame(frame1)
        frame1_5.grid(column=2, row=1)
        self.gen_rng_key_btn = Button(frame1_5, text='Generate a random key', wraplength=100, command=self.gen_rng_key)
        self.gen_rng_key_btn.pack()


        #packing everything
        self.lbl1.pack(side=TOP)
        self.input_txt.pack()
        self.lbl3.pack(side=TOP)
        self.output.pack()
        self.generate_btn.grid(column=1, row=0)
        lbl2.pack(side=TOP)
        self.key.pack()
        self.switch_btn.pack()

    def vernam_cipher(self):
        if self.controller.choice.get() == 'encrypt':
            out = vernamcipher.encrypt(self.input_txt.get('1.0', 'end-1c'), self.key.get('1.0', 'end-1c'))
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', out)
        else:
            out = vernamcipher.decrypt(self.input_txt.get('1.0', 'end-1c'), self.key.get('1.0', 'end-1c'))
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', out)

    def switch(self):
        if self.controller.choice.get() == 'encrypt':
            self.generate_btn.config(text='Decrypt')
            self.switch_btn.config(text='Switch to encrypt')
            self.controller.choice.set('decrypt')
            self.lbl1.config(text='Cipher text')
            self.lbl3.config(text='Plain text')
        elif self.controller.choice.get() == 'decrypt':
            self.generate_btn.config(text='Encrypt')
            self.switch_btn.config(text='Switch to decrypt')
            self.controller.choice.set('encrypt')
            self.lbl1.config(text='Plain text')
            self.lbl3.config(text='Cipher text')

    def set_init(self):
        if self.controller.choice.get() == 'decrypt':
            self.generate_btn.config(text='Decrypt')
            self.switch_btn.config(text='Switch to encrypt')
            self.controller.choice.set('decrypt')
            self.lbl1.config(text='Cipher text')
            self.lbl3.config(text='Plain text')
        elif self.controller.choice.get() == 'encrypt':
            self.generate_btn.config(text='Encrypt')
            self.switch_btn.config(text='Switch to decrypt')
            self.controller.choice.set('encrypt')
            self.lbl1.config(text='Plain text')
            self.lbl3.config(text='Cipher text')

    def copy(self):
        self.controller.master.clipboard_clear()
        self.controller.master.clipboard_append(self.output.get('1.0', 'end-1c'))

    def gen_rng_key(self):
        rng_key = vernamcipher.gen_rng_key(self.input_txt.get('1.0', 'end-1c'))
        self.key.delete('1.0', 'end')
        self.key.insert('1.0', rng_key)

class EnigmaFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.place(relheight=1, relwidth=1)
        label = Label(self, text='Enigma')
        label.pack(side=TOP, pady=10)

        frame1 = Frame(self, bg = 'ivory2') 
        frame1.pack(fill='both', expand = True)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)
        frame1.rowconfigure(2, weight=1)

        frame1_1 = Frame(frame1) #input
        frame1_1.grid(column=0, row=0)
        self.input_txt = Text(frame1_1, height=5, width=20)
        lbl1 = Label(frame1_1)
        lbl1.config(text = 'Input')
        lbl1.pack(side=TOP)
        self.input_txt.pack()

        generate_btn = Button(frame1, text='Generate', height=2, width=15, font=('Arial', 16), command=self.enigma_cipher)
        generate_btn.grid(column=1, row=0)

        frame1_2 = Frame(frame1) #output
        frame1_2.grid(column=2, row=0)
        self.output = Text(frame1_2, height=5, width=20)
        lbl2 = Label(frame1_2)
        lbl2.config(text='Output')
        
        img = PhotoImage(file='photos/clipboard.gif').subsample(20) #quick copy and past btn
        self.copy_btn = Button(frame1_2, image = img, text='copy', compound='top', command=self.copy)
        self.copy_btn.image = img
        self.copy_btn.pack(side=RIGHT, padx = (10, 0))
        lbl2.pack(side=TOP)
        self.output.pack()

        frame1_4 = Frame(frame1) #plugboard
        frame1_4.grid(row=1, column=2, sticky='nsew', padx = 10, pady = 10)
        label2 = Label(frame1_4, text='Plugboard')
        label2.pack(side=TOP)
        self.plugboard_txt = Text(frame1_4, height=5, width=20)
        self.plugboard_txt.pack(pady=5)

        frame1_5 = Frame(frame1) #mini description
        frame1_5.grid(row=2, column=2, sticky='nsew')
        des_lbl = Label(frame1_5, wraplength = 250, text='This is a historically accurate Enigma M3, consisting of 3 rotors which can all be configured to - the type, their ring setting and their initial position')
        des_lbl.pack(fill='both', expand=True)




        #------------------------set up rotor selection -----------------------------------------
        #i probably could have made this much more simpler and efficient but i didnt have the time to do so

        frame1_3 = Frame(frame1)
        frame1_3.grid(row=1, column=0, rowspan=2, columnspan=2, sticky='nsew', padx=10, pady=10)

        frame1_31 = Frame(frame1_3, borderwidth=1, relief='solid')
        frame1_31.pack(side=LEFT, padx=10, pady=10, expand=True, fill='both')
        label1 = Label(frame1_31, text='Slowest rotor')
        label1.pack(side=TOP)
        self.slow_rotor = StringVar(frame1_31, value='I') #slow rotor
        btn1s = Radiobutton(frame1_31, text='I', value='I', variable = self.slow_rotor)
        btn2s = Radiobutton(frame1_31, text='II', value='II', variable = self.slow_rotor)
        btn3s = Radiobutton(frame1_31, text='III', value='III', variable = self.slow_rotor)
        btn4s = Radiobutton(frame1_31, text='IV', value='IV', variable = self.slow_rotor)
        btn5s = Radiobutton(frame1_31, text='V', value='V', variable = self.slow_rotor)
        btn1s.pack(anchor=W, pady=2)
        btn2s.pack(anchor=W, pady=2)
        btn3s.pack(anchor=W, pady=2)
        btn4s.pack(anchor=W, pady=2)
        btn5s.pack(anchor=W, pady=2)
        frame1_331 = Frame(frame1_31) #add ring setting and position input fields
        frame1_331.columnconfigure(0, weight=1)
        frame1_331.columnconfigure(1, weight=1)
        frame1_331.rowconfigure(0, weight=1)
        frame1_331.rowconfigure(1, weight=1)
        frame1_331.pack(fill='both', expand=True)
        label31 = Label(frame1_331, text='Ring setting', font='helvetica 8')
        label31.grid(column=0, row=0)
        self.ring_settings = Entry(frame1_331, width=5)
        self.ring_settings.grid(column=0, row=1)
        label32 = Label(frame1_331, text='Position', font='helvetica 8')
        label32.grid(column=1, row=0)
        self.positions = Entry(frame1_331, width=5)
        self.positions.grid(column=1, row=1)

        frame1_32 = Frame(frame1_3, borderwidth=1, relief='solid') #middle rotor
        frame1_32.pack(side=LEFT, padx=10, pady=10, expand=True, fill='both')
        label2 = Label(frame1_32, text='Middle rotor')
        label2.pack(side=TOP)
        self.middle_rotor = StringVar(frame1_32, value='II') 
        btn1m = Radiobutton(frame1_32, text='I', value='I', variable = self.middle_rotor)
        btn2m = Radiobutton(frame1_32, text='II', value='II', variable = self.middle_rotor)
        btn3m = Radiobutton(frame1_32, text='III', value='III', variable = self.middle_rotor)
        btn4m = Radiobutton(frame1_32, text='IV', value='IV', variable = self.middle_rotor)
        btn5m = Radiobutton(frame1_32, text='V', value='V', variable = self.middle_rotor)
        btn1m.pack(anchor=W, pady=2)
        btn2m.pack(anchor=W, pady=2)
        btn3m.pack(anchor=W, pady=2)
        btn4m.pack(anchor=W, pady=2)
        btn5m.pack(anchor=W, pady=2)
        frame1_332 = Frame(frame1_32) #add ring setting and position input fields
        frame1_332.columnconfigure(0, weight=1)
        frame1_332.columnconfigure(1, weight=1)
        frame1_332.rowconfigure(0, weight=1)
        frame1_332.rowconfigure(1, weight=1)
        frame1_332.pack(fill='both', expand=True)
        label31 = Label(frame1_332, text='Ring setting', font='helvetica 8')
        label31.grid(column=0, row=0)
        self.ring_settingm = Entry(frame1_332, width=5)
        self.ring_settingm.grid(column=0, row=1)
        label32 = Label(frame1_332, text='Position', font='helvetica 8')
        label32.grid(column=1, row=0)
        self.positionm = Entry(frame1_332, width=5)
        self.positionm.grid(column=1, row=1)

        frame1_33 = Frame(frame1_3, borderwidth=1, relief='solid') #fast rotor
        frame1_33.pack(side=LEFT, padx=10, pady=10, expand=True, fill='both')
        label3 = Label(frame1_33, text='Fastest rotor')
        label3.pack(side=TOP)
        self.fastest_rotor = StringVar(frame1_33, value='III') 
        btn1f = Radiobutton(frame1_33, text='I', value='I', variable = self.fastest_rotor)
        btn2f = Radiobutton(frame1_33, text='II', value='II', variable = self.fastest_rotor)
        btn3f = Radiobutton(frame1_33, text='III', value='III', variable = self.fastest_rotor)
        btn4f = Radiobutton(frame1_33, text='IV', value='IV', variable = self.fastest_rotor)
        btn5f = Radiobutton(frame1_33, text='V', value='V', variable = self.fastest_rotor)
        btn1f.pack(anchor=W, pady=2)
        btn2f.pack(anchor=W, pady=2)
        btn3f.pack(anchor=W, pady=2)
        btn4f.pack(anchor=W, pady=2)
        btn5f.pack(anchor=W, pady=2)
        frame1_333 = Frame(frame1_33) #add ring setting and position input fields
        frame1_333.columnconfigure(0, weight=1)
        frame1_333.columnconfigure(1, weight=1)
        frame1_333.rowconfigure(0, weight=1)
        frame1_333.rowconfigure(1, weight=1)
        frame1_333.pack(fill='both', expand=True)
        label31 = Label(frame1_333, text='Ring setting', font='helvetica 8')
        label31.grid(column=0, row=0)
        self.ring_settingf = Entry(frame1_333, width=5)
        self.ring_settingf.grid(column=0, row=1)
        label32 = Label(frame1_333, text='Position', font='helvetica 8')
        label32.grid(column=1, row=0)
        self.positionf = Entry(frame1_333, width=5)
        self.positionf.grid(column=1, row=1)


        #insert default values for ease of use
        self.ring_settings.insert(0, 'A')
        self.ring_settingm.insert(0, 'A')
        self.ring_settingf.insert(0, 'A')
        self.positions.insert(0, 1)
        self.positionm.insert(0, 1)
        self.positionf.insert(0, 1)
        self.plugboard_txt.insert('1.0', 'AK BD')

    def enigma_cipher(self):
        if self.ring_settings.get().isalpha(): #convert letter to int incase they input it for the ring setting
            ring_setting_s = (enigmacipher.letter_to_index(self.ring_settings.get())+1)%26
        else:
            ring_setting_s = int(self.ring_settings.get())

        if self.ring_settingm.get().isalpha():
            ring_setting_m = (enigmacipher.letter_to_index(self.ring_settingm.get())+1)%26
        else:
            ring_setting_m = int(self.ring_settingm.get())

        if self.ring_settingf.get().isalpha():
            ring_setting_f = (enigmacipher.letter_to_index(self.ring_settingf.get())+1)%26
        else:
            ring_setting_f = int(self.ring_settingf.get())


        rotor1 = enigmacipher.Rotor(enigmacipher.ROTORS[self.slow_rotor.get()][0], enigmacipher.ROTORS[self.slow_rotor.get()][1], ring_setting_s, int(self.positions.get()))
        rotor2 = enigmacipher.Rotor(enigmacipher.ROTORS[self.middle_rotor.get()][0], enigmacipher.ROTORS[self.middle_rotor.get()][1], ring_setting_m, int(self.positionm.get()))
        rotor3 = enigmacipher.Rotor(enigmacipher.ROTORS[self.fastest_rotor.get()][0], enigmacipher.ROTORS[self.fastest_rotor.get()][1], ring_setting_f, int(self.positionf.get()))
        rotors = [rotor1, rotor2, rotor3]
        enigma = enigmacipher.Enigma(self.plugboard_txt.get('1.0', 'end-1c'), rotors)
        out = enigma.encrypt(self.input_txt.get('1.0', 'end-1c'))
        self.output.delete('1.0', 'end-1c')
        self.output.insert('1.0', out)

    def copy(self):
        self.controller.master.clipboard_clear()
        self.controller.master.clipboard_append(self.output.get('1.0', 'end-1c'))

class RsaFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.place(relheight=1, relwidth=1)
        label = Label(self, text = 'Rsa cipher')
        label.pack(side=TOP, pady=10)

        frame1 = Frame(self, bg='ivory2')
        frame1.pack(fill='both', expand=True)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)
        frame1.rowconfigure(2, weight=1)

        frame1_1 = Frame(frame1) #input
        frame1_1.grid(column=0, row=0)
        self.input_txt = Text(frame1_1, height=5, width=20)
        self.lbl1 = Label(frame1_1)
        self.lbl1.config(text = 'Plain Text')

        frame1_2 = Frame(frame1) #key
        frame1_2.grid(column=2, row=0)
        self.key = Text(frame1_2, height=5, width=20)
        self.lbl2 = Label(frame1_2)
        self.lbl2.config(text='Public Key')

        gen_frame = Frame(frame1) #center generate button + label
        gen_frame.grid(column=1, row=0)
        self.lbl_gen = Label(gen_frame, text='Encrypt')
        self.lbl_gen.pack(side=TOP)
        generate_btn = Button(gen_frame, text='Generate', height=2, width=15, font=('Arial', 16), command=self.rsa_cipher) #generate button

        frame1_3 = Frame(frame1) #output
        frame1_3.grid(column=1, row=1)
        self.output = Text(frame1_3, height=5, width=20)
        self.lbl3 = Label(frame1_3)
        self.lbl3.config(text='Cipher Text')

        frame1_4 = Frame(frame1) #switch between encrypt and decrypt button
        frame1_4.grid(column=0, row=1)
        self.switch_btn = Button(frame1_4, command=self.switch)
        if controller.choice.get() == 'encrypt':
            self.switch_btn.config(text = 'Decrypt')
        else:
            self.switch_btn.config(text = 'Encrypt')

        self.frame1_5 = Frame(frame1)
        self.frame1_5.grid(column=2, row=1)
        self.generated = False
        generate_keys_btn = Button(self.frame1_5, text='Generate new public and private keys', height=2, wraplength=150, justify='center', command=self.gen_keys)
        
        img = PhotoImage(file='photos/clipboard.gif').subsample(20)
        self.copy_btn = Button(frame1_3, image = img, text='copy', compound='top', command=self.copy)
        self.copy_btn.image = img
        self.copy_btn.pack(side=RIGHT, padx = (10, 0))

        #packing everything
        self.lbl1.pack(side=TOP)
        self.input_txt.pack()
        self.lbl3.pack(side=TOP)
        self.output.pack()
        generate_btn.pack(side=BOTTOM)
        self.lbl2.pack(side=TOP)
        self.key.pack()
        self.switch_btn.pack()
        generate_keys_btn.pack(pady=(0, 10))

    def rsa_cipher(self): #encrypting / decrypting
        if self.controller.choice.get() == 'encrypt':
            out = rsacipher.encrypt(self.input_txt.get('1.0', 'end-1c'), self.key.get('1.0', 'end-1c'))
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', out)
        else:
            out = rsacipher.decrypt(self.input_txt.get('1.0', 'end-1c'), self.key.get('1.0', 'end-1c'))
            self.output.delete('1.0', 'end')
            self.output.insert('1.0', out)

    def switch(self): #switch button
        if self.controller.choice.get() == 'encrypt':
            self.lbl_gen.config(text='Decrypt')
            self.switch_btn.config(text='Switch to encrypt')
            self.controller.choice.set('decrypt')
            self.lbl1.config(text='Cipher text')
            self.lbl2.config(text='Private key')
            self.lbl3.config(text='Plain text')
        elif self.controller.choice.get() == 'decrypt':
            self.lbl_gen.config(text='Encrypt')
            self.switch_btn.config(text='Switch to decrypt')
            self.controller.choice.set('encrypt')
            self.lbl1.config(text='Plain text')
            self.lbl2.config(text='Public key')
            self.lbl3.config(text='Cipher text')
    
    def set_init(self):
        if self.controller.choice.get() == 'decrypt':
            self.lbl_gen.config(text='Decrypt')
            self.switch_btn.config(text='Switch to encrypt')
            self.controller.choice.set('decrypt')
            self.lbl1.config(text='Cipher text')
            self.lbl2.config(text='Private key')
            self.lbl3.config(text='Plain text')
        elif self.controller.choice.get() == 'encrypt':
            self.lbl_gen.config(text='Encrypt')
            self.switch_btn.config(text='Switch to decrypt')
            self.controller.choice.set('encrypt')
            self.lbl1.config(text='Plain text')
            self.lbl2.config(text='Public key')
            self.lbl3.config(text='Cipher text')

    def copy(self, where='output'): #quick copy to clipboard button
        self.controller.master.clipboard_clear()
        if where == 'output':
            self.controller.master.clipboard_append(self.output.get('1.0', 'end-1c'))
        elif where == 'public':
            self.controller.master.clipboard_append(self.pub_key_text_widget.get('1.0', 'end-1c'))
        elif where == 'private':
            self.controller.master.clipboard_append(self.priv_key_text_widget.get('1.0', 'end-1c'))

    def gen_keys(self):
        rsa = rsacipher.Rsa() #generate new Rsa object each time button is loaded to create new pub and priv key pair
        pub_key = rsa.public_key
        priv_key = rsa.private_key

        if self.generated == False: #if this is the first time generating keys, sets up all the widgets
            frame1_5_1 = Frame(self.frame1_5)
            frame1_5_1.pack(fill='both', expand=True)

            frame1_5_1.rowconfigure(0, weight=1)
            frame1_5_1.rowconfigure(1, weight=1)
            frame1_5_1.columnconfigure(0, weight=1)
            frame1_5_1.columnconfigure(1, weight=3)

            pub_lbl = Label(frame1_5_1, text='Public key:', wraplength=75)
            priv_lbl = Label(frame1_5_1, text='Private key:', wraplength=75)
            pub_lbl.grid(row=0, column=0, sticky='nsew')
            priv_lbl.grid(row=1, column=0, sticky='nsew')

            frame1_5_2 = Frame(frame1_5_1) #frames for the text widget + copy button
            frame1_5_3 = Frame(frame1_5_1)
            frame1_5_2.grid(column=1, row=0, sticky='nsew')
            frame1_5_3.grid(column=1, row=1, sticky='nsew')

            self.pub_key_text_widget = Text(frame1_5_2, height=3, width=6, font=('Gerogia', 10)) #text widgets containing the key6s
            self.priv_key_text_widget = Text(frame1_5_3, height=3, width=6, font=('Gerogia', 10))
            self.pub_key_text_widget.pack(side=LEFT, expand=True, fill='x')
            self.priv_key_text_widget.pack(side=LEFT, expand=True, fill='x')
            self.pub_key_text_widget.insert('1.0', pub_key)
            self.priv_key_text_widget.insert('1.0', priv_key)

            #add copy buttong for pub & priv keys
            img1 = PhotoImage(file='photos/clipboard.gif').subsample(20)
            img2 = PhotoImage(file='photos/clipboard.gif').subsample(20)
            self.copy_btn1 = Button(frame1_5_2, image = img1, text='copy', compound='top', command=lambda: self.copy('public'))
            self.copy_btn2 = Button(frame1_5_3, image = img2, text='copy', compound='top', command=lambda: self.copy('private'))
            self.copy_btn1.image = img1
            self.copy_btn2.image = img2
            self.copy_btn1.pack(side=RIGHT, expand=True, fill='x', padx=(3, 0))
            self.copy_btn2.pack(side=RIGHT, expand=True, fill='x', padx=(3, 0))
            self.generated = True
        else:
            self.pub_key_text_widget.delete('1.0', 'end')
            self.priv_key_text_widget.delete('1.0', 'end')
            self.pub_key_text_widget.insert('1.0', pub_key)
            self.priv_key_text_widget.insert('1.0', priv_key)

class AnalysisFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.n_windows = 0 #customization variable to make it look nice when multiple windows are open
        self.cracked = False
        self.IoCed = False

        self.place(relheight=1, relwidth=1)
        self.label = Label(self, text = 'Cipher text analysis', font=('Helvetica', 20))
        self.label.pack(pady = 10)

        self.frame1 = Frame(self)
        self.frame1.pack(fill='both', expand=True)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.columnconfigure(2, weight=1)
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=1)
        self.frame1.rowconfigure(2, weight=1)


        frame1_1 = Frame(self.frame1) #input text box
        frame1_1.grid(row=0, column=0, columnspan=3)
        self.label1 = Label(frame1_1, text = 'Input:')
        self.label1.pack(side=TOP)
        self.input_txt = Text(frame1_1, height=5, width=20)
        self.input_txt.pack(side=BOTTOM)


        generate_btn = Button(self.frame1, wraplength=150, text='Generate freq ana. bar chart', height=2, width=15, command=self.display_chart) #generate bar chart button
        generate_btn.grid(column=0, row=1)

        crack_btn = Button(self.frame1, wraplength=150, text='Crack (Caesar cipher only)', height=2, width=15, command=self.crack) #crack caesar cipher button
        crack_btn.grid(column=1, row=1)

        ioc_btn = Button(self.frame1, wraplength=150, text='Calculate index of coincidence', height=2, width=15, command=self.calc_ioc) #calc IoC button
        ioc_btn.grid(column=2, row=1)

    def count_freq(self):
        self.values = ciphercracker.calc_freq(self.input_txt.get('1.0', 'end-1c'))

    def display_chart(self):
        self.count_freq()
        fig = Figure(figsize=(5, 3), dpi=100) #sets the resolution of the figure object and everything within it
        ax = fig.add_subplot(111)

        labels = ["A", "B", "C", "D", 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        ax.bar(labels, self.values) #create the graph
        ax.set_title("Letter Frequency Bar Chart")
        ax.set_ylabel("Value")

        self.n_windows += 1
        window = Toplevel(self.controller.master) #create a new mini window
        window.title('Frequency analysis')
        window.geometry(f'550x350+{300+10*self.n_windows}+{300+10*self.n_windows}') #makes the windows pop up slightly after one another to not be overlapping
        canvas = FigureCanvasTkAgg(fig, master=window) #place the graph in tkinter
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def crack(self):
        outputs = ciphercracker.crack_caesar(self.input_txt.get('1.0', 'end-1c'))
        if self.cracked == False:
            self.frame2 = Frame(self.frame1)
            self.frame4 = Frame(self.frame1)
            self.frame2.grid(column=0, row=2)
            self.frame4.grid(column=2, row=2)
            self.frame2_1 = Frame(self.frame2)
            self.frame4_1 = Frame(self.frame4)
            self.frame2_1.pack(side=RIGHT)
            self.frame4_1.pack(side=RIGHT)

        if self.IoCed == False:
            self.frame3 = Frame(self.frame1) #separated incase the user clicks on calculated IoC before the caesar cipher crack as frames 3 and 3_1 would have been created then
            self.frame3.grid(column=1, row=2)
            self.frame3_1 = Frame(self.frame3)
            self.frame3_1.pack(side=RIGHT)

        if self.IoCed == True:
            try:
                self.ioc_cpy.destroy()
                self.out2.destroy()
            except:
                pass
        
        if self.cracked == True:
            try:
                self.out1.destroy()
                self.out2.destroy()
                self.out3.destroy()
                self.txt_cpy1.destroy()
                self.txt_cpy2.destroy()
                self.txt_cpy3.destroy()
                self.key_cpy1.destroy()
                self.key_cpy2.destroy()
                self.key_cpy3.destroy()
            except:
                pass

        self.out1 = Text(self.frame2, height=5, width=20)
        self.out2 = Text(self.frame3, height=5, width=20)
        self.out3 = Text(self.frame4, height=5, width=20)
        self.out1.insert('1.0', outputs[0][0]+f'\nKey = {outputs[0][1]}') #outputs the cracked text and the key used to crack it
        self.out2.insert('1.0', outputs[1][0]+f'\nKey = {outputs[1][1]}')
        self.out3.insert('1.0', outputs[2][0]+f'\nKey = {outputs[2][1]}')
        self.out1.pack(side=LEFT)
        self.out2.pack(side=LEFT)
        self.out3.pack(side=LEFT)


        img = PhotoImage(file='photos/clipboard.gif').subsample(20) #creates the copy buttons
        self.key_cpy1 = Button(self.frame2_1, width=35, image=img, text='Key', compound='top', command=lambda: self.copy(outputs[0][1]))
        self.key_cpy2 = Button(self.frame3_1, width=35, image=img, text='Key', compound='top', command=lambda: self.copy(outputs[1][1]))
        self.key_cpy3 = Button(self.frame4_1, width=35, image=img, text='Key', compound='top', command=lambda: self.copy(outputs[2][1]))
        self.txt_cpy1 = Button(self.frame2_1, width=35, image=img, text='Text', compound='top', command=lambda: self.copy(outputs[0][0]))
        self.txt_cpy2 = Button(self.frame3_1, width=35, image=img, text='Text', compound='top', command=lambda: self.copy(outputs[1][0]))
        self.txt_cpy3 = Button(self.frame4_1, width=35, image=img, text='Text', compound='top', command=lambda: self.copy(outputs[2][0]))
        self.key_cpy1.image = img
        self.key_cpy2.image = img
        self.key_cpy3.image = img
        self.txt_cpy1.image = img
        self.txt_cpy2.image = img
        self.txt_cpy3.image = img
        self.key_cpy1.pack(side=TOP, padx=(3, 0))
        self.key_cpy2.pack(side=TOP, padx=(3, 0))
        self.key_cpy3.pack(side=TOP, padx=(3, 0))
        self.txt_cpy1.pack(side=BOTTOM, padx=(3, 0))
        self.txt_cpy2.pack(side=BOTTOM, padx=(3, 0))
        self.txt_cpy3.pack(side=BOTTOM, padx=(3, 0))
        

        self.cracked = True

    def calc_ioc(self):
        IoC = round(ciphercracker.index_of_coincidence(self.input_txt.get('1.0', 'end-1c')), 4)

        if self.cracked == False and self.IoCed == False:
            self.frame3 = Frame(self.frame1)
            self.frame3.grid(column=1, row=2)
            self.frame3_1 = Frame(self.frame3)
            self.frame3_1.pack(side=RIGHT)

        if self.cracked == True:
            try: #this destroys the text widgets created by the caesar cipher cracker and it is reliable even if the user never generated those widgets
                self.out1.destroy()
                self.out2.destroy()
                self.out3.destroy()
                self.txt_cpy1.destroy()
                self.txt_cpy2.destroy()
                self.txt_cpy3.destroy()
                self.key_cpy1.destroy()
                self.key_cpy2.destroy()
                self.key_cpy3.destroy()
            except:
                pass
        
        if self.IoCed == True:
            try:
                self.out2.destroy()
                self.ioc_cpy.destroy()
            except:
                pass

        self.out2 = Text(self.frame3, height=5, width=20)
        self.out2.insert('1.0', IoC)
        self.out2.pack(side=LEFT)
        
        img = PhotoImage(file='photos/clipboard.gif').subsample(20)
        self.ioc_cpy = Button(self.frame3_1, image=img, text='Copy', compound='top', command=lambda: self.copy(IoC))
        self.ioc_cpy.image = img
        self.ioc_cpy.pack(padx=(3, 0))


        self.IoCed = True

    def copy(self, input_txt):
        self.controller.master.clipboard_clear()
        self.controller.master.clipboard_append(input_txt)

class InfoFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.place(relheight=1, relwidth=1)
        label1 = Label(self, text = 'Information', font='Helvatica 20')
        label1.pack(side=TOP, padx = 10, pady = 30)

        frame1 = Frame(self)
        frame1.pack(fill='both', expand=True)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)

        frame2 = Frame(frame1) #symmetric
        frame2.grid(column=0, row=0)
        lbl2 = Label(frame2, text='Symmetric', font = 'Helvatica 18')
        lbl2_1 = Label(frame2, wraplength=300, text='Symmetric encryption is encryption where the same key is used for encryption and decryption and so the key must be securely shared first')
        lbl2.pack(side=TOP, pady=(0, 10))
        lbl2_1.pack(side=BOTTOM)

        frame3 = Frame(frame1) #asymmetric
        frame3.grid(column=0, row=1)
        lbl3 = Label(frame3, text='Asymmetric', font = 'Helvatica 18')
        lbl3_1 = Label(frame3, wraplength=300, text='Asymmetric encryption is encryption where encryption/decryption are performed using key-value pairs, one for encryption and one for decryption')
        lbl3.pack(side=TOP, pady=(0, 10))
        lbl3_1.pack(side=BOTTOM)

        frame4 = Frame(frame1) #caesar
        frame4.grid(column=1, row=0)
        lbl4 = Label(frame4, text='Caesar', font = 'Helvatica 18')
        lbl4_1 = Label(frame4, wraplength=300, text='This is a type of substitution cipher in which each letter is shifted by a certain amount of letters along the alphabet')
        lbl4.pack(side=TOP, pady=(0, 10))
        lbl4_1.pack(side=BOTTOM)

        frame5 = Frame(frame1) #vernam
        frame5.grid(column=1, row=1)
        lbl5 = Label(frame5, text='Vernam (One Time Pad)', font = 'Helvatica 18')
        lbl5_1 = Label(frame5, wraplength=300, text='This is one of the ONLY theoretically uncrackable cipher and works by applying a bitwise XOR operation on the message and a key - which should be used once, be truly random and the same length as the message')
        lbl5.pack(side=TOP, pady=(0, 10))
        lbl5_1.pack(side=BOTTOM)

        frame6 = Frame(frame1) #rsa
        frame6.grid(column=2, row=0)
        lbl6 = Label(frame6, text='Rsa', font = 'Helvatica 18')
        lbl6_1 = Label(frame6, wraplength=300, text='This is a type of asymmetric encryption in which a public key is used to encrypt a piece of text and a private key is used to decrypt it')
        lbl6.pack(side=TOP, pady=(0, 10))
        lbl6_1.pack(side=BOTTOM)

        frame7 = Frame(frame1) #enigma
        frame7.grid(column=2, row=1)
        lbl7 = Label(frame7, text='Enigma', font = 'Helvatica 18')
        lbl7_1 = Label(frame7, wraplength=300, text='This is a much more complex substitution cipher in which a plug board swaps pairs of letters and then rotors shift letters. Enigma however does not need a decrypt function since it is symmetric across the reflector and so the same initial state can be used to decrypt the message')
        lbl7.pack(side=TOP, pady=(0, 10))
        lbl7_1.pack(side=BOTTOM)




def Main():
    root = Tk()
    app = Application(root)
    root.mainloop()

Main()
