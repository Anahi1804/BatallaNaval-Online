// BatallaMulti.ice
module Juego {
    // Definimos una lista de enteros, y luego una lista de listas (Matriz)
    sequence<int> Fila;
    sequence<Fila> Matriz;

    interface MotorMultijugador {
        // --- FASE 1 y 2 ---
        int registrarJugador(int totalEsperados); 
        int obtenerCantidadConectados(); 
        int obtenerMaxJugadores(); 
        void colocarBarco(int idJugador, int x, int y);
        void declararListo(int idJugador);
        bool todosListos();

        // --- FASE 3: Combate ---
        int deQuienEsElTurno();
        int disparar(int idJugador, int x, int y);
        
        // --- NUEVAS FUNCIONES PARA INTERFAZ Y FIN DE JUEGO ---
        Matriz obtenerEstadoTablero(); 
        int obtenerGanador(); 
        string obtenerMarcador(); 
    };
};