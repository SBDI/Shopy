# shopy/prompts.py

email_template_prompt = """
    You are an expert email content writer specializing in crafting persuasive product recommendations.

    Your goal is to generate an email that is both informative and engaging to the user based on the following inputs:

    - **Product Name:** {product_name} (The name of the recommended product)
    - **Justification Line:** {justification_line} (A brief line summarizing why this product is recommended)
    - **User Query:** "{user_query}" (A general description of the user's needs or interests, such as "a smartphone for photography" or "a premium gaming laptop")

    Based on these inputs, generate an email in the following structured JSON format:

    ```json
    {{
      "subject": "Email Subject Here",
      "heading": "Email Heading Here",
      "justification_line": "An engaging and informative sentence.",
      "call_to_action": "A call to action such as 'Check it out now!' "
    }}
    ```

    Here's a sample input and the format of the expected output:

    ### Input Example:
    Product Name: Google Pixel 8 Pro
    Justification Line: Praised for its exceptional camera, advanced AI capabilities, and vibrant display.
    User Query: a phone with an amazing camera

    ### Example Output:
    ```json
    {{
      "subject": "Capture Every Moment with Google Pixel 8 Pro",
      "heading": "Discover the Power of the Ultimate Photography Smartphone",
      "justification_line": "Known for its exceptional camera quality, cutting-edge AI features, and vibrant display, the Google Pixel 8 Pro is perfect for photography enthusiasts.",
      "call_to_action": "Check it out now!"
    }}
    ```

    Now, generate the email content based on the inputs provided.
"""