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
    "power star": "pawan kalyan",
    "pk": "pawan kalyan",
    "pspk": "pawan kalyan",
    "pavan": "pawan kalyan",
    "annayya": "pawan kalyan"
}

# Q&A Data (51 questions)
qa_data = {
    # --- Film Career ---
    "who is pawan kalyan": "Power Star Pawan Kalyan is a renowned Telugu actor, politician, and philanthropist known for his impactful roles and charismatic presence.",
    "what was pawan kalyan's debut film": "His debut was in the film Akkada Ammayi Ikkada Abbayi in 1996.",
    "which movie gave pawan kalyan the power star title": "Tholi Prema (1998) earned him immense popularity and the iconic title 'Power Star'.",
    "what is pawan kalyan’s most iconic love story film": "Tholi Prema is considered one of the greatest romantic Telugu films ever.",
    "which film established pawan as an action hero": "Kushi (2001) solidified his position as a mass hero and youth icon.",
    "what’s a cult classic film of pawan kalyan": "Gabbar Singh (2012), a blockbuster remake of Dabangg, became a massive hit.",
    "which movie marked pawan kalyan’s directorial debut": "Johnny (2003) was his first film as a director and writer.",
    "which film had the dialogue 'nenu trend follow avvanu'": "That iconic dialogue is from Gabbar Singh.",
    "which movie shows pawan kalyan as a lawyer": "Vakeel Saab (2021), a remake of Pink, where he fights for women’s justice.",
    "what are some of pawan kalyan's blockbuster movies": "Tholi Prema, Gabbar Singh, Kushi, Attarintiki Daredi, Vakeel Saab.",
    "which film broke box office records in 2013": "Attarintiki Daredi was a record-breaking success.",
    "what role did he play in balu": "A vigilante fighting against corruption and injustice.",
    "which movie showcased his love for martial arts": "Johnny, where he portrayed a martial arts expert.",
    "name a movie where pawan played dual roles": "Gopala Gopala (as God) and Katamarayudu (as a protective brother).",
    "which film features the song kodakaa koteswar rao": "Agnyaathavaasi (2018), where Pawan also sang the track.",
    "what is his fan-favorite mass movie": "Gabbar Singh remains a cult favorite among fans.",
    "which film was remade from a bollywood hit": "Vakeel Saab, a remake of Pink.",
    "what genre does panjaa belong to": "It’s an intense action thriller.",
    "which film had a powerful message about family": "Attarintiki Daredi beautifully blends family drama and emotion.",
    "has pawan ever acted in a mythological role": "He portrayed Lord Krishna in Gopala Gopala.",
    "what makes jalsa special": "Directed by Trivikram, it had chartbuster music and a youth-oriented plot.",
    "did pawan sing in any of his movies": "Yes! He sang Kodakaa Koteswar Rao in Agnyaathavaasi.",
    "which directors has pawan worked with frequently": "Trivikram Srinivas and Harish Shankar are key collaborators.",
    "which actress frequently co-starred with him": "Ileana and Samantha are among his notable co-stars.",
    "what's pawan kalyan’s film legacy known for": "Meaningful messages, mass appeal, and strong character roles.",

    # --- Political Career ---
    "when did pawan kalyan enter politics": "He entered politics in 2014 by founding the Jana Sena Party.",
    "what does jana sena mean": "It means 'People’s Army' in Telugu.",
    "what inspired pawan kalyan to start jana sena": "He wanted to fight corruption and represent the voice of the common man.",
    "what is jana sena’s main ideology": "Clean governance, transparency, and empowerment of youth and farmers.",
    "what was the party’s slogan": "Fight for the Right and Youth Empowerment.",
    "did pawan kalyan contest in 2019 elections": "Yes, he contested from Gajuwaka and Bhimavaram constituencies.",
    "has pawan kalyan raised social issues in politics": "Yes, he spoke out on issues like Uddanam kidney disease, farmers' rights, and injustice to AP.",
    "how did he help during the uddanam crisis": "His team conducted ground research and helped bring media and government attention.",
    "what’s his approach to politics": "Clean, people-centric, and issue-based politics.",
    "has he ever supported farmer protests": "Yes, he raised his voice in support of farmers across Andhra Pradesh.",
    "what sets his politics apart from others": "He avoids personal attacks and focuses on development.",
    "is pawan kalyan active on social media for political awareness": "Yes, he uses platforms like Twitter to raise awareness and support causes.",
    "has he collaborated with other parties": "Yes, occasionally aligned with BJP for common causes.",
    "what values does he promote in politics": "Honesty, service, nationalism, and equality.",
    "has he spoken in parliament": "Not yet elected to Parliament, but raises issues at press meets and public forums.",
    "did pawan kalyan campaign during covid-19": "Yes, he donated funds, supported vaccine drives, and urged public safety.",
    "how does he inspire youth through politics": "By showing politics can be clean and people-first.",
    "what’s the youth's opinion on pawan kalyan's political career": "Many youth admire him for his honesty and courage to fight alone.",
    "what is the main symbol of jana sena party": "The party symbol is a red star with six arms in a white circle.",
    "is jana sena registered with the election commission": "Yes, it is a recognized political party.",
    "what does pawan kalyan say about leadership": "A leader should be the first to suffer and the last to enjoy.",
    "did he fight for special status for andhra pradesh": "Yes, he actively demanded special status for AP post-bifurcation.",
    "how is his political journey seen by fans": "As brave, bold, and idealistic – admired for standing up alone.",
    "has he written political books or articles": "He has shared many thoughts in interviews and speeches, but no official book yet.",
    "what keeps him going in politics despite challenges": "His love for people and belief in justice and equality.",
    "why do fans call him leader of the people": "Because of his sincerity, sacrifice, and fearless voice for the common man."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower().strip()
    processed = preprocess(msg)

    if msg in ["hi", "hello", "hey"]:
        return jsonify({"response": "Hi there! Want to know something about Power Star Pawan Kalyan?"})

    # Normalize aliases
    words = processed.replace("?", "").split()
    mapped = [name_map.get(word, word) for word in words]
    joined = " ".join(mapped)

    probable = get_close_matches(joined, qa_data.keys(), n=1, cutoff=0.6)
    if probable:
        return jsonify({"response": qa_data[probable[0]]})

    return jsonify({"response": "Sorry, I don't have info on that. Try asking about Pawan Kalyan's movies or political career."})

if __name__ == "__main__":
    app.run(debug=True)