import streamlit as st
import pandas as pd
import openai

# Set the page configuration immediately, before any other Streamlit commands
st.set_page_config(page_title="BotWander Chatbot", page_icon=":camping:", layout="wide")

# Load the OpenAI and Google API key from Streamlit secrets (ensure your API key is correctly placed here)
openai.api_key = st.secrets["openai_api_key"]
google_maps_api_key = st.secrets["google_maps_api_key"]

# Load the CSV file (caching to avoid reloading)
@st.cache_data
def load_data():
    df = pd.read_csv('questions_and_generated_answers_with_images.csv')
    return df

df = load_data()

# Function to generate a response based on user input
def generate_response(question, df):
    # Check if the expected columns exist
    if 'Question' not in df.columns or 'Generated_Answer' not in df.columns or 'Image URL' not in df.columns:
        st.error("The CSV file does not contain the required 'Question', 'Generated_Answer', or 'Image URL' columns.")
        return "Error: Missing columns in the CSV."

    # Check if the question exists in the CSV
    if question in df['Question'].values:
        answer = df[df['Question'] == question]['Generated_Answer'].values[0]
        image_url = df[df['Question'] == question]['Image URL'].values[0] if pd.notna(df[df['Question'] == question]['Image URL'].values[0]) else None
    else:
        # If the question is not found in the CSV, use GPT-3.5 Turbo to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant focused on helping backpackers."},
                {"role": "user", "content": question}
            ]
        )
        answer = response['choices'][0]['message']['content']
        image_url = None
    
    return answer, image_url

