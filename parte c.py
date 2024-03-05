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

def ejecutar_simulacion(cant_procesos, intervalo_llegada, ram_size=100, cpu_speed=1, num_cpus=1):
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    ram = simpy.Container(env, init=ram_size, capacity=ram_size)
    cpu = simpy.Resource(env, capacity=num_cpus)
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
intervalos_llegada = 10


ram_size_estrategia_1 = 200
tiempos_promedio_estrategia_1 = []
desviaciones_estandar_estrategia_1 = []

for cant in cant_procesos:
    tiempos_estrategia_1 = ejecutar_simulacion(cant, intervalos_llegada, ram_size_estrategia_1)
    tiempos_promedio_estrategia_1.append(np.mean(tiempos_estrategia_1))
    desviaciones_estandar_estrategia_1.append(np.std(tiempos_estrategia_1))


plt.errorbar(cant_procesos, tiempos_promedio_estrategia_1, yerr=desviaciones_estandar_estrategia_1, fmt='o')
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio en la computadora')
plt.title('Estrategia 1: Tiempo promedio de proceso vs. Número de procesos (RAM=200)')
plt.grid(True)
plt.show()


cpu_speed_estrategia_2 = 6
tiempos_promedio_estrategia_2 = []
desviaciones_estandar_estrategia_2 = []

for cant in cant_procesos:
    tiempos_estrategia_2 = ejecutar_simulacion(cant, intervalos_llegada, cpu_speed=cpu_speed_estrategia_2)
    tiempos_promedio_estrategia_2.append(np.mean(tiempos_estrategia_2))
    desviaciones_estandar_estrategia_2.append(np.std(tiempos_estrategia_2))


plt.errorbar(cant_procesos, tiempos_promedio_estrategia_2, yerr=desviaciones_estandar_estrategia_2, fmt='o')
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio en la computadora')
plt.title('Estrategia 2: Tiempo promedio de proceso vs. Número de procesos (CPU=6 instrucciones por unidad de tiempo)')
plt.grid(True)
plt.show()


num_cpus_estrategia_3 = 2
tiempos_promedio_estrategia_3 = []
desviaciones_estandar_estrategia_3 = []

for cant in cant_procesos:
    tiempos_estrategia_3 = ejecutar_simulacion(cant, intervalos_llegada, num_cpus=num_cpus_estrategia_3)
    tiempos_promedio_estrategia_3.append(np.mean(tiempos_estrategia_3))
    desviaciones_estandar_estrategia_3.append(np.std(tiempos_estrategia_3))


plt.errorbar(cant_procesos, tiempos_promedio_estrategia_3, yerr=desviaciones_estandar_estrategia_3, fmt='o')
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio en la computadora')
plt.title('Estrategia 3: Tiempo promedio de proceso vs. Número de procesos (2 CPUs)')
plt.grid(True)
plt.show()
