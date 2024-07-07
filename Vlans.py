def verificar_vlan(vlan):
  if 0 <= vlan <= 99:
    return "VLAN simple"
  elif 100  <= vlan <= 199:
    return "VLAN extendida"

vlan = int(input("Ingresa el número de VLAN: "))

tipo_vlan = verificar_vlan(vlan)
print("la VLAN {vlan} es {tipo_vlan}")
