def chat_until_success(query):
    while True:
        try:
            from g4f.client import Client
            from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots, Bing, DeepInfra
            import g4f.debug
            from g4f.cookies import set_cookies

            client = Client(
                provider=RetryProvider([DeepInfra], shuffle=True)
            )
                        
            response = client.chat.completions.create(
                model="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
                messages=[{"role": "user", "content": query}],
            )
            # print(response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")

def main():
    print(chat_until_success("Hello World"))

if __name__ == "__main__":
    main()
