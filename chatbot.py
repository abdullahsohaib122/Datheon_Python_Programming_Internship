
import json
import re
import random
from pathlib import Path
from difflib import SequenceMatcher


# ============================================================
# Datheon Python Programming Internship
# Task 4: Rule-Based Customer Support Chatbot
# Version: 5.1
# ============================================================


BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faqs.json"


# -------------------- DEFAULT RESPONSES --------------------

REPLIES = {
    "greeting": [
        "Hello! Welcome to the customer support chatbot.",
        "Hi there! How can I help you today?",
        "Hey! Ask me anything about the internship."
    ],
    "how_are_you": [
        "I'm doing great! Thanks for asking.",
        "I'm functioning well and ready to help!"
    ],
    "identity": [
        "I'm a rule-based customer support chatbot built with Python."
    ],
    "conversation": [
        "I'm here to help! What would you like to know?"
    ],
    "pleasant": [
        "Glad to hear that!",
        "That's great!",
        "Happy to help!"
    ],
    "compliment": [
        "Thank you! I'm glad I could help."
    ],
    "thanks": [
        "You're welcome!",
        "Happy to help!",
        "Anytime!"
    ],
    "no_problem": [
        "No problem! Let me know if you need anything else."
    ],
    "positive": [
        "Great! Let me know if you need any further assistance."
    ],
    "negative": [
        "I'm sorry to hear that. Tell me a little more so I can help."
    ],
    "farewell": [
        "Goodbye! Best of luck with your internship.",
        "See you later! Have a great day.",
        "Bye! Feel free to come back whenever you need help."
    ],
    "help": [
        "You can ask me about internship enrollment, FAQs, "
        "business hours, project submission, certificates, "
        "or the chatbot itself."
    ],
    "unknown": [
        "Sorry, I didn't understand that. Could you rephrase it?",
        "I'm not sure about that. Try asking about enrollment, "
        "business hours, project submission, or certificates.",
        "I couldn't find a suitable answer. Please try different wording."
    ]
}


# -------------------- INTENT PATTERNS --------------------

PATTERNS = {
    "exit": (
        r"\b(bye|goodbye|exit|quit|see you|see ya|"
        r"good night|goodbye chatbot)\b"
    ),

    "greeting": (
        r"\b(hi|hello|hey|salam|assalamualaikum|"
        r"good morning|good afternoon|good evening)\b"
    ),

    "how_are_you": (
        r"\b(how are you|how are u|how are things|"
        r"how's it going|how do you feel)\b"
    ),

    "identity": (
        r"\b(who are you|what are you|your name|"
        r"what can you do|tell me about yourself)\b"
    ),

    "conversation": (
        r"\b(let's talk|can we talk|talk to me|"
        r"are you there|anyone there)\b"
    ),

    "pleasant": (
        r"\b(i am fine|i'm fine|i am good|i'm good|"
        r"doing well|all good|great thanks)\b"
    ),

    "thanks": (
        r"\b(thanks|thank you|thx|thank u|many thanks)\b"
    ),

    "compliment": (
        r"\b(good job|well done|you are great|"
        r"you're great|awesome chatbot|nice work)\b"
    ),

    "no_problem": (
        r"\b(no problem|never mind|it's okay|its okay)\b"
    ),

    "positive": (
        r"\b(great|excellent|perfect|sounds good|"
        r"that's good|that is good)\b"
    ),

    "negative": (
        r"\b(not good|bad experience|i am upset|"
        r"i'm upset|disappointed|unhappy)\b"
    ),

    "help": (
        r"\b(help|what can i ask|available commands|"
        r"what do you support|show options)\b"
    ),

    "source": (
        r"\b(source code|show code|your code|"
        r"how were you built|how do you work)\b"
    ),

    "familiar": (
        r"\b(remember me|do you know me|"
        r"do you remember|who am i)\b"
    ),

    "organization": (
        r"\b(datheon|about the company|about the organization|"
        r"who founded|founder|company history|"
        r"official website|is datheon official)\b"
    ),

    "enrollment": (
        r"\b(enroll|enrollment|register|registration|"
        r"sign up|signup|apply|application|join)\b"
        r".{0,70}\b(in|for|to|the|this|your)?\s*"
        r"\b(internship|intern|program|batch|training)\b"
        r"|\b(how|where|when)\b.{0,40}"
        r"\b(join|enroll|register|apply|sign up)\b"
        r".{0,40}\b(internship|program|batch|training)\b"
    ),

    "internship": (
        r"\b(internship|intern|interns|"
        r"program details|internship details)\b"
    ),

    "submission": (
        r"\b(submit|submission|upload|uploaded|"
        r"turn in|hand in|github|repository|repo|"
        r"student workspace|project deadline)\b"
    ),

    "certificate": (
        r"\b(certificate|certification|completion certificate|"
        r"certificate status|when will i get my certificate)\b"
    ),

    "hours": (
        r"\b(business hours|working hours|office hours|"
        r"opening hours|closing time|office timing|"
        r"when are you open|when does the office close)\b"
    ),

    "where": (
        r"\b(where are you|office location|"
        r"address|location|where is the office)\b"
    ),

    "ready": (
        r"\b(my project is ready|project is ready|"
        r"i have completed my project|"
        r"i finished my project|project completed|"
        r"my task is complete|task completed)\b"
    )
}


