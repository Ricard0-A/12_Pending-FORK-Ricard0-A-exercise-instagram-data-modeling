import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, Table #Table en caso de usar V2 
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# ORDEN :  UNO A UNO ;  UNO A MUCHOS ; MUCHOS A MUCHOS----------------------------------------------------------


# RELATIONSHIP MUCHOS A MUCHOS (V1) --------------------------------------------------------------------

# RESUMIENDO: Una PERSONA puede comprar muchos dulces y los DULCES pueden ser comprados por muchas PERSONAS
# asi que en este caso complejo ya se recomienda una tabla extra como intermediaria entre ambas



class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(55), nullable=True, unique=True)
    asociation = relationship('Asociation', back_populates='customer') # Relationship => Name_Class


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(77), nullable=False)
    price = Column(Float, nullable=False, default=1000)
    asociation = relationship('Asociation', back_populates='product') 
    

class Asociation(Base):
    __tablename__ = 'customer_products'
    id = Column(Integer, nullable=False, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id')) # Foreignkey => tablename.id
    product_id  = Column(Integer, ForeignKey('products.id'))
    customer = relationship('Customer', back_populates='asociation') 
    product = relationship('Product', back_populates='asociation')


# RELATIONSHIP MUCHOS A MUCHOS (V2) --------------------------------------------------------------------

asociation_table = Table(
    'asociation',
    Base.metadata,
    Column('customer_id', ForeignKey('customers.id')),
    Column('product_id', ForeignKey('products.id'))
)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(55), nullable=True, unique=True)
    products = relationship('Product', secondary='asociation_table', back_populates='customers')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(77), nullable=False)
    price = Column(Float, nullable=False, default=1000)
    customers = relationship('Customer', secondary='asociation_table', back_populates='products')




# RELATIONSHIP UNO A MUCHOS-------------------------------------------------------------------------------------

# RESUMIENDO: "Un USER puede tener muchos POST, pero cada POST puede pertenecer solo a un USER"
# Y POR ESO SE USA FOREIGN KEY en POST, por que cada post va a pertenecer a cada usuario, digamos 
# que el hijo deberia llevar la foreignkey, No el padre osea que el padre no lleva foreign Key! 
# Ojo que solo en el ambito de relacion uno a muchos

# Integridad referencial: La clave foránea es como un "enlace" que conecta las dos 
# tablas. Al colocarla en la tabla hija, aseguramos que los valores de esta clave
# existan en la tabla padre. Y no alreves por que un usuario no va a pertenecer a cada post

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False )
    name = Column(String(88), nullable=True, unique=True )
    email = Column(String(88), nullable=True, unique=True )
    post = relationship('Post', back_populates='user_id', userList=False) # Relationship siempre apunta al nombre de la otra Clase
    # Si userList estuviera en False, esto seria relacion uno a uno

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False )
    title = Column(String(77), nullable=True, unique=False, )
    content = Column(String(99), nullable=True, unique=False)
    user_id = Column(Integer, ForeignKey('users.id')) #Foreignkey siempre apunta al tablename
    user = relationship('User', back_populates='post') #Backpopulates, siempre al otro atributo relationship de la otra clase



# RELATIONSHIP UNO A UNO-----------------------------------------------------------------------------------------

# class Parents(Base):
#     __tablename__ = 'parents'
#     id = Column(Integer, primary_key=True)
#     nombre = Column(String(80), nullable=True)

        
#     # Le llamo child por que esa va a ser su relacion desde parents...con Child.
#     #  
#     # Pero el valor de back_populates, debe ser Parents, PORQUE me estoy refiriendo
#     # que va transladarse hasta el otro atributo que tambien relaciona, y ese atributo se llama 
#     # parents ! ( Linea 34)
#     child = relationship('Child', back_populates='parents')

#     def __repr__(self):
#         return f"Interviewing Parents's ID ? {self.id}"                      


# class Child(Base):
#     __tablename__ = 'children'
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String(80), nullable=True)
    
#     parent_id = Column(Integer, ForeignKey('parents.id'))

#     parents = relationship('Parents', back_populates='child')

# ------------------------------------------------------------------------------------------------------------


# RELACION GENERAL DE EJEMPLO ---------------------------------------------------------------------------


# Esta clase es para crear 1 tabla
# class Person(Base):
#     __tablename__ = 'person'
#     id = Column(Integer, primary_key=True) #A la vez que instanciamos id a la clase Column, le sigue sus argumentos para que la clase Column funcione bn
#     name = Column(String(80), default='AIA')
#     email = Column(String(80), nullable=True  ,unique=True)


#     # Ojo  interesante para convertir a json al usar flask para consultar base de datos
#     def serialize(self):
#         return {
#             "id" : self.id
#         }


# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)


#     # Estos 2 codigo son para relacionar tablas

      # Va a buscar a la tablename con id       
#     person_id = Column(Integer, ForeignKey('person.id')) #El famoso foreignKey
#     # Va a buscar el nombre de la Clase de la tabla, no el tablename 
#     person = relationship(Person) #La relacion directa

# -------------------------------------------------------------------------------------------------

# # Este codigo es para transferir codigo sqlalchemy hasta un diagrama grafico, osea esto 
# # es relevante pero de forma dinamica 
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e


# TIPS-------------------------------------------------------------------------------------------------



# 1- Un usuario puede tener muchos posts pero cada post solo puede pertenecer a un usuario!.

# Esto significa que en Users no necesitas referenciar cada post individualmente, porque sería redundante 
# (¿imaginas tener una columna que contenga todos los IDs de los posts en Users? ¡Sería un caos!).

# 2- En el back_popular siempre se pone el atributo relationship de la otra clase que quieres relacionar
# aunque sea confuso escribirlo, hazlo

# 3- ForeignKey apunta al nombre de la tabla que quieres vincular y ademas con .id , accedes al ID de esa tabla 

# 4- Relationship en su primer armento pones el nombre de la CLase de la otra tabla , para vincular
