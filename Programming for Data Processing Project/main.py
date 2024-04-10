# For menu
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
# For data wrangling 
import pandas as pd
# For visualization
import matplotlib.pyplot as plt
import seaborn as sns

def generate_csv():
    # Aquí va tu código para generar el archivo CSV
    messagebox.showinfo("Información", "Archivo CSV generado correctamente")

def show_information_csv():    
    valoresEquipo_file_path = 'data/valoresEquipo.csv'
    valoresJugadores_file_path = 'data/valoresJugadores.csv'
    jugadoresHistoricosGoles_file_path = 'data/jugadoresHistoricosGoles.csv'

    if os.path.exists(valoresEquipo_file_path) and os.path.exists(valoresJugadores_file_path) and os.path.exists(jugadoresHistoricosGoles_file_path):
        # Read CSV data
        data1 = pd.read_csv(valoresEquipo_file_path)
        data2 = pd.read_csv(valoresJugadores_file_path)
        data3 = pd.read_csv(jugadoresHistoricosGoles_file_path)

        # Create Tkinter window
        root = tk.Tk()
        root.title("CSV Information")

        # Create text widget to display data
        text_widget = tk.Text(root)
        text_widget.pack()

        # Insert data from each CSV file into the text widget
        text_widget.insert(tk.END, "valoresEquipo.csv\n")
        text_widget.insert(tk.END, data1.head())
        text_widget.insert(tk.END, "\n\n")

        text_widget.insert(tk.END, "valoresJugadores.csv\n")
        text_widget.insert(tk.END, data2.head())
        text_widget.insert(tk.END, "\n\n")

        text_widget.insert(tk.END, "jugadoresHistoricosGoles.csv\n")
        text_widget.insert(tk.END, data3.head())

        root.mainloop()
    else:
        messagebox.showinfo("ERROR", "At leat one CSV file have not been generated yet or correctly.")

