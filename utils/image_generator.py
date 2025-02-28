import os
from openai import OpenAI
import base64

def generate_tax_impact_image(total_tax, lost_wealth):
    """Generate a visually appealing image showing tax impact using DALL-E"""
    client = OpenAI()
    
    # Create a prompt that will generate a visually appealing financial visualization
    prompt = f"""
    Create a minimalist infographic showing Canadian tax impact.
    A professional financial chart with two main numbers:
    Annual Tax: ${total_tax:,.0f}
    30-Year Lost Wealth: ${lost_wealth:,.0f}
    Use blue and red color scheme, clean modern design, white background.
    Include Canadian maple leaf symbol.
    """
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
