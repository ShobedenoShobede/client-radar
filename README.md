# Client Radar

Client Radar is a Streamlit app that analyzes client emails, briefs, and contracts for freelance-business risk signals.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Set your Groq API key before scanning:

```bash
export GROQ_API_KEY="your-groq-api-key"
```

For Streamlit Community Cloud, deploy the `main` branch with `app.py` as the main file, then add this secret in **App settings → Secrets**:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

Never commit the API key to the repository.
