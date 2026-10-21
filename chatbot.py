
import json
import re
import random
from pathlib import Path
from difflib import SequenceMatcher


# ==========================================================
# DATHEON INTERNSHIP SUPPORT BOT - VERSION 5.0
# Rule-based conversational chatbot
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faqs.json"


# -------------------- FAQ LOADING --------------------

def load_faqs():
    try:
        with FAQ_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("FAQ JSON must contain an object.")

        greetings = data.get("greetings", [])
        faqs = data.get("faqs", [])

        if not isinstance(greetings, list):
            greetings = []

        if not isinstance(faqs, list):
            faqs = []

        valid_greetings = [
            item.strip().lower()
            for item in greetings
            if isinstance(item, str) and item.strip()
        ]

        valid_faqs = []

        for faq in faqs:
            if not isinstance(faq, dict):
                continue

            intent = faq.get("intent", "")
            question = faq.get("question", "")
            answer = faq.get("answer", "")
            keywords = faq.get("keywords", [])

            if not all(
                isinstance(value, str) and value.strip()
                for value in (intent, question, answer)
            ):
                continue

            if not isinstance(keywords, list):
                keywords = []

            valid_faqs.append({
                "intent": intent.strip().lower(),
                "question": question.strip(),
                "answer": answer.strip(),
                "keywords": [
                    item.strip().lower()
                    for item in keywords
                    if isinstance(item, str) and item.strip()
                ],
            })

        return valid_greetings, valid_faqs

    except FileNotFoundError:
        print("Warning: faqs.json was not found.")
    except json.JSONDecodeError as error:
        print(f"Warning: Invalid JSON: {error}")
    except (OSError, ValueError) as error:
        print(f"Warning: Could not load FAQs: {error}")

    return [], []


GREETINGS, FAQS = load_faqs()


# -------------------- NATURAL RESPONSES --------------------

REPLIES = {
    "greeting": [
        "Hello! 😊 How can I help you today?",
        "Good to see you! What would you like to know?",
        "Hey there! I'm ready to help.",
        "Good morning! Hope you're having a good day. What can I help with?",
        "Hi! What's on your mind?",
        "Hello dear! 😊 How may I assist you?"
    ],

    "how_are_you": [
        "I'm doing well, thanks for asking! How are you?",
        "I'm here and ready to help! 😊 How's your day going?",
        "All good on my side! What can I help you with today?",
        "I'm working well, thank you! What would you like to talk about?"
    ],

    "identity": [
        "I'm the Internship Support Bot, a Python-based chatbot demo. "
        "I use programmed rules and a JSON FAQ file to answer questions.",

        "I'm a chatbot, not a human. This version uses Python, regular "
        "expressions, keyword matching and saved FAQs to respond.",

        "You’re chatting with the Internship Support Bot. I can answer "
        "supported questions, but I can't access private student accounts."
    ],

    "conversation": [
        "Of course! 😊 Go ahead, I'm listening.",
        "Absolutely. What would you like to talk about?",
        "Sure! Tell me what's on your mind.",
        "Of course, you can ask me a question. I'll do my best to help.",
        "I'm here to help. What would you like to know?"
    ],

    "pleasant": [
        "It's nice talking to you too! 😊 What can I help you with?",
        "Likewise! I'm glad we can chat.",
        "That's nice of you to say! What shall we talk about?",
        "Glad to chat with you! What would you like to know?",
        "Thank you! I'm happy to help whenever I can."
    ],

    "compliment": [
        "Thank you! 😊 I'm glad I could help.",
        "That's kind of you! Let me know if you need anything else.",
        "I appreciate that! What else can I help you with?",
        "Thanks! I'll do my best to keep helping you."
    ],

    "thanks": [
        "You're very welcome! 😊",
        "Happy to help!",
        "Anytime! Let me know if you have another question.",
        "Glad I could help. Is there anything else you'd like to know?"
    ],

    "no_problem": [
        "No problem at all! 😊 I'm here if you need anything.",
        "That's completely fine. Feel free to come back whenever you need help.",
        "All good! Let me know if another question comes up.",
        "No worries. Have a great day!"
    ],

    "positive": [
        "Great! 😊 What would you like to do next?",
        "Sounds good! How can I help from here?",
        "Perfect. Let me know what you'd like to know next."
    ],

    "negative": [
        "No problem. We can leave it there for now.",
        "That's absolutely fine! I'm here if you need anything later.",
        "Understood. Feel free to ask whenever you want."
    ],

    "farewell": [
        "It was nice chatting with you! Take care and best of luck! 👋",
        "Goodbye! Have a wonderful day, and good luck with your projects!",
        "See you later! Feel free to return whenever you need help.",
        "Take care! Wishing you success with your internship."
    ],

    "help": [
        "Here's what I can help with:\n"
        "• Greetings and general conversation\n"
        "• Internship and organization questions\n"
        "• Project tasks and submission FAQs\n"
        "• Certificate information\n"
        "• Business hours listed in the sample FAQ\n"
        "• My identity and information sources\n\n"
        "Ask in your own words, or type 'bye' to end the chat.",

        "You can ask me about project submission, GitHub, certificates, "
        "internship details, business hours or how I work. "
        "I can also handle everyday greetings and short replies."
    ],

    "unknown": [
        "I want to give you an accurate answer. Could you explain what you mean?",
        "I'm not quite sure I understood that. Could you try asking another way?",
        "Could you add a little detail? I don't want to guess and give you the wrong answer.",
        "I couldn't confidently match that to my available information. "
        "Could you rephrase your question?",
        "I'm happy to help, but I need a little more context to answer correctly."
    ]
}


