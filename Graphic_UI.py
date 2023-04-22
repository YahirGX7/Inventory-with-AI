import tkinter as tk
from Used_classes import *
from PIL import Image, ImageTk
import cv2
import tkinter.messagebox as messagebox

#Creates the application object
class IA_with_Inventory(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        #Setting up all we need, like the UsingAI atribute, the int variables of the Entry labels, the video capture atribute, etc
        self.title = ("Inventario con IA y GUI")

        self.QuantityToDelete = tk.IntVar(self)
        self.QuantityToAdd = tk.IntVar(self)
        self.VideoReader = cv2.VideoCapture(0)
        self.VideoLabel = tk.Label(self)
        self.VideoLabel.pack(fill="both")
        self.UsedAI = UsingAI()
        self.init_widgets()
        self.Streaming()

    #With this funcion the app shows a Video Streaming in a tkinter label
    def Streaming(self):
        ret, Frame = self.VideoReader.read()
        if ret == True:
            try:
                cv2image = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
    
                self.VideoLabel.imgtk = imgtk
                self.VideoLabel.configure(image=imgtk)
                self.VideoLabel.after(50, self.Streaming)
    
            except Exception as e:
                messagebox.showerror("Error en Streaming", e)

    #This defines an AddedProducts funtion that takes the last frame in Video Streaming and adds a product using the value in the Entry label and self.UsedAI methods
    def AddedProducts(self, quantity):
        try:
            ret, frame = self.VideoReader.read()
            if ret == True:
                predictions = self.UsedAI.ProccesImageProduct(frame)
                prediction = self.UsedAI.MakingPredictions(predictions) 
                self.UsedAI.AddingProducts(prediction, quantity)

        except Exception as e:
            messagebox.showerror("Error en AddedProducts", e)

    #Function that takes the last frame in the Video Streaming and deletes the product using the value in the Entry label and self.UsedAI methods
    def DeletedProducts(self, quantity):
        try:
            ret, frame = self.VideoReader.read()
            if ret == True:
                predictions = self.UsedAI.ProccesImageProduct(frame)
                prediction = self.UsedAI.MakingPredictions(predictions) 
                self.UsedAI.DeletingProducts(prediction, quantity)

        except Exception as e:
            messagebox.showerror("Error en DeletedProducts", e)

    #Once again this takes the last frame of Video Streaming, and using the prediction shows the product, price and stock
    def SearchedProducts(self):
        try:
            ret, frame = self.VideoReader.read()
            if ret == True:
                predictions = self.UsedAI.ProccesImageProduct(frame)
                prediction = self.UsedAI.MakingPredictions(predictions) 
                product = self.UsedAI.SearchingProducts(prediction)
                messagebox.showinfo("Producto encontrado", f"Este es {product[0]}, el cual tiene un precio de {product[1]}MXN y se tiene un stock de {product[2]}")

        except Exception as e:
            messagebox.showerror("Error en SearchedProducts", e)

    #This defines the widgets to add, delete, search products and close the application
    def init_widgets(self):
        tk.Button(self, 
                  text="Añadir cantidad!",
                  command=lambda: self.AddedProducts(self.QuantityToAdd.get())
                  ).pack(
                    fill=tk.X,
                    side=tk.TOP,
                    padx=22,
                    pady=22)
        
        tk.Entry(self, 
                 textvariable=self.QuantityToAdd,
                 selectborderwidth=3
                 ).pack(fill=tk.X,
                    side=tk.TOP,
                    padx=22,
                    pady=22)
        
        tk.Button(self, 
                  text="Borrar cantidad!",
                  command=lambda: self.DeletedProducts(self.QuantityToDelete.get())
                  ).pack(
                    fill=tk.X,
                    side=tk.TOP,
                    padx=22,
                    pady=22)
        
        tk.Entry(self, 
                 textvariable=self.QuantityToDelete,
                 selectborderwidth=3
                 ).pack(fill=tk.X,
                    side=tk.TOP,
                    padx=22,
                    pady=22)
        
        tk.Button(self, 
                  text="Buscar producto!",
                  command=self.SearchedProducts
                  ).pack(
                    fill=tk.X,
                    side=tk.TOP,
                    padx=22,
                    pady=22)
        
        tk.Button(self, text="Salir",
                    activebackground="DeepSkyBlue2",
                    command=self.ClosingApp
                    ).pack(fill="x",
                        padx=30, 
                        pady=30, 
                        side="top")
    
    #This function release the webcam and close the app    
    def ClosingApp(self):
        self.VideoReader.release()
        self.destroy()