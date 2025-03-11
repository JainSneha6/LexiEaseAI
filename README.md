# **LexiEase AI - An AI Powered Dyslexic Support System**

**LexiEase AI** is an AI-powered system that offers personalized learning support for individuals with dyslexia. The platform provides dyslexia screening, tailored learning paths, and various assistive tools to improve accessibility and enhance learning outcomes for dyslexic individuals. 

## **Introduction**

**LexiEaseAI is an AI-powered learning platform** designed to enhance cognitive skills, reading abilities, and academic performance through personalized assessments and interactive tools. 

**Supported by Informatica’s secure and scalable infrastructure, it ensures a seamless and efficient learning experience.**

<div align="center">
  <img src="https://github.com/user-attachments/assets/972384a0-ec2a-475c-8b75-f906afb1a0d6" width="800">
</div>

---

## **What Problems Does LexiEase AI Solve?**

1. **Limited Access to Dyslexia Screening**  
   Many individuals with dyslexia struggle to get timely and affordable screenings, leading to delayed interventions and missed educational opportunities.

2. **Lack of Personalized Learning Paths**  
   Traditional learning resources are not tailored to the unique needs of dyslexic learners, making it harder for them to achieve their full potential in conventional educational settings.

3. **Insufficient Support Tools for Dyslexic Learners**  
   Dyslexic individuals often lack access to specialized tools, like writing assistants and document simplifiers, that can make reading and learning more accessible and enjoyable.

<div align="center">
  <img src="https://github.com/user-attachments/assets/41df37ef-b19d-44c2-a87d-3d80c068fa6c" width="800">
</div>

---

## **List Of Features**

<div align="center">
  <img src="https://github.com/user-attachments/assets/a48e2245-9911-4ff3-b6a6-57d4b171c2d1" width="800">
</div>

<div align="center">
  <img src="https://github.com/user-attachments/assets/c6be600b-8771-495d-9a81-269325103a36" width="800">
</div>

### **1. Dyslexic Screening Test**

- **Phonological Awareness Test**
  - Providing easy, medium and hard words from various CSVs of Phoneme, Irregular, Multisyllable and Nonsensical to check their phonological awareness.
  - The CSVs are ingested to **Snowflake tables** using **Informatica's Data Ingestion**
  - **Informatica's Data Profiling** is done to get Claire's insights on the data along with the null & distinct percentages.
  - The words are provided to them in an audio format coverted using Google Text To Speech.
  - The written word is checked against the audio word and a score is calculated.

<div align="center">
  <img src="https://github.com/user-attachments/assets/f000c4ae-f281-4454-a12b-e20eb0bf8055" width="600">
</div>

- **Gray Oral Reading Test**
  - Providing easy, medium and hard words from Reading Passages CSV.
  - Data is ingested into **Snowflake tables** using **Informatica's Data Ingestion**.
  - **Informatica's Data Profiling** is done to get Claire's insights on the data along with the null & distinct percentages.
  - Rule Specifications and Cleansing of the data was done using **Informatica's Data Quality**
  - Creating mappings of the data by using Data Quality Assets & Aggregates using **Informatica's Data Integration**.
  - Linear Regression based model to calculate the fluency based on various parameters using **Informatica's Model Serve**
  - A fluency rating is then provided to the user.

<div align="center">
  <img src="https://github.com/user-attachments/assets/c674c08c-cecb-4e27-b234-23729834e6a6" width="600">
</div>

---

### **2. Personalized Learning Path**

<div align="center">

| **Level of Dyslexia**  | **Personalized Learning Path**  |
|------------------------|--------------------------------|
| **Mild**              | Reading Passages & Reading Comprehensions |
| **Moderate**          | Reading Passages, Comprehensions & Memory Games |
| **Severe**            | Reading Passages, Comprehensions, Memory Games & Phonological Games |

</div>

---

