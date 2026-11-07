import os
import sys
from datetime import datetime

def get_project_config(idea):
    idea_lower = idea.lower()
    
    # 1. Détection Téléphone / Smartphone
    if any(k in idea_lower for k in ["telephone", "téléphone", "phone", "smartphone"]):
        return {
            "type": "phone_stand",
            "material": "PLA+ / PETG",
            "color": "0x6366f1",  # Indigo / Purple
            "layer_height": "0.2 mm",
            "infill": "20% (Gyroid)",
            "walls": 4,
            "supports": "Non (Design auto-portant)"
        }
    # 2. Détection caméra / support mural
    elif any(k in idea_lower for k in ["caméra", "camera", "mural"]):
        return {
            "type": "camera",
            "material": "PETG",
            "color": "0x3b82f6",
            "layer_height": "0.2 mm",
            "infill": "35% (Gyroid)",
            "walls": 4,
            "supports": "Oui (Brim)"
        }
    # 3. Détection boîtier / électronique
    elif any(k in idea_lower for k in ["boitier", "boîtier", "case", "raspberry"]):
        return {
            "type": "box",
            "material": "PLA+",
            "color": "0x10b981",
            "layer_height": "0.16 mm",
            "infill": "20% (Grid)",
            "walls": 3,
            "supports": "Non"
        }
    # 4. Détection engrenage / pièce mécanique
    elif any(k in idea_lower for k in ["engrenage", "gear", "mecanique"]):
        return {
            "type": "gear",
            "material": "ABS / Carbon",
            "color": "0xf59e0b",
            "layer_height": "0.12 mm",
            "infill": "50% (Cubic)",
            "walls": 5,
            "supports": "Non"
        }
    # 5. Par défaut (Forme abstraite / Torus)
    else:
        return {
            "type": "generic",
            "material": "PLA",
            "color": "0x8b5cf6",
            "layer_height": "0.2 mm",
            "infill": "25% (Grid)",
            "walls": 3,
            "supports": "Oui"
        }

