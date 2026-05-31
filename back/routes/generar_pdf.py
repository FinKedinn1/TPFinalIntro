from io import BytesIO

from flask import Blueprint, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from db import get_db_connection


generar_pdf_bp = Blueprint("generar_pdf", __name__)


def escribir_texto_multilinea(pdf, texto, x, y, ancho_maximo, alto_linea):
    palabras = texto.split()
    linea_actual = ""

    for palabra in palabras:
        linea_de_prueba = f"{linea_actual} {palabra}".strip()

        if pdf.stringWidth(linea_de_prueba, "Helvetica", 10) <= ancho_maximo:
            linea_actual = linea_de_prueba
        else:
            pdf.drawString(x, y, linea_actual)
            y -= alto_linea
            linea_actual = palabra

    if linea_actual:
        pdf.drawString(x, y, linea_actual)
        y -= alto_linea

    return y


@generar_pdf_bp.route("/menu/pdf", methods=["GET"])
def descargar_menu_pdf():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        c.nombre_plato,
        c.descripcion,
        c.precio,
        c.categoria,
        c.stock,
        COALESCE(pp.es_popular, FALSE) AS popular,
        COALESCE(pp.promedio_estrellas, 0.00) AS promedio_estrellas,
        COALESCE(pp.`cantidad_resenas`, 0) AS cantidad_resenas
    FROM carta c
    LEFT JOIN platos_populares pp
        ON c.id_plato = pp.id_plato
    ORDER BY c.categoria, c.nombre_plato
    """

    cursor.execute(query)
    platos = cursor.fetchall()

    cursor.close()
    connection.close()

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)
    ancho_pagina, alto_pagina = A4

    margen_x = 2 * cm
    margen_superior = 2 * cm
    y = alto_pagina - margen_superior

    pdf.setTitle("Menu - La Taberna del Dragon")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(margen_x, y, "Menu - La Taberna del Dragon")

    y -= 1 * cm

    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        margen_x,
        y,
        "Listado generado automaticamente desde la base de datos."
    )

    y -= 1.2 * cm

    if not platos:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(margen_x, y, "No hay platos cargados en la carta.")
    else:
        categoria_actual = None

        for plato in platos:
            if y < 4 * cm:
                pdf.showPage()
                y = alto_pagina - margen_superior

            categoria = plato["categoria"] or "Sin categoria"

            if categoria != categoria_actual:
                categoria_actual = categoria

                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(margen_x, y, categoria_actual)

                y -= 0.8 * cm

            nombre = plato["nombre_plato"]
            descripcion = plato["descripcion"] or "Sin descripcion"
            precio = plato["precio"]
            stock = plato["stock"]
            popular = plato["popular"]
            promedio_estrellas = plato["promedio_estrellas"]
            cantidad_resenas = plato["cantidad_resenas"]

            texto_stock = "Disponible" if stock else "Sin stock"

            texto_popular = ""
            if popular:
                texto_popular = (
                    f" - Plato popular "
                    f"({promedio_estrellas}/5, {cantidad_resenas} reseñas)"
                )

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(
                margen_x,
                y,
                f"{nombre} - ${precio}{texto_popular}"
            )

            y -= 0.6 * cm

            pdf.setFont("Helvetica", 10)
            y = escribir_texto_multilinea(
                pdf=pdf,
                texto=descripcion,
                x=margen_x,
                y=y,
                ancho_maximo=16 * cm,
                alto_linea=0.45 * cm
            )

            pdf.setFont("Helvetica-Oblique", 9)
            pdf.drawString(margen_x, y, texto_stock)

            y -= 0.8 * cm

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="menu_taberna_del_dragon.pdf",
        mimetype="application/pdf"
    )
