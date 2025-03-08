# **LexiEase AI - An AI Powered Dyslexic Support System**

**LexiEase AI** is an AI-powered system that offers personalized learning support for individuals with dyslexia. The platform provides dyslexia screening, tailored learning paths, and various assistive tools to improve accessibility and enhance learning outcomes for dyslexic individuals. 

## **Introduction**

**LexiEaseAI is an AI-powered learning platform** designed to enhance cognitive skills, reading abilities, and academic performance through personalized assessments and interactive tools. 

**Supported by Informatica’s secure and scalable infrastructure, it ensures a seamless and efficient learning experience.**


![image](https://github.com/user-attachments/assets/972384a0-ec2a-475c-8b75-f906afb1a0d6)

---

## **What Problems Does LexiEase AI Solve?**

1. **Limited Access to Dyslexia Screening**  
   Many individuals with dyslexia struggle to get timely and affordable screenings, leading to delayed interventions and missed educational opportunities.

2. **Lack of Personalized Learning Paths**  
   Traditional learning resources are not tailored to the unique needs of dyslexic learners, making it harder for them to achieve their full potential in conventional educational settings.

3. **Insufficient Support Tools for Dyslexic Learners**  
   Dyslexic individuals often lack access to specialized tools, like writing assistants and document simplifiers, that can make reading and learning more accessible and enjoyable.

![image](https://github.com/user-attachments/assets/41df37ef-b19d-44c2-a87d-3d80c068fa6c)

---

## **List Of Features**

![image](https://github.com/user-attachments/assets/a48e2245-9911-4ff3-b6a6-57d4b171c2d1)
![image](https://github.com/user-attachments/assets/c6be600b-8771-495d-9a81-269325103a36)

### **1. Dyslexic Screening Test**

- **Phonological Awareness Test**
  - Providing easy, medium and hard words from various CSVs of Phoneme, Irregular, Multisyllable and Nonsensical to check their phonological awareness.
  - The CSVs are ingested to **Snowflake tables** using **Informatica's Data Ingestion**
  - **Informatica's Data Profiling** is done to get Claire's insights on the data along with the null & distinct percentages.
  - The words are provided to them in an audio format coverted using Google Text To Speech.
  - The written word is checked against the audio word and a score is calculated.
 
    ![PhonologicalAwarenessTest](https://github.com/user-attachments/assets/8f79b525-72ee-4f48-aaff-5ff638753f94)

- **Reading Passages**
  - Providing easy, medium and hard words from Reading Passages CSV.
  - Data is ingested into **Snowflake tables** using **Informatica's Data Ingestion**.
  - **Informatica's Data Profiling** is done to get Claire's insights on the data along with the null & distinct percentages.
  - Rule Specifications and Cleansing of the data was done using **Informatica's Data Quality**
  - Creating mappings of the data by using Data Quality Assets & Aggregates using **Informatica's Data Integration**.
  - Linear Regression based model to calculate the fluency based on various parameters using **Informatica's Model Serve**
  - A fluency rating is then provided to the user.
 
    ![GrayOralReadingTest drawio](https://github.com/user-attachments/assets/5c937e5c-a76c-48e9-9569-4a73627b7a55)

### **2. Personalized Learning Path**

<div align="center">

| **Level of Dyslexia**  | **Personalized Learning Path**  |
|------------------------|--------------------------------|
| **Mild**              | Reading Passages & Reading Comprehensions |
| **Moderate**          | Reading Passages, Comprehensions & Memory Games |
| **Severe**            | Reading Passages, Comprehensions, Memory Games & Phonological Games |

</div>

### **3. AI Chatbot**
- Creating a text to text chatbot recipe using **Informatica's Application Integration**.
- Creating an **App Connection** and **Process Object** for Gemini Model.
- Using **Assignment** Node to create a prompt for the LLM to respond.
- Using **Sevice** Node to connect to the **App Connection**
- Using another **Assignment** Node to assign the final LLM Response.
- Utilizing **Informatica's Application Integration Console** to get the REST API to integrate with our frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/d75dd984-9839-496d-91e8-4560cb3f5ea9" width="600">
</div>


### **4. Notes Generation**

- Creating a concise notes generation recipe using **Informatica's Application Integration**
- Creating an **App Connection** and **Process Object** for Gemini Model.
- Using **Assignment** Node to first extract the content from the file and then create a prompt for the LLM to respond.
- Using **Sevice** Node to connect to the **App Connection**
- Using another **Assignment** Node to assign the final LLM Response.
- Utilizing **Informatica's Application Integration Console** to get the REST API to integrate with our frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/1c82cf0e-1426-4f57-a37b-38f308588a19" width="600">
</div>


### **5. Mind Map Generation**

- Creating a prompt chaining mind map generation recipe using **Informatica's Application Integration**
- Creating an **App Connection** and **Process Object** for Gemini Model.
- Using **Assignment** Node to create a prompt for the LLM to respond.
- Using **Sevice** Node to connect to the **App Connection**
- Using another **Assignment** Node to assign the final LLM Response.
- This prompt is further chained to get content for multiple nodes of mind map.
- Utilizing **Informatica's Application Integration Console** to get the REST API to integrate with our frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/08dc2e3a-b477-4c01-aaf8-80ab02e62f29" width="600">
</div>

---

## **Informatica's Services**

![image](https://github.com/user-attachments/assets/939fec98-9e7f-44f5-bce9-2e3fb635810a)

### **Data Ingestion**

### **Data Profiling**

### **Data Quality**

### **Data Integration**

### **Model Serve**

### **Application Integration**

### **Application Integration Console**


## **Impact and Benefits for Users**

| **Impact/Benefit**                           | **Description**                                                                                                 |
|----------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **Improved Accessibility**                   | Offers dyslexia-friendly fonts, simplified document views, and multi-language support, enhancing accessibility for diverse users. |
| **Personalized Learning Paths**              | Adapts learning materials and exercises to individual severity levels, improving user engagement and learning outcomes. |
| **Enhanced Learning Support**                | Provides tools like an AI Writing Assistant, phonological improvement activities, and memory games, supporting comprehensive skill development. |
| **Community and Psychological Support**      | Builds a supportive network, connecting dyslexic individuals and psychologists to foster shared understanding and growth. |
| **Time and Cost Efficiency**                 | Reduces dependency on third-party intervention, enabling users to access resources independently and at a lower cost. |




## **Business Relevance & Adoption Model**

LexiEase AI provides a comprehensive solution that can be seamlessly integrated into various business models, making it ideal for companies looking to improve accessibility and inclusivity. Here’s how businesses can adopt and benefit from LexiEase AI:

| **Business Integration**        | **Description**                                                                                                                                                 |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **EdTech Platforms**         | Integrate LexiEase AI as a value-added service to offer personalized dyslexia support, attracting a broader user base and fulfilling inclusivity goals.       |
| **Healthcare Providers**       | Utilize LexiEase AI’s screening and personalized support features to provide early intervention tools for dyslexic patients, adding value to patient care.     |
| **Educational Institutions**   | Schools and universities can adopt LexiEase AI to support dyslexic students with tailored learning aids, enhancing student engagement and performance.          |
| **Corporates & Employers**     | Implement LexiEase AI within corporate learning management systems to ensure inclusive training resources for employees with dyslexia, fostering diversity.    |
| **Non-Profits & NGOs**         | Leverage LexiEase AI to support initiatives aimed at learning disabilities, increasing outreach effectiveness and empowering communities with dyslexia.       |

## **Why Businesses Should Integrate LexiEase AI**
1. **Boost Corporate Social Responsibility (CSR)**: By supporting dyslexic individuals, businesses can demonstrate their commitment to inclusivity and accessibility.
2. **Enhance Brand Image**: Associating with a forward-thinking, inclusive solution enhances brand value and public perception.
3. **Access New User Segments**: Integration opens opportunities to reach individuals and families affected by dyslexia, expanding the customer base.

**LexiEase AI is designed to not only support dyslexic individuals but also provide businesses with a scalable, impactful solution to enhance inclusivity and meet accessibility standards.**

