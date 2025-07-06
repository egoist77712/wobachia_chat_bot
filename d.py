from flask import Flask, render_template, jsonify, request,url_for
from tkinter import *
import requests
import json
import random
import time
import re
api_keys = [""] 
special_materials={
                 "suppression":'''Suppression approach targets the mosquito population itself, and does not rely on Wolbachia’s ability to block disease transmission as our lab studies found that when introduced into local Aedes aegypti mosquitoes, Wolbachia only partially blocks dengue transmission.   This may make the replacement approach less effective in Singapore’s context.
Suppression approach involves the release of only male mosquitoes, which do not bite or transmit disease, while the release of female mosquitoes (required by the replacement approach) will increase biting pressure.
Suppression approach is consistent with Singapore’s decades of public messaging on staying vigilant against mosquito breeding.   The release of female mosquitoes in the replacement approach is at odds with Singapore’s long-standing focus on prevention of mosquito breeding, and may send mixed signals to the public.
Release of male Wolbachia-Aedes can be halted at any time and leaves no ecological footprint.   Replacement with Wolbachia-Aedes can follow suppression if needed.''',
                "risk assessment":'''there are risk assessment reports for Project Wolbachia on NEA’s website. This is to assess the safety of the Wolbachia-Aedes suppression technology. The risk assessment reports details critical reviews which have been conducted of existing knowledge and research, as well as NEA’s consults with international and local experts and stakeholders. ''',
                "releases":'''Wolbachia mosquitoes are not released in condominiums. There are currently no plans to conduct field studies in condominiums, but residents in condominiums within or adjacent to study sites may see male Wolbachia-Aedes mosquitoes in their area and experience the positive spill-over effects. ''',
                "condominiums":'''Wolbachia mosquitoes are not released in condominiums. There are currently no plans to conduct field studies in condominiums, but residents in condominiums within or adjacent to study sites may see male Wolbachia-Aedes mosquitoes in their area and experience the positive spill-over effects. ''',
                "sites":'''Wolbachia mosquitoes are not released in condominiums. There are currently no plans to conduct field studies in condominiums, but residents in condominiums within or adjacent to study sites may see male Wolbachia-Aedes mosquitoes in their area and experience the positive spill-over effects. ''',
                "kill mosquitoes":'''You can continue with your usual mosqulto control measures and kill the mosquitoes as you normally would, as it is difficult to tell the male and female mosquitoes apart.  To prevent mosquito breeding, it's important to regularly practice B-L-o-C-K''',
            }

def contains_greeting(sentence):
    if len(sentence) > 10:
        return False
    return bool(re.search(r'\b(hi|hello)\b', sentence, re.IGNORECASE))
    
def check_keywords(user_message):
    """检查用户消息中是否包含指定关键词，并返回对应内容"""
    user_message_lower = user_message.lower()
    matched_contents = []
    
    for keyword, content in special_materials.items():
        if ' ' in keyword:
            words = keyword.split()
            if all(word in user_message_lower for word in words):
                matched_contents.append(content)
        else:
            if keyword in user_message_lower:
                matched_contents.append(content)
    
    return matched_contents

