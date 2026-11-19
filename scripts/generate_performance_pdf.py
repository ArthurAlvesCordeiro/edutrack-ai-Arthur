
import io
from html import escape
from typing import Dict, List, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Flowable,
)
from reportlab.lib.units import mm


# ---------------------------------------------------------
# PALETA DE CORES - EDUTRACK AI
# ---------------------------------------------------------

NAVY = colors.HexColor("#14213D")
BLUE = colors.HexColor("#0066CC")
TURQUOISE = colors.HexColor("#14B8A6")
LIGHT_GREY = colors.HexColor("#F3F6FA")
BORDER_GREY = colors.HexColor("#DCE3EA")
TEXT_GREY = colors.HexColor("#334155")
GREEN_BG = colors.HexColor("#E8F5F0")
YELLOW_BG = colors.HexColor("#FFF5E5")
RED_BG = colors.HexColor("#FCEDEC")


# ---------------------------------------------------------
# DADOS DO ALUNO
# ---------------------------------------------------------

def _extract_student_name(payload: Dict[str, Any]) -> str:
    """Obtém o nome do aluno a partir dos campos disponíveis."""

    for key in ["student_name", "name", "full_name", "display_name"]:
        value = payload.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return "Aluno"


# ---------------------------------------------------------
# TABELA DE DISCIPLINAS
# ---------------------------------------------------------

