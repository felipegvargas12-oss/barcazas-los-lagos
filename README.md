# Conectividad Marítima - Región de Los Lagos

## 1. Propósito y Proyección del Proyecto
Este proyecto consiste en una plataforma web colaborativa desarrollada en Django que entrega información centralizada sobre la conectividad marítima y el transporte de barcazas en la Región de Los Lagos. Su objetivo principal es permitir a los usuarios consultar itinerarios, disponibilidad de la flota de naves y el estado operativo de puertos y rampas en tiempo real.

### Proyección Futura
Para las siguientes fases del semestre, el sistema proyecta incorporar:
* Persistencia de datos mediante modelos y base de datos (PostgreSQL/SQLite).
* Sistema de autenticación de usuarios y perfiles diferenciados (Pasajeros / Administradores de navieras).
* Integración con APIs meteorológicas para alertas automáticas según el estado de las mareas y el clima.

---

## 2. Integrantes del Grupo
* **Felipe Ignacio Gómez Vargas**
* **Joaquín Alejandro Oyarzo Igor**
* **Luis Felipe Sánchez Vera**

---

## 3. Requisitos del Sistema e Instalación
Para que pueda ejecutar este proyecto en un entorno local, siga estos pasos:

### 3.1 Clonar el repositorio
Abre tu terminal (Command Prompt/CMD) y clona el repositorio desde GitHub:
cmd
git clone [https://github.com/felipegvargas12-oss/barcazas-los-lagos](https://github.com/felipegvargas12-oss/barcazas-los-lagos)
cd barcazas-los-lagos

### 3.2.- Crear el entorno virtual
Crea un entorno virtual dentro de la carpeta del proyecto:
python -m venv .venv

### 3.3.- Activar el entorno virual
Activa el entorno virtual segun el sistema operativo que se este utilizando:
Windows(CMD): .venv\Scripts\activate
Windows(PowerShell): .venv\Scripts\Activate.ps1
Linux/macOS: source source .venv/bin/activate

### 3.4.- Insatlar las dependencias
Instala Django y las demas llibrerias requeridas registradas en el archivo requirements.txt:
pip install -r requirements.txt

### 3.5.- Ejecutar migraciones iniciales
Ejecuta las migraciones de Django para preparar el sistema:
python manage.py migrate

### 3.6.- Inicia el servidor de desarollo
Inicia el servidor local de prueba:
python manage.py runserver

---

## 4. Estructura del Proyecto y Distribución de Módulos (se ve mejor ene el readme de visual studio code)
El proyecto está compuesto por la carpeta global de confuración (config) y las 3 aplicaciones Django independientes:

barcazas_los_lagos/
│
├── config/                 # Configuración principal del proyecto
│   ├── settings.py         # Configuración global (INSTALLED_APPS, TEMPLATES)
│   └── urls.py             # Enrutador principal mediante include()
│
├── flota/                  # App: Catálogo y gestión de naves
│   ├── urls.py             # Rutas locales (/flota/)
│   ├── views.py            # Vista lista_flota con contexto
│   └── templates/flota/    # Vistas HTML derivadas
│
├── rutas/                  # App: Trayectos y horarios
│   ├── urls.py             # Rutas locales (/ y /horarios/)
│   ├── views.py            # Vistas inicio y horarios
│   └── templates/rutas/    # Vistas HTML derivadas
|
├── templates/              # Directorio global de plantillas
│   └── base.html           # Template maestro con maquetación y menú común
│
├── terminales/             # App: Puertos, rampas y mareas
|   ├── urls.py             # Rutas locales (/terminales/)
|   ├── views.py            # Vista lista_terminales
|   └── templates/terminales/# Vistas HTML derivadas
│
├── .gitignore              # Archivos y carpetas omitidos en Git (.venv, pycache)
├── manage.py               # Script de administración de Django
├── README.md               # Documentación general del proyecto
└── requirements.txt        # Dependencias del proyecto

---

## 5. Registro de Uso de IA
En esta etapa del proyecto se utilizó la herramienta Gemini de Google como apoyo para la resolución de dudas técnicas y arquitectura de software. En total se realizaron 3 iteraciones clave con la IA. A continuación, se detalla el propósito de cada consulta, la efectividad de la respuesta obtenida y los aprendizajes generados por el grupo:

### Iteración 1: Delimitación de la idea y arquitectura base
* **Propósito:** Delimitar la idea del proyecto y estructurar la arquitectura base del sistema en Django conforme a los requerimientos de la evaluación.
* **Prompt utilizado:**
  > *"Estoy comenzando un proyecto en Django para una página sobre conectividad de barcazas en la Región de Los Lagos. Necesito definir 3 aplicaciones independientes que representen módulos reales del sistema. Recuerda que el alcance llega solo hasta templates, sin modelos ni base de datos. Qué estructura me recomiendas?"*
* **Evaluación de la respuesta:** La IA presentó cinco propuestas de arquitectura modular. Tras el análisis grupal, se seleccionaron tres módulos funcionales concretos: Catálogo de embarcaciones (flota), Itinerario de trayectos (rutas) y Ficha de rampas y terminales marítimos (terminales).
* **Aprendizaje obtenido:** Aprendimos sobre la división modular en Django mediante aplicaciones independientes, y así poder mantener un diseño escalable para futuras entregas.

### Iteración 2: Creación de aplicaciones y enrutamiento modular
* **Propósito:** Implementar la estructura física de las aplicaciones e interconectar los archivos de rutas locales con el enrutador principal del proyecto mediante la función include.
* **Prompt utilizado:**
  > *"Explícame paso a paso cómo crear cada app con startapp, configurar los archivos urls.py de cada app y conectarlos al urls.py principal usando include"*
* **Evaluación de la respuesta:** La IA nos dio una guía paso a paso clara para la ejecución del comando startapp, el registro de las aplicaciones dentro de INSTALLED_APPS en settings.py, y la delegación de rutas mediante include.
* **Aprendizaje obtenido:** Pudimos dominar y saber sobre el flujo de enrutamiento de django.

### Iteración 3: Maquetación global y herencia de plantillas
* **Propósito:** Diseñar un sistema de plantillas reutilizable que contenga un menú de navegación unificado mediante herencia de HTML.
* **Prompt utilizado:**
  > *"Necesito crear un template maestro base.html en una carpeta global. Explícame como configurar settings.py, estructurar un menú de navegación con url y hacer que los HTML hijos hereden con extends"*
* **Evaluación de la respuesta:** La IA detalló la configuración del directorio global de plantillas, la construcción del archivo base.html integrando etiquetas {% block %} y enlaces dinámicos con {% url %}, además de la sintaxis {% extends %} para los templates derivados.
* **Aprendizaje obtenido:** Aprendimos sobre como hacer una implementación efectiva de herencia de templates y resolución dinámica de rutas nombradas en Django.

### Iteración 4: Desarrollo del código de las vistas de cada aplicación
* **Propósito:** Solicitar el código completo de las funciones en views.py para cada una de las 3 aplicaciones (flota, rutas y terminales).
* **Prompt utilizado:**
  > *"Necesito que desarrolles el código de las vistas para las 3 aplicaciones que seleccionamos (flota, rutas y terminales). Muestra cómo usar render para renderizar las plantillas y cómo estructurar los diccionarios de contexto con datos dinámicos simulados (listas, variables, booleanos) en cada vista."*
* **Evaluación de la respuesta:** La respuesta fue sumamente clara y completa. La IA proporcionó el código exacto para cada archivo `views.py`, definiendo la lógica de backend necesaria para alimentar las 4 páginas del proyecto con información pertinente sobre barcazas, trayectos y puertos.
* **Aprendizaje obtenido:** Aprendimos a construir funciones de vista en Django que gestionan solicitudes HTTP y empaquetan información estructurada en contexto dinámico para ser consumida por la capa de presentación.

### Iteración 5: Desarrollo de los templates HTML de cada aplicación
* **Propósito:** Obtener el código de las plantillas HTML locales para cada aplicación, asegurando el uso correcto de la herencia del diseño global y el renderizado de datos del contexto con sintaxis for e if.
* **Prompt utilizado:**
  > *"Necesito que desarrolles el código de los templates HTML para cada aplicación dentro de sus carpetas locales. Muestra cómo deben heredar de base.html usando extends y block content, y cómo desplegar el contexto recibido mediante etiquetas for, if y variables."*
* **Evaluación de la respuesta:** La respuesta fue muy eficiente y precisa. La IA entregó el código HTML de las 4 páginas requeridas, aplicando adecuadamente la herencia del archivo maestro e integrando la lógica para mostrar estados operativos y listas detalladas.
* **Aprendizaje obtenido:** Dominamos la creación de plantillas derivadas dentro de la estructura modular de Django, logrando presentar la información del backend de forma organizada y reutilizando el diseño común definido en el proyecto.

---

## 6. Conclusiones y Refleción Grupal
El desarrollo de esta primera etapa permitió consolidar la estructura fundamental de un proyecto web profesional en Django. Se logró abstraer una problemática de conectividad del mundo real y representarla modularmente a través de tres aplicaciones desacopladas, utilizando vistas renderizadas, diccionarios de contexto y herencia de plantillas HTML.

Tuvimos problemas para manejar una colaboracion por Git y GitHub eso no impidio que pudieramos reorganizarnos y poder desarollar el proyecto entre todo el equipo. Asi mismo, la Inteligencia Artificial actuó como un asistente eficiente para resolver dudas de sintaxis y arquitectura, permitiendo al equipo comprender y verificar cada cambio implementado antes de llevarlo a producción. El proyecto queda completamente preparado para poder desarollarse a futuro y para realizar las siguientes evaluaciones.

