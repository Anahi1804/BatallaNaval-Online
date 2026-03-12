import streamlit as st
import Ice
import sys
import Juego
import time

# Configuración de página
st.set_page_config(page_title="Batalla Naval Web", layout="wide")

# --- CONEXIÓN A ZEROICE (RAILWAY) ---
if "servidor" not in st.session_state:
    try:
        communicator = Ice.initialize(sys.argv)
        # ¡AQUÍ ESTÁ TU LINK DE LA NUBE!
        proxy_string = "TableroJuego:default -h gondola.proxy.rlwy.net -p 58461"
        base = communicator.stringToProxy(proxy_string)
        st.session_state.servidor = Juego.MotorMultijugadorPrx.checkedCast(base)
    except Exception as e:
        st.error(f"Error conectando al servidor en la nube: {e}")
        st.stop()

servidor = st.session_state.servidor

# --- VARIABLES DE ESTADO DEL NAVEGADOR ---
if "mi_id" not in st.session_state: st.session_state.mi_id = 0
if "fase" not in st.session_state: st.session_state.fase = "LOBBY"
if "mis_coordenadas" not in st.session_state: st.session_state.mis_coordenadas = []
if "barcos_a_colocar" not in st.session_state: st.session_state.barcos_a_colocar = 10
if "max_jugadores" not in st.session_state: st.session_state.max_jugadores = 0

st.title("⚓ Batalla Naval Royale")

# Verificar si alguien ya ganó
try:
    ganador = servidor.obtenerGanador()
    if ganador > 0:
        marcador = servidor.obtenerMarcador()
        st.success(f"¡EL JUGADOR {ganador} HA GANADO LA PARTIDA!")
        st.code(marcador)
        if st.button("Reiniciar mi página"): st.session_state.clear(); st.rerun()
        st.stop()
except:
    pass

# --- FASE 1: LOBBY ---
if st.session_state.fase == "LOBBY":
    st.subheader("Sala de Espera")
    max_srv = servidor.obtenerMaxJugadores()
    
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
    st.info(f"Eres el Jugador {st.session_state.mi_id} | Esperando a los demás... ({conectados}/{st.session_state.max_jugadores})")
    if conectados == st.session_state.max_jugadores:
        st.session_state.fase = "POSICIONAMIENTO"
        st.rerun()
    else:
        time.sleep(2) # Polling: Recarga la página cada 2 segundos
        st.rerun()

# --- FASE 2: POSICIONAMIENTO ---
elif st.session_state.fase == "POSICIONAMIENTO":
    st.subheader(f"JUGADOR {st.session_state.mi_id} | Oculta tus {st.session_state.barcos_a_colocar} barcos")
    colocados = len(st.session_state.mis_coordenadas)
    st.progress(colocados / st.session_state.barcos_a_colocar)
    
    tamano = st.session_state.max_jugadores * 3
    for x in range(tamano):
        cols = st.columns(tamano)
        for y in range(tamano):
            if (x, y) in st.session_state.mis_coordenadas:
                cols[y].button("🚢", key=f"pos_{x}_{y}", disabled=True)
            else:
                if cols[y].button("🌊", key=f"pos_{x}_{y}"):
                    servidor.colocarBarco(st.session_state.mi_id, x, y)
                    st.session_state.mis_coordenadas.append((x, y))
                    if len(st.session_state.mis_coordenadas) >= st.session_state.barcos_a_colocar:
                        servidor.declararListo(st.session_state.mi_id)
                        st.session_state.fase = "ESPERANDO_LISTOS"
                    st.rerun()

# --- FASE 3: ESPERANDO FLOTAS ---
elif st.session_state.fase == "ESPERANDO_LISTOS":
    st.info("Flota lista. Esperando a que los enemigos terminen de esconder sus barcos...")
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
        st.warning(f"¡ES TU TURNO JUGADOR {st.session_state.mi_id}! Dispara en el Radar.")
    else:
        st.info(f"Turno del Jugador {turno_actual}... Esperando tu turno.")

    matriz = servidor.obtenerEstadoTablero()
    tamano = st.session_state.max_jugadores * 3

    col_izq, col_der = st.columns(2)
    
    # DIBUJAR DEFENSA
    with col_izq:
        st.markdown("### Tu Flota (Defensa)")
        for x in range(tamano):
            cols = st.columns(tamano)
            for y in range(tamano):
                valor = matriz[x][y]
                if (x, y) in st.session_state.mis_coordenadas:
                    if valor > 0 and str(st.session_state.mi_id) in str(valor):
                        cols[y].button("💥", key=f"def_{x}_{y}", disabled=True) # Me dieron
                    else:
                        cols[y].button("🚢", key=f"def_{x}_{y}", disabled=True) # A salvo
                else:
                    if valor == -1:
                        cols[y].button("⚪", key=f"def_{x}_{y}", disabled=True) # Agua
                    else:
                        cols[y].button("🌊", key=f"def_{x}_{y}", disabled=True) # Niebla

    # DIBUJAR RADAR ATAQUE
    with col_der:
        st.markdown("### Radar (Ataque)")
        for x in range(tamano):
            cols = st.columns(tamano)
            for y in range(tamano):
                valor = matriz[x][y]
                if valor == -1:
                    cols[y].button("⚪", key=f"atk_{x}_{y}", disabled=True) # Agua
                elif valor > 0:
                    cols[y].button(f"J{valor}", key=f"atk_{x}_{y}", disabled=True) # Barco Hundido
                else:
                    # Casilla disponible
                    if turno_actual == st.session_state.mi_id:
                        if cols[y].button("🎯", key=f"atk_{x}_{y}"):
                            res = servidor.disparar(st.session_state.mi_id, x, y)
                            if res > 0: st.toast(f"¡Fuego efectivo! Impactaste a: J{res}")
                            st.rerun()
                    else:
                        cols[y].button("🎯", key=f"atk_disabled_{x}_{y}", disabled=True)

    # Si no es tu turno, actualiza la pantalla sola para ver si te disparan
    if turno_actual != st.session_state.mi_id:
        time.sleep(2)
        st.rerun()