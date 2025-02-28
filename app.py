import streamlit as st
import cv2
import base64
from pint import UnitRegistry

# Initialize the Pint unit registry
ureg = UnitRegistry()

# Function to load and process a background image using OpenCV,
# then return the image as a base64-encoded string
def get_bg_image_base64(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return ""
    # Apply a Gaussian blur for a soft background effect
    img = cv2.GaussianBlur(img, (21, 21), 0)
    # Encode image as JPEG
    _, buffer = cv2.imencode('image.jpg', img)
    img_base64 = base64.b64encode(buffer).decode()
    return img_base64

# Define common units by category
common_units = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "foot", "yard", "mile", "inch"],
    "Mass": ["gram", "kilogram", "milligram", "pound", "ounce"],
    "Volume": ["liter", "milliliter", "gallon", "quart", "pint"],
    "Time": ["second", "minute", "hour", "day"],
}

temperature_mapping = {
    "celsius": "degC",
    "fahrenheit": "degF",
    "kelvin": "kelvin"
}

def convert_units(value, from_unit, to_unit, category):
    try:
        if category == "Temperature":
            from_unit = temperature_mapping.get(from_unit.lower(), from_unit)
            to_unit = temperature_mapping.get(to_unit.lower(), to_unit)
        result = value * ureg(from_unit)
        converted = result.to(to_unit)
        return converted.magnitude
    except Exception as e:
        st.error(f"Conversion error: {e}")
        return None

def main():
    # Set up the page configuration
    st.set_page_config(page_title="Professional Unit Converter", layout="wide")

    # Get the base64 string for the background image (update the path if needed)
    bg_image = get_bg_image_base64("Maquinaria Engranajes Industrial Líneas de Pantalla Imagen para Descarga Gratuita - Pngtree.jpeg")

    # Inject custom CSS with a background image and refined styling
    st.markdown(f"""
        <style>
            /* Set the full-page background image */
            body {{
                background-image: url("data:image/jpg;base64,{bg_image}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                margin: 0;
                padding: 0;
            }}
            /* Remove the default background of the main container */
            [data-testid="stAppViewContainer"] {{
                background-color: transparent;
            }}
            /* Title and subtitle styling with text-shadow for better contrast */
            .title {{
                font-size: 3rem;
                font-weight: bold;
                color: #ffffff;
                text-align: center;
                margin-top: 20px;
                text-shadow: 2px 2px 4px #000;
            }}
            .subtitle {{
                font-size: 1.5rem;
                color: #dddddd;
                text-align: center;
                margin-bottom: 20px;
                text-shadow: 1px 1px 3px #000;
            }}
            /* Frosted glass effect for the input and result boxes */
            .box {{
                background: rgba(0, 0, 0, 0.4);
                border-radius: 15px;
                padding: 30px;
                margin: 20px auto;
                max-width: 600px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                color: #ffffff;
            }}
            /* Button styling */
            .stButton>button {{
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 1.2rem;
            }}
            .stButton>button:hover {{
                background-color: #45a049;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Page header
    st.markdown('<p class="title">Professional Unit Converter</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Convert any unit with style!</p>', unsafe_allow_html=True)
    
    # Sidebar for selecting conversion category
    st.sidebar.header("Settings")
    category = st.sidebar.selectbox("Select Conversion Category", list(common_units.keys()))
    units = common_units.get(category, [])

    # Options box for user inputs
    st.markdown('<div class="box">', unsafe_allow_html=True)
    value = st.number_input("Enter the value to convert:", value=1.0, step=0.1)
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    st.markdown('</div>', unsafe_allow_html=True)

    # Convert button and result display in a styled box
    if st.button("Convert"):
        conversion_result = convert_units(value, from_unit, to_unit, category)
        if conversion_result is not None:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.success(f"{value} {from_unit} = {conversion_result:.4g} {to_unit}")
            st.markdown('</div>', unsafe_allow_html=True)
            st.balloons()  # Celebrate a successful conversion

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("Developed with Streamlit, Pint, and OpenCV by Ace.")

if __name__ == "__main__":
    main()
