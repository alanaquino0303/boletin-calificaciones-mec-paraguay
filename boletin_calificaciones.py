from fpdf import FPDF    
import datetime    
import os    
    
# Función para validar calificaciones (1 a 5).    
def input_float(prompt):    
    while True:    
        s = input(prompt).strip()    
        s = s.replace(",", ".")    
        try:    
            val = float(s)    
            if 1 <= val <= 5:    
                return round(val, 2)    
            else:    
                print("Ingrese un número entre 1 y 5.")    
        except ValueError:    
            print("Valor no válido. Intente de nuevo.")    
    
# Recolección de datos.    
def gather_data():    
    print("DATOS GENERALES")    
    usuario = input("Nombre de usuario: ")    
    institucion = input("Nombre del colegio: ")    
    turno = input("Turno: ")    
    curso = input("Curso: ")    
    seccion = input("Sección: ")    
    ano = input("Año: ")    
    
    print("\nDATOS DEL ALUMNO/A")    
    nombre = input("Nombre y apellido del alumno: ")    
    ci = input("C.I. del alumno: ")    
    edad = input("Edad: ")    
    sexo = input("Sexo (M/F): ")    
    enfasis = input("Énfasis: ")    
    
    print("\nASIGNATURAS")    
    asignaturas = []    
    while True:    
        nombre_asig = input("Nombre de la asignatura (ENTER para terminar): ")    
        if not nombre_asig:    
            break    
        plan = input("Tipo de plan (Común/Específico): ")    
        profesor_a = input("Profesor/a: ")    
        c1 = input_float(" Calificación 1ª etapa: ")    
        c2 = input_float(" Calificación 2ª etapa: ")    
        final = round((c1 + c2) / 2, 2)    
        asignaturas.append({    
            "plan": plan,    
            "nombre": nombre_asig,    
            "profesor": profesor_a,    
            "c1": c1,    
            "c2": c2,    
            "final": final    
        })    
        print("Asignatura agregada.\n")    
    
    mensaje = input("\nInforme descriptivo para el alumno/a: ")    
    
    return {    
        "usuario": usuario,    
        "institucion": institucion,    
        "turno": turno,    
        "curso": curso,    
        "seccion": seccion,    
        "ano": ano,    
        "nombre": nombre,    
        "ci": ci,    
        "edad": edad,    
        "sexo": sexo,    
        "enfasis": enfasis,    
        "asignaturas": asignaturas,    
        "mensaje": mensaje    
    }    
    
# Clase PDF.    
class BoletinPDF(FPDF):    
    def header(self):    
        # Logo del MEC.    
        if os.path.exists("logo_mec.png"):    
            self.image("logo_mec.png", x=15, y=8, w=20)    
        # Título del MEC.    
        self.set_font("Helvetica", "B", 14)    
        self.cell(0, 8, "MINISTERIO DE EDUCACIÓN Y CIENCIAS", ln=1, align="C")    
        self.ln(2)    
    
