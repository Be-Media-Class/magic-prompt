"""
Space Kid - Blender Scene Script
Recria a ilustração flat do astronauta sentado com rádio retrô.
Rode no Scripting Editor do Blender: clique em Run Script.
"""

import bpy
import bmesh
from mathutils import Vector
import math
import random

# ── Limpa a cena ──────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

# ── Paleta ────────────────────────────────────────────────────────────────────
def mat(name, color, roughness=1.0, emission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Specular IOR Level"].default_value = 0.0
    if emission > 0:
        bsdf.inputs["Emission Color"].default_value = (*color, 1)
        bsdf.inputs["Emission Strength"].default_value = emission
    return m

C_BLACK  = (0.04, 0.03, 0.03)
C_RED    = (0.65, 0.08, 0.05)
C_BEIGE  = (0.82, 0.65, 0.38)
C_CREAM  = (0.90, 0.78, 0.55)
C_GRAY   = (0.45, 0.45, 0.45)
C_LGRAY  = (0.65, 0.65, 0.65)
C_SKY    = (0.06, 0.02, 0.02)
C_SKIN   = (0.75, 0.22, 0.08)
C_VISOR  = (0.08, 0.06, 0.06)
C_STAR   = (0.95, 0.90, 0.75)
C_PLANET1= (0.70, 0.15, 0.08)
C_PLANET2= (0.88, 0.74, 0.50)

M_BLACK  = mat("Black",  C_BLACK)
M_RED    = mat("Red",    C_RED)
M_BEIGE  = mat("Beige",  C_BEIGE)
M_CREAM  = mat("Cream",  C_CREAM)
M_GRAY   = mat("Gray",   C_GRAY)
M_LGRAY  = mat("LGray",  C_LGRAY)
M_SKY    = mat("Sky",    C_SKY)
M_SKIN   = mat("Skin",   C_SKIN)
M_VISOR  = mat("Visor",  C_VISOR)
M_STAR   = mat("Star",   C_STAR,  emission=3.0)
M_P1     = mat("Planet1",C_PLANET1)
M_P2     = mat("Planet2",C_PLANET2)

def assign(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)
    return obj

def add_cube(name, loc, scale, mat_=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    if mat_:
        assign(obj, mat_)
    return obj

def add_sphere(name, loc, radius, mat_=None, segs=32):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=radius, segments=segs, ring_count=segs//2)
    obj = bpy.context.object
    obj.name = name
    if mat_:
        assign(obj, mat_)
    return obj

def add_cylinder(name, loc, radius, depth, mat_=None):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=radius, depth=depth, vertices=32)
    obj = bpy.context.object
    obj.name = name
    if mat_:
        assign(obj, mat_)
    return obj

# ── Chão lunar ────────────────────────────────────────────────────────────────
ground = add_cube("Ground", (0, 0, -0.5), (8, 8, 0.3), M_BEIGE)

# Faixa de sombra no chão (sob o personagem)
shadow = add_cube("Shadow", (0.2, 0, -0.18), (1.4, 1.0, 0.01), M_GRAY)

# ── Fundo (céu) ───────────────────────────────────────────────────────────────
sky = add_cube("Sky", (0, 4, 3), (8, 0.1, 8), M_SKY)

# ── Estrelas ──────────────────────────────────────────────────────────────────
random.seed(42)
for i in range(40):
    x = random.uniform(-6, 6)
    z = random.uniform(1, 7)
    r = random.uniform(0.02, 0.06)
    s = add_sphere(f"Star_{i}", (x, 3.9, z), r, M_STAR, segs=8)

# ── Planeta ao fundo ──────────────────────────────────────────────────────────
planet = add_sphere("Planet", (1.5, 3.8, 6.5), 0.55, M_P1, segs=32)

# Faixas do planeta
for i, z_off in enumerate([-0.15, 0.15]):
    ring = add_cylinder(f"PlanetRing_{i}", (1.5, 3.75, 6.5 + z_off), 0.52, 0.14, M_P2)

# ── RÁDIO RETRÔ ───────────────────────────────────────────────────────────────
# Corpo principal
radio_body = add_cube("RadioBody", (-0.7, 0, 0.15), (0.35, 0.25, 0.40), M_LGRAY)

# Face frontal vermelha
radio_face = add_cube("RadioFace", (-0.35, -0.02, 0.15), (0.02, 0.22, 0.35), M_RED)

# Botões
for i, bz in enumerate([0.30, 0.10, -0.10]):
    btn = add_cube(f"RadioBtn_{i}", (-0.34, -0.02, bz), (0.015, 0.04, 0.06), M_BLACK)

# Painel lateral escuro
panel = add_cube("RadioPanel", (-0.72, -0.02, 0.38), (0.32, 0.22, 0.04), M_GRAY)

# Alça topo
handle = add_cube("RadioHandle", (-0.70, 0, 0.62), (0.15, 0.04, 0.04), M_LGRAY)

# Antena do rádio
antenna = add_cylinder("Antenna", (-0.55, 0, 1.1), 0.015, 1.1, M_LGRAY)
antenna_ball = add_sphere("AntennaBall", (-0.55, 0, 1.68), 0.04, M_LGRAY, segs=12)

# ── PERSONAGEM ────────────────────────────────────────────────────────────────

# Pernas (dobradas, sentado)
leg_r = add_cube("LegR", (0.55, 0, 0.02), (0.36, 0.18, 0.08), M_BLACK)
leg_l = add_cube("LegL", (0.10, 0, -0.12), (0.10, 0.18, 0.18), M_BLACK)

# Pé direito
foot_r = add_cube("FootR", (0.82, 0, -0.04), (0.12, 0.16, 0.06), M_BLACK)

# Meias / canelas
shin_r = add_cube("ShinR", (0.72, 0, 0.12), (0.08, 0.14, 0.16), M_LGRAY)

# Sapatos
shoe_r = add_cube("ShoeR", (0.84, 0, -0.05), (0.14, 0.15, 0.055), M_BLACK)

# Corpo (torso sentado)
torso = add_cube("Torso", (0.10, 0, 0.35), (0.28, 0.22, 0.28), M_BLACK)

# Braços
arm_l = add_cube("ArmL", (-0.22, 0, 0.22), (0.08, 0.18, 0.22), M_BLACK)
arm_r = add_cube("ArmR", (0.40, 0, 0.22), (0.08, 0.18, 0.22), M_BLACK)

# Pescoço / anel do capacete
neck_ring = add_cylinder("NeckRing", (0.10, 0, 0.68), 0.18, 0.06, M_LGRAY)

# Capacete (esfera grande)
helmet = add_sphere("Helmet", (0.10, 0, 0.85), 0.32, M_CREAM, segs=48)

# Viseira (semi-esfera escura)
visor = add_sphere("Visor", (0.10, -0.18, 0.85), 0.25, M_VISOR, segs=48)
visor.scale = (1, 0.45, 0.82)

# Rosto / cabeça visível
face = add_sphere("Face", (0.10, -0.15, 0.82), 0.18, M_SKIN, segs=32)
face.scale = (0.9, 0.55, 0.85)

# Olhos
eye_l = add_sphere("EyeL", (-0.04, -0.28, 0.83), 0.04, M_BLACK, segs=12)
eye_r = add_sphere("EyeR", (0.22, -0.28, 0.83), 0.04, M_BLACK, segs=12)

# Reflexo no capacete
reflex = add_sphere("HelmetReflex", (0.22, -0.26, 0.99), 0.04, M_CREAM, segs=12)
reflex2 = add_sphere("HelmetReflex2", (0.30, -0.25, 0.93), 0.025, M_CREAM, segs=12)

# Detalhe lateral do capacete (abraçadeiras)
for side, x in [("L", -0.16), ("R", 0.36)]:
    clamp = add_cylinder(f"Clamp{side}", (x, 0, 0.80), 0.04, 0.06, M_GRAY)
    clamp.rotation_euler = (math.radians(90), 0, 0)

# Zíper / detalhe no torso
zipper = add_cube("Zipper", (0.10, -0.22, 0.45), (0.02, 0.01, 0.15), M_GRAY)

# ── CÂMERA ────────────────────────────────────────────────────────────────────
bpy.ops.object.camera_add(location=(0, -6, 2.2))
cam = bpy.context.object
cam.rotation_euler = (math.radians(82), 0, 0)
bpy.context.scene.camera = cam

# Câmera ortográfica para manter o estilo flat
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 4.2

# ── ILUMINAÇÃO ────────────────────────────────────────────────────────────────
# Luz principal suave (sem sombras duras)
bpy.ops.object.light_add(type='AREA', location=(3, -3, 5))
key = bpy.context.object
key.data.energy = 400
key.data.size = 5
key.rotation_euler = (math.radians(45), 0, math.radians(30))

# Rim light lateral
bpy.ops.object.light_add(type='AREA', location=(-4, -1, 3))
rim = bpy.context.object
rim.data.energy = 150
rim.data.size = 3
rim.data.color = (1.0, 0.85, 0.6)

# ── RENDER ────────────────────────────────────────────────────────────────────
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.film_transparent = False
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (*C_SKY, 1)
bg.inputs["Strength"].default_value = 0.5

# ── Toon shading via Freestyle ────────────────────────────────────────────────
scene.render.use_freestyle = True
scene.render.line_thickness = 1.2

print("✓ Space Kid scene criada! Pressione F12 para renderizar.")
