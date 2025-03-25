import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Set up the page
st.set_page_config(page_title="Emotion Wheel", layout="wide", initial_sidebar_state="collapsed")
st.title("Emotion Wheel")

# Define emotion data
emotion_data = [
    # HAPPY
    ["Happy", "Content", "Playful"],
    ["Happy", "Content", "Free"],
    ["Happy", "Content", "Joyful"],
    ["Happy", "Interested", "Curious"],
    ["Happy", "Interested", "Inquisitive"],
    ["Happy", "Proud", "Successful"],
    ["Happy", "Proud", "Confident"],
    ["Happy", "Accepted", "Respected"],
    ["Happy", "Accepted", "Valued"],
    ["Happy", "Powerful", "Courageous"],
    ["Happy", "Powerful", "Creative"],
    ["Happy", "Peaceful", "Loving"],
    ["Happy", "Peaceful", "Thankful"],
    ["Happy", "Trusting", "Sensitive"],
    ["Happy", "Trusting", "Intimate"],
    
    # SURPRISED
    ["Surprised", "Excited", "Energetic"],
    ["Surprised", "Excited", "Eager"],
    ["Surprised", "Amazed", "Awe"],
    ["Surprised", "Amazed", "Astonished"],
    ["Surprised", "Confused", "Perplexed"],
    ["Surprised", "Confused", "Disillusioned"],
    ["Surprised", "Startled", "Shocked"],
    ["Surprised", "Startled", "Dismayed"],
    ["Surprised", "Unfocused", "Distracted"],
    ["Surprised", "Unfocused", "Sleepy"],
    
    # BAD
    ["Bad", "Stressed", "Out of control"],
    ["Bad", "Stressed", "Overwhelmed"],
    ["Bad", "Busy", "Pressured"],
    ["Bad", "Busy", "Rushed"],
    ["Bad", "Bored", "Apathetic"],
    ["Bad", "Bored", "Indifferent"],
    ["Bad", "Tired", "Unfocused"],
    ["Bad", "Tired", "Sleepy"],
    ["Bad", "Anxious", "Overwhelmed"],
    ["Bad", "Anxious", "Scared"],
    
    # FEARFUL
    ["Fearful", "Scared", "Helpless"],
    ["Fearful", "Scared", "Frightened"],
    ["Fearful", "Anxious", "Worried"],
    ["Fearful", "Anxious", "Overwhelmed"],
    ["Fearful", "Insecure", "Inferior"],
    ["Fearful", "Insecure", "Inadequate"],
    ["Fearful", "Weak", "Worthless"],
    ["Fearful", "Weak", "Insignificant"],
    ["Fearful", "Rejected", "Excluded"],
    ["Fearful", "Rejected", "Persecuted"],
    ["Fearful", "Threatened", "Nervous"],
    ["Fearful", "Threatened", "Exposed"],
    
    # ANGRY
    ["Angry", "Distant", "Withdrawn"],
    ["Angry", "Distant", "Numb"],
    ["Angry", "Critical", "Skeptical"],
    ["Angry", "Critical", "Dismissive"],
    ["Angry", "Disgusted", "Disapproving"],
    ["Angry", "Disgusted", "Judgmental"],
    ["Angry", "Disapproving", "Embarrassed"],
    ["Angry", "Disapproving", "Disappointed"],
    ["Angry", "Awful", "Nauseated"],
    ["Angry", "Awful", "Detestable"],
    ["Angry", "Repelled", "Horrified"],
    ["Angry", "Repelled", "Hesitant"],
    ["Angry", "Aggressive", "Hostile"],
    ["Angry", "Aggressive", "Provoked"],
    ["Angry", "Mad", "Jealous"],
    ["Angry", "Mad", "Furious"],
    ["Angry", "Bitter", "Indignant"],
    ["Angry", "Bitter", "Violated"],
    ["Angry", "Humiliated", "Ridiculed"],
    ["Angry", "Humiliated", "Disrespected"],
    ["Angry", "Let down", "Betrayed"],
    ["Angry", "Let down", "Resentful"],
    
    # SAD
    ["Sad", "Lonely", "Isolated"],
    ["Sad", "Lonely", "Abandoned"],
    ["Sad", "Vulnerable", "Victimized"],
    ["Sad", "Vulnerable", "Fragile"],
    ["Sad", "Despair", "Grief"],
    ["Sad", "Despair", "Powerless"],
    ["Sad", "Guilty", "Ashamed"],
    ["Sad", "Guilty", "Remorseful"],
    ["Sad", "Depressed", "Empty"],
    ["Sad", "Depressed", "Inferior"],
    ["Sad", "Hurt", "Disappointed"],
    ["Sad", "Hurt", "Embarrassed"]
]

