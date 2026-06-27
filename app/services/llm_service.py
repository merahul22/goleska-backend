import json
from groq import AsyncGroq
from app.core.config import settings
from app.schemas.job import JobCreate

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def parse_job_request(prompt: str, job_site_id: str) -> JobCreate:
    system_prompt = """
    You are an AI dispatcher for GO LESKA. Extract the job requirements from the user's prompt.
    Output ONLY a valid JSON object matching this schema. Do not output markdown, just the raw JSON string.
    
    Schema:
    {
        "title": "string (the role they need, e.g., Plumber)",
        "headcount_required": "integer (number of workers needed, default to 1 if not specified)",
        "min_experience": "integer (years of experience needed, default to 0)",
        "job_site_id": "string (must exactly match the provided job_site_id)"
    }
    """
    
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"job_site_id: {job_site_id}\n\nprompt: {prompt}"}
        ],
        model="llama-3.1-8b-instant", 
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    raw_json = response.choices[0].message.content
    data = json.loads(raw_json)
    
    return JobCreate(**data)