# Main function to run the app
def main():
    # Initialize session state for tab selection if it doesn't exist
    if 'tab' not in st.session_state:
        st.session_state['tab'] = 'Country'

    # Create columns for layout
    col1, col2, col3 = st.columns([1, 2, 1])  # 1/4 left, 2/4 center, 1/4 right
    
    # Left side with tabs and logo
    with col1:
        # Display the logo at the top left corner
        st.image("https://i.imgur.com/SheyoGh.png", width=150)

        # Apply custom CSS to set the width for the selectbox and buttons
        st.markdown(
            """
            <style>
            .stSelectbox, .stButton > button {
                width: 100% !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Create buttons for navigation and update session state on button clicks
        st.write("### Navigation")
        country_selection = st.selectbox("Select a Country", ["Singapore", "Malaysia", "Thailand", "Vietnam", "Indonesia"])
        
        if country_selection == "Singapore":
            st.session_state['tab'] = 'Country'
        else:
            st.session_state['tab'] = f'Country_{country_selection}'

        # Dropdown menu for interests with --select-- as the first option
        interests_selection = st.selectbox(
            "Choose your interests",
            [
                "--select--",
                "Sketching & Art",
                "Photography",
                "Nature & Hiking",
                "Culture & History",
                "Food Exploration",
                "Adventure & Outdoor Sports",
                "Wildlife & Conservation",
                "Music & Festivals",
                "Spiritual & Wellness Travel",
                "Urban Exploration",
                "Volunteering & Social Impact"
            ]
        )
        
        # Only set the session state if an interest is selected (not --select--)
        if interests_selection != "--select--":
            st.session_state['tab'] = 'Interests'

        # Separate dropdown for Itinerary
        itinerary_selection = st.selectbox(
            "Select an Itinerary option",
            ["--select--", "Itinerary"]
        )

        if itinerary_selection == "Itinerary":
            st.session_state['tab'] = 'Itinerary'

        # Separate dropdown for Route
        route_selection = st.selectbox(
            "Select a Route option",
            ["--select--", "Route"]
        )

        if route_selection == "Route":
            st.session_state['tab'] = 'Route'

    # Middle section where the content of each tab will be displayed
    with col2:
        # Use session state to display the correct tab content
        if st.session_state['tab'] == 'Country':
            st.write("## Why Backpackers Should Visit Singapore")

            # Display the image for Singapore map
            st.image("https://i.imgur.com/c5BXXYu.jpeg")

            # Content explaining why backpackers should visit Singapore
            st.write("""
            Singapore blends tradition and modernity, making it an ideal destination for budget-conscious backpackers. Explore vibrant areas like Chinatown and Little India, enjoy street food at hawker centers, and relax in spots like Gardens by the Bay. Wondering "How many days should I stay in Singapore?" Ask the BotWander Chatbot for personalized advice. With affordable hostels, efficient transport, and a safe environment, Singapore offers an unforgettable experience for those seeking adventure on a budget.
            """)

            # Insert backpacker tips for Singapore in table format
            st.write("Whether it’s your first time or you’re a seasoned backpacker, these tips will help you explore Singapore like a pro. Keep these in mind for a smooth, fun, and respectful adventure!")

            # Markdown table for tips
            st.markdown("""
            | **Tip**                                | **Details**                                                                                                                                                            |
            |----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
            | **No Chewing Gum**                     | **Chewing gum** is banned in Singapore! You won’t find it in stores, and bringing it in is restricted. Avoid **chewing gum in public** to steer clear of fines.         |
            | **Return Your Trays**                  | After enjoying a meal at a hawker center or food court, remember to **return your tray**. Use the tray return stations in both **Halal** and **Non-Halal** sections.    |
            | **Respect Cultural Diversity**         | Singapore is **multicultural**. When visiting **temples, mosques**, or **churches**, dress modestly and **remove your shoes** before entering.                         |
            | **No Tipping Required**                | Tipping isn’t common here! **Service charges** are included in the bill at most places. No need to worry about tipping, even in taxis.                                  |
            | **Littering Can Lead to Fines**        | Singapore takes **cleanliness** seriously, and **littering** is a big no-no. Use trash bins or risk a **fine**!                                                         |
            | **Mind Your Manners on Public Transit**| Give up your seat to **elderly** folks, **pregnant women**, or those in need. Also, keep the **noise** down when riding the MRT (trains).                               |
            | **Smoke Only in Designated Areas**     | **Smoking** isn’t allowed in public spaces like malls and parks. Look for the **designated smoking zones** to stay on the right side of the law.                       |
            | **Tap Water is Safe**                  | No need to buy bottled water—**Singapore’s tap water** is perfectly safe to drink! Bring a **reusable water bottle** to stay hydrated.                                  |
            | **Eat Like a Local at Hawker Centres** | Singapore’s **hawker centers** are the best places for **cheap, tasty food**. Try iconic dishes like **Chicken Rice, Laksa**, or **Satay** without breaking your budget. |
            | **Respect Halal/Non-Halal Sections**   | Pay attention to **Halal** and **Non-Halal** sections in food courts. It’s respectful to **return trays** to the right section, especially in mixed dining groups.      |
            """)

            st.write("Enjoy your adventure in Singapore, and remember: being a respectful backpacker makes for an even more rewarding trip!")

        elif st.session_state['tab'] in ['Country_Malaysia', 'Country_Thailand', 'Country_Vietnam', 'Country_Indonesia']:
           
            # Display the same image for Malaysia, Thailand, Vietnam, and Indonesia
            st.image("https://i.imgur.com/nrrjzET.jpeg")

        elif st.session_state['tab'] == 'Interests' and interests_selection == 'Sketching & Art':
            st.write("### Sketching & Art in Singapore: How to Use the BotWander Chatbot")
            
            st.write("""
            As a backpacker passionate about **Sketching & Art**, you can use the **BotWander Chatbot** to discover inspiring locations, cultural insights, and practical tips in Singapore. 
            Here are some questions and prompts you can ask the chatbot to guide your artistic journey through the city-state.
            """)

            # Section 1: Art Supply Stores
            st.write("### 1. Art Supply Stores")
            st.write("- **Question Example**: \"Where can I buy art supplies in Singapore?\"")
            st.write("""
            The chatbot will guide you to popular art supply stores such as **Art Friend** (at Bras Basah Complex), **Overjoyed** (on Short Street), or **Straits Art** (on North Bridge Road), where you can find all your sketching materials.
            """)

            # Section 2: Discover Singapore’s Culture Through Art
            st.write("### 2. Discover Singapore’s Culture Through Art")
            st.write("- **Question Example**: \"What are some cultural landmarks to sketch in Singapore?\"")
            st.write("- **Question Example**: \"Where can I sketch traditional Singaporean architecture?\"")
            st.write("""
            The chatbot will highlight locations like **Chinatown**, **Little India**, and **Kampong Glam**, where you can capture Singapore's rich cultural heritage through your sketches of temples, colorful shophouses, and street scenes.
            """)

            # Section 3: Explore Singapore’s Art Scene
            st.write("### 3. Explore Singapore’s Art Scene")
            st.write("- **Question Example**: \"What are the best art galleries or museums to visit in Singapore?\"")
            st.write("- **Question Example**: \"Is there any street art I can sketch in Singapore?\"")
            st.write("""
            You’ll be guided to must-see places like the **National Gallery Singapore**, **ArtScience Museum**, or **Gillman Barracks**, as well as areas like **Haji Lane** and **Little India**, where you can find vibrant street art.
            """)

            # Section 4: Attend Art Events and Workshops
            st.write("### 4. Attend Art Events and Workshops")
            st.write("- **Question Example**: \"Are there any sketching meetups or art workshops in Singapore?\"")
            st.write("- **Question Example**: \"What art events are happening in Singapore this month?\"")
            st.write("""
            The chatbot can provide information on local art workshops, sketching meetups, and events such as **Singapore Art Week**, giving you the chance to connect with fellow artists.
            """)

        elif st.session_state['tab'] == 'Interests' and interests_selection == 'Photography':
            st.write("### Photography in Singapore: How to Use the BotWander Chatbot")
    
            st.write("""
            As a backpacker passionate about **Photography**, you can use the **BotWander Chatbot** to explore the vibrant scenes, hidden gems, and practical advice for capturing stunning moments in Singapore. 
            Here are some questions and prompts you can ask the chatbot to guide your photography adventure through the city-state.
            """)

            # Section 1: Photography Gear Stores
            st.write("### 1. Photography Gear Stores")
            st.write("- **Question Example**: \"Where can I buy photography gear in Singapore?\"")
            st.write("- **Question Example**: \"Is there a place to rent camera equipment in Singapore?\"")
            st.write("""
            The chatbot will guide you to popular photography gear stores like **Cathay Photo** (at Peninsula Plaza), **Alan Photo** (in Sim Lim Square), or rental services for camera equipment.
            """)

            # Section 2: Capture Singapore’s Iconic Landmarks
            st.write("### 2. Capture Singapore’s Iconic Landmarks")
            st.write("- **Question Example**: \"What are the best places to photograph the Marina Bay Sands skyline?\"")
            st.write("- **Question Example**: \"Where can I get the best shots of the Singapore Flyer at sunset?\"")
            st.write("""
            The chatbot will highlight popular photography spots like **Marina Bay Sands**, **Merlion Park**, and **Gardens by the Bay**, perfect for skyline and sunset shots.
            """)

            # Section 3: Hidden Photography Spots
            st.write("### 3. Hidden Photography Spots")
            st.write("- **Question Example**: \"Can you suggest some hidden photography spots in Singapore?\"")
            st.write("- **Question Example**: \"Where can I find nature spots for photography in Singapore?\"")
            st.write("""
            You’ll discover lesser-known spots like **Tiong Bahru**, **Kranji Marshes**, and **MacRitchie Reservoir**, where you can capture unique angles of nature and urban scenery.
            """)

            # Section 4: Attend Photography Meetups and Workshops
            st.write("### 4. Attend Photography Meetups and Workshops")
            st.write("- **Question Example**: \"Are there any photography workshops or meetups in Singapore?\"")
            st.write("- **Question Example**: \"What photography events are happening in Singapore this month?\"")
            st.write("""
            The chatbot will provide details on photography meetups, workshops, and events like **PhotoWalk Singapore** or exhibitions at the **National Gallery**.
            """)

            # Section 5: Street Photography Opportunities
            st.write("### 5. Street Photography Opportunities")
            st.write("- **Question Example**: \"Where can I capture street photography in Singapore?\"")
            st.write("- **Question Example**: \"What are some photogenic neighborhoods to explore in Singapore for street shots?\"")
            st.write("""
            Explore vibrant neighborhoods like **Chinatown**, **Little India**, and **Haji Lane**, known for their street art and lively atmosphere, perfect for street photography.
            """)

        elif st.session_state['tab'] == 'Interests' and interests_selection == 'Nature & Hiking':
            st.write("### Nature & Hiking in Singapore: How to Use the BotWander Chatbot")
    
            st.write("""
            As a backpacker passionate about **Nature & Hiking**, you can use the **BotWander Chatbot** to explore lush green spaces, hiking trails, and hidden natural gems in Singapore. 
            Here are some questions and prompts you can ask the chatbot to guide your outdoor adventures through the city-state.
            """)

            # Section 1: Nature Reserves and Parks
            st.write("### 1. Nature Reserves and Parks")
            st.write("- **Question Example**: \"What are the best nature reserves to visit in Singapore?\"")
            st.write("- **Question Example**: \"Where can I find scenic hiking trails in Singapore?\"")
            st.write("""
            The chatbot will guide you to top nature reserves like **MacRitchie Reservoir**, **Bukit Timah Nature Reserve**, and **Sungei Buloh Wetland Reserve**.
            """)

            # Section 2: Hidden Natural Gems
            st.write("### 2. Hidden Natural Gems")
            st.write("- **Question Example**: \"Can you suggest some hidden natural spots in Singapore?\"")
            st.write("- **Question Example**: \"Where can I find quiet nature trails for a peaceful hike?\"")
            st.write("""
            You’ll discover off-the-beaten-path spots like **Coney Island**, **Labrador Nature Reserve**, and **Kranji Marshes** for a more serene experience.
            """)

            # Section 3: Hiking Trails
            st.write("### 3. Hiking Trails")
            st.write("- **Question Example**: \"What are the best beginner-friendly hiking trails in Singapore?\"")
            st.write("- **Question Example**: \"Are there any challenging hikes for advanced hikers in Singapore?\"")
            st.write("""
            The chatbot will highlight trails ranging from beginner-friendly walks like **Southern Ridges** to challenging hikes like **Bukit Timah Hill**.
            """)

            # Section 4: Attend Outdoor Events and Meetups
            st.write("### 4. Attend Outdoor Events and Meetups")
            st.write("- **Question Example**: \"Are there any nature walk meetups or hiking events in Singapore?\"")
            st.write("- **Question Example**: \"What nature-related events are happening in Singapore this month?\"")
            st.write("""
            You’ll receive details on outdoor meetups, nature walks, and events like the **Nature Society (Singapore)** activities.
            """)

            # Section 5: Wildlife and Birdwatching
            st.write("### 5. Wildlife and Birdwatching")
            st.write("- **Question Example**: \"Where can I go for birdwatching in Singapore?\"")
            st.write("- **Question Example**: \"Which nature reserves have the most wildlife to observe?\"")
            st.write("""
            For wildlife lovers, the chatbot will suggest spots like **Sungei Buloh Wetland Reserve** and **Pulau Ubin**, known for their rich biodiversity and birdwatching opportunities.
            """)


        elif st.session_state['tab'] == 'Itinerary':
            st.write("### Plan your itinerary.")

            # Display the example questions
            st.write("#### Question Example:")
            st.write("- Can you recommend some affordable hostels in Singapore for under SGD (your budget)?")
            st.write("- What are some alternative accommodations for under (your budget)?")
            st.write("- What’s an ideal one-day itinerary in Singapore for exploring cultural and historic sites with a budget below (your budget)?")
    
            # Embed Google Doc using an iframe
            google_doc_url = "https://docs.google.com/document/d/1ckUS_FFhI3bFew-arLeXEF8eDdyXfuJzyik_kPhM_HI/edit?usp=sharing"
    
            # Use st.markdown with raw HTML to embed the iframe
            st.markdown(f"""
                <iframe src="{google_doc_url}" width="700" height="900"></iframe>
            """, unsafe_allow_html=True)

        elif st.session_state['tab'] == 'Route':
            st.write("### Find directions using Public Transport")

            # Display the example questions
            st.write("#### Question Example:")
            st.write("- How can I travel from (starting location) to (destination)?")

            # Allow user input for start and end locations
            start_location = st.text_input("Enter the starting location", "Changi Airport Singapore")
            end_location = st.text_input("Enter the destination", "Dream Lodge")

            # Create Google Maps Embed URL for directions with public transport mode
            google_maps_embed_url = f"https://www.google.com/maps/embed/v1/directions?key={google_maps_api_key}&origin={start_location}&destination={end_location}&mode=transit"

            # Embed Google Maps Directions iframe
            st.markdown(
                f"""
                <iframe
                    width="700" 
                    height="500" 
                    frameborder="0" 
                    style="border:0"
                    src="{google_maps_embed_url}" 
                    allowfullscreen>
                </iframe>
                """,
                unsafe_allow_html=True
            )


    # Right side with the chatbot interface
    with col3:
        # Define custom CSS for different text elements
        st.markdown(
            """
            <style>
            .small-font {
                font-size: 14px;
            }
            .medium-font {
                font-size: 26px;
            }
            .large-font {
                font-size: 32px;
                font-weight: bold;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
        # Adjusted title and subheader font size
        st.markdown("<div class='large-font'>BotWander Chatbot</div>", unsafe_allow_html=True)
        st.markdown("<div class='medium-font'>Your personal assistant for all things backpacking! Ask me anything about travel tips, destinations, and more.</div>", unsafe_allow_html=True)
    
        # User input section
        st.write("#### What would you like to know?")
        user_input = st.text_input("", placeholder="Enter your travel question here...")

        # Function to handle user input and display response
        if user_input:
            with st.spinner("Preparing your travel tips..."):
                response, image_url = generate_response(user_input, df)
        
                # Display image first if it exists
                if image_url and pd.notna(image_url):
                    st.image(image_url, caption=f"Related to: {user_input}")
        
                # Display response with smaller font size
                st.markdown(f"<div class='small-font'><strong>Response:</strong></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='small-font'>{response}</div>", unsafe_allow_html=True)

    # Footer section
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
            text-align: center;
            padding: 10px;
        }
        </style>
        <div class="footer">
            <p>BotWander Chatbot © 2024 | Powered by OpenAI GPT-3.5 Turbo</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Run the app
if __name__ == "__main__":
    main()
