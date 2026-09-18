import streamlit as st
import os
from groq import Groq
from datetime import datetime
import json
import hashlib

st.set_page_config(
    page_title="Client Radar — Freelance Red-Flag Scanner",
    page_icon="🚩",
    layout="centered"
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", ""))
client = Groq(api_key=GROQ_API_KEY)

PAYPAL_EMAIL = "omni.growth.venture@gmail.com"  # your email

def get_working_model(client):
    try:
        models = client.models.list()
        available = [m.id for m in models.data]
        for preferred in ["openai/gpt-oss-120b", "qwen/qwen3.6-27b", "llama-3.1-8b-instant"]:
            if preferred in available:
                return preferred
        return available[0] if available else "llama-3.1-8b-instant"
    except Exception:
        return "openai/gpt-oss-120b"


PROMPT = """You are a freelance business risk analyst with 15 years of experience.

Analyze the following client communication, brief, or contract that a freelancer received.

CLIENT MESSAGE:
\"\"\"
{content}
\"\"\"

Return your analysis in this EXACT format (markdown):

## RISK SCORE
[GREEN / YELLOW / RED] — one word plus a one-line reason.

## TOP 5 RED FLAGS
1. **[Flag name]** — quote the exact wording, then explain the risk in one sentence.
2. ... (5 total)

## THE 3 BIGGEST RISKS
- **Financial risk:** ...
- **Scope risk:** ...
- **Relationship risk:** ...

## SAFE REPLY (copy-paste ready)
Write a polite, professional email the freelancer can send to fix the issues before signing. 150 words max.

## CONTRACT CLAUSES TO ADD
- 3-5 specific clauses the freelancer should add (name + one sentence each).

## VERDICT
One sentence: should the freelancer take this client? Why or why not?
"""


st.title("🚩 Client Radar")
st.markdown("**Score any client before you sign.** Paste their email, brief, or contract below. Get a risk score, red flags, and a copy-paste safe reply in 30 seconds.")

with st.form("scan_form"):
    content = st.text_area(
        "Paste the client message, brief, or contract:",
        height=250,
        placeholder="Example: 'Hey, we love your work. We need this done ASAP for $X. We pay net-60. Let's start Monday...'"
    )
    submitted = st.form_submit_button("🔍 Scan This Client")

if submitted:
    if not content or len(content) < 30:
        st.error("Please paste at least a few sentences from the client.")
    else:
        with st.spinner("Analyzing risk signals..."):
            model = get_working_model(client)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": PROMPT.format(content=content[:4000])}],
                temperature=0.4,
                max_tokens=2000
            )
            result = response.choices[0].message.content

        st.success("✅ Scan complete. Review before replying to the client.")
        st.markdown("---")
        st.markdown(result)

        st.markdown("---")
        st.download_button(
            "📥 Download full report (.md)",
            data=result,
            file_name=f"client_scan_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown"
        )

        st.divider()
        st.subheader("💳 Unlock unlimited scans — $19/month")
        st.markdown("You've used 1 of 2 free scans this month. Upgrade to scan every client before signing.")

        paypal_html = f"""
        <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
            <input type="hidden" name="cmd" value="_xclick-subscriptions">
            <input type="hidden" name="business" value="{PAYPAL_EMAIL}">
            <input type="hidden" name="lc" value="US">
            <input type="hidden" name="item_name" value="Client Radar — Pro Monthly">
            <input type="hidden" name="a3" value="19.00">
            <input type="hidden" name="p3" value="1">
            <input type="hidden" name="t3" value="M">
            <input type="hidden" name="src" value="1">
            <input type="hidden" name="sra" value="1">
            <input type="hidden" name="currency_code" value="USD">
            <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_subscribeCC_LG.gif"
                   border="0" name="submit" alt="Subscribe with PayPal">
        </form>
        """
        st.markdown(paypal_html, unsafe_allow_html=True)
        st.caption("Cancel anytime. Billed monthly.")

st.divider()
st.caption("Client Radar · Built for freelancers who don't get burned twice.")