import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# tk.Tk. Administra las diferentes páginas y proporciona la lógica para cambiar entre ellas.

class BioApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Caculo para el dimensionamiento de biodigestores y para su viabilidad para la implementación")
        self.geometry("1400x900")
        self.configure(bg="gainsboro")

# Hace ocupar todo el espacio disponible, adaptándose al tamaño de la ventana/pantalla.

        self.Contenedor = tk.Frame(self, bg="gainsboro")
        self.Contenedor.pack(fill="both", expand=True)

        self.pantalla = {}

# Inicializa y gestiona varias páginas en la aplicación Tkinter, permitiendo moverse entre ellas

        for F in (Paginainicio, Paginaresultado, Tabla1, Tabla2, Tabla3, Bioreactores):
            Nombrepagina = F.__name__
            Pantalla = F(parent=self.Contenedor, controlador=self)
            Pantalla.configure(bg="gainsboro")
            self.pantalla[Nombrepagina] = Pantalla
            Pantalla.grid(row=0, column=0, sticky="nsew")

        self.TipoPagina("Paginainicio")

    def TipoPagina(self, Nombrepagina):
        Pantalla = self.pantalla[Nombrepagina]
        Pantalla.tkraise()

# Relaciona los campos de Entradas y los cálculos en los campos de salida

    def calculate(self):
        try:
            T = float(self.pantalla["Paginainicio"].T.get())
            TRH = float(self.pantalla["Paginainicio"].TRH.get())
            CED = float(self.pantalla["Paginainicio"].CED.get())
            R = int(self.pantalla["Paginainicio"].R.get())
            EPBE = float(self.pantalla["Paginainicio"].EPBE.get())
            CSV = float(self.pantalla["Paginainicio"].CSV.get())
            PBCSV = float(self.pantalla["Paginainicio"].PBCSV.get())

            TRBB = self.calcular_TRBB(T)
            ZGT = self.calcular_ZGT(T)
            LANR = self.calcular_LANR(R, CED)
            VUBR = round(self.calcular_VUBR(TRH, CED, LANR), 4)
            PBR = round(self.calcular_PBR(CED, EPBE, CSV, PBCSV), 4)
            CH4=  round(self.calcular_CH4(PBR), 4)
            PER = round(self.calcular_PER(PBR), 4)
            H2SR = round(self.calcular_H2SR(PBR), 4)
            ESBR = round(self.calcular_ESBR(CED), 4)

            self.pantalla["Paginaresultado"].actualizador_resultados(ZGT, TRBB,  LANR, VUBR, PBR, CH4, PER, H2SR, ESBR)
            self.TipoPagina("Paginaresultado")

        except ValueError:
            self.pantalla["Paginainicio"].Mensajeerror("Por favor, ingrese números y utilice puntos para los decimales.")

# Cálculos y condicionales

    def calcular_ZGT(self, T):
        if  0 <= T <= 5:
            return "Zona bajo 0. Debe introducir (T >5C°) para activar las bacterias, ya que no hay rango optimo para el proceso."
        elif 5 <= T <= 22:
            return "Se encuentra en regiones de altiplano, y puede que influyan condiciones de Valle. (Rango: Psycrophilico)."
        elif 22 < T <= 32:
            return "Se encuentra en regiones de Valle, y puede que influyan condiciones de Altiplano y Trópico. (Rango: Mesophilico)."
        elif 32 < T <= 40:
            return "Se encuentra en regiones de Trópico, y puede que influyan condiciones de Valle. (Rango: Thermophilico)."
        elif 40 < T <= 56:
            return "Zonas de alta temperatura tipo desérticas, necesita control de T. (Rango: Thermophilico)."
        else:
            return "La temperatura ingresada deberia estar entre 0C° a 56C°"

    def calcular_TRBB(self, T):
        if  0 <= T <= 5:
            return "Debes por lo menos mantener la T >=7 C°  en el sistema, para tener una fermentación Psycrophilica."
        elif 5 <= T <= 22:
            return "La temperatura que se recomienda dentro del sistema es de 10 a 28 C°."
        elif 22 < T <= 32:
            return "La temperatura que se recomienda dentro del sistema es de 28 a 40 C°."
        elif 32 < T <= 40:
            return "La temperatura que se recomienda dentro del sistema es de 40 a 75 C°."
        elif 40 < T <= 56:
            return "Debes mantener una T<=75 C°  en el sistema para tener una fermentación Thermophilica."
        else:
            return "A esta temperatura no es viable económicamente los procesos de fermentación bacteriana"

    def calcular_LANR(self, R, CED):
        if R == 0:
            return 0
        elif R == 1:
            return CED
        elif R == 2:
            return (CED+(CED*0.05) * 2)
        elif R == 3:
            return (CED+(CED*0.05) * 3)
        else:
            return "Elija un valor entre 0 y 3 con respecto al tipo de material que suministrará"
        
    def calcular_VUBR(self, TRH, CED, LANR):
        return (TRH * ((CED+LANR) / 1000) / 2.4) + (TRH * ((CED+LANR) / 1000))

    def calcular_PBR(self, CED, EPBE, CSV, PBCSV):
        if CSV > 0:
            return ((CED)*CSV)*PBCSV
        else:
            return (CED*EPBE)

    def calcular_CH4(self, PBR):
        return PBR * 0.65
    
    def calcular_PER(self, PBR):
        return PBR * 2.4

    def calcular_H2SR(self, PBR):
        return (PBR * 0.0005)

    def calcular_ESBR(self, CED):
        return 0.98 * CED

