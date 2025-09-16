from apscheduler.schedulers.background import BackgroundScheduler
from .models import FirstAidGuide
from datetime import datetime
import random, json, re, requests

# ... keep your get_youtube_link, topics, call_ollama_remote_model here ...

from apscheduler.schedulers.background import BackgroundScheduler
from .models import FirstAidGuide
from datetime import datetime
import random, json, re, requests

# ---- YouTube helper ----
def get_youtube_link(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
    except Exception as e:
        print("⚠️ YouTube search scraping failed:", e)
    return f"https://youtube.com/results?search_query={query.replace(' ', '+')}"

# ---- Topics ----
topics = [
    "first aid for pets",
    "pet nutrition guide",
    "dog grooming at home",
    "how to handle pet anxiety",
    "heatstroke symptoms in cats",
    "vaccination checklist for puppies",
    "preventing parasites in pets",
    "pet dental care",
    "how to travel with pets",
    "common pet illnesses"
]

# ---- Ollama model call ----
OLLAMA_BASE_URL = "http://127.0.0.1:8001/"

def call_ollama_remote_model(prompt: str) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": "llama3:latest", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        if response.ok:
            return response.json()["response"]
        else:
            print("⚠️ Ollama error:", response.status_code, response.text)
            return ""
    except Exception as e:
        print("❌ Error calling Ollama server:", e)
        return ""

def generate_and_post_guides():
    max_guides = 5
    generated = 0
    attempted_topics = set()

    while generated < max_guides:
        try:
            topic_pool = [t for t in topics if t not in attempted_topics]
            if not topic_pool:
                attempted_topics.clear()
                topic_pool = topics

            topic = random.choice(topic_pool)
            attempted_topics.add(topic)

            prompt = f"""
            Generate a helpful guide about: "{topic}".
            Return ONLY valid JSON in format:
            {{
                "title": "...",
                "steps": ["Step 1...", "Step 2...", "Step 3..."],
                "youtube_url": "https://youtube.com/watch?v=...",
                "category": "e.g. Pet Nutrition, Grooming, First Aid"
            }}
            """

            content = call_ollama_remote_model(prompt)
            content = re.sub(r"^```(?:json)?", "", content.strip())
            content = re.sub(r"```$", "", content.strip())
            guide_data = json.loads(content)

            if isinstance(guide_data.get("steps", [])[0], dict):
                guide_data["steps"] = [step.get("step_title", "Unnamed Step") for step in guide_data["steps"]]

            guide_data["youtube_url"] = get_youtube_link(topic)

            FirstAidGuide.objects.create(
                title=guide_data["title"],
                steps=guide_data["steps"],
                youtube_url=guide_data["youtube_url"],
                category=guide_data.get("category", "General Pet Guide")
            )

            print(f"✅ Guide on '{topic}' added at {datetime.now()}")
            generated += 1

        except Exception as e:
            print(f"❌ Failed for '{topic}' → {e}")
            continue

# Start scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(generate_and_post_guides, 'interval', hours=12)
scheduler.start()