# -------------------- TYPO CORRECTION --------------------

TYPO_CORRECTIONS = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "plz": "please",
    "pls": "please",
    "thx": "thanks",
    "thanx": "thanks",
    "helo": "hello",
    "helloo": "hello",
    "hii": "hi",
    "heyy": "hey",
    "gladt": "glad",
    "enrolll": "enroll",
    "enrol": "enroll",
    "regster": "register",
    "regist er": "register",
    "aply": "apply",
    "aplly": "apply",
    "internsh ip": "internship",
    "intership": "internship",
    "interrnship": "internship",
    "internhips": "internship",
    "submision": "submission",
    "submisson": "submission",
    "certifcate": "certificate",
    "certficate": "certificate",
    "buisness": "business",
    "houres": "hours",
    "projecct": "project",
    "myprojevct": "myproject",
    "rady": "ready",
    "thier": "their",
    "recieve": "receive",
    "teh": "the",
    "wht": "what",
    "hw": "how",
    "whr": "where",
    "abt": "about",
    "info": "information",
    "asignmnt": "assignment",
    "assignmnt": "assignment",
    "complet": "complete",
    "completd": "completed",
    "cert": "certificate",
    "gud": "good",
    "nic": "nice",
    "awsome": "awesome",
    "bottt": "bot"
}