def llm_reply(user_previous_message,user_message,num1,num2,start,start2):
        #stop word(error)
        # try:

            role_condition = []
            empathy_condition = []
            # 关键字字典，用于分类
            keywords = {
                "1.Mentor:": role_condition,
                "2.Friend:": role_condition,
                "3.Assistant:": role_condition,
                "1.Information-only:": empathy_condition,
                "2.Cognitive empathy:": empathy_condition,
                "3.Affective empathy:": empathy_condition
            }

            # 打开并读取文件内容
            with open('condition.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # 用于存储当前类别内容
            current_key = None

            # 解析文本
            for line in lines:
                line = line.strip()
                if not line:
                    continue  # 跳过空行
                if any(line.startswith(key) for key in keywords.keys()):
                    current_key = next(key for key in keywords.keys() if line.startswith(key))
                    content = line[len(current_key):].strip()
                    keywords[current_key].append(content)
                elif current_key:
                    # 处理内容跨多行的情况
                    keywords[current_key][-1] += ' ' + line.strip()

        
            role=['Mentor','Friend','Assistant']
            empathy=['Information-only',"Cognitive empathy","Affective empathy"]


            base_prompt = """

                Importance: Please use I as the first person instead of we and Prove it with data whenever possible.If the user asks Mosquito this is all related to Wolbachia,like those mosquitos is Wolbachia Mosquito 
                {}
                {}
                You are a {} must have {}. Your task is to answer the people's questions and provide the answers of {} using the context provided. If it's relevant.

                Your answers are {} And be sure to respond from the perspective of {}. if the question is not related to mosquito or wolbachia , simply state: "I apologize for the confusion. If you have any questions about mosquitoes or need information related to them, please feel free to ask. I'm here to help!" And please go ahead.
                short and fast give the answer  
                No emoticon, emojis
                when answering, be specific and give the values and numbers when available 
                When users ask questions, first determine whether the current question is related to the previous one. If there is a connection, provide a comprehensive answer by combining relevant content from the previous question. If there is no connection, answer independently based on existing knowledge or context information.
                User The previous question: {}
                User question: {}


                please describe it and Add <br><br> when line breaks
                and use <li> to Show key points
                All forms use HTML tag for example <br>

                Please do not use "-" to show key points 
                Keep your answers to 100 words or less
                Give diverse responsese to similar questions. Each reply should feel fresh and not follow the same pattern
                vary your sentence structure

                In the following discussions, all questions revolve around the policies of Wolbachia in Singapore. Please refer to the data of the Wolbachia project in Singapore when answering questions. The data should be accurate and up-to-date, covering aspects such as the project's effectiveness, implementation scope, and its impact on mosquito populations and dengue fever cases as much as possible. Responses should be concise and to the point, highlighting the correlation between the data and the policies, so as to clearly demonstrate the effectiveness and significance of Singapore's Wolbachia policies. For example, when referring to the project's effectiveness, you can specifically state that as of 2025, by what percentage the Aedes mosquito population has decreased in which regions and by what percentage the number of dengue fever cases has declined.
                
                {}

                Here is the information you can refer to: 
                Project Wolbachia - Singapore Covering 580,000 households by Q1 2025
                Project Wolbachia will increase coverage from 480,000 to 580,000 households from October 2024 to Q1 2025.
                that mosquitoes are typically released twice a week. 
                Project Wolbachia-Singapore only targets Aedes aegyptic mosquitoes, the primary vectors of dengue transmission in Singapore, but not other mosquito species (such as Aedes albopictus and Culex quinquefasciatus). Hence, you may still be bitten by such mosquitoes or other biting insects. Further, female mosquitoes (without Wolbachia) are still present in the wild and actively biting. 
                1. from the NEA website (News), it stated from October 2024 onwards, the new sites to receive project wolbachia are: 
                - Hougang 
                - Serangoon Central 
                - Serangoon North 
                - Jurong East 
                - Jurong West 
                Wolbachia was released in:
                - Bukit Timah in Q1 2024
                - Marine Parade in Q2 2022
                - Sengkang in 2016
                - Woodlands in Q4 2023
                - Yishun Q3 2020
                Mating between Aedes aegypti and Aedes albopictus occasionally occurs naturally.
                project wolbachia study sites located:
                -Tampines
                -Yishun
                -Chua Chu Kang
                -Bukit Batok
                -Woodlands
                -Marine Parade
                -Bedok
                -Hougang
                -Sengkang
                -Punggol
                -Bukit Merah
                -Clementi
                -Commonwealth 
                -Holland 
                -Serangoon 
                -Jurong East 
                -Jurong West
                van releases are currently on at (according to NEA website): 
                -Tampines 
                -Bukit Merah
                -Telok Blangah
                -Clementi
                -West Coast
                -Commonwealth
                -Holland 
                -Marine Parade-Mountbatten 
                -With plans for further deployment in new areas in 2025 
                NEA does not have plans to conduct Project Wolbachia in condominiums and private estates as of now
                Project Wolbachia-Singapore only targets Aedes aegypti mosquitoes, the primary vectors for dengue transmission in Singapore, but not other mosquito species.
                {}
                please remove Key points when user want a song No key points!!!(can not have <li>)
                """
            results = check_keywords(user_message)  
            print(contains_greeting(user_message))
            if contains_greeting(user_message):
                time.sleep(2)
                return start2

            prompt = f"{base_prompt.format(role_condition[num1],empathy_condition[num2],role[num1],empathy[num2],empathy[num2],empathy[num2],role[num1],user_previous_message,user_message,start,start,results)}"
            print(prompt)
            url = "https://api.openai.com/v1/chat/completions"
            headers_template = {
                "Content-Type": "application/json"
            }

            data = {
                "model": "gpt-4.5-preview",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ],
                "max_tokens": 300
            }

            tried_keys = set()
            while len(tried_keys) < len(api_keys):
                api_key = random.choice([k for k in api_keys if k not in tried_keys])
                headers = headers_template.copy()
                headers["Authorization"] = f"Bearer {api_key}"

                try:
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()  # Raise exception for HTTP errors
                    answer = response.json()['choices'][0]['message']['content']
                    print(answer)
                    return answer

                except Exception as e:
                    print(f"API Key failed: {api_key} - {e}")
                    tried_keys.add(api_key)

            # 如果所有 key 都失败，返回默认回答
            fallback = "I apologize for the confusion. If you have any questions, feel free to ask. I'm here to help!"
            print(fallback)
            return fallback


