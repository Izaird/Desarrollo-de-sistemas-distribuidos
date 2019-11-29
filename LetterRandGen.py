import random #Generador de archivos con numeros random
import string
random.choice(string.ascii_lowercase)
random.seed(12)
n_archivos= int(input("¿Cuantos archivos deseas generar?"))
randfile = [None]*n_archivos
for j in range(0 , n_archivos ):
    randfile[j] = open("RandFiles/RandomArrs" + str(j) + ".txt", "w+" )
    n=int(input('How many to generate?: '))
    for i in range(0,n):
        if(i==n-1):
            line = random.choice(string.ascii_lowercase)
            randfile[j].write(line)
        else:
            line = random.choice(string.ascii_lowercase)
            randfile[j].write(line)
    #print(line)
for j in range(0 , n_archivos ):
    randfile[j].close()