# -------------------- PATTERNS --------------------

PATTERNS = {
    "exit": (
        r"\b(bye|goodbye|good bye|farewell|"
        r"see you|see ya|take care|talk to you later|"
        r"got to go|have to go|i have to leave)\b"
    ),

    "greeting": (
        r"\b(hello|hey|hi|howdy|"
        r"good morning|good afternoon|good evening|"
        r"good night|morning|afternoon|evening)\b"
    ),

    "how_are_you": (
        r"\b(how are you|how are you doing|"
        r"how have you been|how is it going|"
        r"how's it going|hows it going|"
        r"how are things|are you doing well)\b"
    ),

    "identity": (
        r"\b(are you a bot|are you human|are you a human|"
        r"are you real|are you a real person|"
        r"who are you|what are you|"
        r"are you an ai|are you artificial intelligence|"
        r"what is your name|whats your name|"
        r"who am i talking to)\b"
    ),

    "conversation": (
        r"\b(can i talk to you|can we talk|"
        r"may i talk to you|i want to talk|"
        r"let's talk|lets talk|"
        r"can i ask you something|"
        r"may i ask you something|"
        r"are you there|are you listening)\b"
    ),

    "pleasant": (
        r"\b(glad to (talk|chat|speak|meet)|"
        r"good to (talk|chat|meet|speak)|"
        r"nice to (talk|chat|meet|speak)|"
        r"pleased to (meet|talk|chat)|"
        r"pleasure (talking|meeting|speaking)|"
        r"enjoyed (talking|chatting|meeting)|"
        r"happy to (talk|chat|meet))\b"
    ),

    "thanks": (
        r"\b(thanks|thank you|thankyou|thx|"
        r"many thanks|much appreciated)\b"
    ),

    "compliment": (
        r"\b(you are helpful|you're helpful|"
        r"you are great|you're great|"
        r"you are amazing|you're amazing|"
        r"you are nice|you're nice|"
        r"you helped me|you are the best|"
        r"good job|well done)\b"
    ),

    "no_problem": (
        r"\b(no nothing|nothing else|nothing more|"
        r"no thanks|no thank you|"
        r"that's all|that is all|"
        r"nothing for now|not anything|"
        r"no need|never mind|nevermind|"
        r"leave it|not now|nope)\b"
    ),

    "positive": (
        r"^(yes|yes please|yeah|yep|sure|"
        r"okay|ok|alright|all right|"
        r"sounds good|of course|please do)[!. ]*$"
    ),

    "negative": (
        r"^(no|nope|not really|"
        r"i don't think so|i do not think so)[!. ]*$"
    ),

    "help": (
        r"\b(help|help me|show menu|show options|"
        r"what can you do|what can you help me with|"
        r"how can you help|how may you help|"
        r"how can you assist|available options)\b"
    ),

    "source": (
        r"\b(how do you know|how did you know|"
        r"where did you get|where do you get|"
        r"what is your source|where is your source|"
        r"source of this|source of the information|"
        r"where did this come from|"
        r"how can you confirm|is that official|"
        r"are you sure|where did you learn)\b"
    ),

    "familiar": (
        r"\b(are you familiar|do you know about|"
        r"are you aware of|do you understand|"
        r"tell me about this project|"
        r"explain this project)\b"
    ),

    "organization": (
        r"\b(what is datheon|tell me about datheon|"
        r"about datheon|daitheon|"
        r"datheon organization|who runs datheon|"
        r"who founded datheon|what organization is this|"
        r"which organization|who is behind datheon)\b"
    ),

    "internship": (
        r"\b(what is this internship|"
        r"tell me about the internship|"
        r"internship details|internship program|"
        r"what is the program about|"
        r"what does this internship involve|"
        r"what will i learn|what are the internship tasks)\b"
    ),

    "submission": (
        r"\b(submit|submission|upload|"
        r"turn in|hand in|github repository|"
        r"project submission|submit my task)\b"
    ),

    "certificate": (
        r"\b(certificate|certificates|certificayte|"
        r"certificte|certifcate|certificat|"
        r"credentials|credential|"
        r"certificate status|official certificate)\b"
    ),

    "hours": (
        r"\b(business hours|opening hours|opening time|"
        r"working hours|when are you open|"
        r"when do you close|office timing|office hours)\b"
    ),

    "where": (
        r"\b(where|which page|which section|"
        r"where can i find|where do i find|"
        r"where can i see|where do i see|"
        r"where do i check|how can i check|"
        r"how do i check|from where)\b"
    ),

    "ready": (
        r"\b(my project is ready|"
        r"project is completed|"
        r"i have finished my project|"
        r"i completed my project|"
        r"my task is done)\b"
    )
}


