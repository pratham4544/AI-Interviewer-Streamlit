import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from datetime import datetime

SAVE_DIR = "saved_diagrams"
os.makedirs(SAVE_DIR, exist_ok=True)

st.set_page_config(page_title="Draw.io Save PNG", layout="wide")
st.title("📐 Draw.io Diagram Editor with PNG Submit")

filename = st.text_input("Enter filename", value="my_diagram")

# Hidden input for base64 PNG string
png_base64 = st.text_area("PNG Base64 (Hidden)", key="png_data", height=100, label_visibility="collapsed")

if png_base64 and filename:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.png"
        image_data = base64.b64decode(png_base64.split(',')[1])
        path = os.path.join(SAVE_DIR, full_filename)
        with open(path, "wb") as f:
            f.write(image_data)
        st.success(f"✅ Diagram saved at: `{path}`")
    except Exception as e:
        st.error(f"❌ Failed to save image: {e}")

# Embed draw.io + JS to capture and send PNG back to Streamlit
components.html(
    f"""
    <iframe id="drawio-frame" 
            style="width:100%; height:600px; border:0;"
            src="https://embed.diagrams.net/?embed=1&proto=json&spin=1&ui=min&noSaveBtn=1&noExitBtn=1">
    </iframe>

    <script>
        const frame = document.getElementById("drawio-frame");
        let currentXML = "";

        window.addEventListener("message", function(event) {{
            const msg = JSON.parse(event.data);
            if (msg.event === "init") {{
                frame.contentWindow.postMessage(JSON.stringify({{
                    action: "load",
                    xml: "<mxGraphModel><root><mxCell id='0'/><mxCell id='1' parent='0'/></root></mxGraphModel>"
                }}), "*");
            }} else if (msg.event === "save" || msg.event === "autosave") {{
                currentXML = msg.xml;
            }} else if (msg.event === "export") {{
                const pngBase64 = "data:image/png;base64," + msg.data;
                const hiddenInput = window.parent.document.querySelector("textarea");
                hiddenInput.value = pngBase64;
                hiddenInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
            }}
        }});

        function submitDiagram() {{
            if (!currentXML) {{
                alert("Draw something first!");
                return;
            }}
            frame.contentWindow.postMessage(JSON.stringify({{
                action: "export",
                format: "png",
                xml: currentXML
            }}), "*");
        }}

        const btn = document.createElement("button");
        btn.innerText = "📤 Submit Diagram (Save as PNG)";
        btn.style.marginTop = "10px";
        btn.style.padding = "10px 20px";
        btn.style.fontSize = "16px";
        btn.style.backgroundColor = "#007bff";
        btn.style.color = "white";
        btn.style.border = "none";
        btn.style.borderRadius = "5px";
        btn.style.cursor = "pointer";
        btn.onclick = submitDiagram;
        document.body.appendChild(btn);
    </script>
    """,
    height=700,
)
