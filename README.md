This is an empty repository so I can try out vibe coding with OpenAI's codex. As a demo project, I want to build a general Chat AI system that does such:
- Users are generally Koreans and Japanese (but for the sake of the demo, let's focus on Korean)
- Obviously, the users will speak to the system in Korean, and expect outputs to be in full natural Korean.
- There's an existing Korean LLM (called Tri) that I built, which is very good at Korean understanding, but lacking in general capabilities than other English models like ChatGPT. 
- There's a plan to improve it as we go, but basically I want to create an AI system that serves the Korean users better, and I don't care which models we use ultimately.
- However, simply wrapping ChatGPT doesn't do the magic, as numerous other players tried and failed. In fact, it even directly competes with ChatGPT and doesn't do much better through "mere prompting"
- What I want to build is to use our model - Tri - as the central orchestrator to allocate tasks to Gemini (default, multi-lingual reasoning, cheapest possible API), ChatGPT (generic reasoning, math, science, etc.), and Claude (Coding) according to their specialties.
- Tri will take in user input, rewrite it in English (as it's superior in translation), and dispatch them to each API based on their specialities, take back the output from each model, score the best, translate and rewrite the best in Korean, and serve it back to the user.

## Running the demo

Install Python 3.10 or later. Then install the dependencies:

```bash
pip install -r requirements.txt
```

Set the required API keys as environment variables:

* `OPENAI_API_KEY` - key for OpenAI's ChatGPT API
* `GEMINI_API_KEY` - key for Google's Gemini API
* `ANTHROPIC_API_KEY` - key for Anthropic's Claude API

Run the orchestrator:

```bash
python orchestrator.py
```

The program will repeatedly prompt for Korean input, send the translated
request to each model, select the best response, translate it back to Korean
and display the result.
