import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def find_latest_image(pattern):
    """Finds the most recently created image matching a pattern."""
    files = glob.glob(pattern)
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def build_preprint_pdf(filename="Morphing_Wing_Preprint.pdf"):
    print("Generating manuscript PDF with updated pneumatic dual-regime context...")

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=15,
        leading=19,
        alignment=1,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.HexColor('#111111')
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8,
        alignment=4 # Justified text
    )
    
    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Italic'],
        fontSize=9,
        leading=12,
        alignment=1,
        spaceBefore=4,
        spaceAfter=12,
        textColor=colors.HexColor('#444444')
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("<b>Aerodynamic Proof-of-Concept for a Dual-Regime Pressurized Morphing Wing Across Subsonic, Transonic, and Supersonic Regimes</b>", title_style))
    story.append(Paragraph("<b>Author:</b> Research Team &nbsp;&nbsp;|&nbsp;&nbsp; <b>Preprint Server:</b> engrXiv", caption_style))
    story.append(Spacer(1, 8))

    # Abstract
    story.append(Paragraph("<b>Abstract</b>", heading_style))
    story.append(Paragraph(
        "This study presents a computational fluid dynamics (CFD) proof-of-concept evaluating a novel dual-regime pneumatic morphing wing operating from Mach 0.15 to Mach 2.5. The architecture features an internal rigid biconvex core surrounded by a flexible elastomeric skin that inflates into a high-lift supercritical profile for subsonic/transonic flight and evacuates flush against the core to form a razor-thin biconvex shape for supersonic flight. Static rigid-mesh simulations across 43 aerodynamic test cases demonstrate significant wave drag mitigation through the transonic dip zone (Mach 0.8–1.2) and an aerodynamic efficiency recovery to (L/D)<sub>max</sub> ≈ 9.3 at Mach 2.5. These static numerical results establish baseline feasibility prior to experimental laboratory wind-tunnel validation.",
        body_style
    ))

    # Section 1: Concept & Methodology
    story.append(Paragraph("<b>1. Morphing Architecture & CFD Methodology</b>", heading_style))
    story.append(Paragraph(
        "<b>1.1 Pneumatic Morphing Concept:</b> The hybrid structural architecture combines an ultra-sharp, load-bearing rigid biconvex core with an outer flexible elastomeric composite skin. Pressurization of internal pneumatic chambers with Nitrogen expands the skin into a rounded, high-camber supercritical airfoil tailored for subsonic high-lift and transonic shock delay. Gas evacuation causes the skin to contract tightly against the rigid core, exposing a sharp biconvex profile to minimize supersonic wave drag.",
        body_style
    ))
    story.append(Paragraph(
        "<b>1.2 Computational Setup:</b> To establish aerodynamic proof-of-concept without the immediate overhead of dynamic mesh fluid-structure interaction (FSI), static rigid-mesh simulations were executed using OpenFOAM (<i>rhoSimpleFoam</i> and <i>rhoCentralFoam</i>). These simulations capture the discrete geometric boundary states (fully inflated supercritical vs. fully collapsed biconvex) across 43 flow conditions spanning Mach 0.15 to 2.5.",
        body_style
    ))

    # Section 2: Aerodynamic Results
    story.append(Paragraph("<b>2. Results & Aerodynamic Performance</b>", heading_style))
    story.append(Paragraph(
        "Lift curve slopes (<i>dC<sub>L</sub>/dα</i>) show linear subsonic behavior in the inflated supercritical state, achieving high peak efficiency ((L/D)<sub>max</sub> > 30 at Mach 0.4). Transonic compressibility effects cause expected slope reductions between Mach 0.8 and 1.2.",
        body_style
    ))

    # Figure 1: Lift Curve
    cl_img = find_latest_image("Cl_vs_AoA_fixed*.png")
    if cl_img:
        story.append(KeepTogether([
            Image(cl_img, width=450, height=250),
            Paragraph("<b>Figure 1:</b> Lift curves (<i>C<sub>L</sub></i> vs α) across subsonic, transonic, and supersonic speed regimes.", caption_style)
        ]))

    story.append(Paragraph(
        "Drag polars highlight zero-lift drag penalties ($C_{D0}$) during the transonic wave drag rise. Evacuating the skin into the thin biconvex profile for supersonic regimes suppresses frontal area and turns detached bow shocks into attached oblique shocks.",
        body_style
    ))
    
    # Figure 2: Drag Polar
    cd_img = find_latest_image("Drag_Polar_fixed*.png")
    if cd_img:
        story.append(KeepTogether([
            Image(cd_img, width=450, height=250),
            Paragraph("<b>Figure 2:</b> Drag polars (<i>C<sub>L</sub></i> vs <i>C<sub>D</sub></i>) demonstrating wave drag transitions.", caption_style)
        ]))

    story.append(Paragraph(
        "The peak efficiency envelope highlights the transonic dip zone (Mach 0.8–1.2), where (L/D)<sub>max</sub> drops to localized minima before recovering to 9.3 at Mach 2.5 due to the sharp biconvex supersonic profile.",
        body_style
    ))
    
    # Figure 3: Peak Efficiency
    ld_img = find_latest_image("Max_LD_vs_Mach_fixed*.png")
    if ld_img:
        story.append(KeepTogether([
            Image(ld_img, width=450, height=230),
            Paragraph("<b>Figure 3:</b> Peak aerodynamic efficiency ((L/D)<sub>max</sub>) across Mach numbers, highlighting the transonic dip zone.", caption_style)
        ]))

    # Section 3: Conclusion & Next Steps
    story.append(Paragraph("<b>3. Conclusion & Experimental Roadmap</b>", heading_style))
    story.append(Paragraph(
        "Static rigid-mesh CFD evaluations confirm the baseline aerodynamic proof-of-concept for the pressurized dual-regime morphing wing concept. The geometric transition effectively manages transonic wave drag and preserves supersonic efficiency. Following this publication, research will transition to experimental laboratory testing of a physical elastomeric prototype in a high-speed wind tunnel to validate dynamic pressure actuation, elastomeric skin deformation, and dynamic aeroelastic stability.",
        body_style
    ))

    doc.build(story)
    print(f"\nSUCCESS: Updated PDF generated successfully as '{os.path.abspath(filename)}'")

if __name__ == "__main__":
    build_preprint_pdf()