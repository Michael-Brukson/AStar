import customtkinter as ctk
from CTkListbox import *
from tkinter import *
from tkinter.ttk import *
import os
from PIL import Image, ImageTk, ImageDraw
from functools import partial

class GridMake:
    __SAVE_DIR = "./mazes/"

    def __init__(self, width: int= 600, height: int= 440):
        menus = [
                ("☰", [("Open", self.__file_select), ("New", None)]),
                ("⚙", [("Temp", None)])
                ]

        self.__root = ctk.CTk()
        self.__root.title("")
        self.__root.geometry(f"{width}x{height}")

        content = ctk.CTkFrame(self.__root)
        content.pack(fill=ctk.BOTH, expand=True)

        self.__upper = ctk.CTkFrame(content)
        self.__upper.pack(side=ctk.TOP, fill=ctk.Y, padx=6, pady=6)

        self.__lower = ctk.CTkFrame(content)
        self.__lower.pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=True, padx=6, pady=6)

        self.__main_menu = Menu(self.__root)
        
        for menu in menus:
            self.__add_menu(*menu)

        self.__start_canvas(width=width, height=height)

        self.__add_select()

        self.__add_save()

        self.__root.config(menu = self.__main_menu)


    def __start_draw(self, event) -> None:
        self.__last_x, self.__last_y = event.x, event.y


    def __draw(self, event) -> None:
        if self.__last_x is not None and self.__last_y is not None:
            self.__canvas.create_line(self.__last_x, self.__last_y, event.x, event.y, 
                                     fill=self.__fill.get(), width=2, capstyle=ctk.ROUND, smooth=ctk.TRUE)
            try:
                self.__pil_draw.line([self.__last_x, self.__last_y, event.x, event.y],
                                 fill=self.__fill.get(), width=2)
            except Exception as e:
                print(e)
                pass
            
            self.__last_x, self.__last_y = event.x, event.y


    def __stop_draw(self, event) -> None:
        self.__last_x, self.__last_y = None, None


    def __start_canvas(self, width: int, height: int) -> None:
        self.__canvas = ctk.CTkCanvas(self.__upper, bg="white", width=width, height=height)
        self.__canvas.pack()

        self.__image_cache = None
        self.__canvas_photo = None

        self.__pil_image = Image.new("RGBA", (width, height), "WHITE")
        self.__pil_draw = ImageDraw.Draw(self.__pil_image)

        self.__last_x, self.__last_y = None, None

        self.__canvas.bind("<Button-1>", self.__start_draw)
        self.__canvas.bind("<B1-Motion>", self.__draw)
        self.__canvas.bind("<ButtonRelease-1>", self.__stop_draw)


    def __add_select(self) -> None:
        self.__fill = StringVar()
        cols: list = ["black", "red", "blue"]
        self.__fill.set("black")

        for color in cols:
            self.__radio = ctk.CTkRadioButton(self.__lower, text=color, value=color, 
                                              variable=self.__fill, corner_radius=10).pack(side=LEFT)


    def __add_menu(self, label: any, items: list) -> None:
        men = Menu(self.__main_menu, tearoff=0)
        self.__main_menu.add_cascade(label=label, menu = men, font=("Arial", 16))

        for item in items:
            men.add_command(label= item[0], command=item[1])


    def __list_files(self) -> list:
        images: list = []
        
        for file in os.listdir(self.__SAVE_DIR):
            if file.endswith('.png') or file.endswith('.jpg'):
                images.append(file)
        return images


    def __open_file(self, wind, event) -> None:        
        image = self.__image_cache

        canvas_w = self.__canvas.winfo_width()
        canvas_h = self.__canvas.winfo_height()
        if not canvas_w or not canvas_h:
            try:
                canvas_w = int(self.__canvas['width'])
                canvas_h = int(self.__canvas['height'])
            except Exception:
                canvas_w, canvas_h = 600, 400

        img_w, img_h = image.size
        ratio = min(canvas_w / img_w, canvas_h / img_h, 1.0)
        new_size = (max(1, int(img_w * ratio)), max(1, int(img_h * ratio)))
        if new_size != image.size:
            image = image.resize(new_size, Image.LANCZOS)

        image = ImageTk.PhotoImage(image)
        self.__canvas_photo = image

        try:
            self.__pil_image.paste(image, (x, y), image)
        except Exception:
            try:
                self.__pil_image.paste(image.convert("RGBA"), (x, y))
            except Exception:
                pass

        self.__canvas.delete("all")
        x = (canvas_w - new_size[0]) // 2
        y = (canvas_h - new_size[1]) // 2
        self.__canvas.create_image(x, y, anchor=ctk.NW, image=self.__canvas_photo)

        wind.destroy()


    def __preview_file(self, wind, event) -> None :
        selection = event.widget

        current: int = selection.curselection()

        try:
            current: str = selection.get(current)
        except Exception:
            return

        preview_frame = getattr(wind, "preview_frame", None)

        prev = getattr(wind, "preview", None)
        if prev is not None:
            try:
                prev.destroy()
            except Exception:
                pass
            wind.preview = None

        try:
            image = self.__read_image(current)
            image.thumbnail((350, 250), Image.LANCZOS)
            image = ctk.CTkImage(light_image=image, dark_image=image, size=(image.width, image.height))
            lab = ctk.CTkLabel(preview_frame, image=image, text="")
            lab.pack(side=ctk.BOTTOM, expand=True)
            lab.image=image
            wind.preview = lab
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)
            pass


    def __file_select(self) -> None:
        wind = ctk.CTkToplevel(self.__root)
        wind.title("Select file")
        wind.geometry("700x400")

        content = ctk.CTkFrame(wind)
        content.pack(fill=ctk.BOTH, expand=True)

        left = ctk.CTkFrame(content)
        left.pack(side=ctk.LEFT, fill=ctk.Y, padx=6, pady=6)

        right = ctk.CTkFrame(content)
        right.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=6, pady=6)

        wind.preview_frame = right

        selection = CTkListbox(master=left)
        selection.pack(side=ctk.LEFT, fill=ctk.Y, padx=6, pady=6)

        selection.bind('<<ListboxSelect>>', partial(self.__preview_file, wind))
        selection.bind('<Double-1>', partial(self.__open_file, wind))

        for file in self.__list_files():
            selection.insert(ctk.END, file)


    def __read_image(self, filename: str) -> Image:
        path = self.__SAVE_DIR + filename
        try:
            image = Image.open(path).convert("RGBA")
            self.__image_cache = image
            return image.copy()
        except Exception:
            return
        
    def __add_save(self) -> None:
        def prevent_default(event):
            self.__save_canvas()
            return "break"

        save_file_btn = ctk.CTkButton(self.__lower, text="Save", command=self.__save_canvas, width=75)
        save_file_btn.pack(side=ctk.RIGHT, padx=5)

        self.__filename_field = ctk.CTkTextbox(self.__lower, width=200, height=10)
        self.__filename_field.pack(side=ctk.RIGHT)
        self.__filename_field.bind("<Return>", command=prevent_default)

    
    def __save_canvas(self) -> None:
        name = self.__filename_field.get('0.0', 'end').strip()
        if not name:
            name = "default"
        filename = self.__SAVE_DIR + name + ".png"

        try:
            self.__pil_image.save(filename, "PNG")
            print(f"Image saved as {filename}")
        except Exception as e:
            print("Failed to save image:", e)


    def run(self) -> None:
        self.__root.mainloop()


if __name__ == "__main__":
    gm = GridMake()
    gm.run()
