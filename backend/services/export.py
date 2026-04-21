from models.database import Recipe


def export_as_markdown(recipe: Recipe) -> str:
    lines = [
        f"# {recipe.title}",
        "",
        f"**Meal Type:** {recipe.meal_type or 'N/A'}",
        f"**Dietary Focus:** {recipe.dietary_focus or 'N/A'}",
        f"**Created At:** {recipe.created_at}",
        "",
        "## Ingredients",
        "",
    ]
    for ing in recipe.ingredients.split(","):
        lines.append(f"- {ing.strip()}")
    lines += ["", "## Steps", "", recipe.steps]
    return "\n".join(lines)


def export_as_pdf(recipe: Recipe) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib import colors
        import io

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("Title2", parent=styles["Heading1"],
                                     textColor=colors.HexColor("#e85d04"))
        h2 = ParagraphStyle("H2", parent=styles["Heading2"],
                             textColor=colors.HexColor("#333333"))

        story = [
            Paragraph(recipe.title, title_style),
            Spacer(1, 0.3*cm),
            Paragraph(f"<b>Meal Type:</b> {recipe.meal_type or 'N/A'}", styles["Normal"]),
            Paragraph(f"<b>Dietary Focus:</b> {recipe.dietary_focus or 'N/A'}", styles["Normal"]),
            Paragraph(f"<b>Created:</b> {recipe.created_at}", styles["Normal"]),
            Spacer(1, 0.5*cm),
            Paragraph("Ingredients", h2),
        ]
        for ing in recipe.ingredients.split(","):
            story.append(Paragraph(f"• {ing.strip()}", styles["Normal"]))
        story += [
            Spacer(1, 0.5*cm),
            Paragraph("Steps", h2),
            Paragraph(recipe.steps.replace("\n", "<br/>"), styles["Normal"]),
        ]
        doc.build(story)
        return buffer.getvalue()
    except ImportError:
        raise RuntimeError("reportlab is not installed")
