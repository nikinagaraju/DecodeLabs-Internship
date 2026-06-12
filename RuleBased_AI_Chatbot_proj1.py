# ============================================================
#  PROJECT 1 — Rule-Based AI Chatbot
#  DecodeLabs Industrial Training Kit | Batch 2026
#  Built by: AI & ML Engineering Intern
# ============================================================

# ──────────────────────────────────────────────
#  KNOWLEDGE BASE  (Dictionary — O(1) lookup)
# ──────────────────────────────────────────────
responses = {
    # Greetings
    "hello"         : "Hey there! 👋 I'm DecoBot. How can I assist you today?",
    "hi"            : "Hi! Great to see you. What can I help you with?",
    "hey"           : "Hey! I'm here and ready to help. What's up?",
    "good morning"  : "Good morning! ☀️ Hope you're having a productive day!",
    "good afternoon": "Good afternoon! 🌤️ How can I help you right now?",
    "good evening"  : "Good evening! 🌙 What can I do for you tonight?",

    # About the bot
    "who are you"   : "I'm DecoBot 🤖 — a rule-based AI chatbot built for DecodeLabs' Project 1.",
    "what are you"  : "I'm DecoBot, an AI chatbot that uses logic-based rules to respond to you!",
    "what can you do": "I can answer questions, tell jokes, share AI facts, and have a basic conversation with you!",

    # Help
    "help"          : "Sure! Try asking me: 'tell me a joke', 'what is AI', 'what time is it', or just say 'hello'!",

    # AI / Tech facts
    "what is ai"    : "AI (Artificial Intelligence) is the simulation of human intelligence by machines. 🧠",
    "what is ml"    : "Machine Learning is a subset of AI where systems learn from data to improve over time. 📊",
    "what is deep learning": "Deep Learning uses neural networks with many layers to learn complex patterns. 🔬",
    "what is python": "Python is a popular programming language widely used in AI, ML, and data science. 🐍",

    # Fun
    "tell me a joke": "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😄",
    "another joke"  : "Why did the AI go to school? To improve its 'learning' rate! 🎓🤖",
    "fun fact"      : "Fun fact: The term 'Artificial Intelligence' was coined by John McCarthy in 1956! 🤯",

    # Time / Date
    "what time is it": None,   # resolved below
    "what is today"  : None,   # resolved below

    # Motivational
    "motivate me"   : "You're building AI systems — that's incredible! Keep going, one line of code at a time. 🚀",
    "i am tired"    : "Take a short break, drink some water 💧, and come back stronger. You've got this!",
    "i am bored"    : "Let's fix that! Ask me a riddle, a joke, or an AI fact. I'm full of surprises! 🎉",

    # Farewells
    "bye"           : "Goodbye! 👋 It was great chatting with you. See you soon!",
    "goodbye"       : "Take care! Come back anytime you need help. 😊",
    "see you"       : "See you later! Keep learning and building great things! 🌟",
    "thank you"     : "You're welcome! 😊 Is there anything else I can help you with?",
    "thanks"        : "Anytime! Don't hesitate to ask more questions. 🙌",
}


# ──────────────────────────────────────────────
#  HELPER FUNCTIONS  (for dynamic responses)
# ──────────────────────────────────────────────
import datetime 

def _get_time():
    """Returns current time as a string."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now} ⏰"

def _get_date():
    """Returns today's date as a string."""
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today} 📅"

def get_response(clean_input: str) -> str:
    # Handle dynamic responses here
    if clean_input == "what time is it":
        return _get_time()
    if clean_input == "what is today":
        return _get_date()
    
    # Handle static responses from your dictionary
    return responses.get(clean_input, FALLBACK)


# Rebuild dynamic entries after functions are defined
responses["what time is it"] = _get_time()
responses["what is today"]   = _get_date()


# ──────────────────────────────────────────────
#  PHASE 1 — INPUT SANITIZATION
# ──────────────────────────────────────────────
def sanitize(raw_input: str) -> str:
    """Lowercase + strip whitespace for consistent matching."""
    return raw_input.lower().strip()


# ──────────────────────────────────────────────
#  PHASE 2 — PROCESS (Intent Matching)
# ──────────────────────────────────────────────
FALLBACK = "🤔 Hmm, I don't understand that yet. Try asking 'help' to see what I can do!"

def get_response(clean_input: str) -> str:
    """
    O(1) dictionary lookup with fallback.
    Professional approach: responses.get(key, fallback)
    """
    # Refresh time/date on every call so they're always accurate
    if clean_input == "what time is it":
        return _get_time()
    if clean_input == "what is today":
        return _get_date()

    return responses.get(clean_input, FALLBACK)


# ──────────────────────────────────────────────
#  PHASE 3 — OUTPUT (Infinite Loop / Heartbeat)
# ──────────────────────────────────────────────
EXIT_COMMANDS = {"exit", "quit", "stop", "shutdown"}

def run_chatbot():
    print("=" * 55)
    print("  🤖  DecoBot — Rule-Based AI Chatbot  🤖")
    print("  DecodeLabs Industrial Training Kit | 2026")
    print("=" * 55)
    print("  Type 'help' to see what I can do.")
    print("  Type 'exit' / 'quit' to stop the chatbot.")
    print("=" * 55)
    print()

    # ── THE HEARTBEAT: Infinite Loop ──────────────────────
    while True:
        raw_input = input("You: ")           # Phase 1 — raw input
        clean_input = sanitize(raw_input)    # Phase 1 — sanitize

        # EXIT STRATEGY — clean break command
        if clean_input in EXIT_COMMANDS:
            print("DecoBot: Shutting down... Goodbye! 👋 Keep building great things! 🚀")
            print("=" * 55)
            break

        # Phase 2 — process + Phase 3 — output
        reply = get_response(clean_input)
        print(f"DecoBot: {reply}")
        print()


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    run_chatbot()