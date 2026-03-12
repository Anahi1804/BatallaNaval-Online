import sys
import Ice
import tkinter as tk
from tkinter import simpledialog, messagebox
import Juego

BG_MAIN = "#2C3E50"      
COLOR_AGUA = "#34495E"   
COLOR_FALLO = "#95A5A6"  
COLOR_ACIERTO = "#E74C3C" 
COLOR_MIO = "#2ECC71"    
COLOR_TEXTO = "#ECF0F1"  

class ClienteBatallaNaval:
    def __init__(self, master, servidor):
        self.master = master
        self.servidor = servidor
        self.master.title("Batalla Naval Royale - Interfaz Dual")
        self.master.geometry("1000x550") # Ventana más ancha para dos tableros
        self.master.config(bg=BG_MAIN)
        
        self.mi_id = 0
        self.max_jugadores = 0
        self.fase = "LOBBY" 
        self.barcos_a_colocar = 10 # ¡5 Barcos!
        self.barcos_colocados = 0
        self.mis_coordenadas = [] # Guardamos dónde pusimos los nuestros
        
        self.botones_defensa = {} # Tablero izquierdo
        self.botones_ataque = {}  # Tablero derecho
        
        self.lbl_estado = tk.Label(master, text="Conectando...", font=("Verdana", 14, "bold"), bg=BG_MAIN, fg=COLOR_TEXTO)
        self.lbl_estado.pack(pady=10)
        
        # Contenedor principal para poner los tableros lado a lado
        self.frame_contenedor = tk.Frame(master, bg=BG_MAIN)
        self.frame_contenedor.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Panel Izquierdo (Mi Flota)
        self.frame_izq = tk.Frame(self.frame_contenedor, bg=BG_MAIN)
        self.frame_izq.pack(side=tk.LEFT, expand=True, fill="both", padx=10)
        tk.Label(self.frame_izq, text="TU FLOTA (Posición y Defensa)", bg=BG_MAIN, fg=COLOR_TEXTO).pack()
        self.grid_defensa = tk.Frame(self.frame_izq, bg=BG_MAIN)
        self.grid_defensa.pack(expand=True, fill="both")
        
        # Panel Derecho (Radar de Ataque)
        self.frame_der = tk.Frame(self.frame_contenedor, bg=BG_MAIN)
        self.frame_der.pack(side=tk.RIGHT, expand=True, fill="both", padx=10)
        tk.Label(self.frame_der, text="RADAR DE ATAQUE (Dispara aquí)", bg=BG_MAIN, fg=COLOR_TEXTO).pack()
        self.grid_ataque = tk.Frame(self.frame_der, bg=BG_MAIN)
        self.grid_ataque.pack(expand=True, fill="both")

        self.iniciar_conexion()

    def iniciar_conexion(self):
        max_servidor = self.servidor.obtenerMaxJugadores()
        esperados = max_servidor
        
        if max_servidor == 0:
            esperados = simpledialog.askinteger("Partida", "¿Cuántos jugadores?", minvalue=2, maxvalue=4)
            if not esperados: self.master.quit(); return
                
        self.mi_id = self.servidor.registrarJugador(esperados)
        self.max_jugadores = esperados
        self.actualizar_estado_periodicamente()

    def actualizar_estado_periodicamente(self):
        ganador = self.servidor.obtenerGanador()
        if ganador > 0:
            marcador = self.servidor.obtenerMarcador()
            messagebox.showinfo("Fin", f"¡EL JUGADOR {ganador} HA GANADO!\n\n{marcador}")
            self.master.quit(); return

        if self.fase == "LOBBY":
            conectados = self.servidor.obtenerCantidadConectados()
            if conectados == self.max_jugadores:
                self.fase = "POSICIONAMIENTO"
                self.lbl_estado.config(text=f"JUGADOR {self.mi_id} | Oculta tus {self.barcos_a_colocar} barcos en el panel Izquierdo")
                self.dibujar_tableros()
            else:
                self.lbl_estado.config(text=f"Jugador {self.mi_id} | Esperando... ({conectados}/{self.max_jugadores})")
                
        elif self.fase == "ESPERANDO_LISTOS":
            if self.servidor.todosListos(): self.fase = "COMBATE"
                
        elif self.fase == "COMBATE":
            matriz_actual = self.servidor.obtenerEstadoTablero()
            
            # ¡AQUÍ ESTÁ EL PRIMER CAMBIO! Debe decir * 3
            tamano = self.max_jugadores * 3
            
            for x in range(tamano):
                for y in range(tamano):
                    valor = matriz_actual[x][y]
                    btn_def = self.botones_defensa[(x,y)]
                    btn_atk = self.botones_ataque[(x,y)]
                    
