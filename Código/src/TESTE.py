texto = "marca: NVIDIA modelo: 30"

index = texto.index("marca:")

print(index)

print(index+1)

print(texto.split()[index+1])

print(texto.split()[index:index+1])