def normalize_text(text):
    """Normalize user input for reliable pattern matching."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s'-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def correct_typos(text):
    """Correct common spelling mistakes without external libraries."""
    words = text.split()
    corrected_words = []

    for word in words:
        corrected_words.append(TYPO_CORRECTIONS.get(word, word))

    return " ".join(corrected_words)


def fuzzy_text(text):
    """Apply conservative fuzzy matching to common words."""
    words = text.split()
    common_words = [
        "hello",
        "internship",
        "certificate",
        "submission",
        "project",
        "register",
        "enroll",
        "business",
        "hours",
        "ready",
        "thanks",
        "help"
    ]

    corrected = []

    for word in words:
        if word in TYPO_CORRECTIONS:
            corrected.append(TYPO_CORRECTIONS[word])
            continue

        best_match = word
        best_score = 0.0

        if len(word) >= 5:
            for candidate in common_words:
                score = SequenceMatcher(
                    None, word, candidate
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_match = candidate

        if best_score >= 0.84 and best_match != word:
            corrected.append(best_match)
        else:
            corrected.append(word)

    return " ".join(corrected)


# -------------------- LOAD FAQ DATA --------------------

def load_faqs():
    """
    Load FAQ data from faqs.json.

    Expected format:
    {
        "faqs": [
            {
                "keywords": ["hours", "timing"],
                "answer": "Example answer"
            }
        ]
    }
    """
    if not FAQ_FILE.exists():
        print(
            "[Warning] faqs.json was not found. "
            "Built-in responses will still work."
        )
        return []

    try:
        with FAQ_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            faqs = data.get("faqs", [])
        elif isinstance(data, list):
            faqs = data
        else:
            print("[Warning] FAQ file has an invalid structure.")
            return []

        if not isinstance(faqs, list):
            print("[Warning] The 'faqs' field must be a list.")
            return []

        valid_faqs = []

        for item in faqs:
            if not isinstance(item, dict):
                continue

            keywords = item.get("keywords", [])
            answer = item.get("answer", "")

            if (
                isinstance(keywords, list)
                and isinstance(answer, str)
                and answer.strip()
            ):
                valid_faqs.append({
                    "keywords": [
                        str(keyword).lower().strip()
                        for keyword in keywords
                        if str(keyword).strip()
                    ],
                    "answer": answer.strip()
                })

        return valid_faqs

    except json.JSONDecodeError:
        print(
            "[Warning] faqs.json contains invalid JSON. "
            "Please check its format."
        )
        return []

    except OSError as error:
        print(f"[Warning] Could not read FAQ file: {error}")
        return []


# -------------------- FAQ MATCHING --------------------

def find_faqs(text, faqs):
    """Find FAQ answers using keyword matching."""
    matches = []
    normalized = normalize_text(text)

    for faq in faqs:
        keywords = faq.get("keywords", [])
        answer = faq.get("answer", "")

        for keyword in keywords:
            keyword = normalize_text(keyword)

            if not keyword:
                continue

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, normalized):
                matches.append(answer)
                break

    return matches


# -------------------- CHATBOT CLASS --------------------

class SupportChatbot:
    """Rule-based customer support chatbot."""

    def __init__(self):
        self.faqs = load_faqs()
        self.user_name = None
        self.message_count = 0

    @staticmethod
    def pick(intent):
        """Return a random response for an intent."""
        return random.choice(REPLIES[intent])

    def answer_topic(self, topic, user_text):
        """Answer topic-specific questions."""

        if topic == "enrollment":
            return (
                "For internship enrollment, check the official "
                "program announcement or instructions provided "
                "by your internship coordinator. Follow the stated "
                "registration process and submit accurate details. "
                "I don't have a verified registration link, so I "
                "won't invent one."
            )

        if topic == "organization":
            return (
                "I'm configured to answer questions related to the "
                "Datheon Python Programming Internship task. I don't "
                "have verified information about the organization's "
                "founders, full history, or official registration status. "
                "Please consult its official materials for confirmation."
            )

        if topic == "internship":
            return (
                "This chatbot is designed for internship-related "
                "questions, including enrollment, assignments, "
                "project submission, and certificates. Ask me about "
                "any of these topics."
            )

        if topic == "submission":
            return (
                "The sample FAQ for this project says to submit "
                "your project through a public GitHub repository "
                "using the Student Workspace. Check your actual "
                "internship instructions to confirm the required "
                "submission method and deadline."
            )

        if topic == "certificate":
            return (
                "The sample FAQ says certificates are issued "
                "3–5 business days after code review. This is "
                "sample project data, not a verified Datheon policy. "
                "For your actual certificate status, contact your "
                "internship coordinator."
            )

        if topic == "hours":
            return (
                "The sample FAQ lists business hours as Monday "
                "to Friday, 9:00 AM–6:00 PM IST. Please verify "
                "these times against the actual organization's "
                "official information."
            )

        if topic == "where":
            return (
                "I don't have a verified office address. Please "
                "check the organization's official website or "
                "internship communication for its location."
            )

        if topic == "source":
            return (
                "I'm a Python rule-based chatbot. I use regular "
                "expressions, keyword matching, typo correction, "
                "and FAQ data loaded from a JSON file to generate "
                "responses."
            )

        if topic == "familiar":
            return (
                "I can use information from our current conversation, "
                "but I don't automatically know your identity or "
                "remember personal details across separate sessions."
            )

        if topic == "ready":
            if re.search(
                r"\b(submit|submission|upload|github|repo|"
                r"student workspace|where|how)\b",
                user_text
            ):
                return (
                    "Great! If your project is ready, review your "
                    "internship instructions, check that your GitHub "
                    "repository contains the required files, and "
                    "follow the official submission process."
                )

            return (
                "Great! Your project is ready. Before submitting, "
                "test your code, check for errors, include a README, "
                "and follow the internship's official submission "
                "instructions."
            )

        return None

    def detect_intents(self, text):
        """Detect all matching intents in normalized input."""
        detected = []

        for intent, pattern in PATTERNS.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                detected.append(intent)

        return detected

    def respond(self, user_input):
        """Generate a response and an exit flag."""
        original = user_input.strip()

        if not original:
            return "Please type a message so I can help.", False

        self.message_count += 1

        normalized = normalize_text(original)
        corrected = correct_typos(normalized)
        corrected = fuzzy_text(corrected)
        corrected = normalize_text(corrected)

        # Exit has priority, avoiding duplicate farewell messages.
        if re.fullmatch(
            r"(bye|goodbye|exit|quit|see you|see ya|"
            r"good night|goodbye chatbot)",
            corrected
        ):
            return self.pick("farewell"), True

        intents = self.detect_intents(corrected)

        # Handle project readiness before general FAQ topics.
        if "ready" in intents:
            return self.answer_topic("ready", corrected), False

        # Enrollment should take priority over general internship.
        topic_priority = [
            "enrollment",
            "submission",
            "certificate",
            "hours",
            "where",
            "organization",
            "source",
            "familiar",
            "internship"
        ]

        for topic in topic_priority:
            if topic in intents:
                response = self.answer_topic(topic, corrected)

                if response:
                    return response, False

        # Search the loaded FAQ dataset.
        faq_matches = find_faqs(corrected, self.faqs)

        if faq_matches:
            return faq_matches[0], False

        # Handle social and conversational intents.
        conversational_priority = [
            "how_are_you",
            "identity",
            "greeting",
            "thanks",
            "compliment",
            "no_problem",
            "pleasant",
            "negative",
            "positive",
            "conversation",
            "help"
        ]

        for intent in conversational_priority:
            if intent in intents:
                return self.pick(intent), False

        return self.pick("unknown"), False

    def run(self):
        """Start the interactive chatbot."""
        print("=" * 58)
        print("  DATHEON INTERNSHIP SUPPORT CHATBOT - VERSION 5.1")
        print("=" * 58)
        print("Hello! I'm your Python-based support chatbot.")
        print("Type 'help' to see topics you can ask about.")
        print("Type 'bye', 'exit', or 'quit' to end the chat.")
        print("-" * 58)

        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print("\nBot:", self.pick("farewell"))
                break

            response, should_exit = self.respond(user_input)
            print("Bot:", response)

            if should_exit:
                print("-" * 58)
                print(
                    f"Chat ended. Messages received: "
                    f"{self.message_count}"
                )
                break


# -------------------- PROGRAM ENTRY POINT --------------------

def main():
    chatbot = SupportChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
