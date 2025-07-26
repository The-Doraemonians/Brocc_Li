#set page("a4", columns: 2, numbering: "1")
#set text(font: "New Computer Modern")
#set par(justify: true, first-line-indent: 1em)
#set heading(numbering: "1.")

#place(
  top + center,
  scope: "parent",
  float: true,
  [
    Dialog Systems (MA-INF 4238) -- Summer Semester 2025

    #text(size: 14pt)[
      *Brocc Li* \
      *Your Personalized Diet Management Companion*
    ]

    #grid(
      columns: (1fr, 1fr),
      inset: (y: 5pt),
      [
        Nijat Sadikhov \
        50186266 \
        #link("mailto:s05nsadi@uni-bonn.de", "s05nsadi@uni-bonn.de")
      ],
      [
        Omar Elsebaey \
        50357345 \
        #link("mailto:s28oelse@uni-bonn.de", "s28oelse@uni-bonn.de")
      ],
      [
        Qingyu Zhao \
        50357949 \
        #link("mailto:s18qzhao@uni-bonn.de", "s18qzhao@uni-bonn.de")
      ],
      [
        Viet Dung Nguyen \
        50348141 \
        #link("mailto:s18vnguy@uni-bonn.de", "s18vnguy@uni-bonn.de")
      ],
    )

    #datetime.today().display("[month repr:long] [day], [year]")
  ],
)


#heading(numbering: none)[Abstract]

Maintaining a healthy diet is a significant challenge for many, often due to a lack of personalized, accessible, and affordable guidance. This report details the design and implementation of Brocc Li, a personalized diet management companion developed to address this gap. Brocc Li utilizes a large language model (LLM) agent built on a modular, tool-based architecture. The system takes user-specific inputs—such as age, dietary goals, and restrictions—and leverages a suite of specialized tools to perform tasks including preference extraction, recipe searching via web scraping, and nutritional analysis. The primary outputs are comprehensive 7-day meal plans, cost-effective shopping lists, and detailed diet reports with actionable recommendations. Evaluation with test users yielded positive feedback on the system's utility and user-friendliness. However, the project also highlighted key challenges, primarily the data reliability issues inherent in web scraping and the computational complexity of real-time planning. This report discusses these findings, the system's architecture, and outlines a roadmap for future work focused on enhancing data source reliability and optimizing algorithmic performance.

Check the Github repo for more details.
#footnote[https://github.com/The-Doraemonians/Brocc_Li]


#heading(numbering: none, level: 2)[Keywords]

Personalized diet, dialog systems, LLM agent, tool use, health management


= Introduction <sec:introduction>

The pursuit of a healthy lifestyle is a universal goal, yet many individuals struggle to maintain a balanced diet. The reasons are multifaceted, ranging from a lack of knowledge about nutrition to the difficulty of balancing dietary needs with budget, convenience, and personal taste. Existing solutions often provide generic advice that fails to account for an individual's unique circumstances, such as specific health goals (e.g., weight loss, muscle gain), dietary restrictions (e.g., vegetarian, gluten-free), and financial constraints. This creates a clear need for an accessible, affordable, and user-friendly diet management solution that can deliver truly personalized guidance.

To address this problem, we developed Brocc Li, a personalized diet management companion. The project's central objective was to create an intelligent agent capable of generating tailored diet plans that are both nutritionally sound and practical for the user. By leveraging the advanced natural language understanding and generation capabilities of modern Large Language Models (LLMs), Brocc Li aims to act as a personal diet assistant, simplifying the complex process of meal planning and grocery shopping.

This paper documents the journey of creating Brocc Li, from its initial concept to its implementation and evaluation. We begin by detailing the system's architecture and the methods employed in its construction, focusing on its tool-based agent design. We then present the results achieved, including the types of outputs the system generates. Subsequently, we engage in a discussion of our findings, analyzing both the successes and the limitations encountered during the project, particularly regarding data acquisition and computational performance. Finally, we conclude by summarizing our work and proposing concrete directions for future enhancements.

= Materials & Methods <sec:materials-and-methods>

The methodology behind Brocc Li is rooted in a modular, agent-based architecture designed to systematically process user needs and generate a complete dietary solution. The overall process can be broken down into four key stages, as illustrated in Figure 1.
#image("image1.png")
Figure 1: High-level system methodology. 

The process flows from initial user input to the final exported report, passing through analysis and planning stages.

