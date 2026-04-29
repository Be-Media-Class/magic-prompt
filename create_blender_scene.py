"""
Blender Python script - Astronaut on a Planet Surface
Recria a cena flat/vector: astronauta sentado ao lado de um rádio retrô,
sob um céu estrelado com planeta ao fundo.

Como usar:
  1. Abra o Blender
  2. Vá em Scripting > New
  3. Cole este script e pressione Run Script (Alt+P)
  4. Ou via terminal: blender --background --python create_blender_scene.py
"""

import bpy
import math
import random

# ---------------------------------------------------------------------------
# Limpar cena
# ---------------------------------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for d in [bpy.data.materials, bpy.data.meshes, bpy.data.cameras, bpy.data.lights]:
    for item in d:
        d.remove(item)

# ---------------------------------------------------------------------------
# Paleta de cores (RGBA)
# ---------------------------------------------------------------------------
BLACK    = (0.030, 0.020, 0.020, 1.0)
DARK_BG  = (0.015, 0.010, 0.010, 1.0)
BEIGE    = (0.910, 0.785, 0.595, 1.0)
CREAM    = (0.940, 0.865, 0.680, 1.0)
RED      = (0.720, 0.100, 0.100, 1.0)
ORANGE   = (0.680, 0.220, 0.065, 1.0)
GRAY     = (0.520, 0.520, 0.520, 1.0)
DARK_GRAY= (0.300, 0.300, 0.300, 1.0)
LIGHT_GRAY=(0.700, 0.700, 0.700, 1.0)
STAR_W   = (0.950, 0.900, 0.760, 1.0)
VISOR    = (0.060, 0.045, 0.045, 1.0)
PLANET_R = (0.640, 0.140, 0.090, 1.0)

# ---------------------------------------------------------------------------
# Factory de material (Emission = flat, sem iluminação)
# ---------------------------------------------------------------------------
_mat_cache = {}

def mat(name, color):
    if name in _mat_cache:
        return _mat_cache[name]
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    nodes.clear()
    emit = nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value = color
    emit.inputs['Strength'].default_value = 1.0
    out  = nodes.new('ShaderNodeOutputMaterial')
    links.new(emit.outputs[0], out.inputs[0])
    _mat_cache[name] = m
    return m

# ---------------------------------------------------------------------------
# Helpers de criação de objetos
# ---------------------------------------------------------------------------
def box(name, loc, scale, color):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(name + '_m', color))
    return obj

