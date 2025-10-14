# Legal Research Chatbot

An AI-powered legal assistant specializing in Indian laws with global legal system knowledge.

## Features

- Comprehensive Indian legal database covering major acts and regulations
- AI-powered responses using OpenAI GPT (when API key is provided)
- Global legal system information and comparisons
- User-friendly chat interface with typing animations
- Quick access to common legal queries
- Responsive design for all devices
- **Offline standalone version available**

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the repository**

2. **Run the setup script:**
   ```
   setup.bat
   ```

   This will:
   - Create a virtual environment
   - Install required packages (Flask, flask-cors, openai)

### Configuration

To enable AI-powered responses, you need to have the OpenAI library installed and provide your own API key.

If you need to install the required packages manually:
```
pip install Flask flask-cors openai==0.28.1
```

Note: This application uses openai version 0.28.1 for compatibility.

**To use the AI features, you need to set your OpenAI API key:**
- On Windows: `set OPENAI_API_KEY=your_actual_api_key_here`
- On macOS/Linux: `export OPENAI_API_KEY=your_actual_api_key_here`

## Running the Application

1. **Start the backend server:**
   ```
   run.bat
   ```
   Or manually:
   ```
   venv\Scripts\activate
   python chatbot.py
   ```

2. **Open the frontend:**
   Open [chatpot.html](file:///c%3A/Users/Acer/Desktop/hackerthon/chatpot.html) in your web browser

## Alternative: Standalone Offline Version

If you're experiencing connection issues or prefer to use the chatbot offline, we've included a standalone version that works completely without any internet connection:

- **File**: [standalone_legal_chatbot.html](file:///c%3A/Users/Acer/Desktop/hackerthon/standalone_legal_chatbot.html)
- **Features**: 
  - No internet required
  - No API keys needed
  - All legal knowledge embedded locally
  - Same legal information with improved search
  - Faster response times

To use the standalone version, simply double-click on [standalone_legal_chatbot.html](file:///c%3A/Users/Acer/Desktop/hackerthon/standalone_legal_chatbot.html) or access it through the link on the main page.

## Usage

### Legal Queries
- Ask specific questions about Indian laws, procedures, or rights
- Examples:
  - "What are my rights as a consumer in India?"
  - "Explain IPC Section 302"
  - "How to file a consumer complaint?"
  - "What is the procedure for company registration?"

### Global Legal Information
- Explore different legal systems worldwide
- Compare legal frameworks across countries
- View global legal statistics

## Project Structure

```
├── chatbot.py          # Backend Flask server (requires API key for AI features)
├── chat.js             # Frontend JavaScript
├── chat.css            # Styling
├── chatpot.html        # Main HTML interface
├── legal_training_data.json  # Training data for legal queries
├── requirements.txt    # Python dependencies
├── setup.bat           # Setup script
├── run.bat             # Run script
├── standalone_legal_chatbot.html  # Offline standalone version
└── README.md           # This file
```

## API Integration

The chatbot uses OpenAI's GPT models for enhanced responses. To use this feature:

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Set it as an environment variable:
   - Windows: `set OPENAI_API_KEY=your_actual_api_key_here`
   - macOS/Linux: `export OPENAI_API_KEY=your_actual_api_key_here`

When a valid API key is provided:
- Queries are processed through GPT for detailed, contextual responses
- Responses follow a structured format:
  1. Direct Answer
  2. Legal Framework
  3. Practical Application
  4. Key Considerations
  5. Next Steps
  6. Additional Resources

Without the OpenAI library or if there are connection issues, the system falls back to a keyword-based search of the legal corpus.

## Troubleshooting

If you encounter the error "Sorry, I encountered an error processing your request. Please try again.":

1. **Check Python Installation**: Ensure Python 3.7+ is installed and accessible from the command line
2. **Verify OpenAI Library**: Make sure the openai library is installed (`pip install openai==0.28.1`)
3. **Check API Key**: Ensure your OpenAI API key is properly set as an environment variable
4. **Check Internet Connection**: The application needs internet access to connect to OpenAI API
5. **Firewall/Proxy**: Ensure your firewall or proxy isn't blocking the connection to OpenAI

**Alternative Solution**: Use the [standalone_legal_chatbot.html](file:///c%3A/Users/Acer/Desktop/hackerthon/standalone_legal_chatbot.html) file which works completely offline without any external dependencies.

## Legal Disclaimer

This chatbot provides legal information, not legal advice. For specific legal situations, please consult with a qualified attorney.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is for educational purposes. See the LICENSE file for details.

## Developer

**Nirmal Subedi**
- BCA Data Science, SRM IST Trichy
- From Nepal, studying in India
- Bringing cross-cultural perspectives to legal technology innovation