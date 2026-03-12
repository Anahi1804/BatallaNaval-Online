import streamlit as st
import Ice
import sys
import Juego
import time

# --- CONFIGURACIÓN DE PÁGINA Y CSS (TIPO TKINTER) ---
st.set_page_config(page_title="Batalla Naval Royale", layout="wide", initial_sidebar_state="collapsed")

# Inyectamos CSS para imitar tu diseño de Tkinter
st.markdown("""
    <style>
        /* Fondo principal oscuro */
        .stApp {
            background-color: #2C3E50;
            color: #ECF0F1;
        }
        /* Juntar los botones de la cuadrícula para que parezca un tablero real */
        div[data-testid="column"] {
            padding: 0px !important;
        }
        div.stButton > button {
            width: 100%;
            height: 60px;
            font-size: 24px;
            border-radius: 2px;
            margin: 1px 0px;
            background-color: #34495E;
            color: white;
            border: 1px solid #1ABC9C;
            transition: 0.2s;
        }
        div.stButton > button:hover {
            border: 2px solid #2ECC71;
            transform: scale(1.05);
        }
        /* Títulos */
        h1, h2, h3 { color: #2ECC71 !important; text-align: center; font-family: 'Verdana', sans-serif; }
        .stAlert > div { background-color: #34495E; color: white; border: 1px solid #E74C3C; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A ZEROICE (RAILWAY) ---
if "servidor" not in st.session_state:
    try:
        communicator = Ice.initialize(sys.argv)
        # Asegúrate de que este sea tu link de Railway actual
        proxy_string = "TableroJuego:default -h gondola.proxy.rlwy.net -p 58461"
        base = communicator.stringToProxy(proxy_string)
        st.session_state.servidor = Juego.MotorMultijugadorPrx.checkedCast(base)
    except Exception as e:
        st.error(f"Error conectando al servidor en la nube: {e}")
        st.stop()

servidor = st.session_state.servidor

# --- VARIABLES DE ESTADO ---
if "mi_id" not in st.session_state: st.session_state.mi_id = 0
if "fase" not in st.session_state: st.session_state.fase = "LOBBY"
if "mis_coordenadas" not in st.session_state: st.session_state.mis_coordenadas = []
if "barcos_a_colocar" not in st.session_state: st.session_state.barcos_a_colocar = 10
if "max_jugadores" not in st.session_state: st.session_state.max_jugadores = 0

st.title("⚓ BATALLA NAVAL ONLINE ⚓")

# Verificar Ganador
try:
    ganador = servidor.obtenerGanador()
    if ganador > 0:
        marcador = servidor.obtenerMarcador()
        st.success(f"🏆 ¡EL JUGADOR {ganador} HA GANADO LA PARTIDA! 🏆")
        st.code(marcador)
        st.stop()
except:
    pass

# --- FASE 1: LOBBY ---
if st.session_state.fase == "LOBBY":
    st.markdown("### 🎮 Sala de Espera")
    max_srv = servidor.obtenerMaxJugadores()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if max_srv == 0:
            esperados = st.number_input("¿Cuántos jugadores serán en total?", min_value=2, max_value=4, value=2)
            if st.button("Crear Partida y Unirse"):
                st.session_state.mi_id = servidor.registrarJugador(int(esperados))
                st.session_state.max_jugadores = int(esperados)
                st.session_state.fase = "ESPERANDO_LOBBY"
                st.rerun()
        else:
            st.info(f"Hay una partida abierta para {max_srv} jugadores.")
            if st.session_state.mi_id == 0:
                if st.button("Unirse a la partida"):
                    st.session_state.mi_id = servidor.registrarJugador(max_srv)
                    st.session_state.max_jugadores = max_srv
                    st.session_state.fase = "ESPERANDO_LOBBY"
                    st.rerun()

elif st.session_state.fase == "ESPERANDO_LOBBY":
    conectados = servidor.obtenerCantidadConectados()
    st.info(f"⏳ Eres el Jugador {st.session_state.mi_id} | Esperando a los demás... ({conectados}/{st.session_state.max_jugadores})")
    if conectados == st.session_state.max_jugadores:
        st.session_state.fase = "POSICIONAMIENTO"
        st.rerun()
    else:
        time.sleep(2)
        st.rerun()

# --- FASE 2: POSICIONAMIENTO ---
elif st.session_state.fase == "POSICIONAMIENTO":
    st.markdown(f"### 🟩 JUGADOR {st.session_state.mi_id} | Oculta tus {st.session_state.barcos_a_colocar} barcos")
    colocados = len(st.session_state.mis_coordenadas)
    st.progress(colocados / st.session_state.barcos_a_colocar)
    
    tamano = st.session_state.max_jugadores * 3
    
    # Centrar el tablero
    _, col_centro, _ = st.columns([1, 2, 1])
    with col_centro:
        for x in range(tamano):
            cols = st.columns(tamano)
            for y in range(tamano):
                if (x, y) in st.session_state.mis_coordenadas:
                    cols[y].button("🟩", key=f"pos_{x}_{y}", disabled=True) # Barco colocado
                else:
                    if cols[y].button("🟦", key=f"pos_{x}_{y}"): # Agua libre
                        servidor.colocarBarco(st.session_state.mi_id, x, y)
                        st.session_state.mis_coordenadas.append((x, y))
                        if len(st.session_state.mis_coordenadas) >= st.session_state.barcos_a_colocar:
                            servidor.declararListo(st.session_state.mi_id)
                            st.session_state.fase = "ESPERANDO_LISTOS"
                        st.rerun()

# --- FASE 3: ESPERANDO FLOTAS ---
elif st.session_state.fase == "ESPERANDO_LISTOS":
    st.info("🛡️ Flota lista. Esperando a que los enemigos terminen de esconder sus barcos...")
    if servidor.todosListos():
        st.session_state.fase = "COMBATE"
        st.rerun()
    else:
        time.sleep(2)
        st.rerun()

# --- FASE 4: COMBATE ---
elif st.session_state.fase == "COMBATE":
    turno_actual = servidor.deQuienEsElTurno()
    if turno_actual == st.session_state.mi_id:
        st.warning(f"🔥 ¡ES TU TURNO JUGADOR {st.session_state.mi_id}! Dispara en el Radar.")
    else:
        st.info(f"⏳ Turno del Jugador {turno_actual}... Prepara tus defensas.")

    matriz = servidor.obtenerEstadoTablero()
    tamano = st.session_state.max_jugadores * 3

    col_izq, espaciador, col_der = st.columns([10, 1, 10])
    
    # --- TABLERO IZQUIERDO: DEFENSA ---
    with col_izq:
        st.markdown("### 🛡️ Tu Flota (Defensa)")
        for x in range(tamano):
            cols = st.columns(tamano)
            for y in range(tamano):
                valor = matriz[x][y]
                # El tablero de defensa SÍ se bloquea para evitar clics accidentales
                if (x, y) in st.session_state.mis_coordenadas:
                    if valor > 0 and str(st.session_state.mi_id) in str(valor):
                        cols[y].button("💥", key=f"def_{x}_{y}", disabled=True) # Me dieron
                    else:
                        cols[y].button("🚢", key=f"def_{x}_{y}", disabled=True) # Mi barco a salvo
                else:
                    if valor == -1:
                        cols[y].button("⬜", key=f"def_{x}_{y}", disabled=True) # Fallaron
                    elif valor > 0:
                        cols[y].button("🟥", key=f"def_{x}_{y}", disabled=True) # Le dieron a otro
                    else:
                        cols[y].button("🌊", key=f"def_{x}_{y}", disabled=True) # Agua intacta

    # --- TABLERO DERECHO: ATAQUE ---
    with col_der:
        st.markdown("### 🎯 Radar (Ataque)")
        for x in range(tamano):
            cols = st.columns(tamano)
            for y in range(tamano):
                valor = matriz[x][y]
                
                # Determinamos la apariencia de la casilla
                if valor == -1:
                    icono = "⬜" # Disparo fallido previo
                elif valor > 0:
                    icono = "🟥" # Impacto previo
                else:
                    icono = "🟦" # Sin descubrir
                
                # LA MAGIA: Si es tu turno, TODAS las casillas son clickeables
                if turno_actual == st.session_state.mi_id:
                    if cols[y].button(icono, key=f"atk_{x}_{y}"):
                        res = servidor.disparar(st.session_state.mi_id, x, y)
                        if res == 8: 
                            st.toast("⚠️ Movimiento inválido o no hay nada más que golpear ahí.", icon="⚠️")
                        elif res > 0: 
                            st.toast(f"💥 ¡Impacto confirmado a la flota {res}!", icon="🔥")
                        else: 
                            st.toast("💦 ¡Cayó en el agua!", icon="💧")
                        st.rerun()
                else:
                    # Si no es tu turno, las bloqueamos para que no acumules clics
                    cols[y].button(icono, key=f"atk_disabled_{x}_{y}", disabled=True)

    # Refrescar pantalla automáticamente si no es mi turno
    if turno_actual != st.session_state.mi_id:
        time.sleep(2)
        st.rerun()

