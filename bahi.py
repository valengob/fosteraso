import streamlit as st
from groq import Groq


st.set_page_config(page_title='Mi primer CHATBOT', page_icon='smile')


MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def congif_chatbot():
    st.sidebar.title('Elección de modelos IA')
    elejirModelo = st.sidebar.selectbox('modelo',options=MODELOS,index=0)

    if elejirModelo == 'llama3-8b-8192':
        st.header(f'ChatBot')
    elif elejirModelo == 'llama3-70b-8192':
        st.header(f'Imagenes')
    elif elejirModelo == 'mixtral-8x7b-32768':
        st.header(f'IA con PY')

    return elejirModelo





def config_user_groq():
    api_key = st.secrets["API_KEY"]
    return Groq(api_key=api_key)


def config_model(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

def cache():
        if "mensajes" not in st.session_state:
            st.session_state.mensajes = []

cache()


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()



def main():
    modelo = congif_chatbot()
    clienteUsuario =config_user_groq()
    cache()

    mensaje = st.chat_input("Escribe tu mensaje:")


    if mensaje:
        actualizar_historial("user", mensaje,"😶‍🌫️")
        chat_completo = config_model(clienteUsuario, modelo, mensaje)
        respuesta_completa= " "
        for frase in chat_completo:
            if frase.choices[0].delta.content:
                respuesta_completa += frase.choices[0].delta.content
        actualizar_historial("assistant", respuesta_completa, "🤖")
    area_chat()

if __name__ == "__main__":
    main()