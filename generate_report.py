import os
from datetime import datetime

def generate_dynamic_report():
    # Récupère l'idée passée par le workflow GitHub (ou valeur par défaut en local)
    project_idea = os.getenv("PROJECT_IDEA", "Projet 3D personnalisé")
    generation_time = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    
    print(f"🚀 Génération dynamique pour le projet : '{project_idea}'")

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Dynamique : {project_idea}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        :root {{ --primary: #3b82f6; --bg: #0f172a; --card-bg: #ffffff; --text: #1e293b; }}
        * {{ box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #f8fafc; color: var(--text); max-width: 900px; margin: 20px auto; padding: 15px; }}
        .card {{ background: var(--card-bg); padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 20px; }}
        h1 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-top: 0; }}
        #viewer-container {{ width: 100%; height: 380px; background: #0f172a; border-radius: 8px; position: relative; overflow: hidden; touch-action: none; cursor: grab; }}
        #viewer-container:active {{ cursor: grabbing; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 12px; margin: 8px 0; background: #f1f5f9; border-radius: 6px; display: flex; align-items: center; }}
        input[type="checkbox"] {{ margin-right: 15px; transform: scale(1.3); cursor: pointer; }}
        .badge {{ display: inline-block; background: var(--primary); color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; }}
        .progress-bar {{ width: 100%; height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; margin-bottom: 15px; }}
        .progress-fill {{ height: 100%; background: #22c55e; width: 0%; transition: width 0.3s; }}
    </style>
</head>
<body>

    <div class="card">
        <h1>📑 Rapport 3D Dynamique</h1>
        <p>⏱️ Généré le : <b>{generation_time}</b></p>
        <p><b>Idée / Objet du Projet :</b> <span class="badge">{project_idea}</span></p>
        
        <div id="viewer-container"></div>
        <p style="text-align:center; font-size:0.85rem; color:#64748b;">💡 Glissez votre doigt ou la souris pour faire pivoter la forme 3D.</p>
    </div>

    <div class="card">
        <h2>🛠️ Checklist de Fabrication</h2>
        <div class="progress-bar"><div id="progress" class="progress-fill"></div></div>
        <ul>
            <li><input type="checkbox" onchange="updateProgress()"> Valider le design CAO / structurel pour : {project_idea}</li>
            <li><input type="checkbox" onchange="updateProgress()"> Préparer les paramètres du Slicer (Optimisation parois/remplissage).</li>
            <li><input type="checkbox" onchange="updateProgress()"> Lancer l'impression 3D ou la fabrication.</li>
            <li><input type="checkbox" onchange="updateProgress()"> Contrôle qualité et finitions.</li>
        </ul>
    </div>

    <script>
        const container = document.getElementById('viewer-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(40, 40, 40);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const pointLight = new THREE.PointLight(0xffffff, 0.9);
        pointLight.position.set(40, 40, 40);
        scene.add(pointLight);

        // Forme 3D générique dynamique
        const group = new THREE.Group();
        const geom1 = new THREE.BoxGeometry(30, 30, 30);
        const mat1 = new THREE.MeshStandardMaterial({{ color: 0x3b82f6, roughness: 0.3 }});
        group.add(new THREE.Mesh(geom1, mat1));

        scene.add(group);

        let isDragging = false, prevX = 0, prevY = 0;
        container.addEventListener('mousedown', e => {{ isDragging = true; prevX = e.clientX; prevY = e.clientY; }});
        window.addEventListener('mousemove', e => {{
            if (!isDragging) return;
            group.rotation.y += (e.clientX - prevX) * 0.01;
            group.rotation.x += (e.clientY - prevY) * 0.01;
            prevX = e.clientX; prevY = e.clientY;
        }});
        window.addEventListener('mouseup', () => {{ isDragging = false; }});

        container.addEventListener('touchstart', e => {{ if (e.touches.length === 1) {{ isDragging = true; prevX = e.touches[0].clientX; prevY = e.touches[0].clientY; }} }}, {{passive: true}});
        container.addEventListener('touchmove', e => {{
            if (!isDragging || e.touches.length !== 1) return;
            group.rotation.y += (e.touches[0].clientX - prevX) * 0.01;
            group.rotation.x += (e.touches[0].clientY - prevY) * 0.01;
            prevX = e.touches[0].clientX; prevY = e.touches[0].clientY;
        }}, {{passive: true}});
        container.addEventListener('touchend', () => {{ isDragging = false; }});

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

    print("✅ Rapport dynamique généré avec succès !")

if __name__ == "__main__":
    generate_dynamic_report()
