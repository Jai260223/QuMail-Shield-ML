from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# --- Clean Color Theme ---
BG_DARK = RGBColor(6, 11, 25)         # Cosmic Navy
CARD_BG = RGBColor(15, 23, 42)        # Container Slate
ACCENT_CYAN = RGBColor(0, 245, 212)   # Key Highlight Cyan
ACCENT_WARN = RGBColor(255, 159, 28)  # Orange Alert
ACCENT_GREEN = RGBColor(52, 211, 153) # Verified Green
ACCENT_RED = RGBColor(248, 113, 113)  # Threat Red
TEXT_WHITE = RGBColor(241, 245, 249)  # Main Text
TEXT_MUTED = RGBColor(148, 163, 184)  # Subtext

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def draw_canvas(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return bg

def add_slide_header(slide, subtitle, title):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_cat = cat_box.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = subtitle.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_CYAN
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

def draw_card(slide, left, top, width, height, title, points, accent=ACCENT_CYAN, title_sz=16, body_sz=12):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = accent
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_head = tf.paragraphs[0]
    p_head.text = title
    p_head.font.size = Pt(title_sz)
    p_head.font.bold = True
    p_head.font.color.rgb = accent
    p_head.space_after = Pt(8)
    
    for pt in points:
        p = tf.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(body_sz)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

# -------------------------------------------------------------
# SLIDE 1: Title & The Big Idea
# -------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
draw_canvas(s1)

tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "QuMail-Shield"
p1.font.size = Pt(48)
p1.font.bold = True
p1.font.color.rgb = ACCENT_CYAN

p2 = tf.add_paragraph()
p2.text = "Sending Quantum-Secure Messages Over Ordinary Gmail"
p2.font.size = Pt(20)
p2.font.bold = True
p2.font.color.rgb = TEXT_WHITE
p2.space_before = Pt(8)

p3 = tf.add_paragraph()
p3.text = "Addressing ISRO Problem Statement SIH1523"
p3.font.size = Pt(14)
p3.font.color.rgb = ACCENT_WARN
p3.space_before = Pt(16)

p4 = tf.add_paragraph()
p4.text = "Core Pillars: Unbreakable Math • AI Camouflage • Live Gmail Integration"
p4.font.size = Pt(12)
p4.font.color.rgb = TEXT_MUTED
p4.space_before = Pt(10)

add_notes(s1, "SPOKEN CUE: Respected judges, today we are presenting QuMail-Shield. It solves a fundamental problem: how can space and defense teams send confidential messages over everyday public email like Gmail without fear of future quantum supercomputers or network interception?")

# -------------------------------------------------------------
# SLIDE 2: The Two Core Problems
# -------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
draw_canvas(s2)
add_slide_header(s2, "The Real-World Threat", "Why Standard Encrypted Email Fails Today")

draw_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "1. The Quantum Time-Bomb (HNDL)",
    [
        "Traditional encryption (RSA / ECC) will break once quantum computers run Shor's algorithm.",
        "'Harvest Now, Decrypt Later': Adversaries record encrypted military/aerospace emails today, saving them to crack open later.",
        "Old sensitive messages stored in inboxes have an expiration date."
    ],
    ACCENT_RED
)

draw_card(s2, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "2. The 'Look at Me' Problem",
    [
        "Standard PGP encryption produces obvious blocks of scrambled text (BEGIN PGP MESSAGE).",
        "Network sniffers and Deep Packet Inspection (DPI) firewalls immediately flag these emails for targeted interception.",
        "Obvious encryption invites suspicion and traffic monitoring."
    ],
    ACCENT_WARN
)

add_notes(s2, "SPOKEN CUE: Everyday email has two massive weaknesses. First, adversaries are actively archiving encrypted emails today so they can crack them later with quantum computers. Second, sending obvious scrambled text raises red flags with network firewalls and filters.")

# -------------------------------------------------------------
# SLIDE 3: How QuMail-Shield Works in 4 Steps
# -------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
draw_canvas(s3)
add_slide_header(s3, "The 4-Step Solution", "How QuMail-Shield Protects Every Message")

draw_card(s3, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
    "1. The Lock",
    [
        "Takes your secret text.",
        "Locks it with One-Time Pad (OTP) bitwise XOR math.",
        "Uses a single-use key stored locally on your device.",
        "Mathematically unbreakable."
    ],
    ACCENT_CYAN
)

draw_card(s3, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
    "2. The Camouflage",
    [
        "Takes a normal picture (PNG).",
        "An unsupervised AI finds the busiest, high-texture zones.",
        "Embeds the locked bits into image pixels.",
        "Picture looks completely untouched."
    ],
    ACCENT_CYAN
)

draw_card(s3, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
    "3. The Transit",
    [
        "Sends the PNG picture as a standard attachment.",
        "Connects directly to real Gmail servers (SMTP).",
        "Google and intermediate routers see only a normal image."
    ],
    ACCENT_WARN
)

