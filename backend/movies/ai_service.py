import os
import json
from groq import Groq
from .models import Movie, UserAction

def get_ai_recommendations(user):
    # ۱. گرفتن تاریخچه کاربر
    user_actions = UserAction.objects.filter(user=user).order_name_or_id = ('-timestamp')[:10] # ۱۰ فعالیت اخیر
    
    clicked_movies = []
    searched_queries = []
    
    for action in user_actions:
        if action.action_type == 'click' and action.movie:
            clicked_movies.append(f"{action.movie.title} ({action.movie.genre})")
        elif action.action_type == 'search' and action.search_query:
            searched_queries.append(action.search_query)

    # ۲. گرفتن تمام فیلم‌های موجود در سایت ما
    all_site_movies = Movie.objects.all()
    movies_list_for_ai = []
    for m in all_site_movies:
        movies_list_for_ai.append({
            "id": m.id,
            "title": m.title,
            "genre": m.genre,
            "plot": m.plot
        })

    # اگر کاربر هیچ تاریخچه‌ای نداشت، فیلم‌های رندوم یا تاپ رو پیشنهاد بده
    if not clicked_movies and not searched_queries:
        # برای سادگی، فعلا لیست خالی می‌فرستیم تا ال‌ال‌ام خودش بر اساس جذابیت فیلم‌های ما انتخاب کنه
        user_profile = "New user with no history yet. Suggest the best entry movies."
    else:
        user_profile = f"Clicked Movies: {', '.join(clicked_movies)}. Searched Terms: {', '.join(searched_queries)}."

    # ۳. اتصال به Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    # ۴. پرامپت سنگین و مهندسی شده
    system_prompt = (
        "You are an expert movie recommendation system for a Netflix-like streaming platform.\n"
        "Your absolute core constraint: You can ONLY recommend movies from the provided 'AVAILABLE_MOVIES' list. Never invent or recommend a movie outside this list.\n"
        "Analyze the 'USER_PROFILE' (their clicks and searches) to understand their taste.\n"
        "Pick exactly 3 movies from AVAILABLE_MOVIES that best match their taste.\n"
        "Return the response in strict JSON format as a list of objects, containing ONLY the movie 'id' and a short 'reason' for the recommendation.\n"
        "Example Output Format:\n"
        "[\n"
        "  {\"id\": 1, \"reason\": \"Because you liked sci-fi and Christopher Nolan movies...\"},\n"
        "  {\"id\": 2, \"reason\": \"Since you searched for action hero movies...\"\n"
        "]"
    )

    user_content = f"USER_PROFILE: {user_profile}\n\nAVAILABLE_MOVIES: {json.dumps(movies_list_for_ai)}"

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # یک مدل بسیار سریع و دقیق
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2, # دما پایین برای اینکه خلاقیت به خرج ندهد و دقیقاً طبق دستور عمل کند
            response_format={"type": "json_object"} # اجبار به خروجی JSON
        )
        
        # تبدیل پاسخ متنی ال‌ال‌ام به دیتای پایتونی
        ai_response = json.loads(completion.choices[0].message.content)
        return ai_response
    except Exception as e:
        print(f"AI Error: {e}")
        return None