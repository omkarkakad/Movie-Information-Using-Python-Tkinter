from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import requests
import io

# API KEY
API_KEY = "fe127a5f"

root = Tk()
root.geometry("850x800+300+20")
root.title("🎬 Movie Info App")
theme_mode = "light"
root.configure(bg="linen")

# Fonts
HEADER_FONT = ("Arial", 28, "bold")
LABEL_FONT = ("Arial", 14, "bold")
TEXT_FONT = ("Arial", 12)

# Header
title_label = Label(root, text="🎬 Movie Info Finder", font=HEADER_FONT, bg="black", fg="white")
title_label.pack(fill=X)

# Search Frame
search_frame = Frame(root, bg="white", bd=2, relief=SOLID)
search_frame.pack(padx=30, pady=20, fill=X)

Label(search_frame, text="Enter Movie Name:", font=LABEL_FONT, bg="white").grid(row=0, column=0, padx=10, pady=15)
movie_entry = Entry(search_frame, font=("Arial", 18), width=30, relief=SOLID)
movie_entry.grid(row=0, column=1, padx=10, pady=15)

# Poster
poster_label = Label(root, bg="linen", relief=SOLID)
poster_label.pack(pady=20)

# Movie Info Text
info_text = Text(root, font=TEXT_FONT, width=80, height=15, wrap=WORD, bd=2, relief=SOLID)
info_text.pack(padx=20, pady=10)

# Fetch Movie Details
def fetch_movie():
    movie_name = movie_entry.get().strip()
    if not movie_name:
        showerror("Input Error", "Please enter a movie name.")
        return

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()

        if data["Response"] == "False":
            raise Exception(data["Error"])

        # Display Movie Info
        info = (
            f"🎬 Title: {data.get('Title', 'N/A')}\n"
            f"📅 Year: {data.get('Year', 'N/A')}\n"
            f"⭐ IMDB Rating: {data.get('imdbRating', 'N/A')}\n"
            f"🕒 Runtime: {data.get('Runtime', 'N/A')}\n"
            f"🎭 Genre: {data.get('Genre', 'N/A')}\n"
            f"🗣 Language: {data.get('Language', 'N/A')}\n"
            f"🎞 Director: {data.get('Director', 'N/A')}\n"
            f"👥 Actors: {data.get('Actors', 'N/A')}\n"
            f"📝 Plot:\n{data.get('Plot', 'N/A')}\n"
        )

        info_text.delete(1.0, END)
        info_text.insert(END, info)

        # Load Poster
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            img_data = requests.get(poster_url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((180, 250))
            photo = ImageTk.PhotoImage(img)
            poster_label.config(image=photo)
            poster_label.image = photo
        else:
            poster_label.config(image="", text="Poster Not Available")

    except Exception as e:
        showerror("Error", str(e))
        info_text.delete(1.0, END)
        poster_label.config(image="", text="")

# Theme Toggle
def toggle_theme():
    global theme_mode
    theme_mode = "dark" if theme_mode == "light" else "light"

    if theme_mode == "dark":
        root.config(bg="#1e1e1e")
        title_label.config(bg="#111", fg="white")
        search_frame.config(bg="#2d2d2d")
        movie_entry.config(bg="#3c3c3c", fg="white", insertbackground="white")
        info_text.config(bg="#2a2a2a", fg="white", insertbackground="white")
        poster_label.config(bg="#1e1e1e")
    else:
        root.config(bg="linen")
        title_label.config(bg="black", fg="white")
        search_frame.config(bg="white")
        movie_entry.config(bg="white", fg="black", insertbackground="black")
        info_text.config(bg="white", fg="black", insertbackground="black")
        poster_label.config(bg="linen")

# Button Frame
btn_frame = Frame(root, bg="linen")
btn_frame.pack(pady=20)

search_btn = Button(btn_frame, text="🔍 Search", font=LABEL_FONT, bg="green", fg="white", width=12, command=fetch_movie)
search_btn.pack(side=LEFT, padx=20)

theme_btn = Button(btn_frame, text="🌙 Toggle Theme", font=LABEL_FONT, bg="purple", fg="white", width=15, command=toggle_theme)
theme_btn.pack(side=LEFT, padx=20)

root.mainloop()
