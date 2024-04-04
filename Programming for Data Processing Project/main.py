import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def generate_csv():
    # Aquí va tu código para generar el archivo CSV
    messagebox.showinfo("Información", "Archivo CSV generado correctamente")

def generate_plot_1():
    # Aquí va tu código para generar la primera gráfica
    messagebox.showinfo("Información", "Gráfica 1 generada")

def generate_plot_2():
    # Aquí va tu código para generar la segunda gráfica
    messagebox.showinfo("Información", "Gráfica 2 generada")

def generate_plot_3():
    # Aquí va tu código para generar la tercera gráfica
    messagebox.showinfo("Información", "Gráfica 3 generada")

def main():
    root = tk.Tk()
    root.title("TRANSFERMARKT STATISTICS") # Título
    root.geometry("1200x625")  # Tamaño de la ventana
    root.resizable(False, False)  # No permitir redimensionar

    # Cambiar el icono de la ventana
    icon_path = os.path.join("utils", "images", "tm_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print("El icono no se pudo encontrar:", icon_path)

    # Configuración de color de fondo 
    root.configure(bg="#2e4053")

    # Frame para la imagen, texto y botón
    frame_image_text = tk.Frame(root, bg="#d5dbdb", padx=10, pady=10)
    frame_image_text.pack(pady=20)

    # Título e imagen
    image_path = os.path.join("utils", "images", "Transfermarkt_logo.png")
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 100), Image.ANTIALIAS)
        transfermarket_logo = ImageTk.PhotoImage(image)

        # Mostrar la imagen en el frame
        label_logo = tk.Label(frame_image_text, image=transfermarket_logo, bg="#d5dbdb")
        label_logo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    else:
        print("La imagen no se pudo encontrar:", image_path)

    # Texto "Welcome to Transfermarkt Statistics" en mayúsculas
    label_welcome = tk.Label(frame_image_text, text="Welcome to Transfermarkt Statistics".upper(), fg="#0e3d48", bg="#d5dbdb", font=("Arial", 20, "bold"))
    label_welcome.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Texto más pequeño en mayúsculas
    label_info = tk.Label(frame_image_text, text="This program will allow you to perform data analysis of the most up-to-date information".upper(), fg="#0e3d48", bg="#d5dbdb", font=("Arial", 12))
    label_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Botón para descargar información con icono
    download_icon_path = os.path.join("utils", "images", "descargar.png")
    if os.path.exists(download_icon_path):
        download_icon = tk.PhotoImage(file=download_icon_path)
        btn_download = tk.Button(frame_image_text, text="  Download Information from the Web  ", command=generate_csv, image=download_icon, compound="left", bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_download.image = download_icon
        btn_download.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="e")
    else:
        btn_download = tk.Button(frame_image_text, text="Download Information from the Web", command=generate_csv, bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_download.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="e")
        print("El icono de descarga no se pudo encontrar:", download_icon_path)

    # Botón para mostrar datos con icono
    show_data_icon_path = os.path.join("utils", "images", "tabla.png")
    if os.path.exists(show_data_icon_path):
        show_data_icon = tk.PhotoImage(file=show_data_icon_path)
        btn_show_data = tk.Button(frame_image_text, text="  Show Data  ", image=show_data_icon, compound="left", bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_show_data.image = show_data_icon
        btn_show_data.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="w")
    else:
        btn_show_data = tk.Button(frame_image_text, text="Show Data", bg="#154360", fg="white", font=("Arial", 12, "bold"))
        btn_show_data.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="w")
        print("El icono de mostrar datos no se pudo encontrar:", show_data_icon_path)

    # Espacio entre el texto y los botones
    tk.Label(root, text="", bg="#2e4053").pack()

    # Botones para mostrar gráficas
    frame_buttons = tk.Frame(root, bg="#2e4053")
    frame_buttons.pack()

    btn_plot_1 = tk.Button(frame_buttons, text="LINE CHART", command=generate_plot_1, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
    btn_plot_1.grid(row=1, column=0, padx=10, pady=10)

    btn_plot_2 = tk.Button(frame_buttons, text="BAR CHART", command=generate_plot_2, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
    btn_plot_2.grid(row=1, column=1, padx=10, pady=10)

    btn_plot_3 = tk.Button(frame_buttons, text="HISTOGRAM", command=generate_plot_3, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
    btn_plot_3.grid(row=1, column=2, padx=10, pady=10)

    # Cargar imagenes plots
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
        print("La imagen del line chart no se pudo encontrar:", line_chart_image_path_image_path)

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
        print("La imagen del bar chart no se pudo encontrar:", bar_chart_image_path)

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
        print("La imagen del histrogram no se pudo encontrar:", histogram_image_path)
    
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
