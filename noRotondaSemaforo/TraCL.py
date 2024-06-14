import traci
import sumolib
import sys
# Ruta a tu archivo sumo
sumoBinary = sumolib.checkBinary('sumo-gui') 
sumoCmd = [sumoBinary, "-c", "osm.sumocfg"]

# Iniciar TraCI
traci.start(sumoCmd)

# Diccionario para almacenar los datos
original_colors = {}
entry_times = {}
exit_times = {}
start_node = "E10"
end_node = "E12"

def promedio(entry_times,exit_times):
    suma = 0
    for key in entry_times.keys():
        if key in exit_times.keys():
            suma = suma + (exit_times[key] - entry_times[key])
        
    numCars = len(entry_times.keys())
    tiempoPromedio = suma / numCars
    return {'suma':suma,'numCars':numCars,'tiempoPromedio':tiempoPromedio}

try:
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep() # Avanza la simulación un paso
    

        for vehicle_id in traci.vehicle.getIDList():
            
            speed = traci.vehicle.getSpeed(vehicle_id)
            current_color = traci.vehicle.getColor(vehicle_id)
            current_edge = traci.vehicle.getRoadID(vehicle_id)
            
            if current_edge == start_node and vehicle_id not in entry_times:
                entry_times[vehicle_id] = traci.simulation.getTime()
                
            if current_edge == end_node and vehicle_id in entry_times and vehicle_id not in exit_times:
                 exit_times[vehicle_id] = traci.simulation.getTime()
                 
            if speed < 0.1:  # Consideramos que está detenido si la velocidad es menor a 0.1 m/s
                if vehicle_id not in original_colors:
                    # Almacena el color original si no está ya almacenado
                    original_colors[vehicle_id] = current_color
                # Cambia el color a rojo
                traci.vehicle.setColor(vehicle_id, (255, 0, 0, 255))  # Rojo
            else:
                if vehicle_id in original_colors:
                    # Restaura el color original
                    traci.vehicle.setColor(vehicle_id, original_colors[vehicle_id])
                    # Elimina el color original del diccionario una vez restaurado
                    del original_colors[vehicle_id]
        step += 1
        if step == 300:
            break                
finally:
    traci.close()    
    print(promedio(entry_times,exit_times))
    sys.exit()
    


