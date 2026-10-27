# AcademiaMarket — Catálogo web de servicios académicos

Aplicación web tipo marketplace (inspirada en Mercado Libre / AliExpress)
para explorar servicios académicos como ensayos, laboratorios, proyectos de
software, tutorías y más.

La solución usa **Flask** como backend ligero y **HTML, CSS y JavaScript**
(modulares, sin frameworks) para el frontend. Reutiliza el dominio y la
interfaz de servicios de la práctica anterior de POO.

## Funcionalidades

- **Vista de cuadrícula:** tarjetas con imagen, categoría, nombre, descripción
  corta, precio, cuotas y un botón de acceso al detalle.
- **Vista de detalle:** imagen a un lado; título, precio, cuotas, descripción
  completa, beneficios y acciones al otro.
- **Búsqueda en tiempo real** por nombre, descripción o categoría.
- **Filtros por categoría** generados dinámicamente desde los datos.
- **Ordenamiento** por relevancia, menor precio, mayor precio y nombre.
- **Rutas con hash:** `#/` para la cuadrícula y `#/producto/1` para el detalle.
  El botón Atrás del navegador funciona.
- **Estados de carga, error y catálogo vacío.**
- **Notificaciones simuladas** al contratar o guardar un servicio.
- **Diseño responsive** para escritorio, tableta y móvil.
- **API REST** preparada para futuras operaciones CRUD.

## Estructura del proyecto

```text
Catalogo/
├── app.py                              # Arranque de Flask
├── requirements.txt                    # Dependencia: Flask
├── main.py                             # Demo de consola anterior (opcional)
│
├── domain/
│   └── categoria_producto.py           # Modelo con validaciones
│
├── services/
│   ├── icatalogo_servicio.py           # Contrato ABC (interfaz)
│   ├── excepciones.py                  # Errores de negocio
│   └── impl/
│       ├── catalogo_servicio_memoria.py
│       └── datos_ejemplo.py            # Datos compartidos web/consola
│
├── ui/                                 # Vistas de consola anteriores
│
└── web/
    ├── app.py                          # Fábrica de la aplicación Flask
    ├── routes/
    │   └── catalogo_api.py             # Endpoints REST
    ├── templates/
    │   └── index.html                  # Documento base de la SPA
    └── static/
        ├── css/styles.css              # Estilos del marketplace
        ├── img/*.svg                   # Imágenes locales de los servicios
        └── js/
            ├── app.js                  # Controlador y router de la SPA
            ├── services/
            │   ├── ICatalogoServicio.js       # Contrato del frontend
            │   └── CatalogoApiServicio.js     # Cliente HTTP
            ├── views/
            │   ├── VistaCuadricula.js
            │   └── VistaDetalleProducto.js
            └── utils/
                ├── formato.js
                └── notificaciones.js
```

## Cómo ejecutar

### 1. Instalar Flask

Desde la carpeta `Catalogo`:

```powershell
python -m pip install -r requirements.txt
```

### 2. Iniciar el servidor

```powershell
python app.py
```

### 3. Abrir en el navegador

```text
http://127.0.0.1:5000
```

En PowerShell puedes abrirlo directamente con:

```powershell
Start-Process "http://127.0.0.1:5000"
```

## API disponible

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/productos` | Lista todos los productos |
| `GET` | `/api/productos/<id>` | Devuelve un producto o 404 |
| `POST` | `/api/productos` | Registra un producto nuevo |
| `DELETE` | `/api/productos/<id>` | Elimina un producto |

Ejemplo de cuerpo para `POST /api/productos`:

```json
{
  "id": 9,
  "nombre": "Curso de refuerzo",
  "descripcion": "Curso corto con ejercicios prácticos.",
  "precio_promedio": 150000,
  "url_imagen": "/static/img/placeholder.svg",
  "categoria": "Asesoría"
}
```

## Arquitectura y separación de responsabilidades

### Backend

- **domain/** modela y valida `CategoriaProducto`. No sabe nada de HTTP.
- **services/icatalogo_servicio.py** define el contrato con `abc.ABC`.
- **services/impl/catalogo_servicio_memoria.py** implementa ese contrato.
- **web/routes/catalogo_api.py** adapta HTTP al dominio y devuelve JSON.
- **web/app.py** inyecta la implementación del servicio en la aplicación.

### Frontend

- **services/ICatalogoServicio.js** es el contrato del frontend: una clase
  abstracta manual que no se puede instanciar.
- **services/CatalogoApiServicio.js** implementa el contrato consumiendo la API.
- **views/VistaCuadricula.js** solo se encarga de la cuadrícula.
- **views/VistaDetalleProducto.js** solo se encarga del detalle.
- **app.js** orquesta rutas, filtros y navegación.

Las vistas no conocen `fetch` ni las URLs de Flask. Solo conocen el contrato.
Si mañana se cambia la API por otro backend, solo se modifica
`CatalogoApiServicio.js`.

## Principio Abierto/Cerrado (OCP)

`ICatalogoServicio` declara lectura y CRUD desde el inicio:

```python
obtener_todos()
buscar_por_id(id)
registrar_producto(producto)
eliminar_producto(id)
```

La UI actual solo usa lectura. Los métodos de escritura ya existen en el
contrato y en la API, por lo que se puede agregar un formulario de
administración sin romper las vistas actuales.

Para cambiar el almacenamiento se crea otra implementación, por ejemplo
`CatalogoServicioSQLite`, y se inyecta en `web/app.py`:

```python
app.extensions["catalogo_servicio"] = CatalogoServicioSQLite()
```

Las rutas y el frontend no necesitan cambios.

## Decisiones de diseño

- Los precios se manejan como `float` para respetar el diagrama original. En
  un sistema real de facturación sería preferible `Decimal`.
- Las imágenes son SVG locales para que la demo funcione sin internet.
- El router usa `location.hash` para no necesitar configuración adicional de
  servidor y permitir recargar o compartir una URL de detalle.
- Se agregó `categoria` al modelo para que los filtros del marketplace sean
  parte del dominio y no datos inventados en la vista.
- La vista de consola anterior se conserva en `main.py` como referencia
  académica; la aplicación principal ahora se ejecuta con `python app.py`.

## Verificación

La aplicación fue probada con el cliente de pruebas de Flask y con un
navegador real:

- `GET /` responde 200.
- La API devuelve los 8 productos con categorías.
- Búsqueda, filtros, ordenamiento y navegación al detalle funcionan.
- Un producto inexistente muestra una vista 404 amigable.
- Lighthouse: 100 en accesibilidad, buenas prácticas y SEO.