*User Input*: The system first collects essential information from the user. This includes demographic data (e.g., age), health metrics (e.g., weight, height), dietary goals (e.g., 'lose weight'), and specific dietary restrictions or preferences (e.g., 'vegetarian'). This information is structured into a simple data format for internal processing.

*Search & Analyze*: Using the user's profile, the agent begins a comprehensive search and analysis phase. This involves web scraping for relevant recipes that match the user's preferences and sourcing local store data to estimate costs and ingredient availability. Simultaneously, nutritional information is gathered and analyzed to ensure the proposed meals align with the user's health objectives.

*Generate Diet Plan*: Based on the analyzed data, the agent constructs a personalized 7-day diet plan. This is an optimization task where the agent balances nutritional targets, cost-effectiveness, and user preferences.

*Export Report*: The final output is compiled into user-friendly documents, including the detailed meal plan, a corresponding shopping list, and a nutritional report with recommendations.

2.1 Agent Architecture

At the core of Brocc Li is a tool-using LLM agent. Instead of a single, monolithic model, our system employs a central agent that orchestrates a collection of specialized "tools." Each tool is a distinct function designed to perform a specific task. This modular architecture, shown in Figure 2, provides flexibility and allows for easier debugging and expansion.

The agent was built using a state-graph framework, with the Gemini-2.5-flash model from Google serving as the core reasoning engine. The agent's main role is to interpret the user's request, decide which tool (or sequence of tools) is needed to fulfill it, and execute them accordingly.

#image("image2.png")
Figure 2: The agent architecture of Brocc Li. 

A central agent utilizes a suite of specialized tools to handle different aspects of the diet planning process.

2.2 Tool Implementation

The key to the system's functionality lies in its tools. The following are the primary tools developed for this project:

*Extract Preferences Tool*: This tool parses the initial user input to create a structured profile. It identifies and categorizes key information like goals and restrictions, making it machine-readable for other tools.
Calculate BMI Tool: A straightforward utility that calculates the Body Mass Index based on user-provided height and weight, providing a baseline health metric.

*Web Scraping Tools*: A set of functions responsible for dynamically searching for and extracting recipe information and grocery prices from various online sources. This was a critical but challenging component due to the inconsistent structure of websites.

*Report and List Generation Tools*: These tools leverage the LLM's generative capabilities. They take the structured data (user preferences, selected recipes, nutritional analysis) and synthesize it into human-readable outputs:
Generate Diet Report: Creates a comprehensive summary of the diet plan, including nutritional breakdowns and health recommendations.

*Generate Shopping List*: Compiles all necessary ingredients from the 7-day meal plan into an organized list.
The tools were defined as Python functions and integrated into the agent's framework. The LLM was prompted to use these functions to achieve its goals, effectively delegating specific tasks to the appropriate module.

= Results <sec:results>

The development of Brocc Li successfully produced a functional prototype capable of delivering on its core promise: personalized diet management. The system's effectiveness was measured by its ability to generate useful, coherent outputs and through qualitative feedback from test users.

*3.1 System Outputs*

The primary results of the system are the tangible outputs it generates for the user.
Generated Personalized 7-Day Meal Plans: The system successfully created week-long meal plans tailored to individual user profiles. For a user aiming for weight loss with a vegetarian restriction, the plan would consist of three balanced, low-calorie vegetarian meals per day, complete with recipes and preparation instructions. An example of a single day's plan is shown in Table 1.

Table 1: Sample one-day meal plan for a vegetarian user.
#table(
  columns: 3,
  table.header[Meal][Dish][Est. Calories],
  [Breakfast], [Greek Yogurt with Berries], [300],
  [Lunch], [Quinoa Salad with Chickpeas], [450],
  [Dinner], [Lentil and Vegetable Stew], [500],
)



Provided Cost-Effective Shopping Lists: By integrating scraped recipe data with local store information, the system generated organized shopping lists. These lists were designed to be cost-effective by grouping ingredients and prioritizing commonly available items.

Delivered Nutritional Analysis with Recommendations: For each generated meal plan, Brocc Li produced a report detailing its nutritional content (e.g., macronutrient ratios, key vitamins, and minerals). The report also included simple, actionable recommendations, such as "Ensure adequate water intake" or "Consider adding a vitamin B12 supplement," based on the user's profile and the generated plan.

*3.2 Evaluation*

To assess the system's real-world utility, we conducted informal testing with a small group of users. They were asked to provide their personal data and evaluate the outputs.