# --- ACTUALIZAR TABLERO IZQUIERDO (DEFENSA) ---
                    if (x,y) in self.mis_coordenadas:
                        # TRUCO: Convertimos todo a texto para buscar nuestro ID
                        # Si soy el J2, pregunto si "2" está dentro de "234"
                        if valor > 0 and str(self.mi_id) in str(valor): 
                            btn_def.config(bg=COLOR_ACIERTO, text="X") # ¡Me dieron!
                        else: 
                            btn_def.config(bg=COLOR_MIO, text="B") # Sigue vivo
                    else:
                        if valor == -1: btn_def.config(bg=COLOR_FALLO, text="O")

                    # --- ACTUALIZAR TABLERO DERECHO (ATAQUE) ---
                    if valor == -1:
                        btn_atk.config(bg=COLOR_FALLO, text="O") 
                    elif valor > 0:
                        # Mostrará "J2" si le diste a uno, o "J234" si le diste a varios al mismo tiempo
                        btn_atk.config(bg=COLOR_ACIERTO, text=f"J{valor}")

                    # --- ACTUALIZAR TABLERO DERECHO (ATAQUE) ---
                    if valor == -1:
                        btn_atk.config(bg=COLOR_FALLO, text="O") # Agua
                    elif valor > 0:
                        btn_atk.config(bg=COLOR_ACIERTO, text=f"J{valor}") # Barco hundido visible para todos

            turno = self.servidor.deQuienEsElTurno()
            if turno == self.mi_id: self.lbl_estado.config(text=f"¡TU TURNO JUGADOR {self.mi_id}! Dispara en el panel Derecho", fg="#F1C40F")
            else: self.lbl_estado.config(text=f"Turno del Jugador {turno}...", fg=COLOR_TEXTO)

        self.master.after(1000, self.actualizar_estado_periodicamente)

    def dibujar_tableros(self):
        tamano = self.max_jugadores * 3 
        for fila in range(tamano):
            self.grid_defensa.grid_rowconfigure(fila, weight=1); self.grid_defensa.grid_columnconfigure(fila, weight=1)
            self.grid_ataque.grid_rowconfigure(fila, weight=1); self.grid_ataque.grid_columnconfigure(fila, weight=1)
            
            for col in range(tamano):
                # Botones de Defensa
                btn_d = tk.Button(self.grid_defensa, text="", bg=COLOR_AGUA, font=("Arial", 9, "bold"))
                btn_d.config(command=lambda x=fila, y=col: self.clic_posicionar(x, y))
                btn_d.grid(row=fila, column=col, sticky="nsew", padx=1, pady=1)
                self.botones_defensa[(fila, col)] = btn_d 
                
                # Botones de Ataque
                btn_a = tk.Button(self.grid_ataque, text="", bg=COLOR_AGUA, font=("Arial", 9, "bold"))
                btn_a.config(command=lambda x=fila, y=col: self.clic_atacar(x, y))
                btn_a.grid(row=fila, column=col, sticky="nsew", padx=1, pady=1)
                self.botones_ataque[(fila, col)] = btn_a 

    def clic_posicionar(self, x, y):
        if self.fase == "POSICIONAMIENTO":
            if (x, y) not in self.mis_coordenadas: 
                self.servidor.colocarBarco(self.mi_id, x, y)
                self.mis_coordenadas.append((x,y)) 
                
                btn = self.botones_defensa[(x, y)]
                btn.config(bg=COLOR_MIO, text="B")
                
                self.barcos_colocados += 1
                if self.barcos_colocados == self.barcos_a_colocar:
                    self.fase = "ESPERANDO_LISTOS"
                    self.lbl_estado.config(text="Flota lista. Esperando enemigos...")
                    self.servidor.declararListo(self.mi_id)

    # ¡Fíjate en los espacios a la izquierda de esta línea!
    def clic_atacar(self, x, y):
        if self.fase == "COMBATE":
            turno_actual = self.servidor.deQuienEsElTurno()
            if turno_actual == self.mi_id:
                resultado = self.servidor.disparar(self.mi_id, x, y)
                
                if resultado == 8:
                    messagebox.showwarning("Aviso", "Movimiento inválido o ya atacaste ahí.")
                elif resultado > 0:
                    messagebox.showinfo("¡BOOM!", f"¡Fuego efectivo! Has impactado a la flota: {resultado}")

# --- PUNTO DE ENTRADA ---
if __name__ == '__main__':
    with Ice.initialize(sys.argv) as communicator:
        # Por ahora lo dejamos local, después le pondremos el link de Railway
        proxy_string = "TableroJuego:default -h 127.0.0.1 -p 10000"
        base = communicator.stringToProxy(proxy_string)
        motor_servidor = Juego.MotorMultijugadorPrx.checkedCast(base)
        ventana_principal = tk.Tk()
        app = ClienteBatallaNaval(ventana_principal, motor_servidor)
        ventana_principal.mainloop()