def sphere(name, loc, scale, color, segs=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=segs // 2, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(name + '_m', color))
    return obj

def cylinder(name, loc, scale, color, rot=(0, 0, 0), verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(name + '_m', color))
    return obj

def plane_h(name, loc, scale, color):
    """Plano horizontal."""
    bpy.ops.mesh.primitive_plane_add(location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(name + '_m', color))
    return obj

# ---------------------------------------------------------------------------
# Mundo / fundo escuro
# ---------------------------------------------------------------------------
world = bpy.context.scene.world
world.use_nodes = True
bg_node = world.node_tree.nodes.get('Background')
if not bg_node:
    bg_node = world.node_tree.nodes.new('ShaderNodeBackground')
bg_node.inputs['Color'].default_value = DARK_BG
bg_node.inputs['Strength'].default_value = 1.0

# ---------------------------------------------------------------------------
# Chão  (dois planos: areia bege + faixa cinza na frente)
# ---------------------------------------------------------------------------
# Plano de areia bege (fundo)
plane_h('ground_sand', (0.0,  1.5, -2.05), (7.0, 4.5, 1.0), BEIGE)
# Faixa cinza na frente (borda inferior)
plane_h('ground_gray', (0.0, -1.0, -2.05), (7.0, 2.0, 1.0), GRAY)
# Borda de transição entre areia e cinza
box('ground_edge', (0.0, 0.35, -2.0), (7.0, 0.08, 0.06), DARK_GRAY)

# ---------------------------------------------------------------------------
# Estrelas
# ---------------------------------------------------------------------------
random.seed(7)
star_mat_obj = mat('star', STAR_W)
for i in range(40):
    x = random.uniform(-3.8, 3.8)
    z = random.uniform(0.2, 5.5)
    y = random.uniform(-0.3, 0.3)
    r = random.uniform(0.012, 0.042)
    # Algumas estrelas com brilho tipo cruz (4 pontas)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=6, ring_count=4, location=(x, y, z))
    s = bpy.context.active_object
    s.name = f'star_{i}'
    s.scale = (r, r, r)
    s.data.materials.append(star_mat_obj)

# Estrela destaque (maior, com brilho de 4 pontos)
sphere('star_bright', (1.2, 0, 2.8), (0.055, 0.055, 0.055), STAR_W, segs=8)
box('star_bright_h', (1.2, 0, 2.8), (0.005, 0.005, 0.120), STAR_W)
box('star_bright_v', (1.2, 0, 2.8), (0.120, 0.005, 0.005), STAR_W)

# ---------------------------------------------------------------------------
# Planeta (esfera dupla: bege com calota vermelha)
# ---------------------------------------------------------------------------
sphere('planet_body', (1.35, 0.0, 4.20), (0.42, 0.42, 0.42), CREAM, segs=32)
# Calota avermelhada na parte superior-central
sphere('planet_cap',  (1.35, 0.0, 4.42), (0.32, 0.32, 0.26), PLANET_R, segs=32)

# ---------------------------------------------------------------------------
# RÁDIO RETRÔ
# ---------------------------------------------------------------------------
rx, ry, rz = -1.05, 0.0, -1.52

# Corpo principal
box('radio_body',   (rx,        ry,       rz + 0.52), (0.195, 0.130, 0.52), GRAY)
# Placa frontal com painel laranja
box('radio_panel',  (rx - 0.195, ry,      rz + 0.52), (0.010, 0.090, 0.38), ORANGE)
# LEDs vermelhos
box('radio_led1',   (rx - 0.196, ry,      rz + 0.70), (0.012, 0.065, 0.085), RED)
box('radio_led2',   (rx - 0.196, ry,      rz + 0.42), (0.012, 0.065, 0.085), RED)
# Base do rádio
box('radio_base',   (rx,        ry,       rz + 0.055), (0.220, 0.145, 0.055), DARK_GRAY)
# Topo / controles
box('radio_top',    (rx,        ry,       rz + 1.005), (0.195, 0.130, 0.005), DARK_GRAY)
# Botão vermelho no topo esquerdo
cylinder('radio_btn_l', (rx - 0.10, ry, rz + 1.04), (0.038, 0.038, 0.025), RED)
# Knob no centro
cylinder('radio_knob', (rx + 0.05, ry, rz + 1.04), (0.030, 0.030, 0.030), DARK_GRAY)
# Detalhe: pequena janela/visor no corpo
box('radio_window', (rx + 0.196, ry, rz + 0.78), (0.010, 0.060, 0.080), DARK_GRAY)
# Fio/cabo embaixo
cylinder('radio_cable', (rx, ry, rz - 0.02), (0.018, 0.018, 0.04), BLACK)

# ---------------------------------------------------------------------------
# ASTRONAUTA
# ---------------------------------------------------------------------------
ax, ay, az = 0.22, 0.0, -1.55   # ponto base (chão debaixo do astronauta)

# ── Tronco / corpo ──────────────────────────────────────────────────────────
# Torso principal (preto)
box('torso',       (ax,       ay, az + 0.62), (0.295, 0.215, 0.40), BLACK)
# Detalhe de zíper (linha clara ao centro)
box('zipper',      (ax,  ay - 0.215, az + 0.62), (0.018, 0.005, 0.36), DARK_GRAY)
# Detalhe vermelho no peito (pequeno emblema)
box('chest_detail',(ax,  ay - 0.215, az + 0.78), (0.045, 0.005, 0.028), RED)

# ── Pernas (sentado, joelhos levantados) ────────────────────────────────────
for side, sx in [('l', -0.14), ('r', 0.14)]:
    # Coxa indo para frente/cima
    box(f'thigh_{side}', (ax + sx, ay + 0.22, az + 0.30), (0.115, 0.255, 0.135), BLACK)
    # Joelho
    sphere(f'knee_{side}', (ax + sx, ay + 0.41, az + 0.29), (0.105, 0.105, 0.110), BLACK, segs=12)
    # Canela descendo
    box(f'shin_{side}',  (ax + sx, ay + 0.15, az + 0.05), (0.100, 0.185, 0.175), BLACK)
    # Perna baixa cinza claro (tipo meia/calça)
    box(f'lleg_{side}',  (ax + sx, ay + 0.05, az - 0.18), (0.090, 0.130, 0.105), LIGHT_GRAY)
    # Sapato (preto, achatado)
    box(f'shoe_{side}',  (ax + sx, ay + 0.00, az - 0.31), (0.110, 0.160, 0.055), BLACK)

# ── Capacete ────────────────────────────────────────────────────────────────
hz = az + 1.12

sphere('helmet',      (ax, ay, hz), (0.345, 0.305, 0.345), CREAM, segs=32)
# Anel do colarinho
cylinder('helm_ring', (ax, ay, hz - 0.30), (0.240, 0.240, 0.045), LIGHT_GRAY)
# Colarinho base
cylinder('helm_collar',(ax, ay, hz - 0.34), (0.255, 0.255, 0.030), DARK_GRAY)

# ── Viseira ──────────────────────────────────────────────────────────────────
# Viseira escura (esfera achatada na frente do capacete)
sphere('visor_dark',  (ax, ay - 0.275, hz), (0.240, 0.115, 0.240), VISOR, segs=24)
# Reflexo branco (ponto de luz no canto superior)
sphere('visor_glare', (ax - 0.075, ay - 0.38, hz + 0.095), (0.048, 0.025, 0.048), STAR_W, segs=8)

# ── Rosto (dentro do capacete) ───────────────────────────────────────────────
sphere('face',       (ax, ay - 0.235, hz - 0.02), (0.175, 0.070, 0.175), ORANGE, segs=24)
# Olhos (pontos pretos)
sphere('eye_l',      (ax - 0.058, ay - 0.30,  hz - 0.015), (0.028, 0.020, 0.028), BLACK, segs=8)
sphere('eye_r',      (ax + 0.058, ay - 0.30,  hz - 0.015), (0.028, 0.020, 0.028), BLACK, segs=8)
# Boca levemente triste (caixa fina)
box('mouth',         (ax, ay - 0.305, hz - 0.075), (0.045, 0.012, 0.010), BLACK)

# ── Antena ───────────────────────────────────────────────────────────────────
cylinder('antenna_rod', (ax + 0.025, ay, hz + 0.565), (0.013, 0.013, 0.280), LIGHT_GRAY)
sphere('antenna_tip',   (ax + 0.025, ay, hz + 0.845), (0.040, 0.040, 0.040), LIGHT_GRAY, segs=8)
# Nó da antena (esfera pequena no meio)
sphere('antenna_node',  (ax + 0.025, ay, hz + 0.580), (0.020, 0.020, 0.020), DARK_GRAY, segs=8)

# ---------------------------------------------------------------------------
# Câmera (ortográfica para o estilo flat)
# ---------------------------------------------------------------------------
bpy.ops.object.camera_add(location=(0.0, -9.0, 0.35))
cam = bpy.context.active_object
cam.name = 'Camera'
cam.rotation_euler = (math.radians(90), 0.0, 0.0)
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 6.2          # zoom: menor = mais próximo
bpy.context.scene.camera = cam

# ---------------------------------------------------------------------------
# Luz ambiente (suave, para não interferir nos materiais Emission)
# ---------------------------------------------------------------------------
bpy.ops.object.light_add(type='SUN', location=(0, -5, 8))
sun = bpy.context.active_object
sun.name = 'Sun'
sun.data.energy = 0.5               # baixo — materiais Emission dominam

# ---------------------------------------------------------------------------
# Configurações de render
# ---------------------------------------------------------------------------
scene = bpy.context.scene
scene.render.resolution_x = 900
scene.render.resolution_y = 1600
scene.render.film_transparent = False
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.filepath = '//render_astronaut.png'

# Usar denoising para resultado mais limpo
scene.cycles.use_denoising = True

# ---------------------------------------------------------------------------
# Smooth shading em tudo (opcional — remova para look mais facetado)
# ---------------------------------------------------------------------------
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()
        obj.select_set(False)

print("=" * 60)
print("Cena criada com sucesso!")
print("Pressione F12 para renderizar.")
print("Saída: render_astronaut.png (ao lado do arquivo .blend)")
print("=" * 60)