def generate_report():
    project_idea = os.getenv("PROJECT_IDEA")
    if not project_idea and len(sys.argv) > 1:
        project_idea = sys.argv[1]
    if not project_idea:
        project_idea = "Projet 3D Personnalisé"

    config = get_project_config(project_idea)
    generation_time = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

    # Géométries 3D Three.js adaptées selon l'idée
    if config["type"] == "phone_stand":
        js_geometry = f"""
        // Socle incliné pour téléphone
        const baseGeo = new THREE.BoxGeometry(35, 6, 45);
        const baseMat = new THREE.MeshStandardMaterial({{ color: {config['color']}, roughness: 0.3 }});
        const base = new THREE.Mesh(baseGeo, baseMat);
        base.position.y = -8;
        group.add(base);

        // Dossier d'appui incliné à 60°
        const backGeo = new THREE.BoxGeometry(32, 45, 5);
        const backMat = new THREE.MeshStandardMaterial({{ color: {config['color']}, roughness: 0.3 }});
        const back = new THREE.Mesh(backGeo, backMat);
        back.position.set(0, 10, -10);
        back.rotation.x = Math.PI / 6;
        group.add(back);

        // Crochet retenue bas
        const lipGeo = new THREE.BoxGeometry(32, 8, 6);
        const lip = new THREE.Mesh(lipGeo, baseMat);
        lip.position.set(0, -3, 15);
        group.add(lip);
        """
    elif config["type"] == "camera":
        js_geometry = f"""
        const baseGeo = new THREE.BoxGeometry(40, 10, 30);
        const baseMat = new THREE.MeshStandardMaterial({{ color: {config['color']}, roughness: 0.3 }});
        const base = new THREE.Mesh(baseGeo, baseMat);
        base.position.y = -5;
        group.add(base);

        const cylGeo = new THREE.CylinderGeometry(8, 8, 25, 32);
        const cylMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, metalness: 0.8 }});
        const cylinder = new THREE.Mesh(cylGeo, cylMat);
        cylinder.rotation.z = Math.PI / 4;
        cylinder.position.set(0, 10, 0);
        group.add(cylinder);
        """
    elif config["type"] == "box":
        js_geometry = f"""
        const boxGeo = new THREE.BoxGeometry(45, 20, 35);
        const boxMat = new THREE.MeshStandardMaterial({{ color: {config['color']}, roughness: 0.4 }});
        const box = new THREE.Mesh(boxGeo, boxMat);
        group.add(box);
        """
    elif config["type"] == "gear":
        js_geometry = f"""
        const gearGeo = new THREE.CylinderGeometry(20, 20, 10, 16);
        const gearMat = new THREE.MeshStandardMaterial({{ color: {config['color']}, metalness: 0.5 }});
        const gear = new THREE.Mesh(gearGeo, gearMat);
        group.add(gear);
        """
    else:
        js_geometry = f"""
        const shapeGeo = new THREE.TorusKnotGeometry(12, 4, 64, 16);
        const shapeMat = new THREE.MeshStandardMaterial({{ color: {config['color']}, roughness: 0.2 }});
        const shape = new THREE.Mesh(shapeGeo, shapeMat);
        group.add(shape);
        """

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard 3D : {project_idea}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        :root {{ --primary: #3b82f6; --bg: #f8fafc; --card-bg: #ffffff; --text: #1e293b; --subtext: #64748b; }}
        * {{ box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); max-width: 950px; margin: 20px auto; padding: 15px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px; }}
        h1 {{ color: #0f172a; margin: 0; font-size: 1.5rem; }}
        .card {{ background: var(--card-bg); padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 20px; }}
        h2 {{ color: #334155; margin-top: 0; font-size: 1.2rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
        #viewer-container {{ width: 100%; height: 380px; background: #0f172a; border-radius: 8px; position: relative; overflow: hidden; touch-action: none; cursor: grab; }}
        #viewer-container:active {{ cursor: grabbing; }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: #f1f5f9; padding: 15px; border-radius: 8px; border-left: 4px solid var(--primary); }}
        .stat-card h3 {{ margin: 0 0 5px 0; font-size: 0.85rem; color: var(--subtext); }}
        .stat-card p {{ margin: 0; font-size: 1rem; font-weight: bold; color: #0f172a; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ padding: 12px; margin: 8px 0; background: #f1f5f9; border-radius: 6px; display: flex; align-items: center; }}
        input[type="checkbox"] {{ margin-right: 15px; transform: scale(1.3); cursor: pointer; }}
        .badge {{ display: inline-block; background: var(--primary); color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }}
        .progress-bar {{ width: 100%; height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; margin-bottom: 15px; }}
        .progress-fill {{ height: 100%; background: #22c55e; width: 0%; transition: width 0.3s; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>📊 Dashboard 3D Dynamique</h1>
        <div style="font-size: 0.85rem; color: #64748b;">⏱️ Généré le : <b>{generation_time}</b></div>
    </div>

    <div class="card">
        <h2>Visualiseur du Projet</h2>
        <p><b>Nom du projet :</b> <span class="badge">{project_idea}</span></p>
        <p><b>Matériau recommandé :</b> <b>{config['material']}</b></p>
        <div id="viewer-container"></div>
        <p style="text-align:center; font-size:0.85rem; color:#64748b; margin-top: 10px;">💡 Glissez avec la souris ou au doigt pour faire pivoter le modèle 3D.</p>
    </div>

    <div class="grid-stats">
        <div class="stat-card">
            <h3>Hauteur de couche</h3>
            <p>{config['layer_height']}</p>
        </div>
        <div class="stat-card">
            <h3>Remplissage (Infill)</h3>
            <p>{config['infill']}</p>
        </div>
        <div class="stat-card">
            <h3>Nombre de parois</h3>
            <p>{config['walls']} murs</p>
        </div>
        <div class="stat-card">
            <h3>Supports d'impression</h3>
            <p>{config['supports']}</p>
        </div>
    </div>

    <div class="card">
        <h2>🛠️ Checklist de Fabrication</h2>
        <div class="progress-bar"><div id="progress" class="progress-fill"></div></div>
        <ul>
            <li><input type="checkbox" onchange="updateProgress()"> Préparation du design 3D pour : {project_idea}</li>
            <li><input type="checkbox" onchange="updateProgress()"> Calibration du plateau et vérification du Z-Offset.</li>
            <li><input type="checkbox" onchange="updateProgress()"> Lancement du Slicing avec le matériau {config['material']}.</li>
            <li><input type="checkbox" onchange="updateProgress()"> Contrôle qualité final et assemblage.</li>
        </ul>
    </div>

    <script>
        const container = document.getElementById('viewer-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(50, 40, 50);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const pointLight = new THREE.PointLight(0xffffff, 0.9);
        pointLight.position.set(50, 50, 50);
        scene.add(pointLight);

        const group = new THREE.Group();
        
        {js_geometry}

        scene.add(group);

        let isDragging = false, prevX = 0, prevY = 0;
        function startDrag(x, y) {{ isDragging = true; prevX = x; prevY = y; }}
        function moveDrag(x, y) {{
            if (!isDragging) return;
            group.rotation.y += (x - prevX) * 0.01;
            group.rotation.x += (y - prevY) * 0.01;
            prevX = x; prevY = y;
        }}
        function stopDrag() {{ isDragging = false; }}

        container.addEventListener('mousedown', e => startDrag(e.clientX, e.clientY));
        window.addEventListener('mousemove', e => moveDrag(e.clientX, e.clientY));
        window.addEventListener('mouseup', stopDrag);

        container.addEventListener('touchstart', e => {{ if (e.touches.length === 1) startDrag(e.touches[0].clientX, e.touches[0].clientY); }}, {{passive: true}});
        container.addEventListener('touchmove', e => {{ if (e.touches.length === 1) moveDrag(e.touches[0].clientX, e.touches[0].clientY); }}, {{passive: true}});
        container.addEventListener('touchend', stopDrag);

        function updateProgress() {{
            const all = document.querySelectorAll('input[type="checkbox"]').length;
            const checked = document.querySelectorAll('input[type="checkbox"]:checked').length;
            document.getElementById('progress').style.width = (checked / all * 100) + '%';
        }}

        function animate() {{
            requestAnimationFrame(animate);
            if (!isDragging) group.rotation.y += 0.005;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>"""

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Dashboard mis à jour avec détection téléphone !")

if __name__ == "__main__":
    generate_report()
