import pandas as pd
import seaborn as sns
from PIL import Image
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

with st.echo(code_location='below'):
    # Загрузка изображения и названия
    st.markdown("<h1 style='text-align: center; color: black;'>Набор данных о сердечных заболеваниях</h2>", unsafe_allow_html=True)
    image = Image.open('./heart.png')

    _, col_2, _ = st.columns(3)
    with col_2:
        st.image(image)

    col_1 = st.columns(1)

    st.subheader('Описание набора данных')
    """
    * возраст - **age** in years; 
    * пол - **sex**;
    * тип боли в груди - **cp:** chest pain type:
        * типичная стенокардия - **typical angina**;
        * атипичная стенокардия - **atypical angina**;
        * неангинозная боль - **non-anginal pain**;
        * бессимптомный - **asymptomatic**;
    * артериальное давление в покое - **trestbps**;
    * холестерин сыворотки в мг/дл - **chol**;
    * уровень сахара в крови натощак > 120 мг/дл - **fbs: (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)**;
    * результаты электрокардиографии в покое - **restecg**:
        * нормальный - **normal**;
        * наличие аномалии ST-T (инверсия зубца T и/или элевация или депрессия ST > 0,05 мВ) - **st**;
        * показывает вероятную или определенную гипертрофию левого желудочка по критериям Эстеса - **hypertroph**;
    * максимальная частота сердечных сокращений - **thalach**;
    * стенокардия, вызванная физической нагрузкой - **exang**;
    * депрессия ST, вызванная физической нагрузкой, по сравнению с состоянием покоя - **oldpeak**
    * наклон пикового сегмента ST при нагрузке - **slope**:
        * восходящий - **upsloping**;
        * плоский - **flat**;
        * нисходящий - **downsloping**;
    * количество крупных сосудов (0-3), окрашенных при флюороскопии - **ca**;
    * болезнь крови - **thal**:
        * нормальный - **normal**; 
        * фиксированный дефект - **fix**; 
        * обратимый дефект - **reverse**;
    * сердечное заболевание - **target**;
    """

    # Загрузка данных с csv файла
    @st.cache
    def get_data():
        data_path = './heart.csv'
        data = pd.read_csv(data_path)

        gender = {1: 'male', 0: 'female'}
        data.sex = [gender[item] for item in data.sex]

        cp = {
            0: 'typical_angina',
            1: 'atypical_angina',
            2: 'nonanginal_pain',
            3: 'asymptomatic'
        }
        data.cp = [cp[item] for item in data.cp]

        sugar = {
            1: True,
            0: False
        }
        data.fbs = [sugar[item] for item in data.fbs]

        rest = {
            0: 'normal',
            1: 'st',
            2: 'hypertroph'
        }
        data.restecg = [rest[item] for item in data.restecg]

        ex = {
            1: 'yes',
            0: 'no'
        }
        data.exang = [ex[item] for item in data.exang]

        slope = {
            0: 'slope',
            1: 'upsloping',
            2: 'flat',
            3: 'downsloping'
        }
        data.slope = [slope[item] for item in data.slope]

        data = data[data['thal'] != 0]
        thal = {
            1: 'normal',
            2: 'fix',
            3: 'reverse'
        }
        data.thal = [thal[item] for item in data.thal]

        target = {
            0: 'healthy',
            1: 'sick'
        }
        data.target = [target[item] for item in data.target]

        def rus_cp(row):
            if row == 'typical_angina':
                return 'Типичная стенокардия'
            if row == 'atypical_angina':
                return 'Атипичная стенокардия'
            if row == 'nonanginal_pain':
                return 'Неангинозная боль'
            if row == 'asymptomatic':
                return 'Бессимптомный'

        data['Тип боли в груди'] = data.apply(lambda row: rus_cp(row['cp']), axis=1)

        return data

    st.subheader('')
    # Create a Check box to display the raw data.
    if st.checkbox('Показать таблицу данных'):
        st.subheader('Данные о сердечных заболеваниях')
        status = st.text('Загрузка...')
        data = get_data()
        count = st.slider('Кол-во строк', 1, data.shape[0], data.shape[0])
        st.write(data[:count+1])
        status.text('Загрузка данных завершена!')

    st.subheader('Визуализация данных при помощи графиков')
    
    #########################################################################
    st.subheader('')
    st.markdown('1) Количество данных по выбранныму признаку')
    data = get_data()

    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        # col_1 = st.columns(1)
        count_plot_by_feature = st.radio(
            "Выберите признак",
            ('target - здоровье', 'sex - пол', 'cp - тип боли в груди', 'fbs - сахар', 'restecg - электрокардиография', 'slope - наклон пикового сегмента ST', 'thal - болезнь крови'))
    
    with col_2:
        select_1 = st.selectbox(
                'Выберите тип графика для построения',
                ('Count plot', 'Pie plot'))
    
    pie_plot = True if select_1 == 'Pie plot' else False
    count_plot_by_feature = count_plot_by_feature.split(' ')[0]

    fig_1 = plt.figure(figsize=(10, 4))
    sns.set_theme(style="darkgrid")
    if pie_plot:
        fig_1 = plt.figure(figsize=(2, 2))
        data_pie = data[count_plot_by_feature].value_counts().to_frame()
        plt.pie(data_pie[count_plot_by_feature].tolist(), labels = data_pie.index.tolist(), autopct='%.0f%%', textprops={"fontsize":6})
        fig_1.suptitle('Соотношение данных по выбранному признаку', fontsize=8)
    else:
        if count_plot_by_feature == 'target':
            ax_1 = sns.countplot(x="target", data=data)
            ax_1.set(xlabel="Здоровье", ylabel = "Количество людей")            
        elif count_plot_by_feature == 'sex':
            ax_1 = sns.countplot(x="sex", data=data)
            ax_1.set(xlabel="Пол", ylabel = "Количество людей")
        elif count_plot_by_feature == 'cp':
            ax_1 = sns.countplot(x="Тип боли в груди", data=data)
            ax_1.set(xlabel="Тип боли в груди", ylabel = "Количество людей")
        elif count_plot_by_feature == 'fbs':
            ax_1 = sns.countplot(x="fbs", data=data)
            ax_1.set(xlabel="Уровень сахара в крови натощак > 120 мг/дл", ylabel = "Количество людей")
        elif count_plot_by_feature == 'restecg':
            ax_1 = sns.countplot(x="restecg", data=data)
            ax_1.set(xlabel="результаты электрокардиографии в покое", ylabel = "Количество людей")
        elif count_plot_by_feature == 'slope':
            ax_1 = sns.countplot(x="slope", data=data)
            ax_1.set(xlabel="Наклон пикового сегмента ST при нагрузке", ylabel = "Количество людей")
        else:
            ax_1 = sns.countplot(x="thal", data=data)
            ax_1.set(xlabel="Болезнь крови", ylabel = "Количество людей")
        plt.title("Количество данных по выбранному признаку", bbox={'facecolor':'1.0', 'pad':5})
    st.pyplot(fig_1)
    #########################################################################

    #########################################################################
    st.markdown('2) Графики распределения количественных переменных')

    col_1, col_2 = st.columns(2)
    with col_1:
        select_2 = st.selectbox(
            'Выберите признак',
            ('age - возраст испытуемых', 'trestbps - артериал. давл. в покое', 'chol - холестерин сыворотки в мг/дл',
            'thalach - макс. частота сердеч. сокращ.', 'oldpeak - депрессия ST под физ. нагрузкой'))
        
    with col_2:
        radio_2 = st.radio(
            "Построить график распределения количественной переменный с учетом пола или целевой переменной.",
            ('Пол', 'Целевая переменная', 'Без'))

    st.subheader('')
    if select_2:
        fig_2 = plt.figure(figsize=(10, 4))
        selected = select_2.split(' ')[0]
        if radio_2 == 'Пол':
            ax_2 = sns.histplot(data=data, x=selected, hue='sex', kde=True)
        elif radio_2 == 'Целевая переменная':
            ax_2 = sns.histplot(data=data, x=selected, hue='target', kde=True)
        else:
            ax_2 = sns.histplot(data=data, x=selected, kde=True)
        plt.title("Распределение количественной перемнной {}".format(selected), bbox={'facecolor':'1.0', 'pad':5})
        st.pyplot(fig_2)

    #########################################################################

    #########################################################################
    st.markdown('3) Соотношение пациентов с сердечным заболеванием и без в зависимости от выбранного признака в датасете')
    select_3 = st.selectbox(
        'Выберите признак',
        ('sex - пол', 'fbs - уровень сахара', 'cp - тип боли в груди', 'restecg - электрокардиография'))

    st.subheader('')

    if select_3:
        help_d = {
            'sex': 'пола',
            'fbs': 'уровня сахара',
            'cp': 'типа боли в груди',
            'restecg': 'электрокардиографии'
        }
        temp = select_3.split(' ')[0]
        fig_3 = go.Figure(
            px.histogram(data, x=temp, color="target", barmode='group', title="Соотношение пациентов с сердечным заболеванием <br> и без в зависимости от " + help_d[temp])
        )
        st.plotly_chart(fig_3, use_container_width=True)
    #########################################################################

    #########################################################################
    st.markdown('4) График распределения данных пол-возраст (+ сердечное заболевание)')

    radio_4 = st.radio(
        "График распределения с учетом сердечных заболеваний",
        ('да', 'нет'))

    if radio_4 == 'да':
        fig_4 = px.box(data, x = "sex", y="age", color='target', title="График распределения признака пол от возраста <br> с учетом сердечных заболеваний")
    else:
        fig_4 = px.box(data, x = "sex", y="age", title="График распределения признака пол от возраста")
        
    fig_4.update_traces(quartilemethod="exclusive")
    st.plotly_chart(fig_4, use_container_width=True)
    #########################################################################

    #########################################################################
    st.markdown('5) Точечный график распределения артериального давления от возраста')

    radio_5 = st.radio(
        "Интерактивный график через plotly",
        ('да', 'нет'))

    if radio_5 == 'да':
        fig_5 = px.scatter(data, x="trestbps", y="age", marginal_x="histogram", marginal_y="histogram", title='График разброса признаков артер. давл. и возраст <br> с гистограммами частот признаков')
        st.plotly_chart(fig_5)
    else:
        ### FROM: https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
        fig_5 = plt.figure(figsize=(16, 10), dpi= 80)
        grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)

        ax_main = fig_5.add_subplot(grid[:-1, :-1])
        ax_right = fig_5.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
        ax_bottom = fig_5.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

        ax_main.scatter('trestbps', 'age', alpha=.8, data=data, cmap="Set1", edgecolors='gray', linewidths=.5)

        ax_bottom.hist(data.trestbps, 40, histtype='stepfilled', orientation='vertical', color='deeppink')
        ax_bottom.invert_yaxis()

        ax_right.hist(data.age, 40, histtype='stepfilled', orientation='horizontal', color='deeppink')

        ax_main.set(title='График разброса признаков артер. давл. и возраст \n с гистограммами частот признаков', xlabel='trestbps', ylabel='age')
        ax_main.title.set_fontsize(20)
        for item in ([ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
            item.set_fontsize(14)

        xlabels = ax_main.get_xticks().tolist()
        ax_main.set_xticklabels(xlabels)
        st.pyplot(fig_5)
        ### END FROM
    #########################################################################
    
    #########################################################################
    st.markdown('6) График распределения типа боли в груди и возраста')

    radio_6 = st.radio(
        "Интерактивный график через plotly lib",
        ('да', 'нет'))

    if radio_6 == 'да':
        fig_6 = px.violin(data, y="age", x="Тип боли в груди", color="Тип боли в груди", box=True, hover_data=data.columns, title='График распределения для типов боли по возрасту')
        st.plotly_chart(fig_6)
    else:
        fig_6 = plt.figure(figsize=(10, 4))
        ax_6 = sns.violinplot(x="Тип боли в груди", y="age", data=data, inner=None)
        plt.title("График распределения для типов боли по возрасту")
        st.pyplot(fig_6)
    #########################################################################

    #############################################################
    st.markdown('7) "Карта" корреляции количественных признаков датасета')
    corr = data.corr()
    fig_7, ax_7 = plt.subplots(figsize=(10, 7))
    sns.heatmap(data.corr(), ax=ax_7, cmap="YlGnBu", linewidths=.5, annot=True)
    st.write(fig_7)
    #############################################################

    #############################################################
    st.markdown('8) График разброса (с регрес.) выбранного признака от возраста с учетом целевой метки')
    select_8 = st.selectbox(
            'Выберите признак',
            ('trestbps - артериал. давл. в покое', 'chol - холестерин сыворотки в мг/дл',
            'thalach - макс. частота сердеч. сокращ.', 'oldpeak - депрессия ST под физ. нагрузкой'))
    
    fig_8, ax_8 = plt.subplots(figsize=(9,5))
    if select_8:
        feature = select_8.split(' ')[0]
        text = " ".join(select_8.split(' ')[2:])
        fig_8 = px.scatter(data, x="age", y=feature, facet_col="target", color="sex", trendline="ols", title='График разброса признака "{}" от возраста <br> с учетом целевой метки'.format(text))
        st.plotly_chart(fig_8)
    #############################################################
