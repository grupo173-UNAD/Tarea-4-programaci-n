from abc import ABC, abstractmethod
from datetime import datetime

#------------------
#MANEJO DE LOGS
#------------------
def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")

#-----------------
#EXEPCIONES PERSONALIZADAS
#--------------------------
class ClienteError(Exception):
    pass
class ServicioError(Exception):
    pass
class ReservaError(Exception):
    pass

#----------------------
#CLASE ABSTRACTA GENERAL
#------------------------
class EntidadSistema(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass

#-----------------------
# CLASE CLIENTE
# ---------------
class Cliente(EntidadSistema):

    def __init__(self, nombre, correo):
        try:
            if not nombre.strip():
                raise ClienteError("El nombre no puede estar vacio")

            if "@" not in correo:
                raise ClienteError("Correo invalido")

            self.__nombre = nombre
            self.__correo = correo

            registrar_log(f"Cliente registrado: {nombre}")

        except Exception as e:
            registrar_log(f"Error creando cliente: {e}")
            raise

#---------
# ENCAPSULACION
# ----------------
@property
def nombre(self):
    return self.__nombre

@property
def correo(self):
    return self.__correo

def mostrar_info(self):
    return f"Cliente: {self.__nombre} - {self.__correo}"

#------------
#CLASE ABSTRACTA SERVICIO
#--------------------------
class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):
        if tarifa_base <= 0:
            raise ServicioError("La tarifa debe ser positiva")
        
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, horas, descuento=0):
        pass

    @abstractmethod
    def descripcion(self):
        pass

#-------------------
#servicio salas
#--------------------
class ReservaSala(Servicio):

    def calcular_costo(self, horas, descuento=0):
        total = self.tarifa_base * horas
        total -= total * descuento
        return total
    
    def descripcion(self):
        return "Servicio de reserva de salas"
    
#-------------
#SERVICIO DE EQUIPOS
#---------------------
class AlquilerEquipos(Servicio):

    def calcular_costo(self, horas, descuento=0):
        impuesto = 0.19
        total = (self.tarifa_base * horas)
        total += total * impuesto
        total -= total * descuento
        return total
    
    def descripcion(self):
        return "Servicio de alquiler de equipos"
    
#------------
#SERVICIO DE ASESORIAS
#----------------------
class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas, descuento=0):
        impuesto = 50000
        total = (self.tarifa_base * horas) + extra
        total -= total * descuento
        return total
    
    def descripcion(self):
        return "Servicio de asesoria especializada"
    
#--------------
#CLASE RESERVA
#------------------
class Reserva:

    def __init__(self, cliente, servicio, horas):
        
        try:

            if not isinstance(cliente, Cliente):
                raise ReservaError("Cliente invalido")
            
            if not isinstance(servicio, Servicio):
                raise ReservaError("Servicio invalido")
            
            if horas <= 0:
                raise ReservaError("La duracion debe ser positiva")
            
            self.cliente = cliente
            self.servicio = servicio
            self.horas = horas
            self.estado = "pendiente"

            registrar_log(f"Reserva creada para {cliente.nombre}")

        except Exception as e:
            registrar_log(f"Error creando reserva: {e}")
            raise

    def confirmar(self):

        try:
            self.estado = "confirmada"
            registrar_log(f"Reserva confirmada para {self.cliente.nombre}")

        except Exception as e:
            registrar_log(f"Error confirmado reserva: {e}")

    def cancelar(self):

        try:
            self.estado = "cancelada"
            registrar_log(f"Reserva cancelada para {self.cliente.nombre}")

        except Exception as e:
            registrar_log(f"Error cancelado reserva: {e}")

    def procesar_pago(self, descuento=0):

        try:
            costo = self.servicio.calcular_costo(self.horas, descuento)

        except Exception as e:
            raise ReservaError("Error calculando el costo") from e
        
        else:
            registrar_log(f"Pago procesado: {costo}")
            return costo
        
        finally:
            registrar_log("Finalizo proceso de pago")

#---------------
#SIMULACION DE OPERACIONES
#-------------------------
clientes = []
reservas = []

print("\n===== SIMULACION DEL SISTEMA =====\n")

operaciones = [

    #Clientes validos
    ("cliente", "juan", "juan@gmail.com"),
    ("cliente", "Ana", "ana@hotmail.com"),

    #cliente invalido
    ("cliente", "", "correo_invalido"),

    #servicios validos
    ("servicio", "sala", 80000),
    ("servicio", "equipo", 50000),
    ("servicio", "asesoria", 120000),

    #Servicio invalido
    ("servicio", "sala", -1000),
]

servicios = []

#--------------------
#CREACION DE CLIENTES Y SERVICIOS
#------------------------------
for op in operaciones:

    try:

        if op[0] == "cliente":

            cliente = Cliente(op[1], op[2])
            clientes.append(cliente)

            print("Cliente creado correctamente")

        elif op[0] == "servicio":

            tipo = op[1]
            tarifa = op[2]

            if tipo == "sala":
                s = ReservaSala("Sala VIP", tarifa)

            elif tipo == "equipo":
                s = AlquilerEquipo("Computador Gamer", tarifa)

            elif tipo == "asesoria":
                s = AsesoriaEspecializada("Consultoria IA", tarifa)

            servicios.append(s)

            print("Servicio creado correctamente")

    except Exception as e:
        print("Error:", e)

#-------------------
#RESERVAS
#-----------------
print("\n===== RESERVAS =====\n")

try:

    r1 = Reserva(clientes[0], servicios[0], 3)
    r1.confirmar()

    costo = r1.procesar_pago(0.1)

    print("Costo reserva 1:", costo)

    reservas.append(r1)

except Exception as e:
    print("Error reserva 1:", e)

try:

    r2 = Reserva(clientes[1], servicios[1], 5)
    r2.confirmar()

    costo = r2.procesar_pago()

    print("Costo reserva 2:", costo)

    reservas.append(r2)

except Exception as e:
    print("Error reserva 2:", e)

#Reserva invalida
try:

    r3 = Reserva("Cliente falso", servicios[0], -2)

except Exception as e:
    print("Reserva fallida:", e)

#-----------------
#MOSTRAR DATOS
#--------------------
print("\n===== CLIENTES =====\n")

for c in clientes:
    print(c.mostrar_info())

print("\n ===== RESERVAS EXITOSAS =====\n")

for r in reservas:
    print(r.cliente.nombre, "-", r.servicio.descripcion(), "- Estado:", r.estado)

print("\nSistema ejecutado correctamente.")