import datetime
import re
import time
import random

EXIT_WORDS = ["quit", "bye", "see you next time", "see you later", "see you soon", "allah hafiz", "exit", "goodbye"]

# Store conversation context
conversation_context = {
    "last_question": None,
    "last_topic": None,
    "waiting_for_goal": False,
    "waiting_for_course": False
}


# ============================================
# HELPER FUNCTIONS
# ============================================
def show_typing_effect():
    """Simulate a human typing/thinking before replying."""
    print("Bot is typing", end="", flush=True)
    for _ in range(random.randint(3, 5)):
        time.sleep(random.uniform(0.4, 0.7))
        print(".", end="", flush=True)
    # small random pause, like someone pausing to think before hitting send
    time.sleep(random.uniform(0.3, 0.8))
    print()


def contains_any(text, keywords):
    """True if any keyword appears anywhere inside text."""
    return any(word in text for word in keywords)


def contains_any_partial(text, keywords):
    """True if any keyword partially matches (for typos)."""
    text_lower = text.lower()
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in text_lower:
            return True
        words = text_lower.split()
        for word in words:
            if len(word) > 3 and (keyword_lower in word or word in keyword_lower):
                return True
            if len(word) > 3 and len(keyword_lower) > 3:
                common = len(set(word) & set(keyword_lower))
                if common / max(len(word), len(keyword_lower)) > 0.6:
                    return True
    return False


def get_time_based_greeting(name):
    present_hour = datetime.datetime.now().hour
    if 5 <= present_hour <= 12:
        time_greeting = "Good Morning"
    elif 12 < present_hour <= 17:
        time_greeting = "Good Afternoon"
    elif 17 < present_hour <= 21:
        time_greeting = "Good Evening"
    else:
        time_greeting = "Good Night"
    return f"{time_greeting}, {name}! 👋 I'm here from The Net Rider, happy to help with courses, fees, enrollment, whatever you need!"


def get_course_suggestion():
    """Return a helpful course suggestion."""
    return ("Here are some popular courses: 🌟\n"
            "- AI Digital Marketing\n"
            "- Web Development\n"
            "- Graphic Designing\n"
            "- Cyber Security\n"
            "- Shopify & E-Commerce\n"
            "- Freelancing Masterclasses\n\n"
            "Which one interests you? I can tell you more! 😊")


# ============================================
# HANDLE GOAL RESPONSES (1-6)
# ============================================
def handle_goal_number(userchat):
    """Handle number responses for goals (1-6)."""
    userchat = userchat.strip()
    
    # Goal 1: Earn Online
    if userchat in ["1", "1.", "earn online", "earn"]:
        return ("Great choice! To earn online, here are the best courses: 🎯 💡\n\n"
                "1. Freelancing Masterclasses (Fiverr, Upwork) - Start earning from day one\n"
                "2. AI Digital Marketing - In-demand skills with AI tools\n"
                "3. Shopify / E-Commerce - Build and launch online stores\n"
                "4. SEO Mastery - Rank content and generate leads\n"
                "5. Video Editing & Animation - High-demand content creation\n\n"
                "These skills allow earning PKR + USD from anywhere in Pakistan!\n\n"
                "Which one interests you the most? I can tell you more!")
    
    # Goal 2: Get a Job
    elif userchat in ["2", "2.", "get a job", "job"]:
        return ("Great choice! To get a job, here are the best courses: 🚀 🔥\n\n"
                "1. Web Development / MERN Stack - High demand skills\n"
                "2. Cyber Security - Critical need in every organization\n"
                "3. App Development - Mobile is the future\n"
                "4. Graphic Designing - Creative roles everywhere\n"
                "5. Microsoft Azure Cloud - Cloud skills are gold\n\n"
                "These skills are what employers are actively hiring for in 2026!\n\n"
                "Which one would you like to learn more about?")
    
    # Goal 3: Start a Business
    elif userchat in ["3", "3.", "start a business", "business"]:
        return ("Great choice! To start a business, here are the best courses: 📚 ✍️\n\n"
                "1. AI Digital Marketing - Grow your online presence\n"
                "2. SEO & Social Media Marketing - Attract more customers\n"
                "3. Shopify / E-Commerce - Launch your online store\n"
                "4. GoHighLevel CRM - Automate your entire business\n"
                "5. AI-based Business Solutions - Stay ahead of competitors\n\n"
                "These courses help you grow and manage your business online!\n\n"
                "Would you like details about any specific course?")
    
    # Goal 4: Freelance
    elif userchat in ["4", "4.", "freelance", "freelancer"]:
        return ("Great choice! To freelance, here are the best courses: 💼 📈\n\n"
                "1. Freelancing Masterclasses - Fiverr & Upwork mastery\n"
                "2. Graphic Designing - Most requested freelance skill\n"
                "3. SEO & Digital Marketing - Sell your services globally\n"
                "4. Video Editing - Always in demand\n"
                "5. Web Development - High-value projects\n\n"
                "These are the most requested skills on freelance platforms!\n\n"
                "Which one matches your interest?")
    
    # Goal 5: Future Skills
    elif userchat in ["5", "5.", "future skills", "future"]:
        return ("Great choice! For future-ready skills, here are the best courses: 🌟 👍\n\n"
                "1. AI Academia - AI Fundamentals, ML, Deep Learning\n"
                "2. AI Chatbots & Agents - Build intelligent systems\n"
                "3. AI Industrial Applications - Industry 4.0 skills\n"
                "4. Cisco / MikroTik Certification - Network of the future\n"
                "5. Microsoft Azure - Cloud is the new normal\n\n"
                "These skills will keep you ahead for the next 10+ years!\n\n"
                "Tell me which one excites you the most!")
    
    # Goal 6: Beginner Friendly
    elif userchat in ["6", "6.", "beginner", "beginner friendly"]:
        return ("Great choice! For beginners, here are the best courses: 💻 🖥️\n\n"
                "1. AI Digital Marketing - Learn practical marketing with AI\n"
                "2. Artificial Intelligence Fundamentals - Build your AI foundation\n"
                "3. Spoken English Training - Communication is key\n"
                "4. Graphic Designing - Start creative from day one\n"
                "5. Web Development - Coding from basics\n\n"
                "All courses are designed to be beginner-friendly with expert guidance!\n\n"
                "Which one would you like to start with?")
    
    return None


# ============================================
# HANDLE "YES" RESPONSES WITH CONTEXT
# ============================================
def handle_yes_response():
    """Handle 'yes' responses based on conversation context."""
    global conversation_context

    if conversation_context.get("waiting_for_goal"):
        conversation_context["waiting_for_goal"] = False
        return ("Great! Let me help you find the perfect course! 🎨 🖌️\n\n"
                "What's your main goal?\n\n"
                "1. Earn Online - Make money through freelancing or digital skills\n"
                "2. Get a Job - Build skills employers are hiring for\n"
                "3. Start a Business - Learn to grow your own venture\n"
                "4. Freelance - Work independently with global clients\n"
                "5. Future Skills - Stay ahead with AI and emerging tech\n"
                "6. Beginner Friendly - Start from scratch with no experience\n\n"
                "Reply with a number (1-6) or tell me your goal in your own words!")

    elif conversation_context.get("last_question") == "specific_course":
        course = conversation_context.get("last_course")
        conversation_context["last_question"] = None
        if course:
            return f"Great choice! 🎯 Here's more about {course}: ✨\n\n" + get_course_details(course)
        else:
            return get_course_suggestion()

    elif conversation_context.get("last_question") == "categorize_courses":
        conversation_context["last_question"] = "beginner_offer"
        return ("Best Courses for Beginners 🛒 💳\n\n"
                "If you're new to tech, start with these:\n\n"
                "1. AI Digital Marketing - Learn practical marketing with AI tools\n"
                "2. Artificial Intelligence Fundamentals - Build your AI foundation\n"
                "3. Spoken English Training - Improve communication skills\n"
                "4. Web Development - Start coding from basics\n"
                "5. Graphic Designing - Creative skills with practical tools\n\n"
                "These build a strong foundation before moving to specialized courses.\n\n"
                "Want me to suggest the best course for your goals? Just tell me what you want to achieve!")

    elif conversation_context.get("last_question") == "beginner_offer":
        conversation_context["waiting_for_goal"] = True
        conversation_context["last_question"] = "goal"
        return ("Great! Let me help you find the perfect course! 📱 📲\n\n"
                "What's your main goal?\n\n"
                "1. Earn Online - Make money through freelancing or digital skills\n"
                "2. Get a Job - Build skills employers are hiring for\n"
                "3. Start a Business - Learn to grow your own venture\n"
                "4. Freelance - Work independently with global clients\n"
                "5. Future Skills - Stay ahead with AI and emerging tech\n"
                "6. Beginner Friendly - Start from scratch with no experience\n\n"
                "Reply with a number (1-6) or tell me your goal in your own words!")

    elif conversation_context.get("last_question") == "enroll":
        return ("Ready to enroll? Here's how: 🎓 🏆\n\n"
                "1. Online: Visit thenetrider.com\n"
                "2. Call/WhatsApp: 0333 999 1018\n"
                "3. Visit Campus: Peer Khursheed Colony Road, Multan\n\n"
                "Students from all Pakistani cities can join online!\n"
                "Want to know about fees first? Just ask!")

    elif conversation_context.get("last_question") == "more_info":
        return ("Here's what else I can tell you about: 📞 ☎️\n\n"
                "- Course details - What you'll learn in each course\n"
                "- Trainers - Who teaches the courses\n"
                "- Student testimonials - What our students say\n"
                "- Certificates - What you get after completion\n"
                "- Fee structure - Cost of each course\n\n"
                "Just ask me about any of these!")

    else:
        return ("Great! I'm here to help! 🕒 📅\n\n"
                "You can ask me about:\n"
                "- Courses - 'What courses do you offer?'\n"
                "- Enrollment - 'How do I join?'\n"
                "- Fees - 'What are the fees?'\n"
                "- Location - 'Where are you located?'\n"
                "- Testimonials - 'What do students say?'\n"
                "- Recommendations - 'What course is best for me?'\n\n"
                "Just type what you want to know!")


def get_course_details(course_name):
    """Get detailed information about a specific course."""
    course_name = course_name.lower()
    
    if "digital marketing" in course_name or "ai marketing" in course_name:
        return ("AI Digital Marketing Course 📝 ✅\n\n"
                "Learn practical, industry-ready skills:\n"
                "- AI-Based SEO strategies\n"
                "- Social Media Marketing (all platforms)\n"
                "- Marketing Funnels\n"
                "- Google Ads & TikTok Agency setup\n"
                "- AI Tools: Manus AI, Buffer, Semrush, Elementor, Rank Math\n"
                "- Content creation with AI\n"
                "- Client handling & real project work\n\n"
                "AI = Dollar Earning Opportunities\n\n"
                "Available: On-Campus & Online nationwide")
    
    elif "web" in course_name or "development" in course_name or "mern" in course_name:
        return ("Web Development / MERN Stack Course 🙌 😄\n\n"
                "Full stack development training:\n"
                "- MongoDB - Express.js - React.js - Node.js\n"
                "- Modern web & app development\n"
                "- Project-based learning\n"
                "- Professional portfolio building\n\n"
                "High demand skills for job market and freelancing!\n\n"
                "Available: On-Campus & Online")
    
    elif "cyber" in course_name or "security" in course_name:
        return ("Cyber Security Course 🌐 🔗\n\n"
                "Secure systems like a pro:\n"
                "- Ethical hacking techniques\n"
                "- Cyber defense strategies\n"
                "- Real security tools\n"
                "- Practical attack & defense scenarios\n\n"
                "One of the most in-demand IT skills!\n\n"
                "Available: On-Campus & Online")
    
    elif "graphic" in course_name or "design" in course_name:
        return ("Graphic Designing Course 💰 💵\n\n"
                "Craft impactful visuals:\n"
                "- Professional design tools\n"
                "- Design industry experts instruction\n"
                "- Hands-on projects\n"
                "- Portfolio development\n\n"
                "Available: On-Campus & Online")
    
    elif "shopify" in course_name or "ecommerce" in course_name:
        return ("Shopify Store Creation & E-Commerce Course 🤝 🙂\n\n"
                "Master the go-to skill for local e-commerce and global dropshipping:\n"
                "- Complete Shopify store setup\n"
                "- Product sourcing & management\n"
                "- SEO for e-commerce\n"
                "- Marketing & sales strategies\n\n"
                "Accessible online nationwide across Pakistan!")
    
    elif "freelance" in course_name or "fiverr" in course_name or "upwork" in course_name:
        return ("Freelancing Masterclasses 📌 🔎\n\n"
                "Learn to earn online:\n"
                "- Fiverr & Upwork mastery\n"
                "- Client acquisition strategies\n"
                "- Profile optimization\n"
                "- Proposal writing & bidding\n"
                "- Project management\n\n"
                "Skills that allow earning PKR + USD from anywhere in Pakistan!")
    
    elif "video" in course_name or "animation" in course_name:
        return ("Video Editing & Animation Course 😊 ✨\n\n"
                "Create stunning content:\n"
                "- Professional editing tools\n"
                "- AI tools for animation\n"
                "- Step-by-step practice\n"
                "- Portfolio building\n\n"
                "Available: On-Campus & Online")
    
    elif "generative" in course_name:
        return ("Generative AI Course 🎯 💡\n\n"
                "Learn AI Tools, Prompt Engineering, Content Generation & Automation:\n"
                "- Working with leading generative AI tools\n"
                "- Prompt engineering fundamentals\n"
                "- AI-powered content generation\n"
                "- Automating creative and business workflows\n\n"
                "Part of our New Session starting 13th July 2026!\n\n"
                "Available: On-Campus & Online")

    elif "ccna" in course_name:
        return ("CCNA Course 🚀 🔥\n\n"
                "Build networking skills and get CCNA certified:\n"
                "- IP addressing, routing, and subnetting\n"
                "- Cisco Packet Tracer hands-on practice\n"
                "- Network troubleshooting\n"
                "- Official CCNA certification prep\n\n"
                "Available: On-Campus & Online")

    elif "autocad" in course_name:
        return ("AutoCAD Course 📚 ✍️\n\n"
                "Learn 2D Drafting & 3D Designing like a pro:\n"
                "- AutoCAD, 3ds Max, and VRay\n"
                "- Architectural drafting and design\n"
                "- 2D and 3D modeling techniques\n\n"
                "Available: On-Campus & Online")

    elif "ai agent" in course_name or "automation" in course_name:
        return ("AI Agents & Automation Course 💼 📈\n\n"
                "Build intelligent AI agents and automate real-world tasks:\n"
                "- Designing autonomous AI agents\n"
                "- Workflow automation\n"
                "- Real-world task automation with AI\n\n"
                "Available: On-Campus & Online")

    else:
        return ("That's a great course choice! 🌟 👍\n\n"
                "For full details, please contact us:\n"
                "- 0333 999 1018\n"
                "- thenetrider.com\n\n"
                "Or ask me about another course!")


# ============================================
# MAIN CHATBOT RESPONSE FUNCTION
# ============================================
def chatbot_response(userchat):
    global conversation_context
    
    userchat = userchat.lower().strip()
    
    # Handle "YES" responses first
    if contains_any(userchat, ["yes", "yeah", "sure", "yep", "ok", "okay", "alright", "absolutely", "definitely", "of course", "yup"]):
        return handle_yes_response()
    
    # Handle goal numbers (1-6) - THIS IS THE KEY FIX
    if conversation_context.get("waiting_for_goal"):
        goal_response = handle_goal_number(userchat)
        if goal_response:
            conversation_context["waiting_for_goal"] = False
            return goal_response
    
    # GREETINGS & INTRODUCTIONS
    if contains_any(userchat, ["hello", "hi", "hey", "salam", "assalam", "howdy"]):
        conversation_context["last_question"] = None
        return "Hey! 👋 I'm The Net Rider assistant. How can I help you today? Try asking about courses, fees, or enrollment! 😊"
    
    elif contains_any(userchat, ["how are you", "how r u", "hru", "how do you do"]):
        conversation_context["last_question"] = None
        return "I'm doing great, thank you! 😄 Always happy to help. What would you like to know about The Net Rider? 🎯"
    
    elif contains_any(userchat, ["your name", "who are you", "introduce yourself", "who is this"]):
        conversation_context["last_question"] = None
        return "I'm The Net Rider's AI chatbot assistant! 🤖✨ Ask me about courses, trainers, fees, or anything about our training programs!"
    
    # ABOUT THE NET RIDER & FOUNDER
    elif contains_any(userchat, ["who founded", "founder", "who started", "who owns", "humayun", "babar"]):
        conversation_context["last_question"] = None
        return ("The Net Rider was founded by Humayun Khan Babar in 2007 in Multan, Pakistan. 💻 🖥️\n\n"
                "He is a recognized AI trainer, Digital Marketing Expert, Network Engineer, "
                "and youth mentor who has trained thousands of students across Pakistan.\n\n"
                "He's also the Founder & CEO of AI Market Minds Agency.")
    
    elif contains_any(userchat, ["what is net rider", "about net rider", "tell me about net rider", "what is tnr"]):
        conversation_context["last_question"] = None
        return ("The Net Rider is a leading AI-based Tech Training Institute and Software House 🚀 "
                "founded in 2007 in Multan, Pakistan.\n\n"
                "We provide advanced skills training in:\n"
                "- AI & Automation\n"
                "- Digital Marketing\n"
                "- Shopify & E-Commerce\n"
                "- Web Development & Coding\n"
                "- Networking & Cyber Security\n"
                "- Freelancing & Online Earning\n\n"
                "Empowering Minds with Future-Ready AI Skills ✨")
    
    # TRAINING MODES
    elif contains_any(userchat, ["training", "mode", "how to study", "learning options", "class types", "on campus", "online", "weekend"]):
        conversation_context["last_question"] = None
        return ("The Net Rider offers 3 flexible training modes: 🎨 🖌️\n\n"
                "On-Campus Training\n"
                "- Hands-on practical sessions\n"
                "- Real experience with expert guidance\n"
                "- Located at Peer Khursheed Colony Road, Multan\n\n"
                "Online Learning\n"
                "- Live Zoom classes nationwide\n"
                "- Recorded lectures for revision\n"
                "- 24/7 support for students from any city\n\n"
                "Weekend Classes\n"
                "- Flexible sessions designed for your convenience\n"
                "- Perfect for working professionals and students\n\n"
                "Which mode interests you?")
    
    # COURSES - GENERAL
    elif contains_any(userchat, ["course", "courses", "what do you teach", "programs", "offerings", "available courses"]):
        conversation_context["last_question"] = "categorize_courses"
        return ("The Net Rider offers 25+ professional courses across multiple domains: 🔒 🛡️\n\n"
                "AI & Tech Core\n"
                "- AI Academia / AI Fundamentals\n"
                "- AI Industrial Applications\n"
                "- AI Chatbots & Agents\n"
                "- AI Digital Marketing\n"
                "- GoHighLevel CRM\n"
                "- Sales Navigator LinkedIn\n\n"
                "Web & Design\n"
                "- Web Development\n"
                "- App Development\n"
                "- MERN Stack Development\n"
                "- Graphic Designing\n"
                "- Figma & UI/UX Design\n"
                "- Blender 3D\n"
                "- Architecture with AI\n\n"
                "Business & E-Commerce\n"
                "- Shopify Store Creation\n"
                "- Digital Marketing & SEO\n"
                "- Social Media Marketing\n"
                "- YouTube Automation\n"
                "- Freelancing Masterclasses\n\n"
                "IT & Certification\n"
                "- Cyber Security\n"
                "- Cisco Networking\n"
                "- MikroTik Certification\n"
                "- Microsoft Azure Cloud\n\n"
                "Content & Media\n"
                "- Video Editing\n"
                "- Cartoon Animation\n"
                "- Embroidery Digitizing\n\n"
                "If you want, I can also list the best courses for beginners.")
    
    # POPULAR COURSES - SETS "waiting_for_goal" FLAG
    elif contains_any(userchat, ["popular", "best", "top", "most popular", "recommended"]):
        conversation_context["waiting_for_goal"] = True
        conversation_context["last_question"] = "goal"
        return ("Most Popular Courses at The Net Rider: 🛒 💳\n\n"
                "1. AI Digital Marketing - Learn AI-based SEO, Social Media Marketing, Funnels, Google Ads, TikTok Agency setup, and tools like Manus AI, Buffer, Semrush, Elementor, Rank Math\n\n"
                "2. GoHighLevel CRM - Build sales funnels, marketing automations, client prospecting, and reputation management\n\n"
                "3. AI Chatbots & Agents - Build intelligent AI systems for client acquisition and workflow automation\n\n"
                "4. Cyber Security - Learn ethical hacking and cyber defense\n\n"
                "5. Web Development / MERN Stack - Full stack development skills\n\n"
                "6. Shopify & E-Commerce - Build and launch online stores\n\n"
                "Want me to suggest the best course for your goals? Just tell me what you want to achieve!")
    
    # GOAL-BASED RECOMMENDATIONS (direct trigger without saying "popular" first)
    elif contains_any(userchat, ["goal", "earn online", "get a job", "start a business", "freelance", "future skills", "beginner"]):
        conversation_context["waiting_for_goal"] = True
        conversation_context["last_question"] = "goal"
        return ("Great! Let me help you find the perfect course! 📱 📲\n\n"
                "What's your main goal?\n\n"
                "1. Earn Online - Make money through freelancing or digital skills\n"
                "2. Get a Job - Build skills employers are hiring for\n"
                "3. Start a Business - Learn to grow your own venture\n"
                "4. Freelance - Work independently with global clients\n"
                "5. Future Skills - Stay ahead with AI and emerging tech\n"
                "6. Beginner Friendly - Start from scratch with no experience\n\n"
                "Reply with a number (1-6) or tell me your goal in your own words!")
    
    # SPECIFIC COURSE DETAILS
    # AI Digital Marketing
    elif contains_any_partial(userchat, ["ai digital marketing", "digital marketing", "ai marketing", "marketing course"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "AI Digital Marketing"
        return ("AI Digital Marketing Course at The Net Rider 🎓 🏆\n\n"
                "Learn practical, industry-ready skills:\n"
                "- AI-Based SEO strategies\n"
                "- Social Media Marketing (all platforms)\n"
                "- Marketing Funnels\n"
                "- Google Ads & TikTok Agency setup\n"
                "- AI Tools: Manus AI, Buffer, Semrush, Elementor, Rank Math\n"
                "- Content creation with AI\n"
                "- Client handling & real project work\n\n"
                "AI = Dollar Earning Opportunities\n\n"
                "Available: On-Campus & Online nationwide\n\n"
                "Students are successfully working with real clients worldwide!\n\n"
                "Would you like to know more about this course?")
    
    # Generative AI
    elif contains_any_partial(userchat, ["generative ai", "gen ai", "prompt engineering"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Generative AI"
        return ("Generative AI Course at The Net Rider 📞 ☎️\n\n"
                "Learn AI Tools, Prompt Engineering, Content Generation & Automation:\n"
                "- Working with leading generative AI tools\n"
                "- Prompt engineering fundamentals\n"
                "- AI-powered content generation\n"
                "- Automating creative and business workflows\n\n"
                "Part of our New Session starting 13th July 2026!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")

    # CCNA
    elif contains_any_partial(userchat, ["ccna", "networking certification"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "CCNA"
        return ("CCNA Course at The Net Rider 🕒 📅\n\n"
                "Build networking skills and get CCNA certified:\n"
                "- IP addressing, routing, and subnetting\n"
                "- Cisco Packet Tracer hands-on practice\n"
                "- Network troubleshooting\n"
                "- Official CCNA certification prep\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")

    # AutoCAD
    elif contains_any_partial(userchat, ["autocad", "2d drafting", "3d designing", "cad course"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "AutoCAD"
        return ("AutoCAD Course at The Net Rider 📝 ✅\n\n"
                "Learn 2D Drafting & 3D Designing like a pro:\n"
                "- AutoCAD, 3ds Max, and VRay\n"
                "- Architectural drafting and design\n"
                "- 2D and 3D modeling techniques\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")

    # AI Agents & Automation
    elif contains_any_partial(userchat, ["ai agents", "ai agent", "ai automation", "automate real-world tasks"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "AI Agents & Automation"
        return ("AI Agents & Automation Course at The Net Rider 🙌 😄\n\n"
                "Build intelligent AI agents and automate real-world tasks:\n"
                "- Designing autonomous AI agents\n"
                "- Workflow automation\n"
                "- Real-world task automation with AI\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")

    # SEO
    elif contains_any_partial(userchat, ["seo", "search engine", "ranking", "google ranking"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "SEO Mastery"
        return ("SEO Mastery Course 🌐 🔗\n\n"
                "Master search engine strategies:\n"
                "- On-page & off-page SEO\n"
                "- Keyword research\n"
                "- Rank Math & SEO tools\n"
                "- Content optimization\n"
                "- Local & global SEO strategies\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Social Media Marketing
    elif contains_any_partial(userchat, ["social media", "smm", "social marketing", "facebook", "instagram", "tiktok"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Social Media Marketing"
        return ("Social Media Marketing Course 💰 💵\n\n"
                "Boost online presence:\n"
                "- All platform strategies (Facebook, Instagram, TikTok, LinkedIn)\n"
                "- Content creation & planning\n"
                "- Engagement & growth tactics\n"
                "- Paid advertising basics\n"
                "- Analytics & reporting\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # GoHighLevel
    elif contains_any_partial(userchat, ["gohighlevel", "ghl", "crm", "funnel", "automation"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "GoHighLevel CRM"
        return ("GoHighLevel (GHL) CRM Course 🤝 🙂\n\n"
                "Master the all-in-one marketing platform:\n"
                "- Build professional sales funnels\n"
                "- Marketing automations\n"
                "- CRM management\n"
                "- AI agents for client acquisition\n"
                "- Social media & email marketing\n"
                "- Reputation management\n"
                "- Client prospecting systems\n\n"
                "Students work on real client projects during training!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Chatbots / Agents
    elif contains_any_partial(userchat, ["chatbot", "agent", "agentic", "ai agent", "automation"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "AI Chatbots & Agents"
        return ("AI Chatbots & Agentic Systems Course 📌 🔎\n\n"
                "Build intelligent AI systems to:\n"
                "- Automate workflows\n"
                "- Acquire clients automatically\n"
                "- Grow businesses faster\n"
                "- Create AI agents for various industries\n\n"
                "This is one of the most in-demand skills for 2026!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Sales Navigator
    elif contains_any_partial(userchat, ["sales navigator", "linkedin", "b2b", "lead generation", "outreach"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Sales Navigator LinkedIn"
        return ("Sales Navigator LinkedIn Course 😊 ✨\n\n"
                "Build a powerful B2B client acquisition system:\n"
                "- LinkedIn Sales Navigator mastery\n"
                "- Proven outreach methods\n"
                "- Lead generation strategies\n"
                "- Client conversion techniques\n\n"
                "'Simply a client-generating machine' - Students say\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Shopify
    elif contains_any_partial(userchat, ["shopify", "ecommerce", "e-commerce", "store", "dropshipping"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Shopify & E-Commerce"
        return ("Shopify Store Creation & E-Commerce Course 🎯 💡\n\n"
                "Master the go-to skill for local e-commerce and global dropshipping:\n"
                "- Complete Shopify store setup\n"
                "- Product sourcing & management\n"
                "- SEO for e-commerce\n"
                "- Marketing & sales strategies\n"
                "- Client acquisition\n\n"
                "Accessible online nationwide across Pakistan!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Web Development
    elif contains_any_partial(userchat, ["web development", "web", "full stack", "mern", "react", "node", "coding"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Web Development"
        return ("Web Development / MERN Stack Course 🚀 🔥\n\n"
                "Full stack development training:\n"
                "- MongoDB - Express.js - React.js - Node.js\n"
                "- Modern web & app development\n"
                "- Project-based learning\n"
                "- Professional portfolio building\n\n"
                "High demand skills for job market and freelancing!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # App Development
    elif contains_any_partial(userchat, ["app development", "mobile app", "android", "ios", "app dev"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "App Development"
        return ("App Development Course 📚 ✍️\n\n"
                "Develop powerful mobile apps:\n"
                "- Hands-on, industry-driven instruction\n"
                "- Cross-platform development\n"
                "- Real project experience\n"
                "- Portfolio building\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Cyber Security
    elif contains_any_partial(userchat, ["cyber security", "cyber", "security", "hacking", "ethical", "cybersecurity"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Cyber Security"
        return ("Cyber Security Course 💼 📈\n\n"
                "Secure systems like a pro:\n"
                "- Ethical hacking techniques\n"
                "- Cyber defense strategies\n"
                "- Real security tools\n"
                "- Practical attack & defense scenarios\n\n"
                "One of the most in-demand IT skills!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Graphic Design
    elif contains_any_partial(userchat, ["graphic design", "graphic", "design", "visual", "creative", "photoshop"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Graphic Designing"
        return ("Graphic Designing Course 🌟 👍\n\n"
                "Craft impactful visuals:\n"
                "- Professional design tools\n"
                "- Design industry experts instruction\n"
                "- Hands-on projects\n"
                "- Portfolio development\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Video Editing
    elif contains_any_partial(userchat, ["video editing", "video", "edit", "animation", "content creation", "premiere"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Video Editing"
        return ("Video Editing & Animation Course 💻 🖥️\n\n"
                "Create stunning content:\n"
                "- Professional editing tools\n"
                "- AI tools for animation\n"
                "- Step-by-step practice\n"
                "- Portfolio building\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Freelancing
    elif contains_any_partial(userchat, ["freelance", "fiverr", "upwork", "earn", "online earning", "make money"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Freelancing Masterclasses"
        return ("Freelancing Masterclasses 🎨 🖌️\n\n"
                "Learn to earn online:\n"
                "- Fiverr & Upwork mastery\n"
                "- Client acquisition strategies\n"
                "- Profile optimization\n"
                "- Proposal writing & bidding\n"
                "- Project management\n"
                "- Scaling your freelancing business\n\n"
                "Skills that allow earning PKR + USD from anywhere in Pakistan!\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Azure / Cloud
    elif contains_any_partial(userchat, ["azure", "cloud", "microsoft", "devops"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Microsoft Azure"
        return ("Microsoft Azure Cloud Course 🔒 🛡️\n\n"
                "Master the go-to certification for cloud growth:\n"
                "- Cloud basics & concepts\n"
                "- Virtual machines & storage\n"
                "- Networking in Azure\n"
                "- Azure CLI & DevOps pipelines\n"
                "- Azure Certificate from The Net Rider\n\n"
                "No prior IT background needed!\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Cisco / Networking
    elif contains_any_partial(userchat, ["cisco", "networking", "mikrotik", "router", "network", "ccna"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Networking Certification"
        return ("Networking Certification Courses 🛒 💳\n\n"
                "Cisco Networking Certification - the go-to certification for smart IT growth\n"
                "MikroTik Certification - master network management\n\n"
                "Learn:\n"
                "- IP addressing & routing\n"
                "- DNS & subnetting\n"
                "- AI-enhanced network monitoring\n"
                "- Cisco Packet Tracer & Wireshark practice\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Figma / UI/UX
    elif contains_any_partial(userchat, ["figma", "ui", "ux", "ui/ux", "prototype", "wireframe"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Figma & UI/UX Design"
        return ("Figma & UI/UX Design Course 📱 📲\n\n"
                "Design interfaces that feel like magic:\n"
                "- User-centric design principles\n"
                "- Figma mastery\n"
                "- Prototyping & wireframing\n"
                "- Design systems\n"
                "- Portfolio projects\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Blender / 3D
    elif contains_any_partial(userchat, ["blender", "3d", "modeling", "animation"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Blender 3D Modeling"
        return ("Blender 3D Modeling & Animation Course 🎓 🏆\n\n"
                "Build 3D mastery with Blender:\n"
                "- 3D modeling fundamentals\n"
                "- Animation techniques\n"
                "- Texturing & rendering\n"
                "- Industry-standard workflows\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Architecture
    elif contains_any_partial(userchat, ["architecture", "autocad", "3ds max", "vray", "building"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "Architecture with AI"
        return ("Architecture with AI Tools Course 📞 ☎️\n\n"
                "Design architectural layouts using:\n"
                "- AutoCAD\n"
                "- 3ds Max\n"
                "- VRay\n"
                "- AI tools for design\n"
                "- Residential & commercial design\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # AI Fundamentals
    elif contains_any_partial(userchat, ["ai fundamentals", "artificial intelligence", "ai basics", "machine learning", "deep learning"]):
        conversation_context["last_question"] = "specific_course"
        conversation_context["last_course"] = "AI Academia"
        return ("AI Academia / Artificial Intelligence Fundamentals 🕒 📅\n\n"
                "Master Artificial Intelligence - the go-to skill for smart future growth:\n"
                "- Machine Learning (ML)\n"
                "- Deep Learning\n"
                "- Python programming\n"
                "- Natural Language Processing (NLP)\n"
                "- Real-world AI applications\n\n"
                "Available: On-Campus & Online\n\n"
                "Would you like to know more about this course?")
    
    # Trainer Information
    elif contains_any_partial(userchat, ["trainer", "teacher", "instructor", "mentor", "who teaches"]):
        conversation_context["last_question"] = None
        return ("Trainers at The Net Rider 📝 ✅\n\n"
                "The courses are primarily trained by Humayun Khan Babar - "
                "founder, AI expert, and Pakistan's recognized AI trainer and youth mentor.\n\n"
                "Why our trainers stand out:\n"
                "- Not just qualified - they're committed to your growth\n"
                "- Bring human insight and mentorship into every session\n"
                "- Provide practical, project-based training\n"
                "- Help students work on real client projects")
    
    # ENROLLMENT & CONTACT
    elif contains_any(userchat, ["enroll", "join", "register", "admission", "sign up", "how to join"]):
        conversation_context["last_question"] = "enroll"
        return ("Ready to Enroll? 🙌 😄\n\n"
                "Here's how you can join The Net Rider:\n\n"
                "Option 1: Online\n"
                "Visit: thenetrider.com\n\n"
                "Option 2: Call/WhatsApp\n"
                "0333 999 1018\n\n"
                "Option 3: Visit Campus\n"
                "Peer Khursheed Colony Road, Multan\n\n"
                "Students from all Pakistani cities can join online!\n"
                "Would you like to know more about enrollment?")
    
    elif contains_any(userchat, ["fee", "fees", "cost", "price", "charges", "payment", "how much"]):
        conversation_context["last_question"] = None
        return ("Fee Information 🌐 🔗\n\n"
                "For the latest fee details, please contact us directly:\n\n"
                "Call: 0333 999 1018\n"
                "WhatsApp: thenetrider.com\n"
                "Visit: thenetrider.com\n\n"
                "Good news! The fee structure is designed to be affordable so everyone can access quality AI education.")
    
    elif contains_any(userchat, ["location", "address", "where", "campus", "multan"]):
        conversation_context["last_question"] = None
        return ("The Net Rider Campuses 💰 💵\n\n"
                "Main Campus: Peer Khursheed Colony Road, Multan, Pakistan\n\n"
                "We also have campuses in:\n"
                "- Multan\n"
                "- Faisalabad\n"
                "- Lahore\n"
                "- Islamabad\n"
                "- Karachi\n"
                "- Dubai\n\n"
                "Can't visit in person? No problem!\n"
                "- Online classes available nationwide\n"
                "- Live Zoom sessions with full mentorship\n"
                "- Recorded lectures for flexibility\n\n"
                "Students from any city in Pakistan (or abroad) can join online!")

    # NEW SESSION / UPCOMING BATCH
    elif contains_any(userchat, ["new session", "new batch", "new class", "new classes",
                                   "upcoming session", "upcoming class", "session start", "class start",
                                   "classes start", "classes starting", "13 july", "13th july",
                                   "13/07", "starting date", "when does the session start",
                                   "when do classes start", "when do new classes start"]):
        conversation_context["last_question"] = None
        return ("New Session Starting from 13th July 2026 🤝 🙂\n\n"
                "The Best Opportunity — Learn Today, Lead Tomorrow!\n"
                "Upgrade Your Skills | Build Your Future | Boost Your Career\n\n"
                "Featured Courses in This Session:\n"
                "- Generative AI - Learn AI Tools, Prompt Engineering, Content Generation & Automation\n"
                "- YouTube Automation - Build & Grow Automated YouTube Channels with AI\n"
                "- Web Development - Master Frontend, Backend & Full Stack Development\n"
                "- CCNA - Build Networking Skills & Get CCNA Certified\n"
                "- AI Digital Marketing - Learn AI Powered Marketing, SEO, Ads, Content & Grow Your Brand\n"
                "- Shopify - Build Profitable eCommerce Stores & Brands\n"
                "- Cyber Security - Learn Ethical Hacking, Security Tools & Protect Digital World\n"
                "- AutoCAD - Learn 2D Drafting & 3D Designing Like a Pro\n"
                "- AI Agents & Automation - Build Intelligent AI Agents & Automate Real-World Tasks\n\n"
                "Why Join:\n"
                "- Expert Instructors - Industry Experienced Professionals\n"
                "- Practical Learning - 100% Hands-on Training\n"
                "- Certificate of Completion - Boost Your Career with Certification\n"
                "- Limited Seats - Hurry Up & Secure Your Seat\n\n"
                "Campuses: Multan | Faisalabad | Lahore | Islamabad | Karachi | Dubai\n\n"
                "Enroll now and take the first step toward a successful future!\n"
                "Contact: +92 333 999 1018\n"
                "Website: www.thenetrider.com")
    
    elif contains_any(userchat, ["contact", "phone", "whatsapp", "number", "call", "email"]):
        conversation_context["last_question"] = None
        return ("Contact The Net Rider 📌 🔎\n\n"
                "- Phone: 0333 999 1018\n"
                "- WhatsApp: thenetrider.com\n"
                "- Email: info@thenetrider.com\n"
                "- Website: thenetrider.com\n"
                "- Contact Form: thenetrider.com/contact/\n\n"
                "We're here to help! Reach out anytime.")
    
    elif contains_any(userchat, ["timing", "hours", "working", "open", "close", "schedule"]):
        conversation_context["last_question"] = None
        return ("Working Hours 😊 ✨\n\n"
                "The Net Rider is open:\n"
                "- Monday to Saturday: 9 AM to 6 PM\n"
                "- Sunday: Closed\n\n"
                "Online classes are available nationwide with flexible scheduling!\n\n"
                "For specific timing inquiries: 0333 999 1018")
    
    elif contains_any(userchat, ["certificate", "certification", "degree", "diploma"]):
        conversation_context["last_question"] = None
        return ("Certificates 🎯 💡\n\n"
                "Yes! Students receive certificates recognized by employers after completing their course.\n\n"
                "What you get:\n"
                "- Professional course completion certificate\n"
                "- Practical skills certification\n"
                "- Industry-recognized credentials\n"
                "- Portfolio of real projects\n\n"
                "These certificates help you stand out in job applications and freelancing profiles!")
    
    # STUDENT TESTIMONIALS & IMPACT
    elif contains_any(userchat, ["testimonial", "review", "success", "student says", "feedback"]):
        conversation_context["last_question"] = None
        return ("What Our Students Say 🚀 🔥\n\n"
                "'My wife completed the AI Digital Marketing course. She is now working with real clients.' - Asad Ghauri\n\n"
                "'I learned AI-Based SEO, Social Media Marketing, Funnels, Google Ads... Now, I am working with real clients.' - Asad Ullah\n\n"
                "'The environment is very practical and skill-focused. I recommend to all...' - Muneeb Mirza\n\n"
                "'Pure understanding for real projects and clients handling... My recommendation is for everyone!' - Zara Mirza\n\n"
                "Our Impact:\n"
                "- 20,000+ students trained\n"
                "- 1,200+ workshops\n"
                "- 10,000+ students trained to take action\n"
                "- 300+ educational partners\n\n"
                "Want to be our next success story?")
    
    # BEGINNER COURSES
    elif contains_any(userchat, ["beginner", "new to tech", "new to coding", "new to this field",
                                   "no experience", "from scratch", "just starting"]):
        conversation_context["last_question"] = None
        return ("Best Courses for Beginners 📚 ✍️\n\n"
                "If you're new to tech, start with these:\n\n"
                "1. AI Digital Marketing - Learn practical marketing with AI tools\n"
                "2. Artificial Intelligence Fundamentals - Build your AI foundation\n"
                "3. Spoken English Training - Improve communication skills\n"
                "4. Web Development - Start coding from basics\n"
                "5. Graphic Designing - Creative skills with practical tools\n\n"
                "These build a strong foundation before moving to specialized courses.\n\n"
                "All courses are beginner-friendly with expert guidance!\n\n"
                "Which one sounds interesting? I can tell you more!")
    
    # HELP & MENU
    elif contains_any(userchat, ["help", "menu", "what can you do", "options", "capabilities"]):
        conversation_context["last_question"] = None
        return ("I can help you with: 💼 📈\n\n"
                "Course Information\n"
                "- All 25+ courses offered\n"
                "- Course details & content\n"
                "- Trainer information\n"
                "- Popular courses\n\n"
                "Enrollment\n"
                "- How to join\n"
                "- Online vs on-campus\n"
                "- Fee structure\n\n"
                "Location & Contact\n"
                "- Campus address\n"
                "- Phone & WhatsApp\n"
                "- Working hours\n\n"
                "Recommendations\n"
                "- Best courses for beginners\n"
                "- Courses based on your goals\n"
                "- Career guidance\n\n"
                "Student Success\n"
                "- Testimonials\n"
                "- Training impact\n"
                "- Certification info\n\n"
                "To exit: type 'bye' or 'quit'\n\n"
                "What would you like to know?")
    
    # SMALL TALK
    elif contains_any(userchat, ["fine", "ok", "okay", "good", "nice"]):
        conversation_context["last_question"] = None
        return "Great! 🙌 Let me know if you have any questions about The Net Rider's courses or programs! 😊"
    
    elif contains_any(userchat, ["thank", "thanks", "thank you"]):
        conversation_context["last_question"] = None
        return "You're welcome! 😊 Happy to help, let me know if anything else comes to mind!"
    
    elif contains_any(userchat, ["good morning", "good afternoon", "good evening", "good night"]):
        conversation_context["last_question"] = None
        greeting = userchat.split()[1] if len(userchat.split()) > 1 else "day"
        return f"Good {greeting} to you too! 😊 How can I assist you today? 🙂"
    
    # FALLBACK
    else:
        conversation_context["last_question"] = None
        return ("Hmm, I'm not totally sure I got that one 🤔 🌟 👍\n\n"
                "Here are a few things you can ask me:\n"
                "- 'What courses do you offer?'\n"
                "- 'Tell me about AI Digital Marketing'\n"
                "- 'How do I enroll?'\n"
                "- 'What are the fees?'\n"
                "- 'Where is The Net Rider located?'\n"
                "- 'What do students say about you?'\n"
                "- 'What's the best course for beginners?'\n\n"
                "Or contact us directly:\n"
                "- 0333 999 1018\n"
                "- thenetrider.com")


# ============================================
# MAIN FUNCTION
# ============================================
def main():
    print("=" * 60)
    print("          THE NET RIDER ASSISTANT 🚀")
    print("          Empowering Minds with Future-Ready AI Skills")
    print("=" * 60)
    print("\n")
    
    name = input("You : Hey, what's your name? ").strip() or "there"
    print()
    show_typing_effect()
    print(f"Bot : {get_time_based_greeting(name)}")
    print("\nYou can ask me things like 'What courses do you offer?' or 'Tell me about AI Digital Marketing' 🙂\n")
    
    while True:
        userchat = input("You : ").strip()
        
        if userchat.lower() in EXIT_WORDS:
            print()
            show_typing_effect()
            print("Bot : Thanks so much for chatting! 😊")
            print("         Visit thenetrider.com or call 0333 999 1018 anytime.")
            print("         Take care, bye! 👋")
            break
        
        if not userchat:
            continue
        
        print()
        show_typing_effect()
        print("Bot :", chatbot_response(userchat))
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()

    