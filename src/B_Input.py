from A_Material import*

def skapa_indata():
    indata = input("Ange material och längd (ex: '13 stål, 40 betong'): ")
    lager_strängar = indata.split(',')
    materialdata = List()

    for i in lager_strängar:
        delar = i.split()
        längd = (float(delar[0]) / 1000 )
        material = delar[1]  

        if material == 'betong':
            materialdata.append((längd, 0)) #index 0 för att skapa_element funktionen ska koppla vilket material
        elif material == 'stål':
            materialdata.append((längd, 1))
        elif material == 'trä':
            materialdata.append((längd, 2))
        else:
            print("du skrev in något fel")

    return materialdata

if __name__ == '__main__':
    test = skapa_indata()
    print(test)

