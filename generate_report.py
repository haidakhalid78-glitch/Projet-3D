import os
import json

def generate_3d_report():
    model_description = "Support mural inclinable pour caméra de sécurité avec système de verrouillage par vis."
    
    print(f"🚀 Génération du rapport complet avec visuels pour : '{model_description}'")

    report_data = {
        "title": model_description,
        "material": "PETG ou PLA+",
        # Vous pouvez remplacer cette URL par l'image de votre choix (ou une photo de votre impression)
        "image_url": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?auto=format&fit=crop&w=800&q=80",
        "settings": {
            "layer_height": "0.2 mm",
            "infill_percentage": 35,
            "infill_pattern": "Gyroid",
            "walls": 4,
            "supports_needed": True,
            "bed_adhesion": "Brim"
        },
        "openscad_code": """// Code OpenSCAD généré automatiquement pour le modèle
module support_camera() {
    difference() {
        cube([60, 40, 20], center=true);
        translate([0, 0, 5]) cylinder(h=25, r=10, center=true);
    }
}
support_camera();""",
        "checklist": [
            "Nettoyer le plateau d'impression à l'alcool isopropylique (IPA).",
            "Vérifier la calibration du premier niveau de couche (Z-offset).",
            "Lancer l'impression 3D avec les paramètres de température recommandés.",
            "Retirer délicatement les supports d'impression après refroidissement.",
            "Effectuer un ponçage léger des zones de contact (papier de verre grain 400)."
        ]
    }

    # Création du fichier unique HTML avec intégration de l'image
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport Visuel - Impression 3D</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; background: #f8fafc; color: #1e293b; max-width: 900px; margin: 40px auto; padding: 20px; }}
        .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); margin-bottom: 20px; }}
        h1 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        h2 {{ color: #334155; margin-top: 0; }}
        pre {{ background: #1e293b; color: #f8fafc; padding: 15px; border-radius: 6px; overflow-x: auto; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ padding: 12px; margin: 8px 0; background: #f1f5f9; border-radius: 6px; display: flex; align-items: center; }}
        input[type="checkbox"] {{ margin-right: 15px; transform: scale(1.4); cursor: pointer; }}
        .badge {{ display: inline-block; background: #3b82f6; color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; }}
        .project-image {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>📑 Rapport de Projet 3D Visuel</h1>
        <p><b>Objet :</b> {report_data['title']}</p>
        <p><b>Matériau recommandé :</b> <span class="badge">{report_data['material']}</span></p>
        
        <!-- Affichage de l'image du projet -->
        <h3>Aperçu / Inspiration du Modèle :</h3>
        <img src="{report_data['image_url']}" alt="Aperçu du modèle 3D" class="project-image">
    </div>

    <div class="card">
        <h2>⚙️ Paramètres Slicer Optimisés</h2>
        <ul>
            <li><b>Hauteur de couche :</b> {report_data['settings']['layer_height']}</li>
            <li><b>Remplissage (Infill) :</b> {report_data['settings']['infill_percentage']}% ({report_data['settings']['infill_pattern']})</li>
            <li><b>Parois / Murs :</b> {report_data['settings']['walls']}</li>
            <li><b>Supports nécessaires :</b> {'Oui' if report_data['settings']['supports_needed'] else 'Non'}</li>
            <li><b>Adhésion au plateau :</b> {report_data['settings']['bed_adhesion']}</li>
        </ul>
    </div>

    <div class="card">
        <h2>📐 Modélisation 3D (Script OpenSCAD)</h2>
        <pre><code>{report_data['openscad_code']}</code></pre>
    </div>

    <div class="card">
        <h2>🛠️ Guide de Fabrication & Checklist Interactive</h2>
        <ul>
"""
    for task in report_data["checklist"]:
        html_content += f'            <li><input type="checkbox"> {task}</li>\n'
    
    html_content += """        </ul>
    </div>
</body>
</html>"""

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Fichier 'report.html' avec visuel généré avec succès !")

if __name__ == "__main__":
    generate_3d_report()
