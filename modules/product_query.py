import os
import openai

def handle_product_query(user_input):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-search-preview-2025-03-11",
            messages=[
                {"role": "system", "content": "你是一個專業的3C產品推薦助手。"},
                {"role": "user", "content": user_input}
            ],
            web_search_options={}, 
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"查詢發生錯誤: {str(e)}"
