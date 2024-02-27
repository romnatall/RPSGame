import streamlit as st
from PIL import Image
from db import SimpleDatabase as sb
from model import guess
import scipy.stats as sc
# game.py этот файл, репозиторий https://github.com/romnatall/RPSGame



db =sb()

wins= db.data.get('win',0)
loses= db.data.get('lose',0)
draws= db.data.get('draw',0)

winrate=str(round((wins/(wins+loses) if (wins+loses)>0 else 1 )*100,ndigits=2))+"% "
play= db.data.get('play','012')
db.data['play']=play
predic={
    "Камень": '0',
    "Ножницы": '1',
    "Бумага": '2'
}
кpredic = {i: key for key, i in predic.items()}

# Загрузка изображений
res=(200,200)
pngs = {
    "Камень": Image.open("images/rock.jpg").resize(res),
    "Ножницы": Image.open("images/scissors.jpeg").resize(res),
    "Бумага": Image.open("images/paper.png").resize(res),
    "win": Image.open("images/win.jpeg").resize(res),
    "lose": Image.open("images/lose.png").resize(res),
    "draw": Image.open("images/draw.jpg").resize(res)
}

with st.spinner("Идет загрузка..."):
    def play_game(player_choice):
        
        #пауза нужна только чтобы было нагляднее при нажатии на  ту же клавишу
        #time.sleep(2)
        pred=guess(db.data['play'])
        db.data['play']+=predic[player_choice]
        pcchoices = {1:"Камень", 2:"Ножницы", 0:"Бумага"}
        computer_choice = pcchoices[pred.index(max(pred))]
    

        col1, col2 = st.columns(2)

        # В первой колонке разместим изображение
        with col1:
            st.write(f"## Вы выбрали:\n {player_choice}")
            st.image(pngs[player_choice])

        # Во второй колонке разместим текст или другие элементы
        with col2:
            st.write(f"## Компьютер выбрал:\n {computer_choice}")
            st.image(pngs[computer_choice])

        col1, col2, col3 = st.columns(3)


        with col2:
                if player_choice == computer_choice:
                    db.data['draw']+=1
                    st.write("## Ничья!")
                    st.image(pngs["draw"])
                elif (
                    (player_choice == "Камень" and computer_choice == "Ножницы") or
                    (player_choice == "Ножницы" and computer_choice == "Бумага") or
                    (player_choice == "Бумага" and computer_choice == "Камень")
                ):
                    db.data['win']+=1
                    st.write("## Победа!")
                    st.image(pngs["win"])
                else:
                    db.data['lose']+=1
                    st.write("## Поражение")
                    st.image(pngs["lose"])

                    
        st.write(f"### ты проиграл с вероятностью {round((1-sc.binom(wins+loses,0.5).cdf(wins))*100,4)} % ")




        
        db.save_data()

# Веб-приложение
st.title("Игра в Камень-Ножницы-Бумага")
st.write("эта игра использует машинное обучение")#эту модель я сам придумал

reset = st.button("Обнулить очки")
if reset:
    db.data['draw']=0
    db.data['win']=0
    db.data['lose']=0
    wins= db.data.get('win',0)
    loses= db.data.get('lose',0)
    draws= db.data.get('draw',0)
    db.save_data()

# Вывод в колонках
col1, col2, col3 = st.columns(3)
with col1:
    st.write("####  Побед: ", wins)

with col2:
    st.write("####  Поражений: ", loses)

with col3:
    st.write("####  Ничьих: ", draws)



st.write("####  Процент побед (не считая ничьих): ", winrate)

# Создаем кнопки для выбора
col1, col2, col3 = st.columns(3)
with col1:
    rock_button = st.button("Камень")
with col2:
    scissors_button = st.button("Ножницы")
with col3:
    paper_button = st.button("Бумага")


# Обработка нажатий кнопок
if rock_button:
    play_game("Камень")
elif scissors_button:
    play_game("Ножницы")
elif paper_button:
    play_game("Бумага")

st.markdown("made by [@romnatall](https://web.telegram.org/k/#@romnatall)")