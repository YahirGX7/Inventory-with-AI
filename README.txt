This project is an inventory management system that uses
computer vision to automatically identify products and track their stock levels. 

To use the system, simply place a product in front of the camera and ensure that it is fully visible.
There is three buttons:

1. Añadir cantidad!: Click this button to add a specified quantity of the identified product to your inventory.

2. Borrar cantidad!: Click this button to remove a specified quantity of the identified product from your inventory.

3. Buscar producto!: Click this button to display information about the identified product, including its name, price, and current stock level.

The predictions of the model provided here are limited due it was trained with a small dataset, if you want to use your own model, replace the path in the atribute
"self.MODEL" in the UsingAI class, also if you model don't use custom layers of tensorflow hub (like MobileNetV2) delete the "custom_objects" parameter.
Also don't forget to change the path to the config.json file in the DB_pymysql class.
The proyect explicity uses MobileNetV2, so if you use another model different of here provided, you need to change the way you preprocces the image in the function "ProccesImageProduct" in the class UsingAI in UsedClasses.py

The table that you need for this to work, can be created with the next code in MySQL Workbench:

create database IA_inventario;

create table Productos_Precios(
    id int not null auto_increment,
    Producto varchar(255),
    Precio float,
    primary key (id)
);
  