Positive Feedback from Test Users: The feedback was largely positive. Users found the meal plans to be relevant and appreciated the convenience of having a complete plan and shopping list generated automatically. The personalized nature of the recommendations was highlighted as a key strength compared to generic diet apps.

Identified Areas for Improvement: The evaluation also confirmed some of the system's limitations. The most frequently cited issue was the accuracy of the data sourced from web scraping. Occasionally, recipes had incorrect ingredient quantities, or price estimates were outdated. This feedback was crucial in identifying data reliability as a primary area for future improvement.

= Discussion <sec:discussion>

The development of Brocc Li provides valuable insights into both the potential and the challenges of using LLM agents for complex, real-world applications like personalized health management.

*4.1 Interpretation of Results*

The successful generation of coherent and personalized diet plans validates our choice of a tool-based agent architecture. This modular approach proved to be highly effective. The LLM excelled at the "soft" tasks of understanding user intent and generating natural language reports, while the specialized tools handled the "hard", deterministic tasks like calculations and data extraction. This division of labor is a powerful paradigm for building robust AI systems. The positive user feedback further suggests that there is a strong demand for such personalized tools and that our system's outputs were perceived as genuinely useful.

*4.2 Challenges and Limitations*

Despite the successes, the project was not without its challenges. The two most significant limitations were data reliability and computational complexity.

Limited Data Reliability from Web Scraping: Our reliance on web scraping for recipe and pricing information was the system's Achilles' heel. Websites frequently change their layout, breaking the scrapers. Furthermore, the data itself is often unstructured and can be inconsistent or inaccurate (e.g., a recipe blog missing nutritional information). This unreliability directly impacts the quality of the generated diet plans and shopping lists, making it the single most critical issue to address.

Computational Complexity in Real-time Planning: Generating a fully optimized 7-day plan is computationally intensive. The process involves multiple LLM calls, extensive web scraping, and solving a complex optimization problem to balance nutrition, cost, and preference. This resulted in processing times that were not suitable for a real-time, interactive experience. The current implementation is better suited for an "offline" generation model where the user submits a request and receives the plan after a few minutes.

These challenges highlight a trade-off: the flexibility of web scraping comes at the cost of reliability, and the depth of personalization comes at the cost of real-time performance.


#heading(numbering: none)[Conclusions]

*5.1 Conclusions*

This project successfully demonstrated the feasibility of creating a personalized diet management companion, Brocc Li, using a tool-based LLM agent. The system is capable of interpreting user needs and generating customized 7-day meal plans, shopping lists, and nutritional reports. The modular architecture proved to be a robust and extensible framework for this task. While the prototype was well-received by users, its practical application is currently limited by challenges in data reliability and computational performance. Brocc Li serves as a strong proof-of-concept that lays the groundwork for a more polished and reliable consumer-facing product.

*5.2 Future Work*

Based on the challenges identified, we have outlined a clear path for future development to evolve Brocc Li from a prototype into a production-ready system.

Enhance Data Sources for Better Reliability: The highest priority is to move away from fragile web scraping. Future versions should integrate with stable, structured data sources via APIs. This includes using dedicated nutritional databases (e.g., USDA FoodData Central, Edamam) for accurate food information and partnering with grocery retailers or data aggregators for reliable pricing and availability data.

Optimize Algorithms for Real-time Performance: To make the system more interactive, performance must be improved. We plan to explore several optimization strategies, such as:
Caching: Caching common recipes and nutritional data to reduce redundant lookups.
Pre-computation: Pre-processing and storing a large database of recipes to enable faster searching.
Model Optimization: Using smaller, fine-tuned models for specific, repetitive tasks instead of relying on a large, general-purpose LLM for everything.

Expand Functionality and User Interaction: Once the core system is more robust, we can expand its capabilities. This includes supporting a wider range of dietary preferences (e.g., paleo, keto, food allergies), integrating with fitness trackers to dynamically adjust plans based on activity levels, and developing a more sophisticated conversational interface for a truly interactive "dialog system" experience.

#heading(numbering: none)[Acknowledgements]

We would like to extend our gratitude to the entire project team for their dedicated contributions. Specifically, we thank Qingyu Zhao for his work on agent pipelining and report generation; Viet Dung Nguyen and Nijat Sadikhov for their efforts in agent pipelining and UI design; and Omar Elsebaey for his programming of the web scraping modules and agent pipeline.

#bibliography("references.bib", title: "References")