### **3. AI Chatbot**
- Creating a text to text chatbot recipe using **Informatica's Application Integration**.
- Creating an **App Connection** and **Process Object** for Gemini Model.
- Using **Assignment** Node to create a prompt for the LLM to respond.
- Using **Service** Node to connect to the **App Connection**
- Using another **Assignment** Node to assign the final LLM Response.
- Utilizing **Informatica's Application Integration Console** to get the REST API to integrate with our frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/957a6763-9b68-40d2-a2da-e539bf356f88" width="600">
</div>

---

### **4. Notes Generation**

- Creating a concise notes generation recipe using **Informatica's Application Integration**
- Creating an **App Connection** and **Process Object** for Gemini Model.
- Using **Assignment** Node to first extract the content from the file and then create a prompt for the LLM to respond.
- Using **Service** Node to connect to the **App Connection**
- Using another **Assignment** Node to assign the final LLM Response.
- Utilizing **Informatica's Application Integration Console** to get the REST API to integrate with our frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/9ad6f8ac-5220-45c8-b503-6ca95399f248" width="600">
</div>

---


### **5. Mind Map Generation**

- Creating a prompt chaining mind map generation recipe using **Informatica's Application Integration**
- Creating an **App Connection** and **Process Object** for Gemini Model.
- Using **Assignment** Node to create a prompt for the LLM to respond.
- Using **Service** Node to connect to the **App Connection**
- Using another **Assignment** Node to assign the final LLM Response.
- This prompt is further chained to get content for multiple nodes of mind map.
- Utilizing **Informatica's Application Integration Console** to get the REST API to integrate with our frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/5e48308f-0925-476c-94ca-8cab05d1f502" width="600">
</div>

---

### **6. Chat with Document**

- A RAG based recipe for asking queries related to uploaded documents using **Informatica's Application Integration**
- Creating a **VectorMatchEntry Process Object** for matching the vector entries.
- Creating a **App Connection** to Gemini & another to the Pinecone DB.
- Creating the base process **Query LLM with Context Using Embeddings Model** that
    - First sets the LLM models and calls the **Generate Embeddings Model** subprocess
    - Then sets the context & query for the LLM model and calls the **Query LLM Gemini** subprocess
    - Finally outputs the response taking into consideration the required context.
- Creating the **Query LLM Gemini** process that
    - First assigns the request using an **Assignment** Node
    - Then uses a **Service** node to connect to the **Gemini App Connection**
    - Finally assigns the LLM response using another **Assignment** Node.
- Creating the **Generate Embeddings Model** process that
    - First calls the **Create Embedding Model** subprocess
    - Then calls the **Pinecone Query** subprocess
    - Finally outputs the context in the form of metadata of the matching vectors.
- Creating the **Pinecone Query** process that
    - First creates the request using an **Assignment** Node
    - Then uses a **Service** Node to connect to the **Pinecone App Connection**
    - Finally outputs the matching vector embeddings using a final **Assignment** Node.
- Creating the **Create Embedding Model** process that
    - First prepares the embeddings request using an **Assignment** Node
    - Then uses a **Service** Node to generate embeddings using the **Gemini App Connection**
    - Finally setting the embeddings using an **Assignment** Node.

<div align="center">
  <img src="https://github.com/user-attachments/assets/7db769c2-9f2d-4325-8291-5d42b23d7129" width="600">
</div>

---

## **Informatica's Services**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/91bc1eba-2848-4d75-b424-0cdcbe108b8a" width="800">
</div>

### **Data Ingestion**  
Data ingestion is the first step in any data pipeline, enabling organizations to collect, import, and transfer data from diverse sources into a centralized system. Informatica provides seamless ingestion from databases, cloud storage, IoT devices, APIs, and streaming platforms. With support for batch and real-time processing, users can efficiently extract data while maintaining high performance and scalability.  

---

