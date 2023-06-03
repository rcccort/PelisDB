import requests
from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()

imageURL = "https://image.tmdb.org/t/p/w200/z9UUfYZzKVBCEFs6TnCdAp5mUbJ.jpg"
imageURL2 = "https://image.tmdb.org/t/p/w200/7AEMH73JTb0qqAZgMj5orBGLUrO.jpg"

response = requests.get(imageURL, stream=True)
response.raw.decode_content = True
response2 = requests.get(imageURL2, stream=True)
response2.raw.decode_content = True
#photo = Image.open(response.raw)
photo = ImageTk.PhotoImage(image=Image.open(response.raw))
photo2 = ImageTk.PhotoImage(image=Image.open(response2.raw))
label = tk.Label(image=photo).grid(column=0, row=0)
label2 = tk.Label(image=photo2).grid(column=1, row=0)

root.mainloop()
#photo.save('pelis/imagen.jpg')

#photo.show()