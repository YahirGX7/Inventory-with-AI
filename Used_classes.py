import pymysql
import tensorflow as tf
import tensorflow_hub as hub 
from tensorflow import keras
import numpy as np
import tkinter.messagebox as messagebox
import cv2
import json

#Create a class that help us to connect to MySQL database and do the pertinent operations
class DB_pymysql():
    def __init__(self):
        #We load a json file to set the variables to the connection and create the connection itself in self.connection
        self.file = open("./config.json", "r")
        self.config = json.load(self.file)
        self.connection = self.conn()

    #Function that return a connection object if all ok using the variables in config.json, otherwise it show us the error in a tkinter message box
    def conn(self):
        try:
            conn = pymysql.connect(host=self.config["host"],
                        port=self.config["puerto"],
                        user=self.config["usuario"],
                        password=self.config["contraseña"],
                        database=self.config["database"])
            return conn

        except Exception as e:
            messagebox.showerror("Error al conectar a MySQL", e)

    #Function to get the cursor object of the database    
    def cur(self):
        return self.connection.cursor()

    #This confirms the operations that we we're doing, like inserts or updates    
    def comm(self):
        self.connection.commit()

#Create a class to let us use an AI model to identify the product
class UsingAI():
    def __init__(self):
        #Setting up all the things we need, like load the model, the cursor of database and tensorflow tools to preprocess the images
        self.DB = DB_pymysql()
        self.MODEL = keras.models.load_model("./hya2.h5", custom_objects={"KerasLayer": hub.KerasLayer})
        self.Preproccesing = tf.keras.preprocessing.image
        self.MobileNetV2 = tf.keras.applications.mobilenet_v2
        self.cursor = self.DB.cur()

    #This function uses the frame readed from the webcam and preprocess it to give it to model
    def ProccesImageProduct(self, frame):
        try:
            converted_image = cv2.resize(frame, (224, 224))
            image_array2 = np.expand_dims(converted_image, axis=0) #Agrega una dimensión extra para representar el batch de imágenes 
            image_preprocessed = self.MobileNetV2.preprocess_input(image_array2)
            return image_preprocessed
        
        except Exception as e:
            messagebox.showerror("Error en ProccesImageProduct", e)

    #This makes and return the prediction of the product with the image preprocessed
    def MakingPredictions(self, image_preprocessed):
        try:
            predictions = self.MODEL.predict(image_preprocessed)
            predicts = np.argmax(predictions)
            return predicts
        
        except Exception as e:
            messagebox.showerror("Error en MakingPredictions", e)
    
    #Adds the product where the id coincides with the prediction
    def AddingProducts(self, predicted, quantity):
        try:
            sql = "UPDATE Productos_Precios SET Cantidad = Cantidad + %s WHERE id = %s;"
            self.cursor.execute(sql, (quantity, predicted))
            self.DB.comm()
            messagebox.showinfo("Hecho!", "Cantidad añadida con exito!")

        except Exception as e:
            messagebox.showerror("Error en AddingProducts", e)

    #Deletes the product where the id coincides with the prediction
    def DeletingProducts(self, predicted, quantity):
        try:
            sql = "UPDATE Productos_Precios SET Cantidad = Cantidad - %s WHERE id = %s;"
            self.cursor.execute(sql, (quantity, predicted))
            self.DB.comm()
            messagebox.showinfo("Hecho!", "Cantidad eliminada con exito!")

        except Exception as e:
            messagebox.showerror("Error en DeletingProducts", e)

    #Search the product where the id coincides with the prediction, and it shows the product, price and stock in a tkinter message box
    def SearchingProducts(self, predicted):
        try:
            sql = "select Producto, Precio, Cantidad from Productos_Precios WHERE id = %s;"
            self.cursor.execute(sql, (predicted))
            Product = self.cursor.fetchone()
            return Product
        
        except Exception as e:
            messagebox.showerror("Error en SearchingProducts", e)



    

        