# Crea e inicializa la interfaz para que el Frame de Entradas se configure y funcione en la ventana principal  y cambie el color de fondo.

class Paginainicio(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="gainsboro")

        self.T = tk.StringVar()
        self.TRH = tk.StringVar()
        self.CED = tk.StringVar()
        self.R = tk.StringVar(value="0")
        self.EPBE = tk.StringVar()
        self.CSV = tk.StringVar(value="0")
        self.PBCSV = tk.StringVar(value="0")

        labeltitulo = tk.Label(self, text="Ingrese los datos para realizar el dimensionamiento y la equivalencia de producción teórica", font=("Arial", 11, "bold"), bg="gainsboro")
        labeltitulo.grid(row=0, column=0, columnspan=2, pady=10)

# Creación de texto para campos de Entradas de las variables

        self.Entradas("Sensación térmica suministrar el promedio de (T) de la zona  C°.", self.T, row=1)
        self.Entradas("Tiempo (Días) de retención hidráulica (TRH), ver tabla 1.", self.TRH, row=3)
        self.Entradas("Cantidad de carga diaria que tendrá el biodigestor (Kg-Lt)", self.CED, row=5)
        self.Entradas("Tipo de material (0- líquidos, 1- muy húmedo, 2- poco húmedo, 3- restos vegetales o material de poca humedad).", self.R, row=7, combobox=True)
        self.Entradas("Equivalente de producción de biogás (M3/Kg), ten en cuenta que la precisión de la producción es\n afectada por el material no organico presente en la carga dispuesta, ver tabla 2.", self.EPBE, row=9)
        self.Entradas("(Opcional de %SV/Kg) Contenido porcentual de sólidos volátiles.", self.CSV, row=11)
        self.Entradas("(Obligatorio ingresar dato, si ingreso en %SV). \nProducción de biogás a partir de sólidos volátiles (M3/Kg SV), o ver tabla 3. ", self.PBCSV, row=13)

        self.etiquetaerror = tk.Label(self, text="", fg="red", bg="gainsboro")
        self.etiquetaerror.grid(row=16, column=0, pady=0, sticky="e")

# Ejecuta y controla  el boton de función calcular y de la img de tablas

        botoncalcular = tk.Button(self, text="Calcular", command=controlador.calculate)
        botoncalcular.grid(row=15, column=0, columnspan=2, pady=1) 

        botondepantallas = tk.Frame(self, bg="gainsboro")
        botondepantallas.grid(row=17, column=0, columnspan=2, pady=2)

        botonTBL1 = tk.Button(botondepantallas, text="Ver Tabla 1", command=lambda: controlador.TipoPagina("Tabla1"))
        botonTBL1.grid(row=0, column=1, padx=2)

        botonTBL2 = tk.Button(botondepantallas, text="Ver Tabla 2", command=lambda: controlador.TipoPagina("Tabla2"))
        botonTBL2.grid(row=0, column=2, padx=2)

        botonTBL3 = tk.Button(botondepantallas, text="Ver Tabla 3", command=lambda: controlador.TipoPagina("Tabla3"))
        botonTBL3.grid(row=0, column=3, padx=2)


        etiquetadereferencias = tk.Label(self, text="REFERENCIAS ", font=("Arial", 9, "bold"), bg="gainsboro")
        etiquetadereferencias.grid(row=18, column=0, columnspan=2, pady=2)
        
        etiquetatextodereferencia = tk.Label(self, text="Casanovas, G., Della, F., Reymundo, F., & Serafini, R. (2019). Guía teórico-práctica sobre el biogás y los biodigestores. FAO.\n"
                                                                                            "Pautrat Guerra, J. A. (2010). Diseño de biodigestor y producción de biogás con excremento vacuno en la granja agropecuaria de Yauris.\n"
                                                                                            "Varnero, M. M. T. (2011). Manual de biogas. Minenergia-PNUD-FAO-GEF. Santiago de Chile.\n"
                                                                                            "Herrero, J. M. (2008). Biodigestores familiares: Guía de diseño y manual de instalación. Jaime Marti Herrero. Y Pautrat Guerra, J. A. (2010).\n"
                                                                                            "Pautrat Guerra, J. A. (2010). Diseño de biodigestor y producción de biogás con excremento vacuno en la granja agropecuaria de Yauris.", font=("Arial", 9),anchor="w", justify="left",  bg="gainsboro")
        etiquetatextodereferencia.grid(row=19, column=0, columnspan=2, pady=0,sticky="w")

