import tkinter as tk
from inflection import titleize
from tkinter import font  as tkfont
from tkinter import ttk

TOPPINGS_FILE_NAME = 'Toppings.txt'

with open(TOPPINGS_FILE_NAME, 'r') as toppingsfile:
    lines = toppingsfile.readlines()
    toppings_list = [line.strip() for line in lines]

# toppings_list = ['Pepperoni', 'Sausage', 'Ham', 'Steak', 'Anchovies', 'Pineapple', 'Green Peppers', 'Mushrooms', 'Banana Peppers']
toppings_choice = []

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()
        frame.event_generate('<<on_show>>')


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Pick a topping!", font=controller.title_font)
        label.pack(side='top')

        self.frame1 = tk.Frame(self, width=300, height=300)
        self.frame1.pack(side='top')

        self.button_frame = None

        frame2 = tk.Frame(self, width=300, height=300)
        frame2.pack(side='bottom')

        self.new_topping = tk.Entry(frame2, bd =5)
        self.new_topping.grid(row=0, column=0)
        self.remove_topping = tk.Entry(frame2, bd =5)
        self.remove_topping.grid(row=1, column=0)


        clear_button = ttk.Button(frame2, text="Clear", command=self.clear_toppings)
        clear_button.grid(row=3, column=0)
        add_toppings_button = ttk.Button(frame2, text='Add Topping', command=self.add_new_topping_click)
        add_toppings_button.grid(row=0, column=1)
        remove_toppings_button = ttk.Button(frame2, text='Remove topping', command=self.delete_toppings_from_menu)
        remove_toppings_button.grid(row=1, column=1)
        finish_button = tk.Button(frame2, text="Finish", command=lambda: controller.show_frame("PageOne"))
        finish_button.grid(row=3, column=1)

        
        
        self.refresh_topping_list()

        self.text_display = tk.Text(self)
        self.update_text_display('\r\n'.join(toppings_choice))
        self.text_display.pack()
    
    def refresh_topping_list(self):
        if self.button_frame:
            self.button_frame.destroy()

        self.button_frame = tk.Frame(self.frame1, width=300, height=300)
        self.button_frame.pack(side='top')

        col = 0
        row = 0

        for i,Topping in enumerate(toppings_list):
            if i % 6 == 0:
                row += 1
                col = 0
            else:
                col += 1
            
            butName = ttk.Button(self.button_frame, text=Topping, command=lambda e=Topping: self.on_toppings_button_click(e))
            butName.grid(row=row, column=col)

    def clear_toppings(self):
        print('clearing')
        del toppings_choice[:]
        self. update_text_display('')

    def on_toppings_button_click(self, selected_topping):
        if selected_topping in toppings_choice:
            toppings_choice.remove(selected_topping)
        else:
            toppings_choice.append(selected_topping)

        print(', '.join(toppings_choice))

        self.update_text_display('\r\n'.join(toppings_choice))

    def update_text_display(self, text):
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        self.text_display.config(state='disabled')

    def add_new_topping_click(self):
        new_topping = self.new_topping.get().lower()
        self.new_topping.delete(0, tk.END)

        if titleize(new_topping) in toppings_list:
            return

        toppings_list.append(titleize(new_topping))
        
        self.refresh_topping_list()
        self.save_toppings_file()

    def delete_toppings_from_menu(self):
        delete_topping = self.remove_topping.get().lower()
        self.remove_topping.delete(0, tk.END)

        if titleize(delete_topping) in toppings_list:
            toppings_list.remove(titleize(delete_topping))

        
        self.refresh_topping_list()
        self.save_toppings_file()

    def save_toppings_file(self):
        with open(TOPPINGS_FILE_NAME, 'r+') as f:
            f.truncate(0)
            f.writelines("\n".join(toppings_list))
               

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.bind('<<on_show>>', self.on_show)

        frame1 = tk.Frame(self, width=300, height=300)
        frame1.pack(side='bottom')
        frame2 = tk.Frame(self, width=300, height=300)
        frame2.pack(side='top')

        button = tk.Button(frame2, text="New order",
                            command=lambda: controller.show_frame("StartPage"))
        button.grid(row=1, column=0)

        label = tk.Label(frame2, text="Thank you for Ordering", font=controller.title_font)
        label.grid(row=0, column=0)

        self.text_display = tk.Text(frame1)
        self.text_display.grid(row=0, column=0)

    def update_ending_toppings(self, text):
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        self.text_display.config(state='disabled')

    def on_show(self, e):
        print(toppings_choice)
        self.update_ending_toppings('\r\n'.join(toppings_choice))

        


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()