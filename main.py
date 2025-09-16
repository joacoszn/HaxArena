import customtkinter as ctk
import webview
import threading
import multiprocessing # Importamos la librería para manejar procesos
# Importamos las funciones de nuestro backend
from backend.auth import iniciar_sesion_usuario, registrar_usuario
from backend.perfil import obtener_perfil_usuario

# --- Función para el Proceso del Juego ---
# Esta función debe estar en el nivel superior para que multiprocessing pueda funcionar correctamente.
def lanzar_proceso_juego():
    """Crea y ejecuta la ventana de webview en un proceso separado."""
    webview.create_window(
        'HaxArena - Haxball',
        'https://www.haxball.com/play',
        width=1280,
        height=720
    )
    webview.start()

# --- Configuración de la Apariencia ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Aplicacion(ctk.CTk):
    """Clase principal de la aplicación que hereda de ctk.CTk para ser la ventana."""
    def __init__(self):
        super().__init__()

        # --- Estado de la Aplicación ---
        self.usuario_actual = None

        # --- Configuración Inicial de la Ventana ---
        self.title("HaxArena Launcher")
        
        # --- Contenedores para las Vistas ---
        self.contenedor_auth = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_perfil = ctk.CTkFrame(self, fg_color="transparent")

        # --- Crear los widgets de todas las vistas ---
        self.crear_widgets_auth()
        self.crear_widgets_principales()
        self.crear_widgets_perfil()
        
        # Iniciar mostrando la vista de autenticación
        self.mostrar_vista_auth()

    # --- Creación de Widgets ---
    def crear_widgets_auth(self):
        """Crea los widgets para la vista de autenticación (login y registro)."""
        self.frame_login = ctk.CTkFrame(self.contenedor_auth, fg_color="transparent")
        titulo = ctk.CTkLabel(self.frame_login, text="HaxArena", font=ctk.CTkFont(size=36, weight="bold"))
        titulo.pack(pady=(20, 20))
        self.entrada_usuario_login = ctk.CTkEntry(self.frame_login, placeholder_text="Usuario", width=250, height=40)
        self.entrada_usuario_login.pack(pady=10)
        self.entrada_clave_login = ctk.CTkEntry(self.frame_login, placeholder_text="Contraseña", show="*", width=250, height=40)
        self.entrada_clave_login.pack(pady=10)
        self.etiqueta_mensaje_login = ctk.CTkLabel(self.frame_login, text="", font=ctk.CTkFont(size=12))
        self.etiqueta_mensaje_login.pack(pady=(0, 10))
        boton_login = ctk.CTkButton(self.frame_login, text="Iniciar Sesión", width=250, height=40, command=self.intentar_login)
        boton_login.pack(pady=20)
        frame_cambio_login = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        frame_cambio_login.pack(pady=10)
        etiqueta_login = ctk.CTkLabel(frame_cambio_login, text="¿No tienes cuenta?")
        etiqueta_login.pack(side="left")
        boton_cambio_login = ctk.CTkButton(frame_cambio_login, text="Regístrate", fg_color="transparent", hover=False, command=self.mostrar_frame_registro)
        boton_cambio_login.pack(side="left")
        
        self.frame_registro = ctk.CTkFrame(self.contenedor_auth, fg_color="transparent")
        titulo_reg = ctk.CTkLabel(self.frame_registro, text="Crear Cuenta", font=ctk.CTkFont(size=36, weight="bold"))
        titulo_reg.pack(pady=(20, 20))
        self.entrada_usuario_registro = ctk.CTkEntry(self.frame_registro, placeholder_text="Usuario", width=250, height=40)
        self.entrada_usuario_registro.pack(pady=10)
        self.entrada_email_registro = ctk.CTkEntry(self.frame_registro, placeholder_text="Email", width=250, height=40)
        self.entrada_email_registro.pack(pady=10)
        self.entrada_clave_registro = ctk.CTkEntry(self.frame_registro, placeholder_text="Contraseña", show="*", width=250, height=40)
        self.entrada_clave_registro.pack(pady=10)
        self.etiqueta_mensaje_registro = ctk.CTkLabel(self.frame_registro, text="", font=ctk.CTkFont(size=12))
        self.etiqueta_mensaje_registro.pack(pady=(0, 10))
        boton_registro = ctk.CTkButton(self.frame_registro, text="Registrarse", width=250, height=40, command=self.intentar_registro)
        boton_registro.pack(pady=20)
        frame_cambio_reg = ctk.CTkFrame(self.frame_registro, fg_color="transparent")
        frame_cambio_reg.pack(pady=10)
        etiqueta_reg = ctk.CTkLabel(frame_cambio_reg, text="¿Ya tienes cuenta?")
        etiqueta_reg.pack(side="left")
        boton_cambio_reg = ctk.CTkButton(frame_cambio_reg, text="Inicia Sesión", fg_color="transparent", hover=False, command=self.mostrar_frame_login)
        boton_cambio_reg.pack(side="left")
        
    def crear_widgets_principales(self):
        """Crea los widgets para la vista principal del launcher."""
        self.etiqueta_bienvenida = ctk.CTkLabel(self.contenedor_principal, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.etiqueta_bienvenida.pack(pady=40)

        boton_jugar = ctk.CTkButton(self.contenedor_principal, text="Jugar Haxball", width=300, height=60, font=ctk.CTkFont(size=18), command=self.iniciar_juego)
        boton_jugar.pack(pady=20)
        
        boton_perfil = ctk.CTkButton(self.contenedor_principal, text="Ver Perfil", width=300, height=60, font=ctk.CTkFont(size=18), command=self.mostrar_vista_perfil)
        boton_perfil.pack(pady=20)

        boton_logout = ctk.CTkButton(self.contenedor_principal, text="Cerrar Sesión", width=120, height=30, command=self.cerrar_sesion)
        boton_logout.pack(side="bottom", pady=20)
        
    def crear_widgets_perfil(self):
        """Crea los widgets para la vista de perfil de usuario."""
        titulo_perfil = ctk.CTkLabel(self.contenedor_perfil, text="Perfil de Usuario", font=ctk.CTkFont(size=36, weight="bold"))
        titulo_perfil.pack(pady=(20, 40))

        frame_datos = ctk.CTkFrame(self.contenedor_perfil)
        frame_datos.pack(pady=20, padx=60, fill="x")

        # Campos de datos (etiqueta y valor)
        etiqueta_nombre = ctk.CTkLabel(frame_datos, text="Nombre de Usuario:", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        etiqueta_nombre.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.valor_nombre = ctk.CTkLabel(frame_datos, text="Cargando...", font=ctk.CTkFont(size=16), anchor="w")
        self.valor_nombre.grid(row=0, column=1, padx=20, pady=15, sticky="w")
        
        etiqueta_email = ctk.CTkLabel(frame_datos, text="Email:", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        etiqueta_email.grid(row=1, column=0, padx=20, pady=15, sticky="w")
        self.valor_email = ctk.CTkLabel(frame_datos, text="Cargando...", font=ctk.CTkFont(size=16), anchor="w")
        self.valor_email.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        etiqueta_miembro = ctk.CTkLabel(frame_datos, text="Miembro desde:", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        etiqueta_miembro.grid(row=2, column=0, padx=20, pady=15, sticky="w")
        self.valor_miembro = ctk.CTkLabel(frame_datos, text="Cargando...", font=ctk.CTkFont(size=16), anchor="w")
        self.valor_miembro.grid(row=2, column=1, padx=20, pady=15, sticky="w")
        
        frame_datos.grid_columnconfigure(1, weight=1) # Permite que la columna de valores se expanda

        boton_volver = ctk.CTkButton(self.contenedor_perfil, text="Volver al Menú", width=200, height=40, command=self.mostrar_vista_principal)
        boton_volver.pack(side="bottom", pady=40)

    # --- Lógica de Navegación y Vistas ---
    def mostrar_vista_auth(self):
        self.contenedor_principal.pack_forget()
        self.contenedor_perfil.pack_forget()
        self.contenedor_auth.pack(fill="both", expand=True, padx=20, pady=20)
        self.geometry("400x580")
        self.resizable(False, False)
        self.mostrar_frame_login()
        self.centrar_ventana()

    def mostrar_vista_principal(self):
        self.contenedor_auth.pack_forget()
        self.contenedor_perfil.pack_forget()
        self.etiqueta_bienvenida.configure(text=f"¡Bienvenido, {self.usuario_actual}!")
        self.contenedor_principal.pack(fill="both", expand=True, padx=20, pady=20)
        self.geometry("800x600")
        self.resizable(True, True)
        self.centrar_ventana()
        
    def mostrar_vista_perfil(self):
        """Busca los datos del usuario actual y los muestra en la vista de perfil."""
        self.contenedor_principal.pack_forget()
        self.contenedor_perfil.pack(fill="both", expand=True, padx=20, pady=20)

        # Actualizar las etiquetas con datos reales
        perfil, mensaje = obtener_perfil_usuario(self.usuario_actual)
        if perfil:
            self.valor_nombre.configure(text=perfil.username)
            self.valor_email.configure(text=perfil.email)
            self.valor_miembro.configure(text=perfil.fecha_creacion_formateada)
        else:
            self.valor_nombre.configure(text="Error")
            self.valor_email.configure(text="Error")
            self.valor_miembro.configure(text=mensaje)

    def mostrar_frame_login(self):
        self.frame_registro.pack_forget()
        self.etiqueta_mensaje_registro.configure(text="")
        self.frame_login.pack(fill="both", expand=True)

    def mostrar_frame_registro(self):
        self.frame_login.pack_forget()
        self.etiqueta_mensaje_login.configure(text="")
        self.frame_registro.pack(fill="both", expand=True)

    # --- Lógica de la Aplicación ---
    def iniciar_juego(self):
        """Oculta el launcher y lanza el juego en un proceso separado."""
        self.withdraw()

        proceso_juego = multiprocessing.Process(target=lanzar_proceso_juego)
        proceso_juego.start()

        hilo_observador = threading.Thread(target=self.esperar_cierre_del_juego, args=(proceso_juego,))
        hilo_observador.start()

    def esperar_cierre_del_juego(self, proceso):
        """Este método se ejecuta en el hilo observador."""
        proceso.join()
        self.after(0, self.deiconify)

    def intentar_login(self):
        usuario = self.entrada_usuario_login.get()
        clave = self.entrada_clave_login.get()
        exito, mensaje = iniciar_sesion_usuario(usuario, clave)
        if exito:
            self.usuario_actual = usuario
            self.mostrar_vista_principal()
        else:
            self.etiqueta_mensaje_login.configure(text=mensaje, text_color="red")

    def intentar_registro(self):
        usuario = self.entrada_usuario_registro.get()
        email = self.entrada_email_registro.get()
        clave = self.entrada_clave_registro.get()
        exito, mensaje = registrar_usuario(usuario, email, clave)
        color = "green" if exito else "red"
        self.etiqueta_mensaje_registro.configure(text=mensaje, text_color=color)
        
    def cerrar_sesion(self):
        self.usuario_actual = None
        self.mostrar_vista_auth()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y}')

# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = Aplicacion()
    app.mainloop()