# Imagen en el lado derecho

        img_pantalla = tk.Frame(self, bg="gainsboro")
        img_pantalla.grid(row=0, column=4, rowspan=30, padx=0, pady=0, sticky="n")

        img_ruta = "imagenes\Características generales del biogás.png" 
        image = Image.open(img_ruta)
        image = image.resize((533, 700), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(img_pantalla, image=photo)
        self.image_label.image = photo
        self.image_label.pack()

# Diseño de los botones, campos de Entradas, mensaje de error y widget desplegable

    def Entradas(self, texto_etiqueta, variable, row, combobox=False):
        label = tk.Label(self, text=texto_etiqueta, font=("Arial", 11), bg="gainsboro")
        label.grid(row=row, column=0, columnspan=2, pady=4, padx=10, sticky="we")
         
        if combobox:
            entry = ttk.Combobox(self, textvariable=variable, values=["0", "1", "2", "3"], state="readonly", font=("Arial", 11), width=98, justify="center")
        else:
            entry = tk.Entry(self, textvariable=variable, font=("Arial", 11), width=98, justify="center")
        entry.grid(row=row+1, column=0, columnspan=2, pady=5, padx=10, sticky="we")

    def Mensajeerror(self, mensaje):
        self.etiquetaerror.config(text=mensaje)

# Crea e inicializa la interfaz para que el Frame de resultados se configure y funcione en la ventana principal.

class Paginaresultado(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="gainsboro")

        label = tk.Label(self, text="Evaluación del sistema según los parametros proporcionados", font=("Arial", 11, "bold"), bg="gainsboro")
        label.grid(row=0, column=0, columnspan=2, pady=10)

# Creación de texto para campos de salida de las variables resultado

        self.resultados = {}

        self.resultados["ZGT"] = self.Salidas("Características de la zona y tipo de fermentación según la temperatura.", 1)
        self.resultados["TRBB"] = self.Salidas("Temperatura recomendada para los procesos de las bacterias dentro del biodigestor.", 3)
        self.resultados["LANR"] = self.Salidas("Razón de mezcla, Lt de agua necesaria para mezclar con los Kg de carga.", 5)
        self.resultados["VUBR"] = self.Salidas("Volumen útil del biodigestor mas su mezcla (m3).", 7)
        self.resultados["PBR"] = self.Salidas("Producción de biogás (m3) en función de la completa degradación de los SV del sustrato (Carga) \n m3/kg o lt/kg según la unidad elegida en la tabla 2 de equivalencia.", 9)
        self.resultados["CH4"] = self.Salidas("Concentración de CH4 para esa producción.", 11)
        self.resultados["PER"] = self.Salidas("Capacidad de producción de energía con motores de alta eficiencia (kWh/m3).", 13)
        self.resultados["H2SR"] = self.Salidas("Concentración H2S resultante para esa producción (H2S/m3 biogás).", 15)
        self.resultados["ESBR"] = self.Salidas("Efluentes (Biofertilizantes) resultantes del proceso en el biodigestor (Kg-Lt).", 17)

# Botón para volver a la página de entrada de datos                                                        

        boton_volver = tk.Button(self, text="Volver", command=lambda: controlador.TipoPagina("Paginainicio"))
        boton_volver.grid(row=19, column=0, columnspan=2, pady=20)

        botondepantallas = tk.Frame(self, bg="gainsboro")
        botondepantallas.grid(row=20, column=0, columnspan=2, pady=10)
        buttonBioreactores = tk.Button(botondepantallas, text="Algunos tipos de biorreactores anaeróbicos", command=lambda: controlador.TipoPagina("Bioreactores"))
        buttonBioreactores.grid(row=20, column=1, padx=5)

# Crea la imagen al lado izquierd de la pagina

        img_pantalla = tk.Frame(self, bg="gainsboro")
        img_pantalla.grid(row=0, column=4, rowspan=30, padx=0, pady=0, sticky="n")

        img_ruta = "imagenes\Comportamiento y sustancias inhibidoras.png"
        image = Image.open(img_ruta)
        image = image.resize((551, 697), Image.LANCZOS)  # Usar Image.LANCZOS para redimensionamiento de alta calidad
        photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(img_pantalla, image=photo)
        self.image_label.image = photo
        self.image_label.pack()

# Diseño de los botones, campos de entradas y el mensaje de error

    def Salidas(self, texto_etiqueta, row):
        label = tk.Label(self, text=texto_etiqueta, font=("Arial", 11), wraplength=970, bg="gainsboro")
        label.grid(row=row, column=0, columnspan=2, pady=2, padx=10, sticky="we")
        result_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=result_var, font=("Arial", 11), state="disabled", width=98, justify="center")
        entry.grid(row=row+1, column=0, columnspan=2, pady=2, padx=10, sticky="we")
        return result_var
    
    
