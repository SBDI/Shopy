# app.py
import asyncio
import streamlit as st
from shopy.main import main
from shopy.models import State
from shopy.utils import clean_llm_output


async def run_shopy(query, email):
    """Runs the Shopy agent and returns the final state."""
    return await main(query, email) # modified main call


st.title("Shopy: Your AI Shopping Assistant")

query = st.text_input("Enter your product query")
email = st.text_input("Enter your email (optional)")

if st.button("Search"):
    if not query:
        st.warning("Please enter a product query.")
    else:
      with st.spinner("Searching for products..."):
        final_state = asyncio.run(run_shopy(query, email))

        if final_state and isinstance(final_state, dict):
            display_data = final_state.get('display_data', {})
            if display_data:
                if display_data.get('best_product'):
                    st.subheader(f"Here is what ShopyAgent suggests: {display_data['best_product'].get('product_name', 'No product')}")
                    st.markdown(f"**Justification:**\n {display_data['best_product'].get('justification', 'No justification')}")
                    if display_data.get('youtube_link'):
                        st.markdown(f"**See the review here:** {display_data['youtube_link']}")
                    if display_data.get('comparison'):
                        st.subheader("Product Comparisons")
                        st.table(display_data['comparison'])
                    if display_data.get('summary'):
                        st.subheader("Summary:")
                        with st.expander("Show Summary"):
                            clean_llm_output(display_data['summary'], console=st)

                
        else:
            st.error("There was an error processing your query. Please try again.")