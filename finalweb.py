import streamlit as st
pip install matplotlib
import matplotlib.pyplot as plt
import os
import io
from PIL import Image
import pandas as pd
import numpy as np
import requests
from io import BytesIO

#FONCTIONS
def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
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

def create_scatter_plot_on_image_PC(img, plot_center, plot_size, point, x_tick_interval, y_tick_interval,
                                 x_tick_start, y_tick_start):

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
    # Plot ticks and label them on the x-axis
    x_ticks_pos = [x_center + i for i in range(0, plot_width + 1, x_tick_interval)]  # Positive x-axis ticks
    x_tick_labels = [x_tick_start + i for i in range(0, len(x_ticks_pos))]  # Start numbering at x_tick_start
    # Plot ticks and label them on the y-axis
    y_ticks_pos = [y_center + i for i in range(0, plot_height + 1, y_tick_interval)]  # Positive y-axis ticks
    y_tick_labels = [y_tick_start + i for i in range(0, len(y_ticks_pos))]  # Start numbering at y_tick_start
    # Add ticks to the plot
    ax.set_xticks(x_ticks_pos)
    ax.set_xticklabels(x_tick_labels)
    ax.set_yticks(y_ticks_pos)
    ax.set_yticklabels(y_tick_labels)
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

def create_scatter_plot_on_image_PT(img, plot_center, plot_size, point_P, point_T, x_tick_interval, y_tick_interval,
                                 x_tick_start, y_tick_start):

    img_width, img_height = img.size
    fig, ax = plt.subplots()
    fig.set_size_inches(img_width / 100, img_height / 100)
    ax.set_xlim(0, img_width)
    ax.set_ylim(0, img_height)
    x_center, y_center = plot_center  # Center of the scatter plot in the image
    plot_width, plot_height = plot_size  # Size of the scatter plot in pixels
    x_ticks_pos = [x_center + i for i in range(0, plot_width + 1, x_tick_interval)]  # Positive x-axis ticks
    x_tick_labels = [x_tick_start + i for i in range(0, len(x_ticks_pos))]  # Start numbering at x_tick_start
    y_ticks_pos = [y_center + i for i in range(0, plot_height + 1, y_tick_interval)]  # Positive y-axis ticks
    y_tick_labels = [y_tick_start + i for i in range(0, len(y_ticks_pos))]  # Start numbering at y_tick_start
    ax.set_xticks(x_ticks_pos)
    ax.set_xticklabels(x_tick_labels)
    ax.set_yticks(y_ticks_pos)
    ax.set_yticklabels(y_tick_labels)
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

def combine_images_side_by_side(img1, img2):
    img1_width, img1_height = img1.size
    img2_width, img2_height = img2.size
    combined_height = max(img1_height, img2_height)
    combined_width = img1_width + img2_width
    combined_image = Image.new("RGB", (combined_width, combined_height))
    combined_image.paste(img1, (0, 0))
    combined_image.paste(img2, (img1_width, 0))
    return combined_image

st.header("Courbes de croissance CH - Néonatologie", divider="red")

A1,A2,A3 = st.columns(3)
with A1 :
    df = pd.DataFrame({'first column': ["fille", "garçon"]})
    sex = st.selectbox("Sexe",df['first column'],key="sex")
#checkbox_selected_F = st.checkbox("Fille")
#checkbox_selected_G = st.checkbox("Garçon")

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

button_clicked = st.button("Placer sur les courbes")
if button_clicked:
    st.write("Voici les valeurs placées sur les courbes de croissance pour un.e ",
             sex," né.e à ", SA_S, SA_J,"/7 SA avec un poids de naissance de ", PN, "g, une taille de naissance de ", TN,
             "cm et un périmètre crânien de naissance de ", PC, "cm.")
    # Example usage
    image_G_PC_url = 'https://i.ibb.co/yBsc7rs/GNEO-PC.jpg'
    image_G_PT_url = 'https://i.ibb.co/3yh9KRw/GNEO-PT.jpg'
    image_F_PC_url = 'https://i.ibb.co/VxZP281/FNEO-PC.jpg'
    image_F_PT_url = 'https://i.ibb.co/c3cnt5T/FNEO-PT.jpg'
    image_G_PC = load_image_from_url(image_G_PC_url)
    image_G_PT = load_image_from_url(image_G_PT_url)
    image_F_PC = load_image_from_url(image_F_PC_url)
    image_F_PT = load_image_from_url(image_F_PT_url)
    plot_center_PC = (177, 172)  # (0,0) in the scatter plot will be at (10,10) in the image
    plot_center_PT = (177, 150)  # (0,0) in the scatter plot will be at (10,10) in the image
    plot_size_PC = (948, 1396)  # Scatter plot size (width, height) in pixels
    plot_size_PT = (948, 1418)  # Scatter plot size (width, height) in pixels

    # Tick settings PC
    x_p_PC = int(SA_S)+(int(SA_J)/7)
    y_p_PC = int(PC)
    x_tick_interval_PC = 43  # Horizontal axis ticks every 10 pixels
    y_tick_interval_PC = 58  # Vertical axis ticks every 20 pixels
    x_tick_start_PC = 20  # Horizontal axis ticks start numbering from 1
    y_tick_start_PC = 16  # Vertical axis ticks start numbering from 43
    x_point_PC = (x_p_PC - x_tick_start_PC)
    y_point_PC = y_p_PC - y_tick_start_PC
    point_PC = (x_point_PC * x_tick_interval_PC, y_point_PC * y_tick_interval_PC)

    # Tick settings PT
    x_p_P = int(SA_S)+(int(SA_J)/7)
    y_p_P = int(PN) / 1000 - 1
    x_p_T = int(SA_S)+(int(SA_J)/7)
    y_p_T = int(TN) / 10
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
        result1 = create_scatter_plot_on_image_PT(image_G_PT, plot_center_PT, plot_size_PT, point_P, point_T,
                                        x_tick_interval_PT,
                                        y_tick_interval_PT, x_tick_start_PT, y_tick_start_PT)
        result2 = create_scatter_plot_on_image_PC(image_G_PC, plot_center_PC, plot_size_PC, point_PC, x_tick_interval_PC,
                                        y_tick_interval_PC, x_tick_start_PC, y_tick_start_PC)

        img_final = combine_images_side_by_side(result1, result2)
        st.image(img_final)
    else:
        result1 = create_scatter_plot_on_image_PT(image_G_PT, plot_center_PT, plot_size_PT, point_P, point_T,
                                        x_tick_interval_PT,
                                        y_tick_interval_PT, x_tick_start_PT, y_tick_start_PT)
        result2 = create_scatter_plot_on_image_PC(image_F_PC, plot_center_PC, plot_size_PC, point_PC, x_tick_interval_PC,
                                        y_tick_interval_PC, x_tick_start_PC, y_tick_start_PC)
        img_final = combine_images_side_by_side(result1, result2)
        st.image(img_final)


st.markdown("Lien vers [Courbes de croissance](https://cdn.paediatrieschweiz.ch/production/uploads/2020/05/Perzentilen_2012_09_15_SGP_f.pdf) de la Société Suisse de Pédiatrie")
st.markdown(":blue-background[Hugo]")
