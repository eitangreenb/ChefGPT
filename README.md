# ChefGPT
A Streamlit app that connects to Open AI's GPT-3 API to generate cooking recipes

## Installation

First, clone the repository and install the dependencies.

```bash
git clone https://github.com/eitangreenb/ChefGPT.git
pip install -r requirements.txt
```

You will need to add your own firebase firestore-key json to the ChatGPT folder.<br>
Edit the `secrets.json` file with your own secret keys:
```bash
{
    "FIREBASE_JSON": "the path to your firestore-key json file",
    "OPENAI_KEY": "your own openai api key"
}
```

To run the app localy use the following command:
```bash
streamlit run .\app\Home.py
```