#### **1. Ingesting Reading Passages CSV into Snowflake Table**  
<p align="center">
  <img src="https://github.com/user-attachments/assets/e587c996-cb99-4104-b3e0-f62f825bd6fe" width="49.7%" />
  <img src="https://github.com/user-attachments/assets/a21a414b-444d-46bf-830b-cd221c89abb3" width="49.7%" />
</p>  

The process starts by ingesting a **Reading Passages CSV file** into a Snowflake table. The first image shows the ingestion pipeline setup, while the second image confirms the successful data load into Snowflake.  

---

#### **2. Ingesting Phoneme Words CSV into Snowflake Table**  
<p align="center">
  <img src="https://github.com/user-attachments/assets/d9ee25b8-0dd5-4ae9-bf22-f9a6bb9f085f" width="49.7%" />
  <img src="https://github.com/user-attachments/assets/01e06a17-7972-41d2-889e-a03a049beae8" width="49.7%" />
</p>  

Here, a **Phoneme Words CSV file** is being ingested into Snowflake. The left image displays the data pipeline configuration, and the right image verifies that the data has been successfully loaded into the database.  

---

#### **3. Ingesting Irregular Words CSV into Snowflake Table**  
<p align="center">
  <img src="https://github.com/user-attachments/assets/e08eae70-1b78-45df-b65b-05b8dd7fce1d" width="49.7%" />
  <img src="https://github.com/user-attachments/assets/72752864-6d45-4358-ab77-5410d181c2d2" width="49.7%" />
</p>  

The ingestion of an **Irregular Words CSV file** into Snowflake is demonstrated. The left-side image shows the ingestion workflow, while the right-side image confirms that the data has been properly ingested into the target table.  

---

#### **4. Ingesting Multisyllable Words CSV into Snowflake Table**  
<p align="center">
  <img src="https://github.com/user-attachments/assets/eeb89f85-ffcd-43a0-8ff1-ab34aad702e8" width="49.7%" />
  <img src="https://github.com/user-attachments/assets/121528d9-fb93-4991-8c4b-70daca4a8872" width="49.7%" />
</p>  

This step involves ingesting a **Multisyllable Words CSV file** into Snowflake. The first image highlights the ETL process, while the second image confirms that all records have been successfully inserted into the Snowflake table.  

---

#### **5. Ingesting Nonsensical Words CSV into Snowflake Table**  
<p align="center">
  <img src="https://github.com/user-attachments/assets/b0b531e9-ae81-43f1-89d6-fe00de47eefe" width="49.7%" />
  <img src="https://github.com/user-attachments/assets/97bad476-20ba-49de-bf53-f0e79cce1c3e" width="49.7%" />
</p>  

Finally, a **Nonsensical Words CSV file** is ingested into Snowflake. The left image represents the data pipeline setup, while the right image displays the Snowflake table populated with the newly ingested data.  

---

### **Data Profiling**  
Understanding the quality, structure, and relationships within your data is critical before analysis and integration. Informatica’s data profiling tools provide deep insights into data patterns, completeness, accuracy, and potential inconsistencies.  

---

#### **Performing Data Profiling on Reading Passages CSV**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/5b25aeab-c2eb-464d-ba84-16a2bb42c37d" width="800">
</div>  

The first image displays the **initial data profiling process** for the Reading Passages CSV file. Here, Informatica scans the dataset to analyze column structure, data types, and overall completeness. It helps identify any anomalies, such as missing values, duplicates, or unexpected data formats.  

---

<div align="center">
  <img src="https://github.com/user-attachments/assets/59e2fa3c-2be6-4e87-9d71-691b3913fc0a" width="800">
</div>  

The second image presents the **detailed profiling results**, highlighting key statistics such as minimum and maximum values, null percentages, unique value distribution, and patterns in the dataset. This information is crucial for assessing data quality before proceeding with integration, transformation, or analytics.  

---

