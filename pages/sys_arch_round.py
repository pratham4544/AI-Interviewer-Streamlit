import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Check for candidate_id
if 'candidate_id' not in st.session_state:
    st.error("⚠️ No candidate ID found. Please start from the homepage.")
    st.stop()

candidate_id = st.session_state.candidate_id

# Set up save directory
SAVE_DIR = Path(__file__).parent.parent / "saved_diagrams"
os.makedirs(SAVE_DIR, exist_ok=True)

# Streamlit setup
st.set_page_config(page_title="System Design Editor", layout="wide")
st.title("🖋️ System Architecture Design")

# Add to session state initialization
if 'drawing_data' not in st.session_state:
    st.session_state.drawing_data = None
if 'png_data' not in st.session_state:
    st.session_state.png_data = None

# Embed Excalidraw
# Updated Excalidraw embed with auto-save functionality
components.html(
    """
    <iframe
        id="excalidraw-frame"
        src="https://excalidraw.com/"
        style="width:100%; height:600px; border:0; border-radius: 4px;"
    ></iframe>
    
    <script>
        const frame = document.getElementById('excalidraw-frame');
        
        window.addEventListener('message', function(event) {
            if (event.origin !== 'https://excalidraw.com') return;
            
            if (event.data.type === 'excalidraw') {
                // Auto-export as PNG
                frame.contentWindow.postMessage(
                    { type: 'exportScene', payload: { format: 'png' } },
                    'https://excalidraw.com'
                );
            }
            
            // Handle exported PNG
            if (event.data.type === 'exportedScene') {
                const pngData = event.data.payload;
                
                // Notify Streamlit with the PNG data
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: {
                        type: 'png',
                        data: pngData
                    }
                }, '*');
            }
        });
    </script>
    """,
    height=650,
    key="excalidraw_component"
)

# Add instructions
# Updated instructions
st.markdown("""
### Instructions:
1. Use the drawing tool above to create your system design
2. Your design will be automatically saved as you draw
3. When you're finished, click the 'Complete Design' button below
""")

# Add save button
# Updated save button
if st.button("Complete Design"):
    component_value = st.session_state.excalidraw_component
    if component_value and isinstance(component_value, dict) and 'data' in component_value:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_design_{candidate_id}_{timestamp}.png"
        filepath = SAVE_DIR / filename
        
        try:
            # Save the PNG data
            png_data = component_value['data']
            if png_data.startswith('data:image/png;base64,'):
                png_data = png_data.split(',')[1]
            
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(png_data))
            
            st.success(f"✅ Design saved successfully as {filename}")
            st.image(filepath, caption="Your System Design")
            
            # Add complete interview button
            if st.button("Complete Interview"):
                st.success("🎉 Congratulations! You've completed all rounds of the interview.")
                st.balloons()
                
        except Exception as e:
            st.error(f"❌ Error saving design: {str(e)}")
            logging.error(f"Save error: {str(e)}")
    else:
        st.warning("Please create and export a design before completing.")