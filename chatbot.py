import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime
import random

# Try to import openai, but handle if it's not available
try:
    import openai
    openai_available = True
    # Set a placeholder API key - users need to set their own key in environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-proj-your-real-api-key-here")
except ImportError:
    openai = None
    openai_available = False
    print("OpenAI library not available - using fallback response system")

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

LEGAL_CORPUS = [
    {
        "title": "Constitution of India",
        "text": "The supreme law of India that establishes the framework for the government, fundamental rights, directive principles, and the structure of the state. Contains 448 articles in 25 parts and 12 schedules."
    },
    {
        "title": "Indian Penal Code, 1860",
        "text": "The main criminal code of India that covers all substantive aspects of criminal law. It was drafted in 1860 and came into force in 1862. Contains 511 sections."
    },
    {
        "title": "Code of Criminal Procedure, 1973",
        "text": "The procedural law for conducting criminal trials in India. It provides the machinery for the investigation of crime, apprehension of suspects, collection of evidence, and trial of offenders."
    },
    {
        "title": "Indian Contract Act, 1872",
        "text": "The law governing contracts in India. It determines the circumstances under which promises made by parties to a contract shall be legally binding. Contains 266 sections."
    },
    {
        "title": "Specific Relief Act, 1963",
        "text": "Provides remedies to enforce civil rights when a person's rights have been violated. It covers specific performance of contracts, injunctions, and restitution."
    },
    {
        "title": "Transfer of Property Act, 1882",
        "text": "Regulates the transfer of property in India. It defines conditions under which property may be transferred and the rights and liabilities of parties involved."
    },
    {
        "title": "Indian Evidence Act, 1872",
        "text": "The law dealing with the rules and regulations concerning evidence in civil and criminal proceedings. It determines what facts may be proved in any legal proceeding."
    },
    {
        "title": "Civil Procedure Code, 1908",
        "text": "The procedural law for conducting civil proceedings in India. It regulates the procedure to be followed by civil courts in the conduct of civil suits."
    },
    {
        "title": "Negotiable Instruments Act, 1881",
        "text": "Governs promissory notes, bills of exchange, and cheques in India. It defines the legal framework for negotiable instruments and related offenses."
    },
    {
        "title": "Companies Act, 2013",
        "text": "Regulates the incorporation, governance, and winding up of companies in India. It replaced the Companies Act, 1956 and introduced several reforms."
    },
    {
        "title": "Income Tax Act, 1961",
        "text": "Governs the taxation of income in India. It defines the rules for income tax collection and administration, covering various heads of income."
    },
    {
        "title": "Goods and Services Tax Act, 2017",
        "text": "The comprehensive indirect tax on manufacture, sale and consumption of goods and services throughout India. It replaced multiple indirect taxes."
    },
    {
        "title": "Sale of Goods Act, 1930",
        "text": "Governs the sale and purchase of goods in India. It defines the rights and obligations of buyers and sellers in commercial transactions."
    },
    {
        "title": "Partnership Act, 1932",
        "text": "Governs the law relating to partnership in India. It defines partnership, rights and duties of partners, and dissolution of partnership."
    },
    {
        "title": "Consumer Protection Act, 2019",
        "text": "Provides for protection of interests of consumers and establishes authorities for timely and effective administration and settlement of consumer disputes."
    },
    {
        "title": "Arbitration and Conciliation Act, 1996",
        "text": "Consolidates and amends the law relating to domestic and international arbitration and enforcement of foreign arbitral awards."
    },
    {
        "title": "Commercial Courts Act, 2015",
        "text": "Provides for the constitution of commercial courts, commercial divisions and commercial appellate divisions in high courts for adjudicating commercial disputes."
    },
    {
        "title": "Insolvency and Bankruptcy Code, 2016",
        "text": "Consolidates the laws relating to reorganization and insolvency resolution of corporate persons, partnership firms and individuals in a time bound manner."
    },
    {
        "title": "Information Technology Act, 2000",
        "text": "Provides the legal framework for electronic governance and recognizes electronic records and digital signatures. It also defines cyber crimes."
    },
    {
        "title": "Right to Information Act, 2005",
        "text": "Empowers citizens to secure access to information under the control of public authorities, promoting transparency and accountability in governance."
    },
    {
        "title": "Motor Vehicles Act, 1988",
        "text": "Regulates road transport vehicles in India. It covers licensing of drivers, registration of vehicles, traffic regulations, and penalties for violations."
    },
    {
        "title": "Factories Act, 1948",
        "text": "Regulates the working conditions in factories. It covers health, safety, welfare, working hours, and employment of young persons in factories."
    },
    {
        "title": "Minimum Wages Act, 1948",
        "text": "Provides for fixing minimum rates of wages in certain employments to ensure fair compensation for workers and prevent exploitation."
    },
    {
        "title": "Industrial Disputes Act, 1947",
        "text": "Provides measures for investigation and settlement of industrial disputes and lays down the rights of workmen and obligations of employers."
    },
    {
        "title": "Maternity Benefit Act, 1961",
        "text": "Regulates the employment of women in certain establishments for certain periods before and after childbirth and provides for maternity and certain other benefits."
    },
    {
        "title": "Prevention of Money Laundering Act, 2002",
        "text": "Provides for prevention of money laundering and to provide for confiscation of property derived from money laundering."
    },
    {
        "title": "Foreign Exchange Management Act, 1999",
        "text": "Consolidates and amends the law relating to foreign exchange with the objective of facilitating external trade and payments."
    },
    {
        "title": "Copyright Act, 1957",
        "text": "Provides for protection of copyright in literary, dramatic, musical and artistic works, cinematograph films and sound recordings."
    },
    {
        "title": "Patents Act, 1970",
        "text": "Governs the patent system in India. It provides for grant of patents for inventions and protection of patentees' rights."
    },
    {
        "title": "Trade Marks Act, 1999",
        "text": "Provides for registration and protection of trade marks and to prevent fraudulent use of trade marks."
    },
    {
        "title": "Competition Act, 2002",
        "text": "Provides for establishment of a Commission to prevent practices having adverse effect on competition and to regulate combinations."
    },
    {
        "title": "Environment Protection Act, 1986",
        "text": "Provides for protection and improvement of environment and prevention of hazards to human beings, other living creatures, plants and property."
    },
    {
        "title": "Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989",
        "text": "Provides for prevention of atrocities against members of Scheduled Castes and Scheduled Tribes and for providing relief and compensation."
    },
    {
        "title": "Protection of Women from Domestic Violence Act, 2005",
        "text": "Provides for more effective protection of rights of women guaranteed under the Constitution who are victims of violence of any kind occurring within the family."
    },
    {
        "title": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
        "text": "Provides protection against sexual harassment of women at workplace and for prevention and redressal of complaints of sexual harassment."
    },
    {
        "title": "Juvenile Justice (Care and Protection of Children) Act, 2015",
        "text": "Provides for care, protection, treatment, development and rehabilitation of juvenile delinquents and neglected juveniles."
    }
]

