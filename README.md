# Travel_Planner_AI_sanhita
Overview
The AI Travel Planner is a Streamlit web application that assists users in planning their trips. It provides two main features:
1.	AI-powered Travel Cost Estimation
2.	AI-generated Travel Itinerary
The app integrates Google's Gemini API for AI-generated responses and LangChain for retrieval-augmented generation (RAG) using travel guides stored in a vector database. Additionally, a chatbot is embedded to answer travel-related queries.
________________________________________
Features and Functionality
1. Banner and UI Setup
•	The app sets a banner image with an overlayed title and subtitle.
•	The sidebar allows users to input their Google API Key for accessing Gemini models.
2. User Inputs for Trip Details
Users can provide:
•	Source & Destination
•	Number of Travelers (Adults & Children)
•	Preferred Transport Mode
•	Currency for cost estimation
•	Travel Date
•	Budget (optional)
•	Food inclusion option
3. AI-powered Travel Cost Estimation
Function: get_ai_travel_cost()
•	Constructs a prompt template using LangChain.PromptTemplate.
•	Uses Google's Gemini-1.5-pro model to estimate travel costs.
•	Factors in transportation, accommodation, food, and miscellaneous expenses.
•	Adjusts prices based on weekends, peak seasons, and visa fees.
•	Returns an AI-generated breakdown of costs.
4. AI-generated Travel Itinerary
Function: generate_itinerary()
•	Creates an AI-generated structured itinerary including: 
o	Must-visit attractions
o	Hidden gems & local experiences
o	Accommodation suggestions
o	Local transport options
o	Recommended restaurants
o	Hourly breakdown of activities
o	Cost-saving travel tips
•	Uses Google's Gemini-1.5-pro model for response generation.
5. Chatbot Integration
The AI Travel Assistant chatbot allows users to ask travel-related questions based on a travel guide PDF using RAG (Retrieval-Augmented Generation).
Key Components:
•	LangChain for Chat Prompt Template
•	Google's Gemini API for responses
•	PDFMiner for loading travel guide PDFs
•	NLTK Text Splitter for chunking text
•	ChromaDB for storing travel guide embeddings
•	Vector search with Google Generative AI embeddings
Functionality:
•	Retrieves relevant context from the travel guide PDF.
•	Uses Gemini API to generate responses tailored to user queries.
•	Provides relevant travel advice, tips, and recommendations.
•	Chatbot is toggleable in the sidebar.
6. Styling and UX Enhancements
•	Custom CSS for UI elements such as: 
o	Banner image with title overlay
o	Styled form fields and labels
o	Themed buttons with hover effects
o	Styled sidebar and chatbot UI
•	Responsive design with Streamlit layout options.
________________________________________
Required Inputs & Dependencies
User Inputs Required:
•	Google API Key (to access Gemini AI)
•	Source & Destination
•	Number of travelers (adults/children)
•	Transport preference (Flight, Train, etc.)
•	Budget (optional)
•	Currency selection
•	Travel Date
•	Food inclusion (checkbox)
•	User questions (for chatbot interaction)
Dependencies:
•	streamlit (for web UI)
•	google.generativeai (for AI responses)
•	langchain (for chatbot and AI workflows)
•	pandas (for data handling)
•	plotly.express (for visualizations)
•	datetime (for date input processing)
•	pdfminer (for extracting travel guide data)
•	NLTK (for text splitting)
•	ChromaDB (for vector-based search)
________________________________________
How It Works
1.	User enters trip details → The AI generates cost estimates & itinerary.
2.	User can interact with the chatbot → The chatbot retrieves relevant answers from a travel guide PDF.
3.	Google API Key validation → Ensures only valid API keys are used.
4.	Custom-styled UI → Provides a visually appealing experience.
________________________________________
Future Enhancements
•	Flight & hotel booking API integration
•	Multi-day itinerary generation
•	Real-time weather & currency exchange rate integration
•	User authentication for personalized trip planning
•	Interactive map-based itinerary visualization
