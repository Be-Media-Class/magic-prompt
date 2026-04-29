"""
Space Kid - Blender Scene Script v2
Recria a ilustração flat do astronauta sentado com rádio retrô.
"""

import bpy
import math
import random

# ── Limpa a cena ──────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in list(bpy.data.materials): bpy.data.materials.remove(m)

# ── Paleta ────────────────────────────────────────────────────────────────────
def mat(name, color, emission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    if emission > 0:
        em = nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (*color, 1)
        em.inputs["Strength"].default_value = emission
        links.new(em.outputs[0], out.inputs[0])
    else:
        diff = nodes.new("ShaderNodeBsdfDiffuse")
        diff.inputs["Color"].default_value = (*color, 1)
        diff.inputs["Roughness"].default_value = 1.0
        links.new(diff.outputs[0], out.inputs[0])
    return m

C_BG     = (0.01, 0.005, 0.005)
C_BLACK  = (0.05, 0.04, 0.04)
C_RED    = (0.65, 0.08, 0.05)
C_BEIGE  = (0.80, 0.63, 0.36)
C_CREAM  = (0.88, 0.76, 0.52)
C_GRAY   = (0.42, 0.42, 0.42)
C_LGRAY  = (0.62, 0.62, 0.62)
C_SKIN   = (0.72, 0.20, 0.06)
C_VISOR  = (0.06, 0.05, 0.05)
C_STAR   = (0.95, 0.90, 0.75)
C_P_RED  = (0.68, 0.12, 0.06)
C_P_CRM  = (0.86, 0.72, 0.48)
C_GROUND = (0.72, 0.55, 0.28)
C_SHADOW = (0.38, 0.30, 0.18)

M_BG     = mat("BG",     C_BG)
M_BLACK  = mat("Black",  C_BLACK)
M_RED    = mat("Red",    C_RED)
M_BEIGE  = mat("Beige",  C_BEIGE)
M_CREAM  = mat("Cream",  C_CREAM)
M_GRAY   = mat("Gray",   C_GRAY)
M_LGRAY  = mat("LGray",  C_LGRAY)
M_SKIN   = mat("Skin",   C_SKIN)
M_VISOR  = mat("Visor",  C_VISOR)
M_STAR   = mat("Star",   C_STAR,  emission=6.0)
M_P_RED  = mat("PRed",   C_P_RED)
M_P_CRM  = mat("PCrm",   C_P_CRM)
M_GROUND = mat("Ground", C_GROUND)
M_SHADOW = mat("Shadow", C_SHADOW)

def assign(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj

def cube(name, loc, scale, m=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    return assign(o, m) if m else o

def sphere(name, loc, r, m=None, seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r, segments=seg, ring_count=seg//2)
    o = bpy.context.object; o.name = name
    return assign(o, m) if m else o

def cyl(name, loc, r, d, m=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=d, vertices=24)
    o = bpy.context.object; o.name = name
    o.rotation_euler = (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]))
    return assign(o, m) if m else o

# ── Fundo (parede de céu) ─────────────────────────────────────────────────────
cube("Sky", (0, 6, 2), (9, 0.1, 10), M_BG)

# ── Chão ──────────────────────────────────────────────────────────────────────
cube("Ground",  (0, 0, -0.22), (9, 9, 0.22), M_GROUND)
cube("Shadow",  (0.3, 0, 0.01), (1.6, 1.0, 0.01), M_SHADOW)

# ── Estrelas ──────────────────────────────────────────────────────────────────
random.seed(7)
for i in range(45):
    x = random.uniform(-5.5, 5.5)
    z = random.uniform(1.2, 8.5)
    r = random.uniform(0.025, 0.07)
    sphere(f"St{i}", (x, 5.9, z), r, M_STAR, seg=6)

# ── Planeta ───────────────────────────────────────────────────────────────────
sphere("Planet", (2.2, 5.5, 7.2), 0.70, M_P_RED, seg=40)
for i, zo in enumerate([-0.20, 0.0, 0.22]):
    cyl(f"PRing{i}", (2.2, 5.4, 7.2 + zo), 0.67, 0.18, M_P_CRM)

# ── RÁDIO RETRÔ ───────────────────────────────────────────────────────────────
rx, ry = -1.05, 0.0
cube("RBody",   (rx, ry, 0.42),  (0.38, 0.28, 0.42), M_LGRAY)
cube("RFaceL",  (rx-0.37, ry, 0.42), (0.015, 0.25, 0.38), M_RED)
cube("RPanel",  (rx, ry-0.27, 0.60), (0.35, 0.025, 0.06), M_GRAY)
for i, bz in enumerate([0.55, 0.38, 0.20]):
    cube(f"RBtn{i}", (rx-0.37, ry, bz), (0.018, 0.05, 0.07), M_RED)
cube("RHandle", (rx, ry, 0.92), (0.16, 0.04, 0.04), M_LGRAY)
cyl("RAnt",     (rx+0.15, ry, 1.55), 0.018, 1.30, M_LGRAY)
sphere("RAntB", (rx+0.15, ry, 2.22), 0.05, M_LGRAY, seg=10)

# ── PERSONAGEM ────────────────────────────────────────────────────────────────
px = 0.4

# Torso
cube("Torso",  (px, 0, 0.50), (0.30, 0.24, 0.30), M_BLACK)

# Zíper
cube("Zip",    (px, -0.24, 0.52), (0.022, 0.01, 0.18), M_GRAY)

# Braços
cube("ArmL",   (px-0.38, 0, 0.40), (0.09, 0.20, 0.20), M_BLACK)
cube("ArmR",   (px+0.38, 0, 0.40), (0.09, 0.20, 0.20), M_BLACK)

# Pernas (sentado — uma esticada, outra dobrada)
cube("LegL",   (px-0.12, 0, 0.05), (0.14, 0.20, 0.12), M_BLACK)
cube("LegR",   (px+0.55, 0, 0.08), (0.48, 0.18, 0.10), M_BLACK)
cube("ShinR",  (px+0.85, 0, 0.22), (0.09, 0.15, 0.22), M_LGRAY)
cube("ShoeR",  (px+0.88, 0, 0.04), (0.14, 0.16, 0.06), M_BLACK)
cube("ShoeL",  (px-0.10, 0, -0.03),(0.12, 0.14, 0.05), M_BLACK)

# Anel do pescoço
cyl("Neck",    (px, 0, 0.84), 0.20, 0.07, M_LGRAY)

# Capacete
sphere("Helm",  (px, 0, 1.02), 0.36, M_CREAM, seg=48)

# Viseira (esfera achatada na frente)
v = sphere("Visor", (px, -0.22, 0.98), 0.27, M_VISOR, seg=48)
v.scale = (1.0, 0.40, 0.85)

# Rosto
f = sphere("Face", (px, -0.18, 0.97), 0.20, M_SKIN, seg=32)
f.scale = (0.88, 0.50, 0.82)

# Olhos
sphere("EyeL", (px-0.07, -0.34, 0.98), 0.045, M_BLACK, seg=10)
sphere("EyeR", (px+0.18, -0.34, 0.98), 0.045, M_BLACK, seg=10)

# Reflexos no capacete
r1 = sphere("Ref1", (px+0.20, -0.30, 1.14), 0.045, M_CREAM, seg=10)
r2 = sphere("Ref2", (px+0.30, -0.27, 1.07), 0.028, M_CREAM, seg=10)

# Abraçadeiras laterais do capacete
for side, x in [("L", px-0.24), ("R", px+0.24)]:
    c = cyl(f"Cl{side}", (x, 0, 0.93), 0.045, 0.07, M_GRAY, rot=(90,0,0))

# ── CÂMERA ────────────────────────────────────────────────────────────────────
bpy.ops.object.camera_add(location=(0.3, -7.5, 2.4))
cam = bpy.context.object
cam.name = "Camera"
cam.rotation_euler = (math.radians(86), 0, 0)
bpy.context.scene.camera = cam
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 5.0

# ── ILUMINAÇÃO ────────────────────────────────────────────────────────────────
bpy.ops.object.light_add(type='AREA', location=(4, -4, 6))
key = bpy.context.object
key.data.energy = 800
key.data.size = 6
key.rotation_euler = (math.radians(50), 0, math.radians(20))

bpy.ops.object.light_add(type='AREA', location=(-5, -2, 4))
fill = bpy.context.object
fill.data.energy = 200
fill.data.size = 4
fill.data.color = (0.9, 0.8, 0.7)

# ── RENDER ────────────────────────────────────────────────────────────────────
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = False
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.film_transparent = False

scene.world.use_nodes = True
bg_node = scene.world.node_tree.nodes["Background"]
bg_node.inputs["Color"].default_value = (*C_BG, 1)
bg_node.inputs["Strength"].default_value = 0.0

scene.render.use_freestyle = True
scene.render.line_thickness = 1.5

scene.render.filepath = "/home/user/magic-prompt/space_kid_render.png"
scene.render.image_settings.file_format = 'PNG'

bpy.ops.render.render(write_still=True)
print("✓ Render salvo em space_kid_render.png")
