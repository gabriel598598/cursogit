edad = int(input('introduce tu edad:'))

resultado1 = edad >= 20 and edad < 30
print(resultado1)
resultado2 = edad >=30 and edad < 40
print(resultado2)

if resultado1 or resultado2:
    print('dentro de rango (29\'s) o (30\')')
    if resultado1:
        print('dentro de los 20\'s')
    elif resultado2:
        print('dentro de los 30\'s')
    else:
        print('fuera de rango')
else:
    print("no esta dentro de los 20's ni 30's")