draw_card(s3, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
    "4. Unlock & Shred",
    [
        "Receiver extracts hidden bits with the matching local key.",
        "Plain text is restored instantly.",
        "The key is immediately shredded from memory forever (Forward Secrecy)."
    ],
    ACCENT_GREEN
)

add_notes(s3, "SPOKEN CUE: Our architecture works in four clean steps. First, we lock the message with unbreakable One-Time Pad math. Second, our AI hides the scrambled bits inside the pixels of a normal picture. Third, we send that picture through normal Gmail. Fourth, the recipient unlocks it and the key is instantly shredded from memory so it can never be stolen.")

# -------------------------------------------------------------
# SLIDE 4: Why the AI Camouflage Is Smart
# -------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
draw_canvas(s4)
add_slide_header(s4, "AI Steganography", "Why We Use Unsupervised K-Means Clustering")

draw_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "The Dumb Way (Blind Embedding)",
    [
        "Hiding data blindly in flat, smooth areas (like a clear blue sky) leaves visible artifacts.",
        "Statistical scanners and Chi-Square analysis easily detect color distortions in flat zones.",
        "Easily caught by Deep Packet Inspection (DPI)."
    ],
    ACCENT_RED
)

draw_card(s4, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "Our AI Way (Unsupervised K-Means)",
    [
        "The AI scans image gradients using Most Significant Bits (MSBs).",
        "It automatically groups pixels into Smooth vs. Chaotic Texture areas without human labels.",
        "It hides secret bits strictly inside the high-texture, noisy zones (like grass, gravel, or details).",
        "Result: PSNR > 50 dB — completely invisible to both human eyes and firewall scanners."
    ],
    ACCENT_GREEN
)

add_notes(s4, "SPOKEN CUE: Why do we need AI for steganography? If you hide data in a smooth blue sky, scanners can detect the slight color shifts. Our unsupervised K-Means model finds the busiest textures in the photo—like trees or shadows—and hides data only there. It is 100% invisible to human eyes and automated security tools.")

# -------------------------------------------------------------
# SLIDE 5: Proof & Live Attack Arena
# -------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
draw_canvas(s5)
add_slide_header(s5, "Demonstration & Proof", "Simulating Quantum Attacks Live in the Prototype")

draw_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "Traditional RSA-2048 Email",
    [
        "Simulates an attacker intercepting normal encrypted email traffic.",
        "Shor's quantum algorithm factors the key in milliseconds (0.042 ms).",
        "Result: Keys extracted and private data is fully exposed.",
        "Fails completely against quantum computers."
    ],
    ACCENT_RED
)

draw_card(s5, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "QuMail-Shield Carrier",
    [
        "Adversary intercepts the PNG image sent over Gmail.",
        "Network scanner logs: [PASS - CLEAN IMAGE] (zero flags).",
        "Quantum brute-force search fails to converge (>2^128 operations).",
        "Result: Proven unbreakable under Shannon's Perfect Secrecy theorem."
    ],
    ACCENT_GREEN
)

add_notes(s5, "SPOKEN CUE: In Tab 5 of our prototype, we show this live. When an attacker runs a simulated quantum attack on standard RSA, it cracks in milliseconds. But when they inspect QuMail-Shield, the network scanner sees a harmless picture, and quantum algorithms fail because One-Time Pad math cannot be brute-forced.")

# -------------------------------------------------------------
# SLIDE 6: Summary & Why QuMail-Shield Wins
# -------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
draw_canvas(s6)
add_slide_header(s6, "Summary & Value Proposition", "Production-Ready Post-Quantum Security Today")

draw_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "Key Project Strengths",
    [
        "100% Compliant with ISRO Problem Statement SIH1523.",
        "Mathematically Unbreakable: True One-Time Pad XOR encryption.",
        "Zero Infrastructure Overhaul: Works immediately over standard Gmail/Outlook.",
        "Single-Use Forward Secrecy: Keys are automatically burned after reading."
    ],
    ACCENT_CYAN
)

draw_card(s6, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
    "Project Status & Roadmap",
    [
        "Working Prototype: Live Streamlit dashboard tested with real Gmail SMTP dispatch [DONE].",
        "Unsupervised AI Stego: K-Means texture masking and PSNR inspection [DONE].",
        "Local Key Manager: Localhost key vault with automatic memory zeroing [DONE].",
        "Next Milestone: Standalone desktop app & hardware QKD optical synchronization."
    ],
    ACCENT_GREEN
)

add_notes(s6, "SPOKEN CUE: To wrap up: QuMail-Shield gives ISRO and defense teams unbreakable post-quantum email security today, using normal Gmail, with zero extra hardware costs. The prototype is fully functional and ready for live demonstration. Thank you!")

# Save
filename = "QuMail_Shield_Simple_Pitch.pptx"
prs.save(filename)
print(f"[+] Successfully generated: {filename}")
