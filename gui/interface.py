from tkinter import *
from tkinter.ttk import Separator;
from PIL import ImageTk, Image, ImageDraw;
import os;
import pyglet;
from tkhtmlview import HTMLLabel;

import main, utils, nlp;

pyglet.font.add_file('res/marugothic.ttf');
pyglet.font.add_file('res/handwriting.otf');

img = None;
images = [];

checking = False;

class ReaderGUI:
    
    point1 = None;
    point2 = None;
    startX = None;
    startY = None;
    highlight = None;
    origin = None;

    sentence = [];

    def __init__(self, master):
    
        master.title('RawMangaSensei');
        master.geometry("860x730");

        self.label = Label(master, text="RawManga-Sensei", font= ("Helvetica", 14));
        self.label.pack();

        self.help = Label(master, text="Scan text to read!", font=('Cursive', 14, 'bold'));
        self.help.place(x=510, y=40);

        self.text = Label(master, text="...", font=(utils.get_font(), 20), justify=LEFT, wraplength=335, background="white");
        self.text.place(x=510, y=70);

        self.separator = Separator(master, orient='horizontal');

        self.frame = HTMLLabel(master, html="<p>scan to get meanings<p>");
        self.frame.place(x=510, y=130, width=850-520, height=2000);

        self.scroll = Scrollbar(self.frame, orient="vertical", command=self.frame.yview);
        self.frame.config(yscrollcommand=self.scroll.set);

        self.scroll.pack(side=RIGHT, fill=Y);

        self.text.update();
        self.separator.place(x=510, y=self.text.winfo_y() + self.text.winfo_height() + 10, width=200, height=0.4);

        self.c = Canvas(master, width=500, height=700);
        self.c.place(x=0, y=30);
        
        self.master = master;
    
    def append_meaning(self, word: nlp.Word):

        self.text.update();

        #Join meanings
        joined: str = "";
        for data in self.sentence: joined += data[1];

        # Place the word data
        meaning = f"""
        <div style=\"border: solid 1px black\">
            <h2>{word.origin}</h2>
            <p><b>{word.reading}</b> ・ <span>"""+(word.jlpt if word.jlpt != [] else "No JLPT") + (", Common word" if word.common else "")+"""</span></p>
        </div>
        """;

        self.frame.set_html(joined + meaning);
        self.sentence.append((word, meaning));

    def update_text(self, new_text):
        
        self.text.config(text=new_text);
        
        self.text.update();
        self.separator.place(x=510, y=self.text.winfo_y() + self.text.winfo_height() + 10, width=200, height=0.4);

    def update_image(self, name):
        global img;

        Tk.update(self.master);

        rawimage1 = Image.open(f"../app/files/{name}");
        rawimage = rawimage1.resize((self.c.winfo_width(), self.c.winfo_height()), Image.LANCZOS);
        self.origin = rawimage;

        img =  ImageTk.PhotoImage(rawimage);
        self.c.create_image(0,0, image=img, anchor=NW);
    
        self.c.update();
        self.aspect_ratio_x, self.aspect_ratio_y = rawimage1.width / self.c.winfo_width(), rawimage1.height / self.c.winfo_height();
        print(self.aspect_ratio_x);

    def motion(self, event):
        global checking;
        self.x, self.y = event.x, event.y;
    
        if checking:
             if(self.point2 != None): self.c.delete(self.point2);
             self.point2 = self.c.create_oval((self.x, self.y, self.x + 10, self.y + 10), fill="blue", outline=None);
    
    def on_sub_click(self, event):
        global checking;

        if(self.startX == None):

            if self.highlight != None: self.c.delete(self.highlight);

            self.c.delete(self.point1);
            self.c.delete(self.point2);

            self.startX = self.x;
            self.startY = self.y;

            checking = True;
            self.point1 = self.c.create_oval((self.startX, self.startY, self.startX + 10, self.startY + 10), fill="blue", outline=None);

        else:
            # Highlight area
            self.x += 10;
            self.y += 10;

            self.highlight = self.create_rectangle(
                x1=min(self.startX, self.x),
                y1=min(self.startY, self.y),
                x2=max(self.startX, self.x),
                y2=max(self.startY, self.y),
                fill="black",
                alpha=.5
            );

            # Get real highlight size
            main.analize_section(
                min(self.startX, self.x) * self.aspect_ratio_x,
                min(self.startY, self.y) * self.aspect_ratio_y,
                max(self.startX, self.x) * self.aspect_ratio_x,
                max(self.startY, self.y) * self.aspect_ratio_y,
                self
            );

            self.frame.set_html("");
            self.sentence = [];

            self.startX = None;
            self.startY = None;

            checking = False;

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            images.append(ImageTk.PhotoImage(image))
            return self.c.create_image(x1, y1, image=images[-1], anchor='nw')

def on_closing():
    root.destroy();
    os._exit(0);

root = Tk();    
my_gui = ReaderGUI(root);
my_gui.update_image(main.file);

root.resizable(False, False);

# Bind canvas events
my_gui.c.bind('<Motion>', my_gui.motion)
my_gui.c.bind("<Button-1>", my_gui.on_sub_click)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop();