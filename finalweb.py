import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import requests
import io

array = pd.DataFrame({
"sex":['F','F','F','F','F','F','F','F','F','F','F','F','F','G','G','G','G','G','G','G','G','G','G','G','G','G'],
"type": ['Poids','Poids','Poids','Taille','Taille','Taille','PC','PC','PC','IMC','IMC','IMC','RPT','Poids','Poids','Poids','Taille','Taille','Taille','PC','PC','PC','IMC','IMC','IMC','RPT'],
"int": ['0-2','0-5','1-18','0-2','0-5','1-18','0-2','0-5','1-18','0-2','0-5','1-18','','0-2','0-5','1-18','0-2','0-5','1-18','0-2','0-5','1-18','0-2','0-5','1-18',''],
'x0': [0,0,1,0,0,1,0,1,1,0,0,1,45,0,0,1,0,0,1,0,1,1,0,0,1,45],
'y0': [2,0,0,25,20,20,31,43,43,11,11,12,1,2,0,0,25,20,30,32,44,44,11,11,12,1],
'xfinal' : [24,60,18.5,24,60,18.5,24,18.5,18.5,60,60,18,120,24,60,18.5,24,60,18.5,24,18.5,18.5,60,60,18,120],
'yfinal': [30,50,160,95,120,180,52,59,59,22,22,34,28,30,55,170,95,130,200,53,61,61,22,22,33,28],
'intx':[39.42,15.77,54.06,39.42,15.77,54.06,39.42,54.06,54.06,15.77,15.77,55.65,12.61,39.42,15.77,54.06,39.42,15.77,54.06,39.42,54.06,54.06,15.77,15.77,55.65,12.61],
'inty':[49.71,27.84,8.70,19.89,13.92,8.70,66.29,87.00,87.00,126.55,126.55,63.27,51.56,49.71,25.31,8.19,19.89,12.65,8.19,66.29,81.88,81.88,126.55,126.55,66.29,51.56],
'link':['https://iili.io/23iGH0B.jpg','https://iili.io/23iG9fV.jpg','https://iili.io/23iG35F.jpg','https://iili.io/23iGH0B.jpg','https://iili.io/23iG9fV.jpg','https://iili.io/23iG35F.jpg','https://iili.io/23iEZOu.jpg','https://iili.io/23iEpiQ.jpg','https://iili.io/23iEpiQ.jpg','https://iili.io/23iEQRe.jpg','https://iili.io/23iEQRe.jpg','https://iili.io/23iEtDb.jpg',
        'https://iili.io/23iG2J1.jpg','https://iili.io/23iGu5X.jpg','https://iili.io/23iGAen.jpg','https://iili.io/23iGRbs.jpg','https://iili.io/23iGu5X.jpg','https://iili.io/23iGAen.jpg','https://iili.io/23iGRbs.jpg','https://iili.io/23iGofp.jpg','https://iili.io/23iGzgI.jpg','https://iili.io/23iGzgI.jpg','https://iili.io/23iGCsR.jpg','https://iili.io/23iGCsR.jpg',
        'https://iili.io/23iG7zG.jpg','https://iili.io/23iGqzJ.jpg']})

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def load_image_from_url(image_url):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        image = Image.open(response.raw)  # No need to save it to disk
        return image
    else:
        print(f"Failed to fetch the image. Status code: {response.status_code}")
        return None

def crop_image_borders(img, border_size):
    img_width, img_height = img.size
    left = border_size
    upper = border_size+110
    right = img_width - border_size
    lower = img_height - border_size-50
    if right > left and lower > upper:
        cropped_img = img.crop((left, upper, right, lower))
        return cropped_img
    else:
        print("Error: Border size is too large for the image dimensions.")

def create_scatter_plot_on_image_PC(img, plot_center, plot_size, point):
    img_width, img_height = img.size
    # Create a figure with the size of the image
    fig, ax = plt.subplots()
    fig.set_size_inches(img_width / 100, img_height / 100)
    # Set the limits of the plot to match the image size
    ax.set_xlim(0, img_width)
    ax.set_ylim(0, img_height)
    # Extract scatter plot parameters
    x_center, y_center = plot_center  # Center of the scatter plot in the image
    plot_width, plot_height = plot_size  # Size of the scatter plot in pixels
    # Plot the point (20, 30) based on the axis scaling
    point_x = x_center + point[0]  # Shift the x-coordinate based on the plot center
    point_y = y_center + point[1]  # Shift the y-coordinate based on the plot center
    # Plot the point in red
    ax.plot(point_x, point_y, 'ro')
    # Remove gridlines
    ax.grid(False)
    ax.set_axis_off()
    # Overlay the plot on the image
    ax.imshow(img, extent=[0, img_width, 0, img_height], zorder=-1)
    fig=plt.gcf()
    img=fig2img(fig)
    border_size = 150  # Number of pixels to crop from each side
    final = crop_image_borders(img, border_size)
    return final

def create_scatter_plot_on_image_PT(img, plot_center, plot_size, point_P, point_T):
    img_width, img_height = img.size
    fig, ax = plt.subplots()
    fig.set_size_inches(img_width / 100, img_height / 100)
    ax.set_xlim(0, img_width)
    ax.set_ylim(0, img_height)
    x_center, y_center = plot_center  # Center of the scatter plot in the image
    plot_width, plot_height = plot_size  # Size of the scatter plot in pixels
    point_x_P = x_center + point_P[0]  # Shift the x-coordinate based on the plot center
    point_y_P = y_center + point_P[1]  # Shift the y-coordinate based on the plot center
    point_x_T = x_center + point_T[0]  # Shift the x-coordinate based on the plot center
    point_y_T = y_center + point_T[1]  # Shift the y-coordinate based on the plot center
    ax.plot(point_x_T, point_y_T, 'ro')
    ax.plot(point_x_P, point_y_P, 'ro')
    ax.grid(False)
    ax.set_axis_off()
    ax.imshow(img, extent=[0, img_width, 0, img_height], zorder=-1)
    fig = plt.gcf()
    img = fig2img(fig)
    border_size = 150  # Number of pixels to crop from each side
    final = crop_image_borders(img, border_size)
    return final

def create_scatter_plot_on_image_two(img, plot_center, plot_size, point_1, point_2):
    img_width, img_height = img.size
    fig, ax = plt.subplots()
    fig.set_size_inches(img_width / 100, img_height / 100)
    ax.set_xlim(0, img_width)
    ax.set_ylim(0, img_height)
    x_center, y_center = plot_center  # Center of the scatter plot in the image
    plot_width, plot_height = plot_size  # Size of the scatter plot in pixels
    point_x_P = x_center + point_1[0]  # Shift the x-coordinate based on the plot center
    point_y_P = y_center + point_1[1]  # Shift the y-coordinate based on the plot center
    point_x_T = x_center + point_2[0]  # Shift the x-coordinate based on the plot center
    point_y_T = y_center + point_2[1]  # Shift the y-coordinate based on the plot center
    ax.plot(point_x_T, point_y_T, 'ro')
    ax.plot(point_x_P, point_y_P, 'ro')
    ax.grid(False)
    ax.set_axis_off()
    ax.imshow(img, extent=[0, img_width, 0, img_height], zorder=-1)
    fig = plt.gcf()
    img = fig2img(fig)
    border_size = 150  # Number of pixels to crop from each side
    final = crop_image_borders(img, border_size)
    return final

plot_center_PC = (177, 172)  # (0,0) in the scatter plot will be at (10,10) in the image
plot_center_PT = (177, 150)  # (0,0) in the scatter plot will be at (10,10) in the image
plot_size_PC = (948, 1396)  # Scatter plot size (width, height) in pixels
plot_size_PT = (948, 1418)  # Scatter plot size (width, height) in pixels

st.set_page_config(
    page_title="Courbes de croissance - CH",
    page_icon=":teddy_bear:")

st.header("Courbes de croissance - CH - :rainbow[***Version TEST***]", divider="rainbow")
tab1, tab2, tab3 = st.tabs([":baby_bottle: **Néonatologie**", ":pushpin: **Points isolés**", ":chart_with_upwards_trend: **Évolution**"])

with tab1:
    A1,A2,A3 = st.columns(3)
    with A1 :
        df = pd.DataFrame({'first column': [" ", "Féminin", "Masculin"]})
        sex = st.selectbox("Sexe",df['first column'],key="sex")

    B1,B2,B3 = st.columns(3)
    with B1:
        SA_S = st.text_input("SA (semaines)",key="SA_S")
    with B2:
        SA_J = st.text_input("/7 (jours)", key="SA_J")

    C1,C2,C3 = st.columns(3)
    with C1:
        PN = st.text_input("Poids (g)", key="PN")
    with C2:
        TN = st.text_input("Taille (cm)", key="TN")
    with C3:
        PC = st.text_input("Périmètre crânien (cm)", key="PCN")

    st.text("")
    button_clicked = st.button("Placer sur les courbes",key="bouton1")

    if sex == "Féminin":
        sex_text = "fille"
    else:
        sex_text = "garçon"

    if button_clicked:
        if sex == " " or SA_J == "" or SA_S == "" or PN == "" or TN == "" or PC == "":
            st.error('Les valeurs ne sont pas toutes indiquées.', icon="🚨")
        else:
            st.write("Voici les valeurs placées sur les courbes de croissance pour un.e ",
                     sex_text," né.e à ", SA_S, SA_J,"/7 SA avec un poids de naissance de ", PN, "g, une taille de naissance de ", TN,
                     "cm et un périmètre crânien de naissance de ", PC, "cm.")

            # Tick settings PC
            x_p_PC = float(SA_S)+(float(SA_J)/7)
            y_p_PC = float(PC)
            x_tick_interval_PC = 43  # Horizontal axis ticks every 10 pixels
            y_tick_interval_PC = 58  # Vertical axis ticks every 20 pixels
            x_tick_start_PC = 20  # Horizontal axis ticks start numbering from 1
            y_tick_start_PC = 16  # Vertical axis ticks start numbering from 43
            x_point_PC = (x_p_PC - x_tick_start_PC)
            y_point_PC = y_p_PC - y_tick_start_PC
            point_PC = (x_point_PC * x_tick_interval_PC, y_point_PC * y_tick_interval_PC)

            # Tick settings PT
            x_p_P = float(SA_S)+(float(SA_J)/7)
            y_p_P = float(PN) / 1000 - 1
            x_p_T = float(SA_S)+(float(SA_J)/7)
            y_p_T = float(TN) / 10
            x_tick_interval_PT = 43  # Horizontal axis ticks every 10 pixels
            y_tick_interval_PT = 202  # Vertical axis ticks every 20 pixels
            x_tick_start_PT = 20  # Horizontal axis ticks start numbering from 1
            y_tick_start_PT = -1  # Vertical axis ticks start numbering from 43
            x_point_P = x_p_P - x_tick_start_PT
            y_point_P = y_p_P - y_tick_start_PT
            point_P = (x_point_P * x_tick_interval_PT, y_point_P * y_tick_interval_PT)
            x_point_T = x_p_T - x_tick_start_PT
            y_point_T = y_p_T - y_tick_start_PT
            point_T = (x_point_T * x_tick_interval_PT, y_point_T * y_tick_interval_PT)

            if sex == "garçon":
                image_G_PC = load_image_from_url('https://i.ibb.co/yBsc7rs/GNEO-PC.jpg')
                image_G_PT = load_image_from_url('https://i.ibb.co/3yh9KRw/GNEO-PT.jpg')
                result1 = create_scatter_plot_on_image_PT(image_G_PT, plot_center_PT, plot_size_PT, point_P, point_T)
                result2 = create_scatter_plot_on_image_PC(image_G_PC, plot_center_PC, plot_size_PC, point_PC)

                A1, A2 = st.columns(2)
                with A1:
                    st.image(result1)
                with A2:
                    st.image(result2)

            else:
                image_F_PC = load_image_from_url('https://i.ibb.co/VxZP281/FNEO-PC.jpg')
                image_F_PT = load_image_from_url('https://i.ibb.co/c3cnt5T/FNEO-PT.jpg')

                result1 = create_scatter_plot_on_image_PT(image_F_PT, plot_center_PT, plot_size_PT, point_P, point_T)
                result2 = create_scatter_plot_on_image_PC(image_F_PC, plot_center_PC, plot_size_PC, point_PC)
                A1, A2 = st.columns(2)
                with A1:
                    st.image(result1)
                with A2:
                    st.image(result2)
                #img_final = combine_images_side_by_side(result1, result2)
                #st.image(img_final)