GLOBAL_LEGAL_SYSTEMS = [
    {
        "name": "Common Law",
        "description": "Based on judicial precedent and case law. Used in UK, USA, Canada, Australia, India.",
        "characteristics": [
            "Judge-made law through precedents",
            "Adversarial system",
            "Binding precedent (stare decisis)",
            "Flexible and adaptive"
        ],
        "countries": ["United Kingdom", "United States", "Canada", "Australia", "India", "Pakistan", "Malaysia"]
    },
    {
        "name": "Civil Law",
        "description": "Based on comprehensive legal codes. Used in most of Europe, Latin America.",
        "characteristics": [
            "Codified statutes as primary source",
            "Inquisitorial system",
            "Judges apply law rather than create it",
            "More predictable and systematic"
        ],
        "countries": ["France", "Germany", "Italy", "Spain", "Brazil", "Mexico", "Japan"]
    },
    {
        "name": "Religious Law",
        "description": "Based on religious texts and doctrines.",
        "characteristics": [
            "Derived from religious scriptures",
            "Divine authority as source",
            "Covers both civil and criminal matters",
            "Limited flexibility for change"
        ],
        "countries": ["Saudi Arabia", "Iran", "Vatican City", "Israel (partially)"]
    },
    {
        "name": "Customary Law",
        "description": "Based on customs and traditions of specific communities.",
        "characteristics": [
            "Oral tradition and community practices",
            "Passed down through generations",
            "Often informal and flexible",
            "Integrated with formal legal systems"
        ],
        "countries": ["Many African nations", "Indigenous communities worldwide", "Tribal regions"]
    }
]

GLOBAL_LEGAL_STATS = {
    "total_countries": 195,
    "common_law_countries": 60,
    "civil_law_countries": 135,
    "religious_law_countries": 25,
    "mixed_system_countries": 40,
    "total_lawyers_worldwide": "10 million+",
    "new_treaties_annually": 100,
    "international_courts": 15
}

