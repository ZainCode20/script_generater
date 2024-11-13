from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
url='https://api.groq.com/openai/v1/chat/completions'
api_key='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'
headers = {"Authorization": f"Bearer {api_key}"}


@app.route('/', methods=['GET'])  # Capitalized 'GET'
def home():
    return jsonify({"Role" : "I am Script writer, if want to write script about any topic let me know i will write for you ....."})





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
        print("Full API response:", response_json)
        # if response.status_code != 200:
        #     return jsonify({"error": "Failed to fetch response from gpt2 API", "details": response.json()}), 500

        # Return the generated response from the LLM
        # llm_response = response.json()
        # generated_text = llm_response[0].get('generated_text', '').strip()
      
        generated_text = response_json.get('choices', [{}])[0].get('message', {}).get('content', 'No content generated')
       
        return   generated_text, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

      


from flask import Flask, request, jsonify


if __name__ == '__main__':
    app.run(debug=True)  # This is to run the app
