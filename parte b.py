import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 42
RAM_SIZE = 100
CPU_SPEED = 1  

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

    procesos = []
    def proceso_generator(env, ram, cpu):
        for _ in range(cant_procesos):
            proceso = Proceso(env, ram, cpu)
            procesos.append(proceso)
            env.process(proceso.run())
            yield env.timeout(random.expovariate(1.0 / intervalo_llegada))

    env.process(proceso_generator(env, ram, cpu))
    env.run()

    for proceso in procesos:
        tiempos_procesos.append(proceso.end_time - proceso.creation_time)

    return tiempos_procesos


cant_procesos = [25, 50, 100, 150, 200]
intervalos_llegada_nuevos = [5, 1] #intervalo más pequeño

for intervalo_nuevo in intervalos_llegada_nuevos:
    tiempos_promedio_nuevos = []
    desviaciones_estandar_nuevas = []

    for cant in cant_procesos:
        tiempos_nuevos = ejecutar_simulacion(cant, intervalo_nuevo)
        tiempos_promedio_nuevos.append(np.mean(tiempos_nuevos))
        desviaciones_estandar_nuevas.append(np.std(tiempos_nuevos))

   
    plt.errorbar(cant_procesos, tiempos_promedio_nuevos, yerr=desviaciones_estandar_nuevas, fmt='o')
    plt.xlabel('Número de procesos')
    plt.ylabel('Tiempo promedio en la computadora')
    plt.title(f'Tiempo promedio de proceso vs. Número de procesos (Intervalo de llegada={intervalo_nuevo})')
    plt.grid(True)
    plt.show()