### **Data Quality**  
Ensuring high-quality data is essential for analytics, reporting, and compliance. Informatica's data quality solutions cleanse, standardize, and enrich data to improve accuracy, completeness, and reliability.  

---

#### **Cleansing Reading Passages CSV**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/88f2035a-d528-41ca-af47-fa1a8c4ebfce" width="800">
</div>  

The first image illustrates the **data cleansing process** for the Reading Passages CSV file. Informatica applies transformation rules to detect and fix inconsistencies such as missing values, incorrect formatting, and invalid entries. This step ensures that the dataset is accurate and structured before further processing.  

---

#### **Rule Specification for Reading Passages CSV**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/1fae2329-5b2d-4e88-9852-f80ecede477d" width="800">
</div>  

The second image shows the **rule specification stage**, where custom validation rules are defined to enforce data quality standards. These rules may include checks for duplicate entries, standardized formatting, and constraints to ensure data integrity. This step helps maintain a clean and consistent dataset for analysis and reporting.  

---

### **Data Integration**  
Organizations deal with vast amounts of data from various sources, making seamless integration a necessity. Informatica's data integration solutions enable real-time and batch processing of data across on-premises, cloud, and hybrid environments.  

Key Features:  
- Support for ETL (Extract, Transform, Load) and ELT (Extract, Load, Transform)  
- Scalable data pipelines with high-performance processing  
- Pre-built connectors for cloud applications, databases, and APIs  
- Real-time streaming and batch data integration capabilities

---

### **Model Serve**  
Informatica’s Model Serve simplifies the deployment and management of machine learning models at scale. It ensures that AI-driven insights are seamlessly integrated into business applications and workflows for predictive analytics and automation.  

---

#### **Linear Regression Model to Predict Fluency Rating**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/c2b671f6-a097-4eaf-9c7f-80469ce8b51a" width="800">
</div>  

The image showcases the **deployment of a Linear Regression model** designed to predict fluency ratings based on various input parameters. This model processes structured data to generate fluency scores, enabling automated assessments and insights.  

Informatica’s Model Serve allows seamless deployment of this machine learning model, ensuring real-time inference, optimized performance, and easy integration with existing data pipelines. This setup supports efficient decision-making

---

### **Application Integration**  
Modern enterprises rely on multiple applications to drive business operations. Informatica’s application integration services enable seamless connectivity between applications, APIs, and services across diverse environments.  

---

#### **1. AI Text-to-Text Chatbot Recipe**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/0b7dbe16-6538-4c75-a5a2-0dc25d2e995d" width="1000">
</div>  

The first image illustrates an **AI-powered Text-to-Text Chatbot integration** using Informatica’s application integration services. This chatbot leverages APIs and workflow automation to process user queries, generate responses, and facilitate seamless conversational AI experiences. The integration ensures real-time interactions while maintaining high reliability and security.  

---

#### **2. Prompt Chaining Mind Map Generation Recipe**  

<div align="center">
  <img src="https://github.com/user-attachments/assets/74b10d91-107d-4482-9774-5a3cbf75289d" width="1000">
</div>  

The second image demonstrates a **Prompt Chaining Mind Map Generation** workflow. This setup allows multiple AI-generated responses to be linked together in a structured way, creating a mind map representation of ideas. By integrating different AI models and APIs, Informatica enables dynamic and automated content generation to enhance brainstorming, research, and decision-making processes.  

---

### **Application Integration Console**  
Managing complex integrations across multiple applications requires visibility and control. Informatica’s Application Integration Console provides a centralized platform to monitor, manage, and troubleshoot integration workflows.  

Key Features:  
- Real-time monitoring of application integration processes  
- Proactive alerts and error handling for quick issue resolution  
- Performance analytics and reporting for optimization  
- Role-based access control for secure management  

---

With Informatica’s powerful suite of services, businesses can ensure high-quality, integrated, and actionable data to drive decision-making, innovation, and operational efficiency.  




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