# -------------------- TEXT PROCESSING --------------------

def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[’`]", "'", text)
    text = re.sub(r"\s+", " ", text)
    return text


def correct_typos(text):
    """Correct common known misspellings."""
    corrections = {
        "intrship": "internship",
        "intership": "internship",
        "interrnship": "internship",
        "certificayte": "certificate",
        "certificte": "certificate",
        "certifcate": "certificate",
        "certificat": "certificate",
        "recieve": "receive",
        "recive": "receive",
        "submision": "submission",
        "submmit": "submit",
        "subbmit": "submit",
        "orgnization": "organization",
        "organisaton": "organization",
        "helo": "hello",
        "helllo": "hello",
        "mornig": "morning",
        "thnaks": "thanks",
        "thak": "thank",
        "talkk": "talk",
        "tallk": "talk",
        "wht": "what",
        "hw": "how",
        "plz": "please",
        "pls": "please",
        "u": "you",
        "ur": "your"
    }

    words = text.split()
    return " ".join(corrections.get(word, word) for word in words)


def match(pattern, text):
    return re.search(pattern, text, re.IGNORECASE) is not None


def pick(category):
    return random.choice(REPLIES[category])


def close_word(word, candidates, threshold=0.84):
    """Find a likely spelling match among known words."""
    best_word = None
    best_score = 0

    for candidate in candidates:
        if abs(len(word) - len(candidate)) > 2:
            continue

        score = SequenceMatcher(None, word, candidate).ratio()

        if score > best_score:
            best_word = candidate
            best_score = score

    return best_word if best_score >= threshold else None


def fuzzy_text(text, known_words):
    """Correct a word only when a close known word exists."""
    corrected = []

    for word in text.split():
        if len(word) < 5 or not word.isalpha():
            corrected.append(word)
            continue

        replacement = close_word(word, known_words)

        corrected.append(replacement if replacement else word)

    return " ".join(corrected)


# -------------------- CHATBOT --------------------

class SupportChatbot:

    def __init__(self):
        self.last_topic = None
        self.last_answer = None
        self.last_intents = []
        self.conversation_started = False

        self.known_words = {
            "internship", "certificate", "organization",
            "submission", "project", "business", "hours",
            "greeting", "morning", "afternoon", "evening",
            "hello", "thanks", "talk", "chat", "help",
            "submit", "upload", "official", "information"
        }

        for faq in FAQS:
            self.known_words.update(faq["question"].lower().split())
            for keyword in faq["keywords"]:
                self.known_words.update(keyword.lower().split())

    def find_faqs(self, text):
        """Match FAQ keywords, phrases and question wording."""
        found = []

        for faq in FAQS:
            score = 0

            for keyword in faq["keywords"]:
                keyword = keyword.lower()

                if keyword in text:
                    score = max(score, 4)
                    continue

                # Fuzzy matching is restricted to single words.
                if " " not in keyword:
                    words = re.findall(r"[a-z]+", text)
                    if any(
                        close_word(word, [keyword], 0.86)
                        for word in words
                        if len(word) >= 5
                    ):
                        score = max(score, 2)

            question_words = [
                word for word in re.findall(
                    r"\b[a-z]{4,}\b", faq["question"].lower()
                )
                if word not in {
                    "what", "when", "where", "your", "have",
                    "does", "this", "that", "from", "with",
                    "will", "into", "how", "much"
                }
            ]

            if question_words:
                hits = sum(
                    1 for word in question_words
                    if word in text.split()
                )

                if hits / len(question_words) >= 0.5:
                    score = max(score, 2)

            if score >= 2:
                found.append((score, faq))

        found.sort(key=lambda item: item[0], reverse=True)

        # Return one strongest FAQ per intent.
        unique = {}
        for score, faq in found:
            if faq["intent"] not in unique:
                unique[faq["intent"]] = faq

        return list(unique.values())

    def source_answer(self):
        if self.last_topic:
            faq = next(
                (
                    item for item in FAQS
                    if item["intent"] == self.last_topic
                ),
                None
            )

            if faq:
                return (
                    f"The information I gave about "
                    f"'{faq['question']}' comes from this demo's "
                    "faqs.json file. It isn't a live check of Datheon "
                    "systems, so please verify important details through "
                    "your official program instructions."
                )

        return (
            "My answers come from programmed Python rules and the sample "
            "FAQs in faqs.json. I don't have live access to Datheon systems "
            "or private student records."
        )

    def location_answer(self):
        if self.last_topic == "certificate":
            return (
                "Start by checking your official internship portal for "
                "certificate or credential updates. I can't see your "
                "account, so I can't confirm your personal status."
            )

        if self.last_topic == "project_submission":
            return (
                "Look in your official internship portal for Student "
                "Workspace or project-submission instructions. The exact "
                "page may vary by batch."
            )

        if self.last_topic == "business_hours":
            return (
                "The hours in this demo come from its sample FAQ. "
                "Please confirm the correct timing with the organization."
            )

        return (
            "What are you trying to find: project-submission instructions, "
            "certificate information, or organization details?"
        )

    def faq_answer(self, intent, faq_matches):
        faq = next(
            (item for item in faq_matches if item["intent"] == intent),
            None
        )

        if faq is None:
            faq = next(
                (item for item in FAQS if item["intent"] == intent),
                None
            )

        if faq:
            self.last_topic = intent
            self.last_answer = faq["answer"]
            return faq["answer"]

        return None

    def answer_topic(self, intent, faq_matches):
        if intent == "organization":
            self.last_topic = "organization"
            return (
                "I can share information available in this demo, but the "
                "current FAQ data doesn't establish all facts about "
                "Datheon. I won't guess about its founders, registration "
                "or official status. Please consult verified organizational "
                "materials for those details."
            )

        if intent == "internship":
            self.last_topic = "internship_details"

            answer = self.faq_answer(
                "internship_details", faq_matches
            )

            return answer or (
                "This chatbot can answer the internship questions covered "
                "by its FAQ data. For the actual program's schedule, "
                "deadlines, eligibility and requirements, follow the "
                "official instructions for your batch."
            )

        if intent == "familiar":
            self.last_topic = "internship_details"
            return (
                "I can explain this chatbot project. It is a rule-based "
                "Python program that uses regex, keyword matching and a "
                "JSON FAQ dataset. If you mean the actual Datheon program, "
                "I can only share information available in the configured "
                "FAQs, not private or live program details."
            )

        if intent == "submission":
            answer = self.faq_answer(
                "project_submission", faq_matches
            )

            return answer or (
                "The demo FAQ may contain submission guidance, but I can't "
                "verify your batch's exact process. Check the official "
                "internship portal and follow its current instructions."
            )

        if intent == "certificate":
            answer = self.faq_answer("certificate", faq_matches)

            return answer or (
                "For your certificate status, check your official internship "
                "portal. I can't access your account or confirm when your "
                "certificate will be issued."
            )

        if intent == "hours":
            answer = self.faq_answer("business_hours", faq_matches)

            return answer or (
                "I don't have verified business hours available. Please "
                "check the organization's official information."
            )

        answer = self.faq_answer(intent, faq_matches)
        return answer

    def respond(self, user_input):
        original = normalize(user_input)

        if not original:
            return "I didn't catch that. Could you type something for me?", False

        text = correct_typos(original)
        text = fuzzy_text(text, self.known_words)

        # Find all relevant FAQ intents.
        faq_matches = self.find_faqs(text)
        faq_intents = {faq["intent"] for faq in faq_matches}

        # -------- 1. Exit takes priority --------
        if match(PATTERNS["exit"], text):
            extra = ""

            if match(PATTERNS["pleasant"], text):
                extra = " It was nice talking to you too!"

            self.conversation_started = False
            return pick("farewell") + extra, True

        # -------- 2. Identity --------
        if match(PATTERNS["identity"], text):
            self.last_topic = "identity"
            self.conversation_started = True
            return pick("identity"), False

        # -------- 3. Source of previous answer --------
        if match(PATTERNS["source"], text):
            return self.source_answer(), False

        # -------- 4. Friendly conversation --------
        if match(PATTERNS["how_are_you"], text):
            return pick("how_are_you"), False

        if match(PATTERNS["conversation"], text):
            return pick("conversation"), False

        if match(PATTERNS["pleasant"], text):
            return pick("pleasant"), False

        if match(PATTERNS["thanks"], text):
            return pick("thanks"), False

        if match(PATTERNS["compliment"], text):
            return pick("compliment"), False

        if match(PATTERNS["no_problem"], text):
            return pick("no_problem"), False

        if match(PATTERNS["help"], text) or text in {
            "help", "menu", "options"
        }:
            return pick("help"), False

        # -------- 5. Recognize topics independently --------
        topics = []

        if match(PATTERNS["organization"], text):
            topics.append("organization")

        if match(PATTERNS["internship"], text):
            topics.append("internship")

        if match(PATTERNS["familiar"], text):
            topics.append("familiar")

        if (
            match(PATTERNS["submission"], text)
            and match(
                r"\b(project|task|assignment|github|repository)\b",
                text
            )
        ):
            topics.append("submission")

        if (
            "project_submission" in faq_intents
            and "submission" not in topics
        ):
            topics.append("submission")

        if match(PATTERNS["certificate"], text) or "certificate" in faq_intents:
            topics.append("certificate")

        if match(PATTERNS["hours"], text) or "business_hours" in faq_intents:
            topics.append("hours")

        # Map any other matched FAQ intents to their stored answers.
        known_intents = {
            "project_submission", "certificate", "business_hours",
            "internship_details", "support"
        }

        for intent in faq_intents:
            if intent in known_intents:
                if intent == "project_submission" and "submission" not in topics:
                    topics.append("submission")
                elif intent == "business_hours" and "hours" not in topics:
                    topics.append("hours")
                elif intent == "internship_details" and "internship" not in topics:
                    topics.append("internship")

        # -------- 6. Greeting detection --------
        greeting = match(PATTERNS["greeting"], text)

        # -------- 7. Contextual follow-up --------
        if match(PATTERNS["where"], text) and not topics:
            return self.location_answer(), False

        if text in {
            "yes", "yes please", "sure", "okay", "ok",
            "tell me more", "what next", "and then",
            "what about that", "and what about it"
        }:
            if self.last_topic in {
                "certificate", "project_submission", "business_hours"
            }:
                return self.location_answer(), False

            return "Sure! What would you like me to explain?", False

        # -------- 8. Respond to recognized topics --------
        responses = []

        for topic in topics:
            answer = self.answer_topic(topic, faq_matches)

            if answer and answer not in responses:
                responses.append(answer)

        # Multiple questions: return answers for each distinct topic.
        if responses:
            if greeting:
                responses.insert(0, pick("greeting"))

            self.conversation_started = True
            return "\n\n".join(responses), False

        # -------- 9. Greeting-only messages --------
        if greeting:
            self.conversation_started = True
            return pick("greeting"), False

        # -------- 10. Short conversational replies --------
        if match(PATTERNS["positive"], text):
            if self.last_topic:
                return pick("positive"), False

            return "Great! 😊 What would you like to talk about?", False

        if match(PATTERNS["negative"], text):
            return pick("negative"), False

        # -------- 11. Ready project --------
        if match(PATTERNS["ready"], text):
            self.last_topic = "project_submission"
            return (
                "Well done on completing your project! 🎉 "
                "Would you like help checking your repository or finding "
                "the official submission instructions?",
                False
            )

        # -------- 12. Natural fallback --------
        return pick("unknown"), False


# -------------------- MAIN PROGRAM --------------------

def main():
    bot = SupportChatbot()

    print("=" * 60)
    print("             DATHEON INTERNSHIP SUPPORT BOT")
    print("                       VERSION 5.0")
    print("=" * 60)
    print("Bot: Hello! 👋 I'm your internship support assistant.")
    print("Bot: Ask me about supported FAQs or just say hello.")
    print("Bot: Type 'help' for options or 'bye' to exit.\n")

    if not FAQS:
        print("Notice: No valid FAQs were loaded from faqs.json.\n")

    while True:
        try:
            user_input = input("You: ")
            response, should_exit = bot.respond(user_input)
            print(f"\nBot: {response}\n")

            if should_exit:
                break

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Chat ended. Take care! 👋")
            break

        except Exception as error:
            print(
                "\nBot: Sorry, something went wrong. "
                "Please try asking again.\n"
            )
            print(f"[Debug information: {error}]\n")


if __name__ == "__main__":
    main()
