import spacy
from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

app = Flask(__name__)

# Flattened alias map if needed later (optional)
name_map = {
    "kbn college": "kbn college",
    "KBN":"kbn college",
    "KBN COLLEGE": "kbn college",
    "Kbn College": "kbn college",
    "kbn": "kbn college",
    "college":"kbn college"
}


qa_data = {
    "Who is the Principal of the College?":"Dr. G. KRISHNAVENI, M.Sc.,M.Phil.,Ph.D. is the current Principal of KBN College",
    "Who is the head of the department of Computer science?":"P.Ravindra",
    "What is the admission process?": "Admissions are done through OAMDC (Online Admission Module for Degree Colleges), where students need to register, choose courses, and lock their options. Final seat allotment is based on merit.",
    "How can I apply for admission?": "You can apply online through the OAMDC portal (https://oamdc.ap.gov.in) by registering with your details and selecting our college.",
    "When does OAMDC 2025 registration for admissions begin?":"Registration starts on August 18, 2025.",
    "What is the last date to register for admission by OAMDC 2025?":"The last date to register is August 20, 2025.",
    "what is the last date for admissions":"The last date to register is August 20, 2025.",
    "Are there additional admission rounds after Phase 1?":"Yes — Phase 2 and spot admissions will occur in September 2025, including internal sliding and spot rounds.",
    "What documents are needed for OAMDC registration?":"You need SSC and Intermediate mark sheets, study certificates (Class 6 to Inter), TC, category/income/residence certificates (if applicable), Aadhar Card, passport photo, signature, and any special category certificates (NCC, Sports, PH, CAP), plus parents’ consent for SC/ST reimbursement.",
    "Is there any scholarship or fee reimbursement available?":"Yes. Students belonging to SC/ST/BC/EWS categories are eligible for government fee reimbursement schemes (as per rules). You need to apply through the Jnanabhumi portal or respective state scholarship portal.",
    "Is there a library in college?": "Yes! Our college provides a well established Library.",
    "Tell me about the college library":"Our UG & PG library has a shelving capacity of more than 56,900 books, supporting both academic and research pursuits. It is a treasure house for knowledge seekers.",
    "How many books are there in the library?": "The library has more than 56,900 books covering UG and PG courses.",
    "Digital library availablity?": "The digital library provide, comfortable seating for students, Wi-Fi access, and inviting reading areas.",
    "Is Wi-Fi available in the library?": "Yes, the library provides Wi-Fi accessible reading areas.",
    "Can students sit and study in the library?": "Yes, the library has comfortable seating arrangements and a peaceful environment for study.",
    "The overview or glance or images of library?": "Sure! You can take a digital glance at our library here: https://www.kbncollege.ac.in/digitallibrary",
    "Is there a Canteen at college":"Yes! Our college has well hygenic Canteen for students as well as faculty.",
    "Tell me about the canteen": "Our college canteen provides a relaxing space for students to hang out. It follows the policy of serving fresh and healthy food at minimal charges.",
    "What kind of food is served in the canteen?": "The canteen prioritizes hygienic, fresh, and healthy food options for students.",
    "Is the food hygienic in the canteen?": "Yes, hygienic food is given the highest priority in our canteen.",
    "Are the canteen charges affordable?": "Yes, the food is served at minimal charges, making it affordable for students.",
    "How is the Cost of items or food items":"the food is served at minimal charges, making it affordable for students.",
    "How is the serving time in the canteen?": "Serving time is managed quickly so that students don’t miss or bunk classes.",
    "Can students relax in the canteen?": "Yes, the canteen is designed as a place where students can relax and hang out during breaks.",
    "Why is the canteen important for students?": "A good canteen improves student comfort and indirectly supports academic performance, as educational psychologists suggest.",
    "pictures of canteen":"Sure! You can take a glance at our canteen here:'https://www.kbncollege.ac.in/canteen",
    "Images of canteen":"Sure! You can take a glance at our canteen here: https://www.kbncollege.ac.in/canteen",
    "Tell me about sports facilities": "Our college offers both outdoor and indoor sports facilities, including cricket, handball, basketball, volleyball, kho-kho, kabaddi, badminton, table tennis, and more.",
        
    # Outdoor Sports
    "What outdoor sports facilities are available?": "Outdoor facilities include 2 cricket nets (red clay & concrete), a bowling machine, handball court with iron goal posts, volleyball, kho-kho, kabaddi, ball badminton courts, parallel and horizontal bars, and a basketball court with LED flood lights.",
    "How many cricket nets are available?": "We have 2 cricket nets for coaching – one red clay pitch and another concrete pitch, along with a bowling machine for practice.",
    "Is there a basketball court in the college?": "Yes, we have a basketball court with concrete flooring, cement posts, and LED flood lights.",
    "What are the facilities for volleyball?": "The volleyball court is made of red clay with permanent iron posts.",
    "Do you have kho-kho and kabaddi courts?": "Yes, separate courts are available for both kho-kho and kabaddi.",
    "What facilities are there for handball?": "The handball court is made of red soil with iron goal posts, enclosed by nets up to 10 ft.",
        
        # Indoor Sports
    "What indoor sports facilities are available?": "Indoor facilities include 2 international Stag table tennis tables, a TT robot machine, badminton court with flood lights, carrom boards, chess, and other indoor games.",
    "Is there a table tennis facility?": "Yes, we have 2 international Stag TT tables and a TT robot machine to teach new techniques.",
    "Do you have a badminton court?": "Yes, we have a badminton court with flood lights for practice.",
    "Can students play indoor games like chess or carrom?": "Yes, there are provisions for carom boards, chess, and other indoor games.",
    "Is there any medical/first aid support for sports injuries?": "Yes, physiotherapy equipment is available to provide first aid for injured players.",
        
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower().strip()
    processed = preprocess(msg)

    if msg in ["hi", "hello", "hey"]:
        return jsonify({"response": "Hi there! How can i help you?"})

    # Normalize aliases
    words = processed.replace("?", "").split()
    mapped = [name_map.get(word, word) for word in words]
    joined = " ".join(mapped)

    probable = get_close_matches(joined, qa_data.keys(), n=1, cutoff=0.6)
    if probable:
        return jsonify({"response": qa_data[probable[0]]})

    return jsonify({"response": "Sorry, I don't have info on that."})

if __name__ == "__main__":
    app.run(debug=True)