with (tab2):

    df2 = pd.DataFrame({'first column': ["Taille et poids", "Périmètre crânien", "IMC"]})
    type = st.multiselect("Type(s) de courbe(s)", df2['first column'], key="type",placeholder="Choisir une ou plusieurs option(s)")
    intervalle = st.radio("Intervalle d'âge adaptée", ["0-2 ans", "0-5 ans", "1-18 ans"], horizontal=True)
    A1, A2, A3 = st.columns(3)
    with A1:
        df = pd.DataFrame({'first column': [" ", "Féminin", "Masculin"]})
        sex = st.selectbox("Sexe", df['first column'], key="sex2")

    if "Taille et poids" in type or "IMC" in type :
        C1, C2, C3 = st.columns(3)
        with C1 :
            if intervalle == "0-2 ans" or intervalle == "0-5 ans":
                age2 = st.text_input("Âge (mois)", key="age_PT_m")
            else:
                age2 = st.text_input("Âge (années)", key="age_PT_a")
        with C2 :
            poids2 = st.text_input("Poids (kg)", key="poids_PT")
        with C3 :
            taille2 = st.text_input("Taille (cm)", key="taille_PT")


    if "Périmètre crânien" in type :
        if "Taille et poids" in type or "IMC" in type :
            D1, D2, D3 = st.columns(3)
            with D1:
                PC2 = st.text_input("Périmètre crânien (cm)", key="PC_PC")
        else:
            D1, D2, D3 = st.columns(3)
            with D1 :
                if intervalle == "0-2 ans":
                    age2 = st.text_input("Âge (mois)", key="age_PC_m")
                else:
                    age2 = st.text_input("Âge (années)", key="age_PC_a")
            with D2 :
                PC2 = st.text_input("Périmètre crânien (cm)", key="PC_PC")

    if type != []:
        button_clicked_2 = st.button("Placer sur les courbes",key="bouton2")
        total = []
        bool = True
        if button_clicked_2:
            if ("Taille et poids" in type or "IMC" in type) and (age2 == "" or poids2 == "" or taille2 == ""):
                st.error('Les valeurs ne sont pas toutes indiquées.', icon="🚨")
                bool = False
            elif ("Périmètre crânien" in type) and (PC2 == "" or age2 == "") and (bool == True) :
                st.error('Les valeurs ne sont pas toutes indiquées.', icon="🚨")
            else:
                if sex == "Féminin" :
                    sex_real = "F"
                elif sex == "Masculin" :
                    sex_real = "G"

                type_modif = []
                for i in type:
                    if i == "Taille et poids":
                        type_modif.append("Taille")
                        type_modif.append("Poids")
                    elif i == "Périmètre crânien":
                        type_modif.append("PC")
                    elif i == "IMC":
                        type_modif.append("IMC")

                if intervalle == "0-2 ans":
                    intervalle_modif = "0-2"
                elif intervalle == "0-5 ans":
                    intervalle_modif = "0-5"
                elif intervalle == "1-18 ans":
                    intervalle_modif = "1-18"

                for i in type_modif :
                    if i == "PC" or i == "IMC":
                        sarray = array[array["sex"] == sex_real]
                        sarray2 = sarray[sarray["type"] == i]
                        sarray3 = sarray2[sarray2["int"] == intervalle_modif]

                        if i == "PC" :
                            y_p_tot = float(PC2)
                        if i == "IMC":
                            y_p_tot = float(poids2)/((float(taille2)/100)**2)

                        if i == "PC" :
                            x_p_tot = float(age2)
                        if i == "IMC":
                            x_p_tot = float(age2)

                        x_tick_interval_tot = sarray3.iloc[0]['intx']  # Horizontal axis ticks every 10 pixels
                        y_tick_interval_tot = sarray3.iloc[0]['inty']  # Vertical axis ticks every 20 pixels
                        x_tick_start_tot = sarray3.iloc[0]['x0']  # Horizontal axis ticks start numbering from 1
                        y_tick_start_tot = sarray3.iloc[0]['y0']  # Vertical axis ticks start numbering from 43
                        x_point_tot = (x_p_tot - x_tick_start_tot)
                        y_point_tot = (y_p_tot - y_tick_start_tot)
                        point_tot = (x_point_tot * x_tick_interval_tot, y_point_tot * y_tick_interval_tot)
                        imgtot = sarray3.iloc[0]['link']

                        result2 = create_scatter_plot_on_image_PC(load_image_from_url(imgtot), plot_center_PC, plot_size_PC, point_tot)

                        total.append(result2)
                    else :
                        if i == "Taille":
                            sarray = array[array["sex"] == sex_real]
                            sarray2 = sarray[sarray["type"] == "Taille"]
                            sarray2P = sarray[sarray["type"] == "Poids"]
                            sarray3 = sarray2[sarray2["int"] == intervalle_modif]
                            sarray3P = sarray2P[sarray2P["int"] == intervalle_modif]

                            y_p_tot_P = float(poids2)
                            y_p_tot_T = float(taille2)
                            x_p_tot_P = float(age2)
                            x_p_tot_T = float(age2)

                            x_tick_interval_tot_T = sarray3.iloc[0]['intx']  # Horizontal axis ticks every 10 pixels
                            y_tick_interval_tot_T = sarray3.iloc[0]['inty']  # Vertical axis ticks every 20 pixels
                            x_tick_interval_tot_P = sarray3P.iloc[0]['intx']  # Horizontal axis ticks every 10 pixels
                            y_tick_interval_tot_P = sarray3P.iloc[0]['inty']  # Vertical axis ticks every 20 pixels
                            x_tick_start_tot_T = sarray3.iloc[0]['x0']  # Horizontal axis ticks start numbering from 1
                            y_tick_start_tot_T = sarray3.iloc[0]['y0']  # Vertical axis ticks start numbering from 43
                            x_tick_start_tot_P = sarray3P.iloc[0]['x0']  # Horizontal axis ticks start numbering from 1
                            y_tick_start_tot_P = sarray3P.iloc[0]['y0']  # Vertical axis ticks start numbering from 43
                            x_point_tot_T = (x_p_tot_T - x_tick_start_tot_T)
                            y_point_tot_T = (y_p_tot_T - y_tick_start_tot_T)
                            pointT = (x_point_tot_T * x_tick_interval_tot_T, y_point_tot_T * y_tick_interval_tot_T)
                            x_point_tot_P = (x_p_tot_P - x_tick_start_tot_P)
                            y_point_tot_P = (y_p_tot_P - y_tick_start_tot_P)
                            pointP = (x_point_tot_P * x_tick_interval_tot_P, y_point_tot_P * y_tick_interval_tot_P)
                            imgtot = sarray3.iloc[0]['link']

                            result2_PT =create_scatter_plot_on_image_two(load_image_from_url(imgtot), plot_center_PC, plot_size_PC, pointT, pointP)

                            total.append(result2_PT)

                length = len(total)
                D1, D2 = st.columns(2)
                with D1:
                    if length>0:
                        st.image(total[0])
                with D2:
                    if length>1:
                        st.image(total[1])
                D3, D4 = st.columns(2)
                with D3:
                    if length>2:
                        st.image(total[2])
                with D4:
                    if length>3:
                        st.image(total[3])
    else:
        st.warning("Choisir un type de courbe.")

