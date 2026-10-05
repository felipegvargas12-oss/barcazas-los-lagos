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

Para la configuración actual de rutas y horarios, también instala PostgreSQL Server, crea la base `barcazas_db` y configura la contraseña local en `.env` a partir de `.env.example`. El archivo `.env` está excluido de Git.

### 3.5.- Ejecutar migraciones iniciales
Ejecuta las migraciones de Django para preparar el sistema:
python manage.py migrate

Para cargar las rutas y horarios ficticios de demostración, ejecuta:
python manage.py cargar_rutas_demo

Para administrar rutas y horarios desde `/admin/`, crea una cuenta administrativa con:
python manage.py createsuperuser

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
│   ├── migrations/         # Esquema de rutas y horarios
│   ├── management/         # Comando cargar_rutas_demo
│   ├── models.py           # Modelos Ruta y Horario
│   └── map_data.py         # Coordenadas de referencia para el mapa
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

Además de las iteraciones anteriores, GitHub Copilot se utilizó posteriormente para ampliar el módulo de rutas y horarios. Esas solicitudes se documentan en la Iteración 6.

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

---

## 7. Cambios recientes en Rutas y Horarios
* **Consulta pública:** Se pueden consultar rutas, estado y próximas salidas futuras desde la página de rutas. Las personas pueden abrir el detalle de cada trayecto desde su nombre.
* **CRUD administrativo:** La creación, edición y eliminación de rutas y horarios se realiza únicamente desde Django Admin (`/admin/`). La página pública no muestra esos controles.
* **Modelo y migraciones:** Se agregó `Horario`, relacionado con `Ruta`, y el indicador `es_demostracion` para distinguir datos ficticios. Las migraciones agregadas son `0002_horario` y `0003_ruta_es_demostracion`.
* **Datos de demostración:** El comando `python manage.py cargar_rutas_demo` crea dos rutas y cuatro salidas ficticias, usando los mismos nombres de Pargua, Chacao y Hornopirén de la sección de terminales. Se puede ejecutar nuevamente sin duplicar esas salidas.
* **Mapa:** El detalle de cada ruta muestra marcadores y una línea esquemática con Leaflet y OpenStreetMap. Las coordenadas son referenciales; el punto de Hornopirén corresponde al centro de la localidad, no a una ubicación confirmada del embarcadero. El mapa no representa navegación real.
* **Diseño y pruebas:** El listado y el detalle del trayecto se adaptaron al estilo de tarjetas de “Puertos y Rampas” y a pantallas móviles. Se añadieron pruebas para consulta pública, carga demo y detalle con mapa. También se agregó `psycopg[binary]` para instalar el controlador de PostgreSQL en Windows.
* **Git:** Los cambios se trabajaron en `feature/consulta-rutas-horarios`; `.env` permanece excluido del repositorio.

### Iteración 8: Implementación de Persistencia PostgreSQL y CRUD Completo de Flota

En esta etapa se utilizó la asistencia de IA para estructurar de forma profesional y segura la persistencia relacional y el ciclo CRUD completo para el módulo de embarcaciones, cumpliendo con las pautas de validación y control de acceso.

#### 1. Infraestructura y Persistencia (Base de Datos y Entorno)
* **Problema:** Conectar el proyecto Django a PostgreSQL local resolviendo dependencias nativas en Windows y resguardando credenciales fuera del control de versiones.
* **Prompt utilizado:**
  > *"Configura la conexión de base de datos en config/settings.py para utilizar PostgreSQL con la librería psycopg en Django 5. Utiliza python-dotenv para cargar variables de entorno (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT) desde un archivo .env que esté protegido por .gitignore. Explica qué paquete binario se requiere en entornos Windows para evitar errores de compilación con C/libpq y cómo aplicar las migraciones iniciales."*

#### 2. Capa de Modelado ORM y Panel Administrativo
* **Problema:** Representar adecuadamente la entidad `Embarcacion` para la navegación regional y dotar al panel de administración de herramientas eficientes de consulta.
* **Prompt utilizado:**
  > *"En la app flota, define el modelo Embarcacion en flota/models.py con los campos: nombre (CharField), matrícula (CharField única e indexada), capacidad de pasajeros (PositiveIntegerField), capacidad vehicular (PositiveIntegerField) y activo (BooleanField). Configura Meta con nombres descriptivos y orden por nombre. Luego, regístralo en flota/admin.py con una clase ModelAdmin que incluya visualización de columnas (list_display), filtros por estado (list_filter) y barra de búsqueda (search_fields)."*

#### 3. Formularios con Validaciones de Negocio (ModelForm)
* **Problema:** Crear un formulario tipado con Bootstrap que impida el ingreso de datos erróneos o incoherentes para la capacidad del transbordador.
* **Prompt utilizado:**
  > *"Crea flota/forms.py implementando un ModelForm para Embarcacion. Agrega widgets HTML con clases CSS de Bootstrap (form-control, form-check-input) y placeholders. Implementa métodos de validación personalizada: clean_matricula para normalizar a mayúsculas y validar una longitud mínima de 4 caracteres, y clean_capacidad_pasajeros para asegurar que el valor sea estrictamente mayor a 0, arrojando forms.ValidationError en caso de error."*

#### 4. Lógica de Control (Vistas CRUD y Enrutamiento)
* **Problema:** Construir las operaciones de listar, crear, modificar y eliminar embarcaciones asegurando la captura de excepciones 404 y retroalimentación al usuario.
* **Prompt utilizado:**
  > *"Implementa en flota/views.py las vistas funcionales para el ciclo CRUD completo de Embarcacion: listar (lista_embarcaciones), registrar (crear_embarcacion), modificar (editar_embarcacion con get_object_or_404) y eliminar (eliminar_embarcacion). Utiliza django.contrib.messages para notificar al usuario sobre cada acción exitosa. Configura las rutas en flota/urls.py con un espacio de nombres app_name = 'flota' y vincúlalas al enrutador principal de Django."*

#### 5. Interfaz de Usuario y Templates Derivados
* **Problema:** Elaborar la presentación visual heredada de `base.html` que permita manipular el CRUD respetando estándares de accesibilidad y confirmación destructiva.
* **Prompt utilizado:**
  > *"Diseña las plantillas HTML dentro de flota/templates/flota/ heredando de base.html:
  > lista_embarcaciones.html: Tabla responsiva con badges para el estado operativo y botones de acción.
  > form_embarcacion.html: Formulario unificado para alta y edición con renderizado de errores por campo y protección CSRF.
  > confirmar_eliminar.html: Cuadro de diálogo de confirmación previa a la baja definitiva.
  > Asegura la visualización del bloque de alertas de Django."*

### Prompts utilizados para esta actualización
> *"necesito trabajaran en el apartado de rutas"*

> *"necesito que las personas puedan consultar sobre los las rutas y los horarios, tambien recuerda crear ramas y el uso correcto de los CRUD"*

> *"solo de demostracion pero que coincidan con los de puertos y rampas"*

> *"las opciones de editar, eliminar o agregar sacalas ya que eso solo deberia de aparecer en las opciones de admin, al igual que el que dice nueva ruta en verde"*

> *"es agregar la opcion de hacer click en unas de las opciones de rutas y horarios y que aparesca el mapa que muestre la ruta de esta ?¿"*

> *"quiero que se vea un poco mas profecional el apartado de rutas y horarios como esta en puertos y rampas"*

> *"ahora necesito que en el readme agreges todos los cambios que se hicieron y los prompts que se utilizaron"*

