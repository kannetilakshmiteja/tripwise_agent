"""Three.js 3D travel scene embedded in Streamlit."""
import streamlit.components.v1 as components


def render_3d_scene(theme: str = "light", height: int = 280, scene: str = "home", node_count: int = 7) -> None:
    bg = "#0b1220" if theme == "dark" else "#e8f4fc"
    fog = "#0b1220" if theme == "dark" else "#d0e8f5"
    plane_color = "#ff6b35" if theme == "light" else "#ff9f5a"
    globe_color = "#0077b6" if theme == "light" else "#38bdf8"
    show_plane = scene in ("home", "flight", "signup")
    show_globe = scene in ("home", "signup", "support")
    show_building = scene == "hotel"
    show_confetti = scene == "confetti"
    label = {
        "home": "TripWise — 20 AI agents orchestration hub",
        "flight": "Flight search — 3D aircraft",
        "hotel": "Hotel booking — city skyline",
        "signup": "Welcome to TripWise",
        "support": "Agent command center",
        "confetti": "Booking confirmed!",
    }.get(scene, "TripWise 3D")
    nc = node_count

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  body {{ margin: 0; overflow: hidden; background: {bg}; }}
  #c {{ width: 100%; height: {height}px; display: block; }}
  .label {{
    position: absolute; bottom: 8px; left: 12px;
    font-family: system-ui, sans-serif; font-size: 11px;
    color: rgba(100,116,139,0.9); pointer-events: none;
  }}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div class="label">{label}</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function() {{
  const canvas = document.getElementById('c');
  const W = canvas.parentElement.clientWidth || 600;
  const H = {height};
  const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true, alpha: true }});
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('{bg}');
  scene.fog = new THREE.Fog('{fog}', 8, 22);

  const camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 100);
  camera.position.set(0, 1.2, 5.5);

  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const dir = new THREE.DirectionalLight(0xffffff, 0.9);
  dir.position.set(5, 8, 5);
  scene.add(dir);
  const point = new THREE.PointLight(0x00b4d8, 0.6, 20);
  point.position.set(-3, 2, 2);
  scene.add(point);

  // Globe
  const globeGeo = new THREE.SphereGeometry(1.35, 48, 48);
  const globeMat = new THREE.MeshPhongMaterial({{
    color: '{globe_color}',
    transparent: true,
    opacity: 0.35,
    wireframe: false,
    shininess: 80
  }});
  const showGlobe = {str(show_globe).lower()};
  const showPlane = {str(show_plane).lower()};
  const showBuilding = {str(show_building).lower()};
  const showConfetti = {str(show_confetti).lower()};
  let globe, wireGlobe;
  if (showGlobe) {{
    globe = new THREE.Mesh(globeGeo, globeMat);
    scene.add(globe);
    const wireGeo = new THREE.SphereGeometry(1.38, 24, 24);
    const wireMat = new THREE.MeshBasicMaterial({{
      color: '{globe_color}', wireframe: true, transparent: true, opacity: 0.25
    }});
    wireGlobe = new THREE.Mesh(wireGeo, wireMat);
    scene.add(wireGlobe);
  }}

  // Orbit rings (agent paths)
  for (let i = 0; i < 3; i++) {{
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(1.9 + i * 0.35, 0.015, 8, 64),
      new THREE.MeshBasicMaterial({{ color: 0x00b4d8, transparent: true, opacity: 0.35 - i * 0.08 }})
    );
    ring.rotation.x = Math.PI / 2 + i * 0.15;
    scene.add(ring);
  }}

  // Airplane body (simplified 3D model)
  const planeGroup = new THREE.Group();
  const body = new THREE.Mesh(
    new THREE.CapsuleGeometry(0.12, 0.7, 4, 12),
    new THREE.MeshPhongMaterial({{ color: '{plane_color}', shininess: 100 }})
  );
  body.rotation.z = Math.PI / 2;
  planeGroup.add(body);

  const wing = new THREE.Mesh(
    new THREE.BoxGeometry(0.9, 0.03, 0.2),
    new THREE.MeshPhongMaterial({{ color: 0xffffff }})
  );
  planeGroup.add(wing);

  const tail = new THREE.Mesh(
    new THREE.BoxGeometry(0.2, 0.25, 0.03),
    new THREE.MeshPhongMaterial({{ color: '{plane_color}' }})
  );
  tail.position.set(-0.45, 0.12, 0);
  planeGroup.add(tail);

  if (showPlane) {{
    planeGroup.position.set(2.2, 0.4, 0);
    planeGroup.scale.set(0.9, 0.9, 0.9);
    scene.add(planeGroup);
  }}

  if (showBuilding) {{
    const hotel = new THREE.Group();
    for (let b = 0; b < 5; b++) {{
      const h = 0.4 + Math.random() * 0.8;
      const box = new THREE.Mesh(
        new THREE.BoxGeometry(0.35, h, 0.35),
        new THREE.MeshPhongMaterial({{ color: 0x64748b + b * 0x111111 }})
      );
      box.position.set((b - 2) * 0.45, h/2 - 0.5, 0);
      hotel.add(box);
    }}
    hotel.position.set(0, -0.3, 0);
    scene.add(hotel);
  }}

  const nodes = [];
  const colors = [0xe85d04, 0x0077b6, 0x00b4d8, 0x059669, 0xd97706, 0x7c3aed, 0xdc2626];
  const nodeTotal = {nc};
  for (let i = 0; i < nodeTotal; i++) {{
    const n = new THREE.Mesh(
      new THREE.SphereGeometry(0.08, 16, 16),
      new THREE.MeshPhongMaterial({{ color: colors[i], emissive: colors[i], emissiveIntensity: 0.3 }})
    );
    const angle = (i / nodeTotal) * Math.PI * 2;
    n.userData = {{ angle, radius: 2.1, speed: 0.3 + i * 0.04, y: Math.sin(i) * 0.4 }};
    scene.add(n);
    nodes.push(n);
  }}

  // Stars
  const starsGeo = new THREE.BufferGeometry();
  const positions = [];
  for (let i = 0; i < 200; i++) {{
    positions.push((Math.random() - 0.5) * 30, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 30);
  }}
  starsGeo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  scene.add(new THREE.Points(starsGeo, new THREE.PointsMaterial({{ color: 0xffffff, size: 0.04, transparent: true, opacity: 0.5 }})));

  const confetti = [];
  if (showConfetti) {{
    const colors = [0xe85d04, 0x0077b6, 0x059669, 0xfbbf24, 0xdc2626];
    for (let i = 0; i < 80; i++) {{
      const p = new THREE.Mesh(
        new THREE.BoxGeometry(0.06, 0.06, 0.02),
        new THREE.MeshBasicMaterial({{ color: colors[i % colors.length] }})
      );
      p.position.set((Math.random()-0.5)*4, Math.random()*3+1, (Math.random()-0.5)*2);
      p.userData.vy = -0.02 - Math.random() * 0.03;
      p.userData.vx = (Math.random()-0.5) * 0.02;
      scene.add(p);
      confetti.push(p);
    }}
  }}

  let t = 0;
  function animate() {{
    requestAnimationFrame(animate);
    t += 0.01;
    if (globe) {{ globe.rotation.y += 0.003; wireGlobe.rotation.y += 0.002; }}
    if (showPlane) {{
      planeGroup.position.x = 2.2 * Math.cos(t * 0.5);
      planeGroup.position.z = 2.2 * Math.sin(t * 0.5);
      planeGroup.rotation.y = -t * 0.5 + Math.PI / 2;
    }}
    confetti.forEach(p => {{
      p.position.y += p.userData.vy;
      p.position.x += p.userData.vx;
      if (p.position.y < -2) p.position.y = 3;
    }});
    nodes.forEach((n, i) => {{
      const a = n.userData.angle + t * n.userData.speed;
      n.position.x = n.userData.radius * Math.cos(a);
      n.position.z = n.userData.radius * Math.sin(a);
      n.position.y = n.userData.y + Math.sin(t * 2 + i) * 0.15;
    }});
    renderer.render(scene, camera);
  }}
  animate();

  window.addEventListener('resize', () => {{
    const w = canvas.parentElement.clientWidth || W;
    camera.aspect = w / H;
    camera.updateProjectionMatrix();
    renderer.setSize(w, H);
  }});
}})();
</script>
</body>
</html>
"""
    components.html(html, height=height + 24, scrolling=False)