with tab3:
    st.error('En cours de construction :building_construction:')
    # im_G_PC_0_2 = load_image_from_url('https://iili.io/23iGofp.jpg')
    # im_G_PC_0_5 = load_image_from_url('https://iili.io/23iGx0N.jpg')
    # im_G_PC_1_18 = load_image_from_url('https://iili.io/23iGzgI.jpg')
    # x_p_PC = 3
    # y_p_PC = 32
    # x_tick_interval_PC = 118  # Horizontal axis ticks every 10 pixels
    # y_tick_interval_PC = 67  # Vertical axis ticks every 20 pixels
    # x_tick_start_PC = 0  # Horizontal axis ticks start numbering from 1
    # y_tick_start_PC = 32  # Vertical axis ticks start numbering from 43
    # x_point_PC = (x_p_PC - x_tick_start_PC)
    # y_point_PC = y_p_PC - y_tick_start_PC
    # point_PC = (x_point_PC * x_tick_interval_PC, y_point_PC * y_tick_interval_PC)
    #
    # result2 = create_scatter_plot_on_image_PC(im_G_PC_0_2, plot_center_PC, plot_size_PC, point_PC, x_tick_interval_PC,
    #                                           y_tick_interval_PC, x_tick_start_PC, y_tick_start_PC)
    # st.image(result2)

    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.1rem;
        }
        .stTabs [data-baseweb="tab-highlight"] {
        background-color:transparent;
        }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

st.sidebar.markdown("Ce projet a été réalisé avec l'accord de l'organe responsable de la Société Suisse de Pédiatrie. Lien vers les [courbes de croissance](https://cdn.paediatrieschweiz.ch/production/uploads/2020/05/Perzentilen_2012_09_15_SGP_f.pdf) officielles.")
st.sidebar.markdown("Pour toute demande de contact, proposition d'amélioration ou rapport d'erreur, compléter le formulaire ci-dessous ou écrire un e-mail à " + '<a href="mailto:croissancech@gmail.com">croissancech@gmail.com</a>',
        unsafe_allow_html=True)



import smtplib
from email.mime.text import MIMEText

email_sender = 'homoncule36@gmail.com'
email_receiver = 'croissancech@gmail.com'
subject = st.sidebar.text_input('Nom, Prénom')
subject2 = st.sidebar.text_input("E-mail")
body = st.sidebar.text_area('Texte')
password = 'wppg htkw grtv izmz'

if st.sidebar.button("Envoyer"):
    if subject != "" and subject2 != "" and body != "":
        try:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = subject+subject2
    
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_sender, password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
    
            st.success('Email sent successfully! 🚀')
        except Exception as e:
            st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")
    else:
        st.error("Merci de compléter tous les champs du formulaire de contact. Si vous souhaitez rester anonyme, vous pouvez compléter les données de contact par une croix "X".", icon="🚨")
        
st.sidebar.markdown(":rainbow[Développé par Hugo] :teddy_bear:")
