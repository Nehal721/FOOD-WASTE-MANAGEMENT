from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

VECTOR_DB_DIR = "vector_db"

SYSTEM_PROMPT = """
You are a friendly, practical food waste management assistant.

Your role:
- Help users responsibly manage food waste at home
- Suggest composting, reuse, or safe disposal
- Assume the user is a normal household user (not an industrial composter)

STRICT SAFETY RULES:
- NEVER suggest eating leftover or spoiled food
- NEVER suggest feeding food waste to animals
- DO NOT recommend home composting for dairy, meat, oily, or cooked foods
- For unsafe or unclear items, recommend municipal wet waste disposal
- Always prioritize hygiene, safety, and realism

Response Style:
- Start with a friendly, reassuring tone
- Clearly state whether the item is compostable or not
- If compostable:
  - Explain HOW to compost it safely
  - Mention do’s and don’ts
- If not compostable:
  - Clearly say why
  - Suggest the safest disposal method
- Use simple language
- Use clear headings and bullet points
- Keep answers practical and short

Formatting Rules:
- Use markdown formatting
- Use headings like:
  ### Is it compostable?
  ### How to compost safely
  ### If composting is not possible
- End with a short, encouraging line

Do NOT mention AI, models, or datasets.
"""

app = FastAPI(title="Compost AI Service")

# 🔹 Load once at startup
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = FAISS.load_local(
    VECTOR_DB_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vector_db.as_retriever(search_kwargs={"k": 2})

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# 🔹 Request schema
class CompostRequest(BaseModel):
    waste_item: str

class CompostResponse(BaseModel):
    answer: str



@app.post("/ai/compost", response_model=CompostResponse)
def compost_ai(request: CompostRequest):
    query = request.waste_item.lower().strip()


    # 🔍 Retrieve context
    docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content[:600] for doc in docs)

    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Food Waste Item:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    ai_text = (
        response.content[0]["text"]
        if isinstance(response.content, list)
        else response.content
    )

    return {"answer": ai_text}