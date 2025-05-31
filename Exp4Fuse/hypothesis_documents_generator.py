from openai import OpenAI


class OpenAIGenerator():
    def __init__(self, model_name, api_key, base_url=None, n=5, max_tokens=128, temperature=0.7, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=['\n\n\n'], wait_till_success=False):
        super().__init__(model_name, api_key)
        self.n = n
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.wait_till_success = wait_till_success
        self._client_init()
        self.base_url = base_url
    

    def generate(self, prompt):
        result = self.client.chat.completions.create(
            messages=[{"role": "system","content":  "Your task is to write a passage to answer the question."},,
                        {"role":"user", "content": prompt}]
            model=self.model_name,
            max_completion_tokens=self.max_tokens,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            top_p=self.top_p,
            n=self.n, # some models only support n=1
            stop=self.stop,
            logprobs=1 # some models are not compatible with this setting
        )





 
