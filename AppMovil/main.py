from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.lang import Builder
import json
import os

def obtener_url_backend():
    ruta_config = 'config.json'
    if not os.path.exists(ruta_config):
        return 'http://127.0.0.1:5000'
        
    with open(ruta_config, 'r') as archivo:
        datos = json.load(archivo)
        return datos.get('BASE_URL', 'http://127.0.0.1:5000')

BASE_URL = obtener_url_backend()


class InicioScreen(Screen):
    def ir_a_carta_publica(self):
        self.manager.current = 'carta'
        self.manager.get_screen('carta').cargar_platos()


class CartaScreen(Screen):
    def cargar_platos(self):
        if 'lista_platos' in self.ids:
            self.ids.lista_platos.clear_widgets()
        
        UrlRequest(
            f"{BASE_URL}/carta",
            on_success=self.platos_cargados_ok,
            on_failure=self.error_carga,
            on_error=self.error_carga
        )

    def platos_cargados_ok(self, req, result):
        if 'lista_platos' not in self.ids:
            return
            
        platos = result
        if not platos:
            self.ids.lista_platos.add_widget(Label(text="No hay platos disponibles hoy.", size_hint_y=None, height=40))
            return

        for plato in platos:
            if isinstance(plato, dict):
                nombre = plato.get('nombre', 'Plato sin nombre')
                precio = plato.get('precio', '')
            else:
                nombre = plato[1]
                precio = plato[3] if len(plato) > 3 else ""

            texto_plato = f"🍕 {nombre} - ${precio}" if precio else f"🍕 {nombre}"
            
            lbl = Label(
                text=texto_plato,
                font_size='18sp',
                size_hint_y=None,
                height=40
            )
            self.ids.lista_platos.add_widget(lbl)

    def error_carga(self, req, error):
        if 'lista_platos' in self.ids:
            self.ids.lista_platos.add_widget(Label(text="Error al conectar con el backend.", color=[1,0,0,1], size_hint_y=None, height=40))


class LoginScreen(Screen):
    def procesar_login(self, email, password):
        if not email or not password:
            self.ids.mensaje_estado.text = "Completa todos los campos."
            return

        payload = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        
        UrlRequest(
            f"{BASE_URL}/login",
            req_body=json.dumps(payload),
            req_headers=headers,
            on_success=self.login_exitoso,
            on_failure=self.login_fallido,
            on_error=self.conexion_error
        )

    def login_exitoso(self, req, result):
        user_data = result.get('usuario')
        nombre_usuario = user_data['nombre'] if isinstance(user_data, dict) else user_data[1]
        
        pantalla_principal = self.manager.get_screen('principal')
        pantalla_principal.ids.bienvenido_label.text = f"¡Hola, {nombre_usuario}!"
        
        self.manager.current = 'principal'
        self.ids.mensaje_estado.text = "" 

    def login_fallido(self, req, result):
        mensaje = result.get('mensaje', 'Credenciales incorrectas') if isinstance(result, dict) else "Error"
        self.ids.mensaje_estado.color = [1, 0, 0, 1]
        self.ids.mensaje_estado.text = mensaje

    def conexion_error(self, req, error):
        self.ids.mensaje_estado.color = [1, 0, 0, 1]
        self.ids.mensaje_estado.text = "No se pudo conectar con el servidor."


class RegistroScreen(Screen):
    def procesar_registro(self, nombre, email, password):
        if not nombre or not email or not password:
            self.ids.mensaje_registro.text = "Completa todos los campos."
            return

        payload = {'nombre': nombre, 'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}

        UrlRequest(
            f"{BASE_URL}/usuarios",
            req_body=json.dumps(payload),
            req_headers=headers,
            on_success=self.registro_exitoso,
            on_failure=self.registro_fallido,
            on_error=self.conexion_error
        )

    def registro_exitoso(self, req, result):
        self.manager.current = 'login'
        self.manager.get_screen('login').ids.mensaje_estado.color = [0, 1, 0, 1]
        self.manager.get_screen('login').ids.mensaje_estado.text = "¡Cuenta creada! Ya puedes ingresar."
        
        self.ids.nombre_input.text = ""
        self.ids.email_registro.text = ""
        self.ids.password_registro.text = ""

    def registro_fallido(self, req, result):
        self.ids.mensaje_registro.color = [1, 0, 0, 1]
        self.ids.mensaje_registro.text = "Error al registrar el usuario."

    def conexion_error(self, req, error):
        self.ids.mensaje_registro.color = [1, 0, 0, 1]
        self.ids.mensaje_registro.text = "Error de conexión."


class PrincipalScreen(Screen):
    def ir_a_reservas(self):
        print("Navegando a reservas...")

    def cerrar_sesion(self):
        self.manager.current = 'inicio'


class RestoApp(App):
    def build(self):
        # 1. Buscamos la ruta absoluta inequívoca del archivo de diseño
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_kv = os.path.join(directorio_actual, 'main.kv')
        
        # 2. Forzamos la limpieza de caché y CARGAMOS el diseño en el motor de Kivy
        try:
            Builder.unload_file(ruta_kv)
        except:
            pass
        Builder.load_file(ruta_kv)
        
        # 3. Ahora que el motor conoce los diseños, creamos el administrador manual
        sm = ScreenManager()
        
        # 4. Registramos las pantallas una por una de forma explícita
        sm.add_widget(InicioScreen(name='inicio'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistroScreen(name='registro'))
        sm.add_widget(PrincipalScreen(name='principal'))
        sm.add_widget(CartaScreen(name='carta'))
        
        # 5. Definimos la pantalla de arranque
        sm.current = 'inicio'
        
        return sm

if __name__ == '__main__':
    RestoApp().run()