def ejecutar_simulacion(cant_procesos, intervalo_llegada, ram_size=100, cpu_speed=1, num_cpus=1):
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    ram = simpy.Container(env, init=ram_size, capacity=ram_size)
    cpu = simpy.Resource(env, capacity=num_cpus)
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

# Ejemplo de uso para las diferentes estrategias de optimización
ram_sizes = [200, 100]
cpu_speeds = [1, 6]
num_cpus_list = [1, 2]

for ram_size in ram_sizes:
    for cpu_speed in cpu_speeds:
        for num_cpus in num_cpus_list:
            tiempos_promedio_opt = []
            desviaciones_estandar_opt = []
            
            for cant in cant_procesos:
                tiempos_opt = []
                for intervalo in intervalos_llegada:
                    tiempos_opt.extend(ejecutar_simulacion(cant, intervalo, ram_size, cpu_speed, num_cpus))
                tiempos_promedio_opt.append(np.mean(tiempos_opt))
                desviaciones_estandar_opt.append(np.std(tiempos_opt))
            
            # Graficar resultados para cada estrategia de optimización
            plt.errorbar(cant_procesos, tiempos_promedio_opt, yerr=desviaciones_estandar_opt, fmt='o')
            plt.xlabel('Número de procesos')
            plt.ylabel('Tiempo promedio en la computadora')
            plt.title(f'Tiempo promedio de proceso vs. Número de procesos (RAM={ram_size}, CPU={cpu_speed}, CPUs={num_cpus})')
            plt.grid(True)
            plt.show()