def _prepare_subjects_table(
    subjects: List[Dict[str, Any]],
    available_width: float,
) -> Table:
    """Cria a tabela de disciplinas com horas opcionais."""

    include_hours = any(
        "hours" in subject and subject.get("hours") is not None
        for subject in subjects
    )

    headers = ["Nome da Disciplina", "ID"]

    if include_hours:
        headers.append("Horas")

    data = [headers]

    for subject in subjects:
        name = escape(str(subject.get("name", "")))
        subject_id = escape(str(subject.get("id", "")))

        row = [
            name,
            subject_id,
        ]

        if include_hours:
            hours = subject.get("hours", "")
            row.append(
                escape(str(hours)) if hours is not None else ""
            )

        data.append(row)

    if include_hours:
        column_widths = [
            available_width * 0.65,
            available_width * 0.17,
            available_width * 0.18,
        ]
    else:
        column_widths = [
            available_width * 0.80,
            available_width * 0.20,
        ]

    table = Table(
        data,
        colWidths=column_widths,
        hAlign="LEFT",
        repeatRows=1,
    )

    table.setStyle(
        TableStyle([
            # Cabeçalho
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            # Linhas alternadas
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white,
                LIGHT_GREY,
            ]),

            # Bordas e alinhamento
            ("GRID", (0, 0), (-1, -1), 0.4, BORDER_GREY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),

            # Espaçamento
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    return table


# ---------------------------------------------------------
# ESTATÍSTICAS DAS TAREFAS
# ---------------------------------------------------------

def _task_statistics(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcula o total e o progresso das tarefas."""

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if str(task.get("status", "")).strip().lower() == "completed"
    )

    pending = sum(
        1 for task in tasks
        if str(task.get("status", "")).strip().lower() == "pending"
    )

    overdue = sum(
        1 for task in tasks
        if str(task.get("status", "")).strip().lower() == "overdue"
    )

    progress = (
        completed / total * 100
        if total > 0
        else 0.0
    )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue,
        "progress": round(progress, 2),
    }


# ---------------------------------------------------------
# BARRA DE PROGRESSO
# ---------------------------------------------------------

class ProgressBar(Flowable):
    """Desenha uma barra horizontal de progresso."""

    def __init__(
        self,
        progress: float,
        width: float,
        height: float = 10,
    ):
        super().__init__()

        self.progress = max(0.0, min(float(progress), 100.0))
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        """
        Informa ao ReportLab o espaço realmente ocupado.

        A largura acompanha a largura disponível no documento
        e a altura é reservada integralmente para a barra.
        """

        self.width = availWidth

        return self.width, self.height

    def draw(self):
        """Desenha o fundo e o preenchimento da barra."""

        self.canv.saveState()

        radius = self.height / 2

        # Fundo da barra
        self.canv.setFillColor(BORDER_GREY)

        self.canv.roundRect(
            0,
            0,
            self.width,
            self.height,
            radius,
            stroke=0,
            fill=1,
        )

        # Progresso preenchido
        fill_width = self.width * (self.progress / 100.0)

        if fill_width > 0:
            self.canv.setFillColor(TURQUOISE)

            self.canv.roundRect(
                0,
                0,
                fill_width,
                self.height,
                min(radius, fill_width / 2),
                stroke=0,
                fill=1,
            )

        self.canv.restoreState()


# ---------------------------------------------------------
# INDICADORES DAS TAREFAS
# ---------------------------------------------------------

def _prepare_indicators_table(
    stats: Dict[str, Any],
    available_width: float,
    styles: Dict[str, Any],
) -> Table:
    """Cria os quatro indicadores compactos de tarefas."""

    indicator_style = ParagraphStyle(
        name="IndicatorStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_GREY,
    )

    indicator_data = [
        [
            Paragraph(
                f"<b>Total de tarefas:</b> {stats['total']}",
                indicator_style,
            ),
            Paragraph(
                f"<b>Concluídas:</b> {stats['completed']}",
                indicator_style,
            ),
        ],
        [
            Paragraph(
                f"<b>Pendentes:</b> {stats['pending']}",
                indicator_style,
            ),
            Paragraph(
                f"<b>Atrasadas:</b> {stats['overdue']}",
                indicator_style,
            ),
        ],
    ]

    table = Table(
        indicator_data,
        colWidths=[
            available_width / 2,
            available_width / 2,
        ],
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), LIGHT_GREY),
            ("BACKGROUND", (1, 0), (1, 0), GREEN_BG),
            ("BACKGROUND", (0, 1), (0, 1), YELLOW_BG),
            ("BACKGROUND", (1, 1), (1, 1), RED_BG),

            ("BOX", (0, 0), (-1, -1), 0.6, BORDER_GREY),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GREY),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ])
    )

    return table


# ---------------------------------------------------------
# GERAÇÃO DO PDF
# ---------------------------------------------------------

def build_pdf(payload: Dict[str, Any]) -> bytes:
    """
    Gera um relatório acadêmico em PDF utilizando ReportLab.

    O arquivo é criado inteiramente em memória e retornado
    como bytes, sem gravação em disco.
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="Relatório de Desempenho Acadêmico",
        author="EduTrack AI",
    )

    elements = []
    styles = getSampleStyleSheet()

    # -----------------------------------------------------
    # ESTILOS
    # -----------------------------------------------------

    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=25,
        textColor=colors.white,
        alignment=1,
        spaceAfter=0,
    )

    header_style = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=NAVY,
        spaceBefore=0,
        spaceAfter=0,
        keepWithNext=True,
    )

    student_style = ParagraphStyle(
        name="StudentName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=NAVY,
    )

    percentage_style = ParagraphStyle(
        name="ProgressPercentage",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=36,

        # IMPORTANTE:
        # leading maior que fontSize evita que a barra
        # ou o próximo elemento invadam o texto.
        leading=46,

        textColor=BLUE,
        alignment=1,
        spaceBefore=0,
        spaceAfter=0,
    )

    normal_style = ParagraphStyle(
        name="ReportNormal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=TEXT_GREY,
    )

    empty_style = ParagraphStyle(
        name="EmptyMessage",
        parent=normal_style,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#64748B"),
        spaceBefore=2,
        spaceAfter=2,
    )

    footer_style = ParagraphStyle(
        name="ReportFooter",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#94A3B8"),
    )

    # -----------------------------------------------------
    # 1. CABEÇALHO
    # -----------------------------------------------------

    header_table = Table(
        [[
            Paragraph(
                "Relatório de Desempenho Acadêmico",
                title_style,
            )
        ]],
        colWidths=[doc.width],
    )

    header_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 15),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
        ])
    )

    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # -----------------------------------------------------
    # 2. NOME DO ALUNO
    # -----------------------------------------------------

    student_name = escape(_extract_student_name(payload))

    elements.append(
        Paragraph(
            f"Aluno: {student_name}",
            student_style,
        )
    )

    elements.append(Spacer(1, 20))

    # -----------------------------------------------------
    # 3. PROGRESSO GERAL
    # -----------------------------------------------------

    tasks = payload.get("tasks", []) or []

    stats = _task_statistics(tasks)

    progress_percent = stats["progress"]

    elements.append(
        Paragraph(
            "Progresso Geral",
            header_style,
        )
    )

    elements.append(Spacer(1, 8))

    # O percentual tem altura de linha própria.
    elements.append(
        Paragraph(
            f"{progress_percent:.1f}%",
            percentage_style,
        )
    )

    # Espaço separado entre o percentual e a barra.
    elements.append(Spacer(1, 8))

    # A barra ocupa uma linha independente.
    elements.append(
        ProgressBar(
            progress=progress_percent,
            width=doc.width,
            height=10,
        )
    )

    elements.append(Spacer(1, 18))

    # -----------------------------------------------------
    # 4. INDICADORES DAS TAREFAS
    # -----------------------------------------------------

    indicator_table = _prepare_indicators_table(
        stats,
        doc.width,
        styles,
    )

    elements.append(indicator_table)
    elements.append(Spacer(1, 22))

    # -----------------------------------------------------
    # 5. DISCIPLINAS
    # -----------------------------------------------------

    subjects = payload.get("subjects", []) or []

    if subjects:
        elements.append(
            Paragraph(
                "Disciplinas",
                header_style,
            )
        )

        elements.append(Spacer(1, 9))

        elements.append(
            _prepare_subjects_table(
                subjects,
                doc.width,
            )
        )

    else:
        elements.append(
            Paragraph(
                "Nenhuma disciplina cadastrada.",
                empty_style,
            )
        )

    elements.append(Spacer(1, 20))

    # -----------------------------------------------------
    # 6. RODAPÉ
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "EduTrack AI | Relatório de Desempenho Acadêmico",
            footer_style,
        )
    )

    # -----------------------------------------------------
    # CONSTRUÇÃO E RETORNO DO PDF
    # -----------------------------------------------------

    doc.build(elements)

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes
