from mistralai import Mistral
import logging

logger = logging.getLogger(__name__)

class SummarizerService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None

    async def summarize(self, text: str) -> str:
        try:
            async with Mistral(api_key=self.api_key) as client:
                messages = [{
                    "role": "user",
                    "content": f"""Перепиши новость в стиле Telegram-канала. Пиши ТОЛЬКО текст поста, без объяснений.
                    
                    {text}
                    
                    Правила оформления:
                    1. Начинай с эмодзи (⚡️, 🔥, 💡, 🚨) и краткого яркого заголовка с тире
                    2. После заголовка ОБЯЗАТЕЛЬНО ставь пустую строку
                    3. Далее 2-3 ОЧЕНЬ КОРОТКИХ предложения основного текста
                    4. Важные слова и цифры выделяй КАПСОМ
                    5. В конце - одно короткое предложение как вывод
                    6. Общая длина текста - не больше 500 символов
                    7. Пиши живым языком, как для друга
                    8. Не используй фразы "читайте далее", "подробнее" и т.п.
                    9. Максимально сокращай все предложения, убирай лишние слова
                    10. В конце каждого поста ставить хэштэги по теме
                    
                    Пример формата:
                    ⚡️ Apple СВОРАЧИВАЕТ работу в России — возвращения не будет
                    
                    Компания изменила условия работы в России впервые с весны 2022 года. Apple прекращает поддержку всех сервисов и выкладывать новый контент в Apple TV+. Тим Кук продолжает брать деньги и платить штрафы в России.
                    
                    Возвращения в Россию можно не ждать.
                    
                    #Apple #IT"""
                }]

                response = await client.chat.complete_async(
                    model="mistral-large-latest",
                    messages=messages,
                )

                if response and response.choices:
                    return response.choices[0].message.content
                
                logger.warning("Не удалось получить корректный ответ от API")
                return text[:1000] + "..."
                
        except Exception as e:
            logger.error(f"Ошибка при обработке текста через AI: {e}")
            return text[:1000] + "..." 