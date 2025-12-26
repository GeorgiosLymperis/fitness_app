import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from smolagents.agents import ChatMessage

class FitnessLLM:
    def __init__(self, model_name: str = "Qwen/Qwen2.5-3B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )
        self.model.eval()

    def generate(self, prompt, max_new_tokens: int = 1000, **kwargs):
        # Handle chat-style input from smolagents
        if isinstance(prompt, list):
            # Each item is likely a ChatMessage or dict with 'role' and 'content'
            parts = []
            for msg in prompt:
                if isinstance(msg, dict):
                    parts.append(msg.get("content", ""))
                elif isinstance(msg, ChatMessage):
                    try:
                        content = msg.content
                        if isinstance(content, list):
                            content = content[0]
                            text = content.get("text", "")
                        else:
                            text = content
                        parts.append(text)
                    except Exception as e:
                        text = ""
                        with open("debug.txt", "w") as f:
                            f.write(str(msg))
                else:
                    raise TypeError(f"Expected ChatMessage or dict, got {type(msg)}")   

               
            prompt = "\n".join(parts)
        if not isinstance(prompt, str):
            raise TypeError(f"Expected prompt to be str, got {type(prompt)}")
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        print("Generating...")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
            )
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        prompt_len = len(prompt)
        answer = answer[prompt_len:]
        chat_message = ChatMessage(role="assistant", content=answer)
        return chat_message