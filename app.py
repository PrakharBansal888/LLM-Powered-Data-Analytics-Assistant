"""
LLM-Powered Data Analytics Assistant
Main Streamlit application
"""
import streamlit as st
from src.utils import load_csv, extract_schema
from src.agent import ask_llm
from src.executor import run_code
from config.settings import MODELS, STREAMLIT_CONFIG

# Configure page
st.set_page_config(**STREAMLIT_CONFIG)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []
if "df" not in st.session_state:
    st.session_state.df = None
if "schema" not in st.session_state:
    st.session_state.schema = None

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    st.subheader("Model")
    selected_model = st.selectbox(
        "Choose a model",
        options=list(MODELS.keys()),
        index=0,
        help="All models are free via OpenRouter"
    )
    st.caption(f"`{MODELS[selected_model]}`")
    
    st.divider()
    
    # Data upload
    st.subheader("📁 Upload Data")
    uploaded = st.file_uploader("CSV file", type=["csv"])
    
    if uploaded:
        try:
            df = load_csv(uploaded)
            st.session_state.df = df
            st.session_state.schema = extract_schema(df)
            st.success(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} cols")
            
            with st.expander("📊 Preview (first 5 rows)"):
                st.dataframe(df.head(), use_container_width=True)
            
            with st.expander("🏗️ Schema"):
                st.code(st.session_state.schema, language="text")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    st.divider()
    
    # Controls
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_display = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════
st.title("📊 Data Analytics Assistant")
st.caption(
    f"Model: **{selected_model}** | "
    f"Ask anything about your data in plain English."
)

# Display chat history
for entry in st.session_state.chat_display:
    with st.chat_message(entry["role"]):
        if entry["role"] == "user":
            st.write(entry["content"])
        else:
            # Assistant response
            if entry.get("model_used"):
                st.caption(f"🤖 {entry['model_used']}")
            
            if entry.get("insight"):
                st.write(entry["insight"])
            
            if entry.get("fig"):
                st.plotly_chart(entry["fig"], use_container_width=True)
            
            if entry.get("result_df") is not None:
                st.dataframe(entry["result_df"], use_container_width=True)
            
            if entry.get("error"):
                st.error(f"❌ Error:\n```\n{entry['error']}\n```")
            
            if entry.get("code"):
                with st.expander("👁️ View generated code"):
                    st.code(entry["code"], language="python")

# ═══════════════════════════════════════════════════════════════
# CHAT INPUT
# ═══════════════════════════════════════════════════════════════
if prompt := st.chat_input("e.g., Show me the top 5 hotels by rating"):
    # Check if data is loaded
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a CSV file first.")
        st.stop()
    
    # Add user message to display
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_display.append({
        "role": "user",
        "content": prompt
    })
    
    # Get LLM response
    with st.chat_message("assistant"):
        with st.spinner(f"🤔 Asking {selected_model}..."):
            result = ask_llm(
                schema=st.session_state.schema,
                question=prompt,
                history=st.session_state.messages,
                model_key=selected_model
            )
        
        # Handle API errors
        if result.get("error"):
            st.error(f"❌ API Error: {result['error']}")
            st.session_state.chat_display.append({
                "role": "assistant",
                "error": result["error"],
                "model_used": selected_model
            })
        else:
            # Add to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": result.get("code", "")
            })
            
            # Execute code if generated
            if result.get("code"):
                with st.spinner("⚡ Executing code..."):
                    exec_result = run_code(result["code"], st.session_state.df)
                
                if exec_result.get("error"):
                    st.error(f"❌ Execution Error:\n```\n{exec_result['error']}\n```")
                    display_entry = {
                        "role": "assistant",
                        "error": exec_result["error"],
                        "model_used": selected_model,
                        "insight": result.get("insight", ""),
                        "code": result.get("code", "")
                    }
                else:
                    # Show results
                    if result.get("insight"):
                        st.write(result["insight"])
                    
                    if exec_result.get("fig"):
                        st.plotly_chart(exec_result["fig"], use_container_width=True)
                    
                    if exec_result.get("result_df") is not None:
                        st.dataframe(exec_result["result_df"], use_container_width=True)
                    
                    if exec_result.get("error") is None and exec_result.get("fig") is None and exec_result.get("result_df") is None:
                        st.info("✅ Code executed successfully (no output)")
                    
                    display_entry = {
                        "role": "assistant",
                        "model_used": selected_model,
                        "insight": result.get("insight", ""),
                        "fig": exec_result.get("fig"),
                        "result_df": exec_result.get("result_df"),
                        "code": result.get("code", "")
                    }
            else:
                display_entry = {
                    "role": "assistant",
                    "error": "No code generated",
                    "model_used": selected_model
                }
            
            st.session_state.chat_display.append(display_entry)