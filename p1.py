import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Para manejar imágenes del LED
import serial
import serial.tools.list_ports

class ESPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de ESP8266MOD con GUI")
        self.serial_connection = None
        self.led_status = False
        self.create_gui()

    def create_gui(self):
        # Crear las pestañas
        tab_control = ttk.Notebook(self.root)
        
        # Pestaña 1: Conexión del puerto y control de LED
        self.tab1 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Conexión y LED')
        
        # Pestaña 2: Selección de tarea con ESP8266MOD
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab2, text='Tareas ESP8266MOD')
        
        tab_control.pack(expand=1, fill='both')

        # Pestaña 1 - Conexión y control de LED
        self.port_label = ttk.Label(self.tab1, text="Selecciona el puerto:")
        self.port_label.pack(pady=10)
        
        self.port_list = ttk.Combobox(self.tab1, values=self.get_ports())
        self.port_list.pack(pady=10)

        self.baudrate_label = ttk.Label(self.tab1, text="Selecciona la velocidad:")
        self.baudrate_label.pack(pady=10)
        
        self.baudrate_list = ttk.Combobox(self.tab1, values=[9600, 115200])
        self.baudrate_list.pack(pady=10)

        self.connect_button = ttk.Button(self.tab1, text="Conectar", command=self.connect_to_esp)
        self.connect_button.pack(pady=10)

        self.disconnect_button = ttk.Button(self.tab1, text="Desconectar", command=self.disconnect_esp)
        self.disconnect_button.pack(pady=10)

        # Imagen LED
        self.led_red_img = ImageTk.PhotoImage(Image.open("led_red.jfif").resize((50, 50)))
        self.led_green_img = ImageTk.PhotoImage(Image.open("led_green.jfif").resize((50, 50)))
        self.led_label = ttk.Label(self.tab1, image=self.led_red_img)
        self.led_label.pack(pady=10)

        self.led_on_button = ttk.Button(self.tab1, text="LED ON", command=self.led_on)
        self.led_on_button.pack(pady=10)

        self.led_off_button = ttk.Button(self.tab1, text="LED OFF", command=self.led_off)
        self.led_off_button.pack(pady=10)

        # Pestaña 2 - Selección de tareas
        self.task_label = ttk.Label(self.tab2, text="Selecciona una tarea:")
        self.task_label.pack(pady=10)

        self.task_spinbox = tk.Spinbox(self.tab2, from_=1, to=5)
        self.task_spinbox.pack(pady=10)

        self.execute_button = ttk.Button(self.tab2, text="Ejecutar tarea", command=self.execute_task)
        self.execute_button.pack(pady=10)

        self.task_output = tk.Text(self.tab2, height=10, width=50)
        self.task_output.pack(pady=10)

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_to_esp(self):
        selected_port = self.port_list.get()
        baudrate = self.baudrate_list.get()
        try:
            self.serial_connection = serial.Serial(selected_port, int(baudrate), timeout=1)
            self.led_label.config(image=self.led_green_img)
            messagebox.showinfo("Conexión exitosa", f"Conectado a {selected_port}")
        except Exception as e:
            messagebox.showerror("Error", f"No se puede conectar al puerto {selected_port}. {e}")
            self.led_label.config(image=self.led_red_img)

    def disconnect_esp(self):
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
            self.led_label.config(image=self.led_red_img)
            messagebox.showinfo("Desconectado", "La conexión con la ESP8266MOD ha sido cerrada.")

    def led_on(self):
        if self.serial_connection:
            self.serial_connection.write(b'H')  # Enviar comando 'H' para encender el LED
            self.led_label.config(image=self.led_green_img)

    def led_off(self):
        if self.serial_connection:
            self.serial_connection.write(b'L')  # Enviar comando 'L' para apagar el LED
            self.led_label.config(image=self.led_red_img)

    def execute_task(self):
        selected_task = int(self.task_spinbox.get())
        if self.serial_connection:
            try:
                if selected_task == 1:
                    self.serial_connection.write(b'1')  # Comando para la tarea 1
                    response = self.serial_connection.readline().decode('utf-8', errors='replace').strip()
                    self.task_output.insert(tk.END, f"Respuesta de ESP8266MOD: {response}\n")
                elif selected_task == 2:
                    self.serial_connection.write(b'2')  # Comando para la tarea 2
                    response = self.serial_connection.readline().decode('utf-8', errors='replace').strip()
                    self.task_output.insert(tk.END, f"Valor analógico: {response}\n")
                elif selected_task == 3:
                    self.serial_connection.write(b'3')  # Comando para activar juego de luces
                    self.task_output.insert(tk.END, "Activando juego de luces\n")
                elif selected_task == 4:
                    self.serial_connection.write(b'4')  # Comando para activar ciclo de intensidad
                    self.task_output.insert(tk.END, "Activando ciclo de intensidad\n")
                elif selected_task == 5:
                    self.serial_connection.write(b'P')  # Comando para luces de policía
                    self.task_output.insert(tk.END, "Activando luces de policía\n")
            except UnicodeDecodeError as e:
                self.task_output.insert(tk.END, f"Error de decodificación: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ESPApp(root)
    root.mainloop()
