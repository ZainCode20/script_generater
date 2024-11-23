from flask import Flask, request, jsonify
import requests
import re
from image_generater import  image_process


app = Flask(__name__)
url='https://api.groq.com/openai/v1/chat/completions'
api_key='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'
headers = {"Authorization": f"Bearer {api_key}"}


@app.route('/', methods=['GET'])  # Capitalized 'GET'
def home():
    return jsonify({"Role" : "I am Script writer, if want to write script about any topic let me know i will write for you ....."})

def extract_prompts(image_prompts):
    """
    Extracts individual prompts from a given string by splitting based on a numbered format.
    """
    # Split based on number and dot followed by space (e.g., "1. ", "2. ")
    prompts = re.split(r'\n\d+\.\s', image_prompts.strip())

    # Remove any empty entries resulting from the split (e.g., leading empty string)
    prompts = [prompt.strip() for prompt in prompts if prompt.strip()]

    return prompts



@app.route('/script_gen', methods=['POST'])
def script_generater():
    try:
        # Get input data from the request
        data = request.get_json()

        # Validate input JSON
        if not data or 'prompt' not in data:
            return jsonify({"error": "Invalid input, 'prompt' is required"}), 400

        # Prepare request headers for Hugging Face API
        
        
        # Call the Hugging Face LLM API with the user's input
        prompt=data.get('prompt')
        print(prompt)
        payload = {
    "model": "llama3-8b-8192",
    "messages": [
        {
            "role": "user",
            "content":f"  You are a creative scriptwrite:{prompt}"
        }
    ],
    "temperature": 1,
         "max_tokens": 1024,
         "top_p": 1,
       
}
        response_out=requests.post(url=url,headers=headers,json=payload)
       
        print("hello response_out  ")


    

       
#=> "The number of parameters in a neural network can impact ...

        # Check if the LLM API request was successful
        response_json = response_out.json()
        # print("script:", response_json)
        # if response.status_code != 200:
        #     return jsonify({"error": "Failed to fetch response from gpt2 API", "details": response.json()}), 500

        # Return the generated response from the LLM
        # llm_response = response.json()
        # generated_text = llm_response[0].get('generated_text', '').strip()
      
        generated_text = response_json.get('choices', [{}])[0].get('message', {}).get('content', 'No content generated')
        image_prompts=prompt_generater(generated_text)
        # img="".image_prompts.stip()
        # print("image list ..",img)
        

# Split scenes based on '**Scene' ............
        
        prompts=extract_prompts(image_prompts)

# Strip any leading/trailing whitespace from each prompt
       
# Display the structured prompts
       
# Display the structured prompts
        print("list prompts  ...",prompts)  
        if len(prompts)!=0:
            image_process(prompts)
        else:
            print("prompt list is empty so not image generated....")    


        
        return   jsonify({"response":image_prompts}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

      

# @app.route('/prompt_gen', methods=['POST'])
def prompt_generater(prompt):
    try:
        # Get input data from the request
        
        # request.get_json()

        # Validate input JSON
        if prompt=='':
        
            return jsonify({"error": "Invalid input, 'prompt' is required"}), 400

        # Prepare request headers for Hugging Face API
        
        
        # Call the Hugging Face LLM API with the user's input
        # prompt=data.get('prompt')
        print(prompt)
        payload = {
    "model": "llama3-8b-8192",
    "messages": [
          {
            "role": "system",
            "content": "You are a professional image prompt generator. Your task is to create detailed and imaginative prompts based on the provided script for generating high-quality images."
        },
        {
            "role": "user",
            "content": f"Here is the script to generate image prompts , generate just consice and each prompt should be 16 words long,not add any irrelevent material in prompts, use names accoding to characters  : {prompt}"
        }
    ],
    "temperature": 1,
         "max_tokens": 1024,
         "top_p": 1,
       
}
        response_out=requests.post(url=url,headers=headers,json=payload)
       
        print("prompt_genrater response.. ")



    

       
#=> "The number of parameters in a neural network can impact ...

        # Check if the LLM API request was successful
        response_json = response_out.json()
        
        # if response.status_code != 200:
        #     return jsonify({"error": "Failed to fetch response from gpt2 API", "details": response.json()}), 500

        # Return the generated response from the LLM
        # llm_response = response.json()
        # generated_text = llm_response[0].get('generated_text', '').strip()
      
        generated_text = response_json.get('choices', [{}])[0].get('message', {}).get('content', 'No content generated')
        print("prompts genreate....", generated_text)
        return   generated_text
        
    except Exception as e:
        return e
    

      


# def prompt_cleaner(prompt):
#     try:
#         # Get input data from the request
        
#         # request.get_json()

#         # Validate input JSON
#         if prompt=='':
        
#             return jsonify({"error": "Invalid input, 'prompt' is required"}), 400

#         # Prepare request headers for Hugging Face API
        
        
#         # Call the Hugging Face LLM API with the user's input
#         # prompt=data.get('prompt')
#         print(prompt)
#         payload = {
#     "model": "llama3-8b-8192",
#     "messages": [
#            {
#         "role": "system",
#         "content": "You are a professional text cleaner. Your task is to clean and simple"
#     },
#     {
#         "role": "user",
#         "content": "Here is the prompts you need to clean : {prompt}"
#     }
#     ],
#     "temperature": 1,
#          "max_tokens": 1024,
#          "top_p": 1,
       
# }
#         response_out=requests.post(url=url,headers=headers,json=payload)
       
#         print("prompt_cleaner response.. ")


    

       
# #=> "The number of parameters in a neural network can impact ...

#         # Check if the LLM API request was successful
#         response_json = response_out.json()
        
#         # if response.status_code != 200:
#         #     return jsonify({"error": "Failed to fetch response from gpt2 API", "details": response.json()}), 500

#         # Return the generated response from the LLM
#         # llm_response = response.json()
#         # generated_text = llm_response[0].get('generated_text', '').strip()
      
#         generated_text = response_json.get('choices', [{}])[0].get('message', {}).get('content', 'No content generated')
#         print("prompts genreate....", generated_text)
#         return   generated_text

#     except Exception as e:
#         return e
    

      








if __name__ == '__main__':
    app.run(debug=True)  # This is to run the app