# Create DataFrame (if needed)
df = pd.DataFrame(emotion_data, columns=["Primary Emotion", "Secondary Emotion", "Tertiary Emotion"])

# Read external HTML, CSS, and JavaScript files
with open('index.html', 'r') as file:
    html_content = file.read()

with open('styles.css', 'r') as file:
    css_content = file.read()

with open('script.js', 'r') as file:
    js_content = file.read()

# Additional JavaScript for communication with Streamlit and to display selected symptoms
js_communication = """
// Create a div for the selected symptoms list if not already present
if (!document.getElementById('selectedSymptomsList')) {
    const list = document.createElement('ul');
    list.id = 'selectedSymptomsList';
    list.style.listStyleType = 'none';
    list.style.padding = '0';
    list.style.textAlign = 'center';
    list.style.fontSize = '16px';
    list.style.maxHeight = '200px';
    list.style.overflowY = 'scroll';  // Always show scrollbar when content overflows
    document.querySelector('.container').appendChild(list);
}

// Attach event listener to the "Show Selected Symptoms" button
if (document.getElementById('showSymptomsButton')) {
    document.getElementById('showSymptomsButton').addEventListener('click', function() {
        const listContainer = document.getElementById('selectedSymptomsList');
        listContainer.innerHTML = ""; // Clear previous list

        if (window.selectedSymptoms && window.selectedSymptoms.length > 0) {
            window.selectedSymptoms.forEach(function(symptom) {
                const li = document.createElement('li');
                li.textContent = symptom;
                listContainer.appendChild(li);
            });
        }
        
        // Send updated symptoms list to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: JSON.stringify({
                action: 'updateSymptoms',
                symptoms: window.selectedSymptoms ? window.selectedSymptoms : []
            })
        }, '*');
    });
}
"""

# Create a full HTML string with inline CSS and JavaScript that references external files
html_string = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Emotion Wheel</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <link rel="stylesheet" href="styles.css">
  <style>
    /* Additional adjustments for Streamlit integration */
    body {{
        display: block;
        min-height: auto;
        background-color: transparent;
    }}
    
    .container {{
        padding: 0;
        margin: 0;
    }}
    
    h1 {{
        display: none;
    }}
    
    /* Ensure clickable sections have a pointer cursor */
    path {{
        cursor: pointer;
        transition: opacity 0.3s, stroke-width 0.3s;
    }}
    
    /* Selected arc styling */
    .selected {{
        stroke: #fff !important;
        stroke-width: 4x !important;
    }}
    
    /* Style for the selected symptoms list with forced scrollbar */
    #selectedSymptomsList {{
        list-style-type: none;
        padding: 0;
        text-align: center;
        font-size: 16px;
        max-height: 200px;
        overflow-y: scroll;
        width: 300px;
        margin: 1rem auto 0 auto;
    }}
    
    #selectedSymptomsList li {{
        background: #444;
        color: #fff;
        margin: 5px auto;
        padding: 5px 10px;
        border-radius: 5px;
        max-width: 300px;
        transition: background-color 0.3s, transform 0.3s;
    }}
    
    #selectedSymptomsList li:hover {{
        background: #555;
        transform: scale(1.02);
    }}
    
    /* Debug panel styles */
    #debug-panel {{
        margin-top: 20px;
        padding: 10px;
        background-color: rgba(0,0,0,0.7);
        border-radius: 5px;
        color: #fff;
        text-align: left;
        font-family: monospace;
        max-height: 200px;
        overflow-y: auto;
        display: none;
    }}
    
    /* Debug toggle button */
    #debug-toggle {{
        background-color: #444;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }}
    
    /* Style for the Show Selected Symptoms button */
    #showSymptomsButton {{
        display: block;
        margin: 20px auto;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div id="emotion-wheel"></div>
    <button id="showSymptomsButton">Show Selected Symptoms</button>
    <ul id="selectedSymptomsList"></ul>
    <div id="debug-panel"></div>
    <button id="debug-toggle">Toggle Debug Panel</button>
  </div>
  <script>
    // Debug logging function
    function debug(msg) {{
        const panel = document.getElementById('debug-panel');
        if (panel) {{
            const line = document.createElement('div');
            line.textContent = `[${{new Date().toLocaleTimeString()}}] ${{msg}}`;
            panel.appendChild(line);
            panel.scrollTop = panel.scrollHeight;
        }}
        console.log(msg);
    }}

    // Toggle debug panel visibility
    document.getElementById('debug-toggle').addEventListener('click', function() {{
        const panel = document.getElementById('debug-panel');
        if (panel.style.display === 'none' || !panel.style.display) {{
            panel.style.display = 'block';
        }} else {{
            panel.style.display = 'none';
        }}
    }});

    debug('Initializing Emotion Wheel...');
    
    {js_content}
    {js_communication}
    
    // Handle click events within the emotion wheel container
    document.getElementById('emotion-wheel').addEventListener('click', function(e) {{
        debug('Wheel container clicked');
        if (e.target === this) return;
        const path = e.target.closest('path');
        if (path) {{
            debug('Path element found, triggering pathClickHandler');
            pathClickHandler.call(path, e);
        }}
    }});
  </script>
