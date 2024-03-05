import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 42
RAM_SIZE = 100
CPU_SPEED = 1  # 3 instrucciones por unidad de tiempo

class Proceso:
    def __init__(self, env, ram, cpu):
        self.env = env
        self.ram = ram
        self.cpu = cpu
        self.instructions_left = random.randint(1, 10)
        self.creation_time = env.now
        self.end_time = None

    def run(self):
        while self.instructions_left > 0:
            with self.cpu.request() as req:
                yield req
                yield self.env.timeout(CPU_SPEED)
                self.instructions_left -= 3 if self.instructions_left >= 3 else self.instructions_left

        self.end_time = self.env.now

def ejecutar_simulacion(cant_procesos, intervalo_llegada):
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    ram = simpy.Container(env, init=RAM_SIZE, capacity=RAM_SIZE)
    cpu = simpy.Resource(env, capacity=1)
    tiempos_procesos = []

    def proceso_generator(env, ram, cpu):
        for _ in range(cant_procesos):
            proceso = Proceso(env, ram, cpu)
            env.process(proceso.run())
            yield env.timeout(random.expovariate(1.0 / intervalo_llegada))

    env.process(proceso_generator(env, ram, cpu))
    env.run()

    for proceso in env.processes:
        if isinstance(proceso, Proceso):
            tiempos_procesos.append(proceso.end_time - proceso.creation_time)

    return tiempos_procesos

# Ejemplo de uso
tiempos_promedio = []
desviaciones_estandar = []
cant_procesos = [25, 50, 100, 150, 200]
intervalos_llegada = [10, 5, 1]

for cant in cant_procesos:
    tiempos = []
    for intervalo in intervalos_llegada:
        tiempos.extend(ejecutar_simulacion(cant, intervalo))
    tiempos_promedio.append(np.mean(tiempos))
    desviaciones_estandar.append(np.std(tiempos))

# Graficar resultados para la parte "a"
plt.errorbar(cant_procesos, tiempos_promedio, yerr=desviaciones_estandar, fmt='o')
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio en la computadora')
plt.title('Tiempo promedio de proceso vs. Número de procesos')
plt.grid(True)
plt.show()

# Ejecutar simulación y graficar resultados para los nuevos intervalos de llegada
intervalos_llegada_nuevos = [5, 1]

tiempos_promedio_nuevos = []
desviaciones_estandar_nuevas = []

for cant in cant_procesos:
    tiempos_nuevos = []
    for intervalo_nuevo in intervalos_llegada_nuevos:
        tiempos_nuevos.extend(ejecutar_simulacion(cant, intervalo_nuevo))
    tiempos_promedio_nuevos.append(np.mean(tiempos_nuevos))
    desviaciones_estandar_nuevas.append(np.std(tiempos_nuevos))

plt.errorbar(cant_procesos, tiempos_promedio_nuevos, yerr=desviaciones_estandar_nuevas, fmt='o')
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio en la computadora')
plt.title('Tiempo promedio de proceso vs. Número de procesos (nuevos intervalos)')
plt.grid(True)
plt.show()
