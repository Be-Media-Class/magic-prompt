"""
Space Kid - Blender Scene v4
Flat emission shaders + freestyle outlines.
Composição: personagem sentado + rádio retrô + estrelas + planeta.
"""
import bpy, math, random

# ── Reset ─────────────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
for m in list(bpy.data.meshes):    bpy.data.meshes.remove(m)

# ── Emission flat material ─────────────────────────────────────────────────────
def emat(name, rgb, strength=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em  = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value    = (*rgb, 1)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return m

SKY    = emat("sky",    (0.008, 0.004, 0.004))
GROUND = emat("ground", (0.72,  0.54,  0.27))
SHADOW = emat("shadow", (0.32,  0.24,  0.12))
BLACK  = emat("black",  (0.06,  0.05,  0.05))
CREAM  = emat("cream",  (0.88,  0.76,  0.52))
SKIN   = emat("skin",   (0.75,  0.20,  0.06))
RED    = emat("red",    (0.60,  0.07,  0.04))
GRAY   = emat("gray",   (0.40,  0.40,  0.40))
LGRAY  = emat("lgray",  (0.62,  0.62,  0.62))
VISOR  = emat("visor",  (0.06,  0.05,  0.05))
STAR   = emat("star",   (0.95,  0.90,  0.75))
PRED   = emat("pred",   (0.55,  0.09,  0.04), strength=1.5)
PCRM   = emat("pcrm",   (0.80,  0.65,  0.38), strength=1.5)
WHITE  = emat("white",  (0.92,  0.90,  0.84))

def am(o, m): o.data.materials.clear(); o.data.materials.append(m); return o
def smooth(o): bpy.ops.object.shade_smooth(); return o
def sub(o, lv=2):
    md = o.modifiers.new("S","SUBSURF"); md.levels=lv; md.render_levels=lv; return o

def box(name, loc, sc, m, sm=False):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name=name; o.scale=sc
    am(o,m)
    if sm: smooth(o)
    return o

def ball(name, loc, r, m, seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r,
                                          segments=seg, ring_count=seg//2)
    o = bpy.context.object; o.name=name
    am(o,m); smooth(o); sub(o,2); return o

def rod(name, loc, r, d, m, rx=0, rz=0):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=d, vertices=24)
    o = bpy.context.object; o.name=name
    o.rotation_euler=(math.radians(rx),0,math.radians(rz))
    am(o,m); smooth(o); return o

# ═══════════════════════════════════════════════════════════════════════════════
# MUNDO
# ═══════════════════════════════════════════════════════════════════════════════

# Sky backdrop: grande plano em y=2, bem atrás de tudo
box("Sky", (0, 2, 3.0), (12, 0.02, 14), SKY)

# Chão
box("Gnd",  (0, 0, -0.30), (12, 12, 0.30), GROUND)
box("Shdw", (0.4, -0.01, 0.01), (1.9, 1.2, 0.01), SHADOW)

# Estrelas — mesmo plano y=1.8 (à frente do céu)
random.seed(42)
for i in range(55):
    x = random.uniform(-3.0, 3.0)
    z = random.uniform(0.8, 4.3)
    r = random.uniform(0.020, 0.065)
    ball(f"s{i}", (x, 1.8, z), r, STAR, seg=6)

# Planeta — à frente das estrelas, y=1.2
ball("Pl",   (0.18, 1.2, 2.92), 0.30, PRED, seg=48)
for i, zo in enumerate([-0.10, 0.06]):
    rod(f"Pr{i}", (0.18, 1.2, 2.92+zo), 0.28, 0.10, PCRM, rx=90)

# ═══════════════════════════════════════════════════════════════════════════════
# RÁDIO RETRÔ
# ═══════════════════════════════════════════════════════════════════════════════
rx = -1.0
box("RBody",  (rx,    -0.01, 0.46), (0.40, 0.30, 0.46), LGRAY, True)
box("RTopP",  (rx,    -0.01, 0.96), (0.38, 0.28, 0.07), GRAY)
box("RLeft",  (rx-0.40, -0.01, 0.46), (0.02, 0.27, 0.40), RED)
for i, bz in enumerate([0.64, 0.44, 0.26]):
    box(f"RB{i}", (rx-0.40, -0.01, bz), (0.025, 0.06, 0.08), BLACK)
# Grille frontal
for gx in [-0.12, 0.0, 0.12]:
    box(f"RG{gx}", (rx+gx, -0.31, 0.40), (0.025, 0.01, 0.28), GRAY)
box("RHnd",   (rx, -0.01, 1.08), (0.15, 0.04, 0.04), LGRAY, True)
# Antena
rod("RAntB", (rx+0.18, -0.01, 1.07), 0.030, 0.09, LGRAY)
rod("RAnt",  (rx+0.18, -0.01, 1.85), 0.017, 1.60, LGRAY)
ball("RAntT",(rx+0.18, -0.01, 2.67), 0.060, LGRAY, seg=10)

# ═══════════════════════════════════════════════════════════════════════════════
# PERSONAGEM
# ═══════════════════════════════════════════════════════════════════════════════
cx = 0.45

# Pernas
box("ThL",  (cx-0.12,  0, 0.09), (0.13, 0.22, 0.09), BLACK)
box("ThR",  (cx+0.50,  0, 0.09), (0.48, 0.19, 0.09), BLACK)
box("KnR",  (cx+0.86,  0, 0.22), (0.11, 0.18, 0.18), BLACK)
box("ShR",  (cx+0.86,  0, 0.01), (0.09, 0.15, 0.10), LGRAY)
box("ShoR", (cx+0.88,  0,-0.09), (0.15, 0.15, 0.06), BLACK)
box("ShoL", (cx-0.13,  0,-0.08), (0.12, 0.14, 0.05), BLACK)

# Torso
box("Tors", (cx,  0, 0.46), (0.29, 0.24, 0.30), BLACK, True)
box("Zip",  (cx, -0.24, 0.47), (0.022, 0.005, 0.22), GRAY)
box("Badg", (cx-0.14,-0.24, 0.58), (0.042, 0.005, 0.042), RED)

# Braços
box("ArmL", (cx-0.38, 0, 0.38), (0.09, 0.20, 0.23), BLACK, True)
box("ArmR", (cx+0.38, 0, 0.38), (0.09, 0.20, 0.23), BLACK, True)

# Pescoço
rod("Neck",  (cx, 0, 0.81), 0.200, 0.08, LGRAY)
rod("NkRng", (cx, 0, 0.84), 0.215, 0.04, GRAY)

# Capacete
helm = ball("Helm", (cx, 0, 1.06), 0.42, CREAM, seg=64)

# Viseira
vis = ball("Vis", (cx, -0.26, 1.02), 0.31, VISOR, seg=48)
vis.scale = (1.0, 0.36, 0.82)
bpy.ops.object.transform_apply(scale=True)

# Rosto
fc = ball("Face", (cx, -0.22, 1.00), 0.22, SKIN, seg=48)
fc.scale = (0.90, 0.46, 0.82)
bpy.ops.object.transform_apply(scale=True)

# Olhos
ball("EyL", (cx-0.08,-0.38, 1.01), 0.052, BLACK, seg=12)
ball("EyR", (cx+0.20,-0.38, 1.01), 0.052, BLACK, seg=12)
ball("ShL", (cx-0.06,-0.42, 1.04), 0.017, WHITE, seg=8)
ball("ShR", (cx+0.22,-0.42, 1.04), 0.017, WHITE, seg=8)

# Clamps laterais
for sx in [(cx-0.32),(cx+0.32)]:
    rod(f"Cl{sx}", (sx, 0, 0.97), 0.050, 0.09, GRAY, rx=90)

# Reflexos no capacete
ball("R1", (cx+0.24,-0.30, 1.22), 0.052, CREAM, seg=10)
ball("R2", (cx+0.34,-0.26, 1.14), 0.032, CREAM, seg=10)

# ═══════════════════════════════════════════════════════════════════════════════
# CÂMERA
# Camera ortho, enquadramento fiel à ilustração:
#   - Personagem + rádio na metade inferior
#   - Planeta no topo direito
#   - Céu estrelado preenchendo a parte superior
# ═══════════════════════════════════════════════════════════════════════════════
bpy.ops.object.camera_add(location=(-0.2, -9.0, 1.9))
cam = bpy.context.object; cam.name = "Cam"
cam.rotation_euler = (math.radians(87), 0, 0)
bpy.context.scene.camera = cam
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 3.0   # largura=3.0 → altura=5.34 → Z range [-0.47, 4.87]

# ═══════════════════════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════════════════════
sc = bpy.context.scene
sc.render.engine           = 'CYCLES'
sc.cycles.samples          = 8
sc.cycles.use_denoising    = False
sc.render.resolution_x     = 1080
sc.render.resolution_y     = 1920
sc.render.film_transparent = False

sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value    = (0, 0, 0, 1)
bg.inputs["Strength"].default_value = 0.0

sc.render.use_freestyle   = True
sc.render.line_thickness  = 1.6
vl = sc.view_layers[0]
vl.use_freestyle = True
vl.freestyle_settings.crease_angle = math.radians(130)

sc.render.filepath = "/home/user/magic-prompt/space_kid_render.png"
sc.render.image_settings.file_format = 'PNG'

bpy.ops.wm.save_as_mainfile(filepath="/home/user/magic-prompt/space_kid.blend")
print("✓ .blend salvo")
bpy.ops.render.render(write_still=True)
print("✓ PNG salvo")
