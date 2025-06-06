import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from datetime import datetime

# Set up save directory
SAVE_DIR = "saved_diagrams"
os.makedirs(SAVE_DIR, exist_ok=True)

# Streamlit setup
st.set_page_config(page_title="Draw.io Save as PNG", layout="wide")
st.title("🖋️ Draw.io Diagram Editor")

# Filename input
filename = st.text_input("Enter filename", value="my_diagram")

# Use session state to store PNG data
if 'png_data' not in st.session_state:
    st.session_state.png_data = ""

# Get PNG data from JavaScript
png_data = st.text_area("PNG Base64 Data", 
                       value=st.session_state.png_data,
                       key="png_base64", 
                       label_visibility="collapsed",
                       height=68)

# Update session state
if png_data != st.session_state.png_data:
    st.session_state.png_data = png_data

# Debug info
if png_data:
    st.write("DEBUG: base64 length:", len(png_data))
    st.write("DEBUG: starts with correct header:", png_data.startswith("data:image/png;base64,"))

# Save PNG if received
if png_data and png_data.startswith("data:image/png;base64,") and filename:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{filename}_{timestamp}"
        
        # Extract base64 data (remove the data URL prefix)
        base64_data = png_data.split(",")[1]
        image_data = base64.b64decode(base64_data)
        
        # Save as PNG file
        png_path = os.path.join(SAVE_DIR, f"{base_filename}.png")
        with open(png_path, "wb") as f:
            f.write(image_data)
        
        # Save as base64 text file
        base64_path = os.path.join(SAVE_DIR, f"{base_filename}.txt")
        with open(base64_path, "w") as f:
            f.write(png_data)
        
        st.success(f"✅ Files saved successfully!")
        st.write(f"🖼️ PNG file: `{png_path}`")
        st.write(f"📄 Base64 file: `{base64_path}`")
        st.write(f"File size: {len(image_data)} bytes")
        
        # Clear the data after saving
        st.session_state.png_data = ""
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Failed to save files: {e}")
        st.write(f"Error details: {str(e)}")

# Manual save button
if st.button("🔄 Refresh to check for new diagram"):
    st.rerun()

# Embed draw.io and JS logic
components.html(
    f"""
    <iframe id="drawio-frame" 
            style="width:100%; height:600px; border:0;"
            src="https://embed.diagrams.net/?embed=1&proto=json&spin=1&ui=min&noSaveBtn=1&noExitBtn=1">
    </iframe>
    
    <script>
        const frame = document.getElementById("drawio-frame");
        let latestXML = "";
        
        // Function to find and update the Streamlit input
        function updateStreamlitInput(base64Data) {{
            console.log("Attempting to update Streamlit input with data length:", base64Data.length);
            
            // Try multiple methods to find the input
            const inputSelectors = [
                'textarea[data-testid="stTextArea"]',
                'textarea[aria-label="PNG Base64 Data"]',
                'textarea[key="png_base64"]',
                'textarea'
            ];
            
            let targetInput = null;
            for (const selector of inputSelectors) {{
                const inputs = window.parent.document.querySelectorAll(selector);
                for (const input of inputs) {{
                    if (input.style.height === '1px' || 
                        input.getAttribute('aria-label') === 'PNG Base64 Data' ||
                        input.id.includes('png_base64')) {{
                        targetInput = input;
                        break;
                    }}
                }}
                if (targetInput) break;
            }}
            
            if (targetInput) {{
                console.log("Found target input, updating...");
                targetInput.value = base64Data;
                targetInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                targetInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                targetInput.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                
                // Also try to trigger Streamlit's change detection
                const event = new Event('input', {{ bubbles: true }});
                targetInput.dispatchEvent(event);
                
                console.log("Input updated successfully");
                alert("Diagram exported! Click 'Refresh to check for new diagram' button to save.");
            }} else {{
                console.error("Could not find target input");
                alert("Export completed but could not find input field. Please refresh the page.");
            }}
        }}
        
        // Receive messages from draw.io
        window.addEventListener("message", function(event) {{
            if (event.source !== frame.contentWindow) return;
            
            try {{
                const msg = JSON.parse(event.data);
                console.log("Received message:", msg.event);
                
                if (msg.event === "init") {{
                    console.log("Draw.io initialized");
                    // Load blank diagram
                    frame.contentWindow.postMessage(JSON.stringify({{
                        action: "load",
                        autosave: 1,
                        xml: "<mxGraphModel><root><mxCell id='0'/><mxCell id='1' parent='0'/></root></mxGraphModel>"
                    }}), "*");
                }}
                else if (msg.event === "autosave" || msg.event === "save") {{
                    latestXML = msg.xml;
                    console.log("XML saved, length:", latestXML.length);
                }}
                else if (msg.event === "export") {{
                    console.log("Export received, data length:", msg.data.length);
                    const base64 = "data:image/png;base64," + msg.data;
                    updateStreamlitInput(base64);
                }}
            }} catch (e) {{
                console.error("Error processing message:", e);
            }}
        }});
        
        function submitDiagram() {{
            if (!latestXML) {{
                alert("Please draw something before submitting.");
                return;
            }}
            
            console.log("Exporting diagram...");
            // Export PNG
            frame.contentWindow.postMessage(JSON.stringify({{
                action: "export",
                format: "png",
                xml: latestXML,
                spin: "Exporting..."
            }}), "*");
        }}
        
        // Create Submit button
        const button = document.createElement("button");
        button.innerText = "📤 Export Diagram as PNG";
        button.style.marginTop = "10px";
        button.style.padding = "10px 20px";
        button.style.fontSize = "16px";
        button.style.backgroundColor = "#007bff";
        button.style.color = "white";
        button.style.border = "none";
        button.style.borderRadius = "5px";
        button.style.cursor = "pointer";
        button.onclick = submitDiagram;
        document.body.appendChild(button);
        
        console.log("Draw.io component loaded");
    </script>
    """,
    height=700,
)