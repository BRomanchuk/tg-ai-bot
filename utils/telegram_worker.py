from .mongo_worker import MongoWorker
from .openai_worker import AIWorker


class TelegramWorker:
    init_openai_context = [{"role": "user", "content": "you are an AI assistant who helps users."}]

    @staticmethod
    async def start(message):
        user_id = message.from_user.id
        user_jsons = MongoWorker.get_user({"telegram_id": user_id})
        if user_jsons is None:
            TelegramWorker.__register_user__(message)
            return await message.reply("you successfully registered")
        return await message.reply("you've registered earlier")

    @staticmethod
    async def reset_context(message):
        user_id = message.from_user.id
        TelegramWorker.__update_user_context__(
            telegram_id=user_id,
            new_context=TelegramWorker.init_openai_context.copy()
        )
        return await message.reply("Your context is updated")

    @staticmethod
    async def gpt(message):
        if AIWorker.count_text_tokens(message.text) > AIWorker.tokens_limit:
            return await message.reply("Your message is to long")

        user_id = message.from_user.id
        user_json = MongoWorker.get_user({"telegram_id": user_id})

        context = user_json["context"]
        context.append({"role": "user", "content": message.text})

        while AIWorker.count_context_tokens(context) > AIWorker.tokens_limit:
            context = context[:1] + context[2:]

        gpt_response = await AIWorker.gpt(messages=context)

        context.append({"role": "system", "content": gpt_response})
        TelegramWorker.__update_user_context__(telegram_id=user_id, new_context=context)

        return await message.reply(gpt_response)

    @staticmethod
    def __update_user_context__(telegram_id, new_context):
        return MongoWorker.update_user_json(
            parameters={"telegram_id": telegram_id},
            updated_json={"context": new_context}
        )

    @staticmethod
    def __register_user__(message):
        user_json = {
            "telegram_id" : message.from_user.id,
            "username" : message.from_user.username,
            "first_name" : message.from_user.first_name,
            "last_name" : message.from_user.last_name,
            "context" : TelegramWorker.init_openai_context.copy()
        }
        return MongoWorker.add_user(user_json=user_json)