# Generación del PDF.    
def generar_pdf(data):    
    pdf = BoletinPDF(orientation='L', unit='mm', format='A4')    
    pdf.add_page()    
    pdf.set_auto_page_break(auto=True, margin=15)    
    
    # Nombre del colegio debajo del MEC.    
    pdf.set_font("Helvetica", "B", 16)    
    pdf.cell(0, 8, data["institucion"].upper(), ln=1, align="C")    
    pdf.ln(6)    
    
    pdf.set_font("Helvetica", "", 10)    
    left_x = 20    
    right_x = 160    
    line_height = 6    
    
    # Datos del alumno (en dos columnas tabuladas).    
    def data_line(left_label, left_value, right_label, right_value, y_offset):    
        pdf.set_xy(left_x, y_offset)    
        pdf.set_font("Helvetica", "B", 10)    
        pdf.cell(40, line_height, f"{left_label}:", 0)    
        pdf.set_font("Helvetica", "", 10)    
        pdf.cell(60, line_height, left_value, 0)    
    
        if right_label:  # Evita imprimir ":" sin texto.    
            pdf.set_xy(right_x, y_offset)    
            pdf.set_font("Helvetica", "B", 10)    
            pdf.cell(30, line_height, f"{right_label}:", 0)    
            pdf.set_font("Helvetica", "", 10)    
            pdf.cell(40, line_height, right_value, ln=1)    
    
    y = 35    
    data_line("NOMBRE Y APELLIDO", data["nombre"], "CURSO", data["curso"], y)    
    data_line("C.I.", data["ci"], "TURNO", data["turno"], y + 6)    
    data_line("SECCIÓN", data["seccion"], "AÑO", data["ano"], y + 12)    
    data_line("ÉNFASIS", data["enfasis"], "EDAD", data["edad"], y + 18)    
    data_line("SEXO", data["sexo"], "", "", y + 24)    

    pdf.ln(20)    
    
    # Tabla de asignaturas.    
    pdf.set_font("Helvetica", "B", 10)    
    pdf.set_fill_color(220, 220, 220)    
    widths = {"plan": 40, "disc": 90, "prof": 50, "c1": 24, "c2": 24, "final": 24}    
    headers = ["PLAN", "DISCIPLINAS", "PROFESOR/A", "1ª ETAPA", "2ª ETAPA", "CALIF. FINAL"]    
    
    for i, h in enumerate(headers):    
        pdf.cell(list(widths.values())[i], 8, h, border=1, align="C", fill=True)    
    pdf.ln()    
    
    pdf.set_font("Helvetica", "", 10)    
    for a in data["asignaturas"]:    
        pdf.cell(widths["plan"], 8, f"Plan {a['plan']}", border=1)    
        pdf.cell(widths["disc"], 8, a["nombre"], border=1)    
        pdf.cell(widths["prof"], 8, a["profesor"], border=1)    
        pdf.cell(widths["c1"], 8, f"{a['c1']:.2f}", border=1, align="C")    
        pdf.cell(widths["c2"], 8, f"{a['c2']:.2f}", border=1, align="C")    
        pdf.cell(widths["final"], 8, f"{a['final']:.2f}", border=1, align="C")    
        pdf.ln()    
    
    # Cálculos.    
    total_puntos = sum(a["final"] for a in data["asignaturas"])    
    promedio = round(total_puntos / len(data["asignaturas"]), 2)    
    
    # Si obtiene 1 en cualquiera de las etapas, no es promovido.    
    tiene_uno = any(a["c1"] == 1 or a["c2"] == 1 for a in data["asignaturas"])    
    promovido = "NO" if tiene_uno else "SÍ"    
    
    pdf.ln(5)    
    pdf.set_font("Helvetica", "B", 11)    
    pdf.cell(50, 8, "TOTAL DE PUNTOS:", 0)    
    pdf.set_font("Helvetica", "", 11)    
    pdf.cell(30, 8, f"{total_puntos:.2f}", ln=1)    
    
    pdf.set_font("Helvetica", "B", 11)    
    pdf.cell(50, 8, "PROMEDIO GENERAL:", 0)    
    pdf.set_font("Helvetica", "", 11)    
    pdf.cell(30, 8, f"{promedio:.2f}", ln=1)    
    
    pdf.set_font("Helvetica", "B", 11)    
    pdf.cell(50, 8, "PROMOVIDO/A:", 0)    
    pdf.set_font("Helvetica", "", 11)    
    pdf.cell(30, 8, promovido, ln=1)    
    
    pdf.ln(5)    
    pdf.set_font("Helvetica", "B", 10)    
    pdf.cell(0, 6, "INFORME DESCRIPTIVO:", ln=1)    
    pdf.set_font("Helvetica", "", 10)    
    pdf.multi_cell(0, 6, data["mensaje"], border=1)    
    
    pdf.ln(12)    
    pdf.set_font("Helvetica", "B", 10)    
    pdf.cell(120, 6, "FIRMA DEL PADRE/MADRE/TUTOR: ___________________________", 0, 0, "L")    
    pdf.cell(120, 6, "FIRMA DEL DIRECTOR/A: ___________________________", 0, 1, "R")    
    
    # Pie de página.    
    pdf.set_y(-15)    
    pdf.set_font("Helvetica", "I", 8)    
    fecha = datetime.datetime.now().strftime("%d/%m/%Y a las %H:%M")    
    pdf.cell(0, 8, f"Generado el {fecha} por {data['usuario']}", align="L")    
    
    filename = f"Boletín_{data['nombre'].replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"    
    pdf.output(filename)    
    print(f"\nPDF generado correctamente: {filename}")    
    
# Ejecución principal.    
def main():    
    data = gather_data()    
    if not data["asignaturas"]:    
        print("No se ingresaron asignaturas.")    
        return    
    generar_pdf(data)    
    
if __name__ == "__main__":    
    main()