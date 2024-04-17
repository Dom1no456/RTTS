import streamlit as st

# Заголовок приложения

st.markdown("<h1 style='text-align: center; color: blue;'>RTTS</h1>", unsafe_allow_html=True)

st.sidebar.info(
    """
    Выберите платформу
    """
)

st.sidebar.markdown(f'''
<a><button style="background-color:lightblue;margin-right: 50px;">Twitch</button></a>
<a><button style="background-color:lightblue;margin-left: 70px;">YouTube</button></a>
''', unsafe_allow_html=True)


# Используем Markdown для вставки стилей CSS
st.sidebar.write("""
    <style>
    
   body {
        background-color:  ightblue !important; /* Цвет фона не меняется почему-то */
        # /* background-image: url('https:/'); Изображение фона можно поставить 
        # background-size: cover; /* Масштабируем изображение до размера контейнера */
        # background-repeat: no-repeat; /* Запрещаем повторение изображения  */
    }

    .container {
        display: flex;
        flex-direction: row;
        align-items: center;
        
    }
  .rectangle {
        width: 700px;
        height: 550px;
        border: 1px solid #ccc;  /* Устанавливаем черные границы */
        background-color: transparent;  /* Прозрачный фон */
        margin-bottom: 20px;  /* Добавляем отступ между прямоугольниками */
        margin-left:-400px;
    }
    .rectangle2 {
        width: 700px;
        height: 550px;
        border: 1px solid #ccc;  /* Устанавливаем черные границы */
        background-color: transparent;  /* Прозрачный фон */
        margin-left:400px;
        margin-top:-570px;  
    }
  
   
  
</style>
""", unsafe_allow_html=True)


# Размещаем кнопку и текстовое поле внутри контейнера
with st.sidebar.container():
    # Текстовое поле для ввода URL
    url = st.text_input('Вставьте URL', key="text_input", value="")

    # Кнопка "Отправить"
    submitted = st.button('Отправить')


st.sidebar.info(
    """
    Не знаю можно написать какую-то хрень, типо как пользоваться приложением и тд :)
    """
)

# Размещаем окна
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="rectangle"></div>', unsafe_allow_html=True)
st.markdown('<div class="rectangle2"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)