def load_training_data():
    try:
        with open('legal_training_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

TRAINING_DATA = load_training_data()

FUNNY_RESPONSES = {
    "hello": "Namaste! 🙏 I'm your legal assistant. Ask me anything about Indian laws!",
    "hi": "Hello! 🙌 Ready to explore the fascinating world of Indian jurisprudence?",
    "hey": "Hey there! ⚖️ What legal conundrum can I help you solve today?",
    "how are you": "I'm just a program, but I'm functioning optimally! 💻 How can I assist you with Indian laws?",
    "what is your name": "I'm the Legal Eagle! 🦅 Your guide through the complex maze of Indian legal system.",
    "who are you": "I'm your friendly legal assistant! 🤖 I know a lot about Indian laws and regulations.",
    "joke": "Why don't lawyers like to go camping? Because they prefer indoor plumbing! 😄",
    "funny": "I'm all about legal humor! Did you know the Indian Penal Code has over 500 sections? That's a lot of laws to keep us in line! 😅",
    "love": "I appreciate your enthusiasm, but I'm programmed to talk about laws, not romance! ❤️‍🔥 Let's discuss something legal instead!",
    "hate": "I understand you might be frustrated, but let's focus on how I can help you with legal matters! ⚖️",
    "goodbye": "See you later! Don't forget to follow the law! 👋",
    "bye": "Bye! Remember, ignorance of the law is no excuse! 😉"
}

def is_legal_question(query):
    legal_keywords = [
        "act", "law", "legal", "court", "judge", "contract", "rights", "duty", "obligation",
        "penal", "code", "constitution", "tax", "company", "business", "property", "sale",
        "consumer", "arbitration", "dispute", "criminal", "civil", "procedure", "evidence",
        "jurisdiction", "appeal", "witness", "defendant", "plaintiff", "accused", "victim",
        "offence", "punishment", "fine", "imprisonment", "bail", "investigation", "indian",
        "constitution", "penal", "contract", "evidence", "transfer", "property", "partnership",
        "consumer", "protection", "information", "technology", "motor", "vehicle", "income",
        "tax", "gst", "goods", "services", "insolvency", "bankruptcy", "arbitration",
        "commercial", "civil", "criminal", "procedure", "minimum", "wages", "factories",
        "industrial", "disputes", "maternity", "benefit", "right", "information", "copyright",
        "patent", "trademark", "competition", "environment", "scheduled", "castes", "tribes",
        "domestic", "violence", "sexual", "harassment", "juvenile", "justice", "money",
        "laundering", "foreign", "exchange", "prevention", "atrocities"
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in legal_keywords)

def is_world_legal_query(query):
    world_keywords = [
        "world", "global", "international", "different countries", "other countries",
        "legal systems worldwide", "world legal systems", "global law", "international law",
        "common law", "civil law", "religious law", "customary law", "legal system types",
        "compare legal systems", "legal systems comparison", "world statistics", "global statistics"
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in world_keywords)

def get_funny_response(query):
    query_lower = query.lower().strip()
    
    if query_lower in FUNNY_RESPONSES:
        return FUNNY_RESPONSES[query_lower]
    
    for key in FUNNY_RESPONSES:
        if key in query_lower:
            return FUNNY_RESPONSES[key]
    
    return "I'm here to help with legal questions, but I appreciate your friendly greeting! 😊 Please ask me something about Indian laws."

def search_corpus(query):
    results = []
    query_lower = query.lower()
    
    for doc in LEGAL_CORPUS:
        if (query_lower in doc["text"].lower() or 
            query_lower in doc["title"].lower() or
            any(word in doc["text"].lower() for word in query_lower.split())):
            results.append(doc)
    
    for item in TRAINING_DATA:
        if (query_lower in item["question"].lower() or 
            query_lower in item["answer"].lower() or
            any(word in item["question"].lower() for word in query_lower.split())):
            results.append({
                "title": f"Q&A: {item['question'][:50]}...",
                "text": f"Question: {item['question']}\nAnswer: {item['answer']}"
            })
    
    return results

def generate_world_legal_response(query):
    query_lower = query.lower()
    
    if "common law" in query_lower:
        system = GLOBAL_LEGAL_SYSTEMS[0]
        return f"**{system['name']} System**\n\n{system['description']}\n\nKey Characteristics:\n" + "\n".join([f"• {char}" for char in system["characteristics"]]) + f"\n\nUsed in countries like: {', '.join(system['countries'][:5])} and others."
    
    elif "civil law" in query_lower:
        system = GLOBAL_LEGAL_SYSTEMS[1]
        return f"**{system['name']} System**\n\n{system['description']}\n\nKey Characteristics:\n" + "\n".join([f"• {char}" for char in system["characteristics"]]) + f"\n\nUsed in countries like: {', '.join(system['countries'][:5])} and others."
    
    elif "religious law" in query_lower:
        system = GLOBAL_LEGAL_SYSTEMS[2]
        return f"**{system['name']} System**\n\n{system['description']}\n\nKey Characteristics:\n" + "\n".join([f"• {char}" for char in system["characteristics"]]) + f"\n\nExamples include: {', '.join(system['countries'][:3])} and others."
    
    elif "customary law" in query_lower:
        system = GLOBAL_LEGAL_SYSTEMS[3]
        return f"**{system['name']} System**\n\n{system['description']}\n\nKey Characteristics:\n" + "\n".join([f"• {char}" for char in system["characteristics"]]) + f"\n\nFound in: {', '.join(system['countries'][:3])} and indigenous communities worldwide."
    
    elif "compare" in query_lower or "difference" in query_lower:
        response = "**Comparison of Global Legal Systems**\n\n"
        for system in GLOBAL_LEGAL_SYSTEMS:
            response += f"**{system['name']}**\n{system['description']}\n\n"
        response += "\nFor detailed comparison, please use the 'Show World Legal Information' feature on the website."
        return response
    
    elif "statistic" in query_lower or "data" in query_lower:
        stats = GLOBAL_LEGAL_STATS
        return f"**Global Legal Statistics**\n\n• Total countries with legal systems: {stats['total_countries']}\n• Common law countries: {stats['common_law_countries']}\n• Civil law countries: {stats['civil_law_countries']}\n• Religious law countries: {stats['religious_law_countries']}\n• Mixed system countries: {stats['mixed_system_countries']}\n• Total lawyers worldwide: {stats['total_lawyers_worldwide']}\n• New international treaties annually: {stats['new_treaties_annually']}\n• International courts: {stats['international_courts']}"
    
    else:
        response = "**Global Legal Systems Overview**\n\n"
        for system in GLOBAL_LEGAL_SYSTEMS:
            response += f"**{system['name']}**: {system['description']}\n\n"
        response += "For detailed information about any specific legal system, please ask about Common Law, Civil Law, Religious Law, or Customary Law."
        return response

def generate_bot_response(user_query, context_docs):
    if is_world_legal_query(user_query):
        return generate_world_legal_response(user_query)
    
    if not is_legal_question(user_query):
        return get_funny_response(user_query)
    
    # Try to use OpenAI API if available
    if openai_available and openai is not None:
        try:
            context = "\n\n".join([f"{doc['title']}: {doc['text']}" for doc in context_docs])
            prompt = (
                "You are an AI legal research assistant specializing in Indian laws with comprehensive knowledge similar to ChatGPT. "
                "Provide detailed, accurate, and comprehensive information. Structure your response in a standardized format:\n"
                "1. Direct Answer: Provide a clear, concise answer to the question\n"
                "2. Legal Framework: Reference relevant acts, sections, and legal principles\n"
                "3. Practical Application: Explain how the law applies in practice\n"
                "4. Key Considerations: Highlight important points or exceptions\n"
                "5. Next Steps: Suggest what actions the user can take\n"
                "6. Additional Resources: Mention related laws or further reading\n"
                "Use formal legal language but ensure clarity. Include section numbers when relevant.\n\n"
                f"Context:\n{context}\n\n"
                f"User Query: {user_query}\n\n"
                "Legal Research Bot (Comprehensive Response):"
            )
            
            try:
                # Try to make the API call
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=800,
                    temperature=0.3,
                    n=1,
                    stop=None
                )
                
                # Process the response
                if isinstance(response, dict) and 'choices' in response:
                    choices = response['choices']
                    if isinstance(choices, list) and len(choices) > 0:
                        choice = choices[0]
                        if isinstance(choice, dict) and 'text' in choice:
                            text = choice['text'].strip()
                            if text:
                                return text
                return "I couldn't generate a response. Please try rephrasing your question."
            except Exception as api_error:
                print(f"OpenAI API error: {api_error}")
                # Fall back to using the context docs
                pass
        except Exception as e:
            print(f"OpenAI API error: {e}")

    # Fallback response when OpenAI is not available or fails
    if context_docs:
        response_parts = []
        for doc in context_docs[:5]:
            response_parts.append(f"**{doc['title']}**\n{doc['text']}\n")
        return "\n".join(response_parts) + "\n\nFor personalized legal advice, please consult with a qualified legal professional."
    else:
        return "I couldn't find specific information about your query in my knowledge base. Please try rephrasing your question or consult with a qualified legal professional."

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "OK"})
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        user_query = data.get("query", "")
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        context_docs = search_corpus(user_query)
        if not context_docs and is_legal_question(user_query) and not is_world_legal_query(user_query):
            context_docs = LEGAL_CORPUS[:7]
            
        bot_response = generate_bot_response(user_query, context_docs)
        
        return jsonify({
            "response": bot_response,
            "sources": [doc["title"] for doc in context_docs[:7]] if context_docs and is_legal_question(user_query) and not is_world_legal_query(user_query) else [],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/")
def index():
    return "AI Legal Research Chatbot Backend is running."

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)