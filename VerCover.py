import requests
from PIL import Image#, ImageTk
#import tkinter as tk

#root = tk.Tk()

imageURL = "https://image.tmdb.org/t/p/w200/z9UUfYZzKVBCEFs6TnCdAp5mUbJ.jpg"

response = requests.get(imageURL, stream=True)
response.raw.decode_content = True
photo = Image.open(response.raw)
#photo = ImageTk.PhotoImage(image=Image.open(response.raw))
#label = tk.Label(image=photo).pack()

#root.mainloop()
#photo.save('pelis/imagen.jpg')

photo.show()