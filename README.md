# Generador de Boletines de Calificaciones

Este proyecto permite generar **boletines de calificaciones personalizados en formato PDF**, siguiendo el formato oficial del **Ministerio de Educación y Ciencias (MEC)** del Paraguay. Su objetivo es automatizar la creación de reportes escolares con información institucional, calificaciones y observaciones, de manera precisa y profesional.

---

## Características principales

- Ingreso de datos institucionales, del alumno/a y del curso.
- Registro flexible de asignaturas, profesores y calificaciones.
- Cálculo automático del promedio y verificación de promoción.
- Generación de boletines en formato PDF.
- Inclusión opcional del logo del MEC en el encabezado.
- Interfaz por consola fácil de usar y completamente local.

---

## Estructura del proyecto

```
/ boletin-calificaciones-mec-paraguay
├── boletin_calificaciones.py                              # Script principal.
├── Boletín_Alan_Gustavo_Aquino_Romero_20251103_2034.pdf   # Ejemplo de salida.
├── logo_mec.png                                           # Logo del MEC (opcional).
└── README.md                                              # Documentación del proyecto.
```

---

## Requisitos

- **Python 3.8 o superior**.
- Librería necesaria:
  ```bash
  pip install fpdf
  ```

---

## Ejecución

### En Linux o macOS
1. Abrir una terminal.
2. Navegar hasta el directorio del proyecto.
3. Ejecutar:
   
   ```bash
   python3 boletin_calificaciones.py
   ```

### En Windows
1. Abrir una terminal.
2. Navegar hasta el directorio del proyecto.
3. Ejecutar:
   
   ```bash
   python boletin_calificaciones.py
   ```

El programa solicitará los datos paso a paso y generará un archivo PDF con el formato:

```
Boletín_Nombre_Apellido_YYYYMMDD_HHMM.pdf
```

---

## Autor

Alan Aquino.