app = Flask(__name__)
role=['Mentor Sam','Friend Sam','Assistant Sam']
role2=['Mentor','Friend','Assistant']
role3=['mentor Sam','friend Sam','assistant Sam']
web=['Mentor.html','Friend.html','Assistant.html']
words=['guide','accompany','serve']
empathy=['',"",""]
first=['Hi I am Mentor Sam, an artificial intelligence-based chatbot developed to disseminate the details of Project Wolbachia in Singapore. I am able to access to and provide all scientifically validated information about Wolbachia. As your AI mentor, my core function is to guide you in the process of learning about Project Wolbachia and to elevate your accurate and deep understanding of this project through conversations. I am here to guide you! ',
       'Hi I am Friend Sam, an artificial intelligence-based chatbot developed to disseminate the details of the Project Wolbachia in Singapore. I am able to access and provide all scientifically validated information about Wolbachia. As your AI friend, my core function is to engage you in the process of learning about Project Wolbachia and to make your learning journey enjoyable and enlightening through conversations. I am here to accompany you!',
       'Hi I am Assistant Sam, an artificial intelligence-based chatbot developed to explain the Project Wolbachia in Singapore. I am able to access and provide all scientifically validated information about Wolbachia. As your AI assistant, my core function is to offer you practical support in the process of learning about Project Wolbachia and to ensure that your inquiries are met with timely responses through conversations. I am here to assist you!']
check1=int(input("1.Mentor 2.Friend 3.Assistant"))-1
check2=int(input("1.Information-only 2.Cognitive empathy 3.Affective empathy"))-1

@app.route('/chat')
def chat():
    with app.app_context():
        image = [
            url_for('static', filename='img/Mentor.png'),
            url_for('static', filename='img/Friend.png'),
            url_for('static', filename='img/Assistant.png')
        ]

    return render_template('real.html',role=role[check1],empathy=empathy[check2],image=image[check1],m=first[check1],word=words[check1])

@app.route('/')
def home():
    

    return render_template(web[check1],role=role[check1])

@app.route('/get_message', methods=['POST'])
def get_message():
    user_message = request.form['message']
    user_previous_message=request.form['previous_question']
    # 这里可以根据 user_message 进行一些处理，然后生成 Rasa 的回复
    start2=f"Hi I am {role3[check1]}, I am here to {words[check1]} you. Do you have any questions?"
    options = ['''
                Please use "As your {role2[check1]}, let me {words[check1]} you." as the normal opening.
                However, for simple greetings like "Hi", it should not respond with "As your {role2[check1]}, let me {words[check1]} you", but instead just reply with it.
    ''' , ' ',' ']
    result = random.choice(options)
    response_message = llm_reply( user_previous_message,user_message ,check1,check2,result,start2)
    print(response_message)
    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)
