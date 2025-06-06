import streamlit as st
import streamlit_drawable_canvas as st_canvas
from PIL import Image
import io
import base64
from datetime import datetime
import os

def save_canvas_image(canvas_result, filename):
    """Save canvas drawing as JPG image"""
    if canvas_result.image_data is not None:
        # Convert numpy array to PIL Image
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        
        # Convert RGBA to RGB (remove transparency for JPG)
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[-1])
        
        # Save as JPG
        rgb_img.save(filename, 'JPEG', quality=95)
        return True
    return False

def main():
    st.set_page_config(page_title="Drawing App", layout="wide")
    
    st.title("🎨 Draw.io Style Drawing App")
    st.markdown("Create your diagram below and click **Submit** to save as JPG")
    
    # Create two columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Drawing Canvas")
        
        # Drawing canvas
        canvas_result = st_canvas.st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Orange with transparency
            stroke_width=3,
            stroke_color="#000000",
            background_color="#FFFFFF",
            background_image=None,
            update_streamlit=True,
            height=500,
            width=700,
            drawing_mode="freedraw",
            point_display_radius=5,
            key="canvas",
        )
    
    with col2:
        st.subheader("Tools & Settings")
        
        # Drawing mode selection
        drawing_mode = st.selectbox(
            "Drawing Mode:",
            ["freedraw", "line", "rect", "circle", "transform", "polygon"]
        )
        
        # Stroke settings
        stroke_width = st.slider("Stroke Width:", 1, 10, 3)
        stroke_color = st.color_picker("Stroke Color:", "#000000")
        
        # Fill settings
        fill_color = st.color_picker("Fill Color:", "#FF6500")
        
        # Background color
        bg_color = st.color_picker("Background Color:", "#FFFFFF")
        
        # File name input
        filename = st.text_input("Filename (without extension):", value="my_diagram")
        
        # Submit button
        if st.button("💾 Submit & Save", type="primary"):
            if canvas_result.image_data is not None:
                # Create directory if it doesn't exist
                os.makedirs("saved_diagrams", exist_ok=True)
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                full_filename = f"saved_diagrams/{filename}_{timestamp}.jpg"
                
                # Save the image
                if save_canvas_image(canvas_result, full_filename):
                    st.success(f"✅ Diagram saved successfully as {full_filename}")
                    
                    # Show preview of saved image
                    with st.expander("Preview Saved Image"):
                        saved_img = Image.open(full_filename)
                        st.image(saved_img, caption="Saved Diagram", use_column_width=True)
                else:
                    st.error("❌ Failed to save diagram. Please draw something first!")
            else:
                st.warning("⚠️ Please draw something on the canvas before submitting.")
        
        # Clear canvas button
        if st.button("🗑️ Clear Canvas"):
            st.rerun()
    
    # Update canvas with new settings
    with col1:
        if drawing_mode or stroke_width or stroke_color or fill_color or bg_color:
            canvas_result = st_canvas.st_canvas(
                fill_color=f"rgba({int(fill_color[1:3], 16)}, {int(fill_color[3:5], 16)}, {int(fill_color[5:7], 16)}, 0.3)",
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                background_color=bg_color,
                background_image=None,
                update_streamlit=True,
                height=500,
                width=700,
                drawing_mode=drawing_mode,
                point_display_radius=5,
                key="canvas_updated",
            )
    
    # Display saved files
    st.subheader("📁 Saved Diagrams")
    if os.path.exists("saved_diagrams"):
        saved_files = [f for f in os.listdir("saved_diagrams") if f.endswith('.jpg')]
        if saved_files:
            st.write(f"Found {len(saved_files)} saved diagrams:")
            for file in saved_files:
                col_file, col_download = st.columns([3, 1])
                with col_file:
                    st.write(f"📄 {file}")
                with col_download:
                    with open(f"saved_diagrams/{file}", "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f.read(),
                            file_name=file,
                            mime="image/jpeg"
                        )
        else:
            st.info("No saved diagrams yet. Create and submit your first diagram!")
    else:
        st.info("No saved diagrams yet. Create and submit your first diagram!")

if __name__ == "__main__":
    main()