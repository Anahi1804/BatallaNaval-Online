import sys
import Ice
import Juego

class MotorMultijugadorI(Juego.MotorMultijugador):
    def __init__(self):
        self.jugadores_conectados = 0
        self.max_jugadores = 0
        self.jugadores_listos = 0
        self.turno_actual = 1
        self.disparos_hechos_este_turno = 0
        
        # Matriz pública de disparos: 0 (Niebla), -1 (Agua), >0 (ID del jugador impactado)
        self.matriz_disparos = []
        
        

        # Flotas secretas: Diccionario de listas para esconder los barcos
        self.flotas = {} 
        self.vidas = {}
        self.puntajes = {}
        self.jugadores_vivos = 0

    def registrarJugador(self, total_esperados, current=None):
        if self.max_jugadores == 0:
            self.max_jugadores = total_esperados
            # ¡Redujimos el mapa! Cambiamos el 5 por un 3
            tamano_cuadricula = self.max_jugadores * 3 
            self.matriz_disparos = [[0 for _ in range(tamano_cuadricula)] for _ in range(tamano_cuadricula)]
        
        self.jugadores_conectados += 1
        id_jugador = self.jugadores_conectados
        
        self.flotas[id_jugador] = []
        self.vidas[id_jugador] = 10  
        self.puntajes[id_jugador] = 0
        self.jugadores_vivos += 1
        return id_jugador

    def obtenerCantidadConectados(self, current=None): return self.jugadores_conectados
    def obtenerMaxJugadores(self, current=None): return self.max_jugadores
    
    def colocarBarco(self, idJugador, x, y, current=None):
        # Guardamos en su flota secreta. Validamos que él mismo no ponga 2 barcos en la misma casilla
        if (x, y) not in self.flotas[idJugador]:
            self.flotas[idJugador].append((x, y))
            return True
        return False

    def declararListo(self, idJugador, current=None):
        self.jugadores_listos += 1

    def todosListos(self, current=None):
        return self.jugadores_listos == self.max_jugadores and self.max_jugadores > 0

    def deQuienEsElTurno(self, current=None):
        return self.turno_actual

    def avanzar_turno(self):
        self.turno_actual += 1
        if self.turno_actual > self.max_jugadores: self.turno_actual = 1
        while self.vidas[self.turno_actual] <= 0 and self.jugadores_vivos > 1:
            self.turno_actual += 1
            if self.turno_actual > self.max_jugadores: self.turno_actual = 1

    def disparar(self, idJugador, x, y, current=None):
        if idJugador != self.turno_actual or self.jugadores_vivos <= 1:
            return 8 

        # ¡ELIMINAMOS EL CAMPO DE FUERZA! 
        # Ya no bloqueamos la casilla. Todos pueden disparar donde sea.

        impacto = False
        ids_impactados = ""

        # Revisamos todas las flotas para ver a quién le damos
        for propietario_id, barcos in self.flotas.items():
            if propietario_id != idJugador and (x, y) in barcos:
                barcos.remove((x, y)) 
                self.vidas[propietario_id] -= 1
                self.puntajes[idJugador] += 1
                
                impacto = True
                ids_impactados += str(propietario_id) 
                
                if self.vidas[propietario_id] == 0:
                    self.jugadores_vivos -= 1

        # --- LÓGICA DEL RADAR PÚBLICO ---
        if impacto:
            valor_anterior = self.matriz_disparos[x][y]
            # Si ya había muertos ahí (ej. un 2), y matamos al 3, se vuelve "23"
            if valor_anterior > 0:
                nuevo_valor = str(valor_anterior) + ids_impactados
                self.matriz_disparos[x][y] = int(nuevo_valor)
                resultado = int(nuevo_valor)
            else:
                self.matriz_disparos[x][y] = int(ids_impactados)
                resultado = int(ids_impactados)
        else:
            # Si fallamos, SOLO marcamos como Agua (-1) si la casilla estaba virgen (0)
            # Si ya había una X roja ahí (>0), la dejamos intacta para no borrarla.
            if self.matriz_disparos[x][y] == 0:
                self.matriz_disparos[x][y] = -1 
            resultado = 0

        # Avanzamos los turnos
        self.disparos_hechos_este_turno += 1
        if self.disparos_hechos_este_turno >= (self.max_jugadores - 1):
            self.disparos_hechos_este_turno = 0
            self.avanzar_turno()

        return resultado
        if idJugador != self.turno_actual or self.jugadores_vivos <= 1:
            return 8 

        if self.matriz_disparos[x][y] != 0:
            return 8

        impacto = False
        ids_impactados = "" # Lo iniciamos vacío como texto

        # Revisamos TODAS las flotas buscando enemigos en esa coordenada
        for propietario_id, barcos in self.flotas.items():
            
            if propietario_id != idJugador and (x, y) in barcos:
                barcos.remove((x, y)) 
                self.vidas[propietario_id] -= 1
                self.puntajes[idJugador] += 1
                
                impacto = True
                # Pegamos el ID del enemigo al texto (Ej: si le damos al 2 y 4, dirá "24")
                ids_impactados += str(propietario_id) 
                
                if self.vidas[propietario_id] == 0:
                    self.jugadores_vivos -= 1

        # Actualizamos el radar
        if impacto:
            # Convertimos "24" a número entero para que Ice lo acepte
            self.matriz_disparos[x][y] = int(ids_impactados) 
            resultado = int(ids_impactados)
        else:
            self.matriz_disparos[x][y] = -1 
            resultado = 0

        self.disparos_hechos_este_turno += 1
        if self.disparos_hechos_este_turno >= (self.max_jugadores - 1):
            self.disparos_hechos_este_turno = 0
            self.avanzar_turno()

        return resultado

    def obtenerEstadoTablero(self, current=None): return self.matriz_disparos

    def obtenerGanador(self, current=None):
        if self.jugadores_vivos <= 1 and self.max_jugadores > 0 and self.jugadores_listos == self.max_jugadores:
            for id_jugador, v in self.vidas.items():
                if v > 0: return id_jugador
        return 0

    def obtenerMarcador(self, current=None):
        texto = "=== MARCADOR FINAL ===\n\n"
        for i in range(1, self.max_jugadores + 1):
            estado = "VIVO" if self.vidas[i] > 0 else "ELIMINADO"
            texto += f"Jugador {i} ({estado}): {self.puntajes[i]} destruidos\n"
        return texto

with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("BatallaAdapter", "default -h 0.0.0.0 -p 10000")
    adapter.add(MotorMultijugadorI(), Ice.stringToIdentity("TableroJuego"))
    adapter.activate()
    print("Servidor listo. Los barcos ahora son secretos.")
    communicator.waitForShutdown()