# Actualiza los resultados utilizando los nuevos valores y utiliza un numero de decimales deseadoo

    def actualizador_resultados(self,ZGT, TRBB, LANR, VUBR, PBR, CH4, PER, H2SR, ESBR):
        self.resultados["ZGT"].set(ZGT) 
        self.resultados["TRBB"].set(TRBB)
        self.resultados["LANR"].set(LANR)
        self.resultados["VUBR"].set(f"{VUBR:.4f}")
        self.resultados["PBR"].set(f"{PBR:.4f}")
        self.resultados["CH4"].set(f"{CH4:.4f}")
        self.resultados["PER"].set(f"{PER:.4f}")
        self.resultados["H2SR"].set(f"{H2SR:.4f}")
        self.resultados["ESBR"].set(f"{ESBR:.4f}")

#Crea una ventana nueva para las tablas 

class Tabla1(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="gainsboro")

        img_ruta = "imagenes\TBL1.jpg"
        self.image = ImageTk.PhotoImage(Image.open(img_ruta).resize((750, 500), Image.LANCZOS))

        tk.Label(self, image=self.image).pack(anchor="center", pady=40)

        botondepantallas = tk.Frame(self, bg="gainsboro")
        botondepantallas.pack(pady=10)
        boton_volver = tk.Button(botondepantallas, text="Volver", command=lambda: controlador.TipoPagina("Paginainicio"))
        boton_volver.grid(row=2, column=0, padx=5)


class Tabla2(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="gainsboro")

        img_ruta = "imagenes\TBL2.jpg"
        self.image = ImageTk.PhotoImage(Image.open(img_ruta).resize((1350, 600), Image.LANCZOS))

        tk.Label(self, image=self.image).pack(anchor="center", pady=20)

        botondepantallas = tk.Frame(self, bg="gainsboro")
        botondepantallas.pack(pady=10)
        boton_volver = tk.Button(botondepantallas, text="Volver", command=lambda: controlador.TipoPagina("Paginainicio"))
        boton_volver.grid(row=2, column=0, padx=5)


class Tabla3(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="gainsboro")

        img_ruta = "imagenes\TBL3.jpg"
        self.image = ImageTk.PhotoImage(Image.open(img_ruta).resize((900, 600), Image.LANCZOS))

        tk.Label(self, image=self.image).pack(anchor="center", pady=10)

        botondepantallas = tk.Frame(self, bg="gainsboro")
        botondepantallas.pack(pady=10)
        boton_volver = tk.Button(botondepantallas, text="Volver", command=lambda: controlador.TipoPagina("Paginainicio"))
        boton_volver.grid(row=2, column=0, padx=5)       

class Bioreactores(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="gainsboro")

        img_ruta = "imagenes\Tipos de biodigestores.png"
        self.image = ImageTk.PhotoImage(Image.open(img_ruta).resize((1360, 650), Image.LANCZOS))

        tk.Label(self, image=self.image).pack(anchor="center", pady=3)

        botondepantallas = tk.Frame(self, bg="gainsboro")
        botondepantallas.pack(pady=10)
        boton_volver = tk.Button(botondepantallas, text="Volver", command=lambda: controlador.TipoPagina("Paginaresultado"))
        boton_volver.grid(row=2, column=0, padx=3)  

# Se ejecuta como una aplicación independiente y realiza únicamente las instrucciones anteriores

if __name__ == "__main__":
    app = BioApp()
    app.mainloop()