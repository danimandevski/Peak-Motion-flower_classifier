from openai import OpenAI
from fastapi import HTTPException
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)
def get_plant_info(scientific_name: str) -> dict:
    prompt = (
        f"Generate a JSON object with exactly tree keys: 'titleLatin', 'titleEn' and 'description'. "
        f"'titleEn' should be the name of a plant with the scientific name '{scientific_name}'"
        f"'titleLatin' should be the scientific name of the plant "
        f". 'description' should be a concise summary in exactly 15 to 20 words. "
        f"Return only valid JSON without any extra text."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a knowledgeable botanist."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the content from the response using dictionary indexing.
        raw_content = response.choices[0].message.content.strip()
        cleaned_string = re.sub(r"^```(?:json)?\s*", "", raw_content, flags=re.MULTILINE)
        cleaned_string = re.sub(r"\s*```$", "", cleaned_string, flags=re.MULTILINE)
        result = json.loads(cleaned_string)
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error calling OpenAI API: {str(e)}")