def generate_line_chart():
    valoresEquipo_file_path = 'data/valoresEquipo.csv'

    if os.path.exists(valoresEquipo_file_path):
        data = pd.read_csv(valoresEquipo_file_path)
        df = data.copy()
        # Change date format
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')

        # Order results by date
        df = df.sort_values(by='Fecha')

        # Filter the 3 most valuable clubs
        top_3_clubs = df.groupby('Nombre Equipo')['Valor Equipo (en millones $)'].max().nlargest(3).index
        df_top_3 = df[df['Nombre Equipo'].isin(top_3_clubs)]

        # Plot the line chart
        plt.figure(figsize=(18, 9))
        for equipo in top_3_clubs:
            df_equipo = df_top_3[df_top_3['Nombre Equipo'] == equipo]
            plt.plot(df_equipo['Fecha'], df_equipo['Valor Equipo (en millones $)'], label=equipo)

        plt.title('Market value evolution of the three most current valuable clubs in Spain')
        plt.xlabel('Date')
        plt.ylabel('Team market value (in million $)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("ERROR", "The CSV file have not been generated yet.")

def generate_bar_chart():
    valoresJugadores_file_path = 'data/valoresJugadores.csv'

    if os.path.exists(valoresJugadores_file_path):
        data1 = pd.read_csv(valoresJugadores_file_path)

        # The 3 most valuable players are group here
        top_players = (data1.groupby('Club')
                    .apply(lambda x: x.nlargest(3, 'Valor Jugador (en millones)'))
                    .reset_index(drop=True))

        # Plotting the bar chart with 3 different colours for each team
        plt.figure(figsize=(18, 9))
        colors = plt.cm.tab10.colors  # Seleccionamos una paleta de colores

        for i, (club, group) in enumerate(top_players.groupby('Club')):
            plt.bar(group['Nombre Jugador'], group['Valor Jugador (en millones)'],
                    color=colors[i], label=club)

        plt.title('Market Value of the Three Most Valuable Players in the Three Most Valuable Clubs in Spain')
        plt.xlabel('Player')
        plt.ylabel('Market Value (in millions)')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Club', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
        
        #Second data plot preparation
        '''data2 = pd.read_csv(valoresJugadores_file_path)
        df1 = data1.copy()
        df2 = data2.copy()
        df2.rename(columns={'Club': 'Edad'}, inplace=True)
        del df2['Valor Jugador (en millones)']
        df_merged = pd.merge(df1, df2, on='Nombre Jugador')

        # Filter Data of the 3 teams
        real_madrid = df_merged[df_merged['Club'] == 'Real Madrid CF']
        real_sociedad = df_merged[df_merged['Club'] == 'Real Sociedad']
        barcelona = df_merged[df_merged['Club'] == 'FC Barcelona']

        # Create subplots for each team
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Barcelona
        sns.regplot(ax=axes[0], x='Edad', y='Valor Jugador (en millones)', data=barcelona, scatter=True, color='blue', line_kws={'color': 'blue'})
        axes[0].set_xlabel('Players Age (Barcelona)')
        axes[0].set_ylabel('Player Value (In Millions)')
        axes[0].set_title('Barcelona')
        axes[0].set_ylim(0, max(df_merged['Valor Jugador (en millones)']))  # Established limits in y axe

        # Real Madrid
        sns.regplot(ax=axes[1], x='Edad', y='Valor Jugador (en millones)', data=real_madrid, scatter=True, color='red', line_kws={'color': 'red'})
        axes[1].set_xlabel('Players Age (Real Madrid)')
        axes[1].set_ylabel('Player Value (In Millions)')
        axes[1].set_title('Real Madrid')
        axes[1].set_ylim(0, max(df_merged['Valor Jugador (en millones)']))  # Established limits in y axe

        # Real Sociedad
        sns.regplot(ax=axes[2], x='Edad', y='Valor Jugador (en millones)', data=real_sociedad, scatter=True, color='green', line_kws={'color': 'green'})
        axes[2].set_xlabel('Players Age (Real Sociedad)')
        axes[2].set_ylabel('Player Value (In Millions)')
        axes[2].set_title('Real Sociedad')
        axes[2].set_ylim(0, max(df_merged['Valor Jugador (en millones)']))  # Established limits in y axe

        plt.tight_layout()
        plt.show()'''
    else:
        messagebox.showinfo("ERROR", "The CSV file have not been generated yet.")

def generate_pie_chart():
    jugadoresHistoricosGoles_file_path = 'data/jugadoresHistoricosGoles.csv'

    if os.path.exists(jugadoresHistoricosGoles_file_path):
        data3 = pd.read_csv(jugadoresHistoricosGoles_file_path)
        df3 = data3.copy()
        nacionalidades_counts = df3['pais'].value_counts()

        # Filter nationalities with a lower of 2% of the total
        threshold = 0.015 * nacionalidades_counts.sum()
        nacionalidades_counts_filtered = nacionalidades_counts[nacionalidades_counts >= threshold]

        # Plot the pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(nacionalidades_counts_filtered, labels=nacionalidades_counts_filtered.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of Player Nationalities in La Liga', pad=30)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
        plt.show()

        # Pie chart of top historical league goal scorers
        df_sorted = df3.sort_values(by='goles', ascending=False).head(10)  # Take the top 10 historical goal scorers
        plt.figure(figsize=(10, 6))
        plt.pie(df_sorted['goles'], labels=df_sorted['Nombre Jugador'], autopct='%1.1f%%', startangle=140)
        plt.title('Top 10 Historical La Liga Goal Scorers', pad=30)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

        # Filter players that are not spanish
        data_no_spanish = df3[df3['pais'] != 'España']

        # Count the number of player of each nationality
        nationality_counts = data_no_spanish['pais'].value_counts()
        threshold = 0.015 * nationality_counts.sum()  # Change variable name
        nationalities_counts_filtered = nationality_counts[nationality_counts >= threshold]  # Change variable name

        # Plot results
        plt.figure(figsize=(8, 8))  # Change grafic size
        plt.pie(nationalities_counts_filtered, labels=nationalities_counts_filtered.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of Player Nationalities in the League', pad=30)
        plt.axis('equal')  # Plot in cake form
        plt.legend(loc='upper right', bbox_to_anchor=(1.5, 1.0))
        plt.show()
    else:
        messagebox.showinfo("ERROR", "The CSV file have not been generated yet.")

def main():
    root = tk.Tk()
    root.title("TRANSFERMARKT STATISTICS") # Title
    root.geometry("1200x625")  # Window size
    root.resizable(False, False)  # No resizabled

    # Window icon
    icon_path = os.path.join("utils", "images", "tm_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print("The icon is not found:", icon_path)

    # Back colour 
    root.configure(bg="#2e4053")

    # Frame for the title, descriptions and 2 first buttons
    frame_image_text = tk.Frame(root, bg="#d5dbdb", padx=10, pady=10)
    frame_image_text.pack(pady=20)

    # Image as title
    image_path = os.path.join("utils", "images", "Transfermarkt_logo.png")
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 100), Image.ANTIALIAS)
        transfermarket_logo = ImageTk.PhotoImage(image)

        label_logo = tk.Label(frame_image_text, image=transfermarket_logo, bg="#d5dbdb")
        label_logo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    else:
        print("The Image is not found:", image_path)

    # Text "Welcome to Transfermarkt Statistics" en mayúsculas
    label_welcome = tk.Label(frame_image_text, text="Welcome to Transfermarkt Statistics".upper(), fg="#0e3d48", bg="#d5dbdb", font=("Arial", 20, "bold"))
    label_welcome.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Description Text
    label_info = tk.Label(frame_image_text, text="This program will allow you to perform data analysis of the most up-to-date information".upper(), fg="#0e3d48", bg="#d5dbdb", font=("Arial", 12))
    label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Information downloader button
    download_icon_path = os.path.join("utils", "images", "descargar.png")
    if os.path.exists(download_icon_path):
        download_icon = tk.PhotoImage(file=download_icon_path)
        btn_download = tk.Button(frame_image_text, text="  Download Information from the Web  ", command=generate_csv, image=download_icon, compound="left", bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_download.image = download_icon
        btn_download.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="e")
    else:
        btn_download = tk.Button(frame_image_text, text="Download Information from the Web", command=generate_csv, bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_download.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="e")
        print("The Download Icon is not found:", download_icon_path)

    # Show data button
    show_data_icon_path = os.path.join("utils", "images", "tabla.png")
    if os.path.exists(show_data_icon_path):
        show_data_icon = tk.PhotoImage(file=show_data_icon_path)
        btn_show_data = tk.Button(frame_image_text, text="  Show Data  ", command= show_information_csv,image=show_data_icon, compound="left", bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_show_data.image = show_data_icon
        btn_show_data.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="w")
    else:
        btn_show_data = tk.Button(frame_image_text, text="Show Data", bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_show_data.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="w")
        print("The Data Show Icon is not found:", show_data_icon_path)

    # Space between buttons
    tk.Label(root, text="", bg="#2e4053").pack()

    # Plots buttons
    frame_buttons = tk.Frame(root, bg="#2e4053")
    frame_buttons.pack()

    btn_plot_1 = tk.Button(frame_buttons, text="LINE CHART", command=generate_line_chart, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
    btn_plot_1.grid(row=1, column=0, padx=10, pady=10)

    btn_plot_2 = tk.Button(frame_buttons, text="BAR CHART", command=generate_bar_chart, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
    btn_plot_2.grid(row=1, column=1, padx=10, pady=10)

    btn_plot_3 = tk.Button(frame_buttons, text="HISTOGRAM", command=generate_pie_chart, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
    btn_plot_3.grid(row=1, column=2, padx=10, pady=10)

    # Plots images
    # Line Chart
    line_chart_image_path_image_path = os.path.join("utils", "images", "line_chart.png")
    if os.path.exists(line_chart_image_path_image_path):
        line_chart_image_path_image = Image.open(line_chart_image_path_image_path)
        line_chart_image_path_image = line_chart_image_path_image.resize((100, 100), Image.ANTIALIAS)
        line_chart_image_path_photo = ImageTk.PhotoImage(line_chart_image_path_image)

        label_image_1 = tk.Label(frame_buttons, image=line_chart_image_path_photo, bg="#2e4053")
        label_image_1.image = line_chart_image_path_photo
        label_image_1.grid(row=0, column=0, padx=10, pady=10)
    else:
        print("The Line Chart Image is not found:", line_chart_image_path_image_path)

    # Bar Chart
    bar_chart_image_path = os.path.join("utils", "images", "bar_chart.png")
    if os.path.exists(bar_chart_image_path):
        bar_chart_image = Image.open(bar_chart_image_path)
        bar_chart_image = bar_chart_image.resize((100, 100), Image.ANTIALIAS)
        bar_chart_photo = ImageTk.PhotoImage(bar_chart_image)

        label_image_2 = tk.Label(frame_buttons, image=bar_chart_photo, bg="#2e4053")
        label_image_2.image = bar_chart_photo
        label_image_2.grid(row=0, column=1, padx=10, pady=10)
    else:
        print("The Bar Chart Image is not found:", bar_chart_image_path)

    #Histogram
    histogram_image_path = os.path.join("utils", "images", "histogram.png")
    if os.path.exists(histogram_image_path):
        histogram_image = Image.open(histogram_image_path)
        histogram_image = histogram_image.resize((100, 100), Image.ANTIALIAS)
        histogram_photo = ImageTk.PhotoImage(histogram_image)

        label_image_3 = tk.Label(frame_buttons, image=histogram_photo, bg="#2e4053")
        label_image_3.image = histogram_photo
        label_image_3.grid(row=0, column=2, padx=10, pady=10)
    else:
        print("The Histogram Image is not found:", histogram_image_path)
    
    # Descripciones    
    label_text_1 = tk.Label(frame_buttons, text="How was the market value \nevolution of the three most \ncurrent valuable clubs in Spain?", fg="white", bg="#2e4053", font=("Arial", 10, "bold"))
    label_text_1.grid(row=2, column=0, padx=10, pady=5)

    label_text_2 = tk.Label(frame_buttons, text="What is the market value \nof the three most valuable players in \nthe three most valuable clubs in Spain?", fg="white", bg="#2e4053", font=("Arial", 10, "bold"))
    label_text_2.grid(row=2, column=1, padx=10, pady=5)

    label_text_3 = tk.Label(frame_buttons, text="What are the historic top scorers' \nplayers’ nationalities in La Liga?", fg="white", bg="#2e4053", font=("Arial", 10, "bold"))
    label_text_3.grid(row=2, column=2, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