</body>
</html>
"""

# Display sidebar options
st.sidebar.header("Emotion Wheel Options")
st.sidebar.markdown("This is an interactive emotion wheel visualization.")
st.sidebar.markdown("Hover over sections to see emotion details.")
st.sidebar.markdown("Click on emotions to select multiple symptoms from any category.")

# Debug mode toggle
debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=False)

# Initialize session state variables if not present
if 'selected_emotions' not in st.session_state:
    st.session_state.selected_emotions = []

if 'current_emotion' not in st.session_state:
    st.session_state.current_emotion = None

if 'symptoms' not in st.session_state:
    st.session_state.symptoms = []

# Embed the HTML content
selected_data = components.html(html_string, height=1050, scrolling=False)

# Process data returned from the component
if selected_data:
    try:
        if debug_mode:
            st.write(f"Debug - Raw component data: {selected_data}")
        data = json.loads(selected_data)
        if debug_mode:
            st.write(f"Debug - Parsed data: {data}")
        if data.get('action') == 'select':
            primary = data.get('primary')
            secondary = data.get('secondary')
            tertiary = data.get('tertiary')
            st.session_state.symptoms = data.get('symptoms', [])
            if tertiary:
                emotion_str = f"{primary} → {secondary} → {tertiary}"
            elif secondary:
                emotion_str = f"{primary} → {secondary}"
            else:
                emotion_str = primary
            st.session_state.current_emotion = emotion_str
            if emotion_str not in st.session_state.selected_emotions:
                st.session_state.selected_emotions.append(emotion_str)
        elif data.get('action') == 'updateSymptoms':
            st.session_state.symptoms = data.get('symptoms', [])
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")



# Additional information section
st.markdown("### About the Emotion Wheel")
st.markdown("""
This wheel categorizes emotions into a hierarchical structure:
- **Primary emotions** (center): Happy, Surprised, Bad, Fearful, Angry, Sad
- **Secondary emotions** (middle ring): More specific derivatives of primary emotions
- **Tertiary emotions** (outer ring): The most specific emotion descriptions

**How to use:**
1. Hover over any section to see the emotion details.
2. Click on sections to select/deselect multiple emotions.
3. Click the "Show Selected Symptoms" button to view your highlighted symptoms.
4. Your selected emotions will appear as symptoms below the wheel and in the sidebar.
""")

# Display current symptoms below using Streamlit
if st.session_state.symptoms:
    st.markdown("### Your Symptoms")
    cols = st.columns(4)
    for i, symptom in enumerate(st.session_state.symptoms):
        parts = symptom.split(' → ')
        primary = parts[0]
        display_text = parts[-1]
        color_map = {
            'Happy': '#e07a5f',
            'Surprised': '#f2cc8f',
            'Bad': '#81b29a',
            'Fearful': '#3d85c6',
            'Angry': '#9575cd',
            'Sad': '#e57373'
        }
        cols[i % 4].markdown(
            f"""<div style="background-color: {color_map.get(primary, '#555')}; 
                           color: white; 
                           padding: 10px; 
                           border-radius: 15px; 
                           margin: 5px 0;
                           text-align: center;">
                {display_text}
            </div>""", 
            unsafe_allow_html=True
        )

# Debug section in sidebar if enabled
if debug_mode:
    st.sidebar.markdown("---")
    st.sidebar.header("Troubleshooting")
    if st.sidebar.button("Force Test Selection (Happy)"):
        st.session_state.selected_emotions.append("Happy")
        st.session_state.symptoms.append("Happy")
        st.experimental_rerun()
    if st.sidebar.button("Clear Debug Messages"):
        st.experimental_rerun()
