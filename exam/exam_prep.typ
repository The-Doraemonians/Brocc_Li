#set page("a4", columns: 1, numbering: "1")
#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true, first-line-indent: 1em)
#set heading(numbering: "1.")

#place(top + center, scope: "parent", float: true, [

  #text(size: 14pt)[
    Dialog Systems Exam Sample Questions
  ]

  July 10, 2025

  #figure(
    image("images/task_oriented_dialog_system.png", width: 70%),
    caption: "Task-oriented Dialog System",
  )<fig:task-oriented-dialog-sys>
])

#let writing-area(height: 1em, width: 2em, body) = {
  let length = width

  box(width: width, height: height, align(center + bottom)[
    #align(top)[#body]
    #line(stroke: 1pt, length: length)
  ])
}

#let answer-box(width: 1fr, height: auto, body) = {
  box(
    width: width,
    height: height,
    inset: 5pt,
    fill: blue.lighten(95%),
    stroke: (paint: blue, thickness: 1pt, dash: "dashed"),
    radius: 3pt,
    [
      #body
    ],
  )
}


#[
  1. Examine the task-oriented dialog system in @fig:task-oriented-dialog-sys. Assume the system uses text and not speech.

  #[
    #set enum(numbering: "(a)", indent: 1em)

    + Write the letter of the corresponding component next to each name:

      - (POL) Dialog Policy: #writing-area()[D]
      - (NLU) Natural Language Understanding: #writing-area()[C]
      - (DST) Dialog State Tracking: #writing-area()[A]
      - (NLG) Natural Language Generation: #writing-area()[B]
      - (DM) Dialog Manager: #writing-area()[E]


    + Write the initials (e.g., DM for Dialog Manager) of the dialog component next to the statement that best matches it:

      - Keeps track of the users goals: #writing-area()[]
      - Historically involved sentence planning and surface realization: #writing-area()[]
      - Proposes an assignment of values to slots from an ontology: #writing-area()[]
      - Typically learned through reinforcement learning and decides what action to take next: #writing-area()[]

  ]

  2. Name and provide examples of five types of dialog system applications.
  #answer-box[
    + *Task-oriented*:
      - Example: Booking a flight, ordering food, scheduling appointments.
    + *Open-domain conversation*:
      - Example: Casual conversation, customer support, mental health chatbots.
    + *Information-seeking*:
      - Example: Answering questions about weather, news, or general knowledge.
    + *Personal assistant*:
      - Example: Setting reminders, managing calendars, controlling smart home devices.
    + *Educational*:
      - Example: Tutoring systems, language learning assistants, interactive quizzes.
  ]

  3. What is turn‑taking in dialog and why is it difficult for a dialog system to handle it? Name and explain at least two reasons.
  #answer-box[

  ]
  4. How is speech different from text for dialog systems? Name five differences.
  #answer-box[
    Natural speech is very different from written text:
    + *ungrammatical*
    + *restarts, hesitations, corrections*
    + *overlaps*
    + *pitch, stress*
    + *accents, dialect*
  ]
  5. Name and explain five types of speech acts.
  #answer-box[
    + *Assertive*: Speaker commits to the truth of a proposition.
      - Example: "It’s raining outside."
    + *Directive*: Speaker wants the listener to do something.
      - Example: "Stop it!"
    + *Commissive*: Speaker commits to doing something themselves.
      - Example: "I’ll come by later."
    + *Expressive*: Speaker expresses their psychological state.
      - Example: "Thank you!"
    + *Declarative*: Speaker performs actions using performative verbs.
      - Example: "You’re fired!"
  ]
  6. Given the following exchange between A and B, which of Grice’s maxims is most clearly broken? What is the implicature of this broken maxim?

  #[
    #set enum(numbering: "(a)", indent: 1em)
    + Person A: Did you study enough for the exam?

    + Person B: I was so busy yesterday. I spent almost the entire day cleaning my house!

    Circle the maxim and describe the implicature below:

    #align(center)[Quantity, Quality, Relation, Manner]

  ]


  7. Describe *grounding* in dialog systems and name at least two grounding signals, each briefly explained in a sentence.

  8. What are anaphora and cataphora, and why are they problematic for dialog systems?

  9. What is adaptation/entrainment in dialog, and in what forms does it take place?

  10. You have developed a function to measure lexical entrainment over the turns in a conversation. You apply this to a dataset of human–machine conversations with your system and find that over time, the entrainment increases. What does this tell you about your system?

  11. What is the difference between a chatbot and a dialog system?

  12. What is an ontology, and how are the ontology slots distinguished from one another?

  13. Explain and give examples for the two semantic concepts in dialog acts.
  #answer-box[
    + *intent or dialogue act type*:
      - encodes the system or the user intention in a (part of) dialogue turn
    + *semantic slots and values*:
      - further describe entities from the ontology that a dialogue turn refers to
  ]
  14. Name and explain three challenges in NLU.
  #answer-box[
    + Spontaneous speech contains mistakes!
      - non-grammatical
      - disfluencies: hesitations, incomplete utterances, self-correction
      - higher ASR errors compared to read speech
    + Possibly unlimited ways to express the same meaning
    + User may behave unexpectedly
      - out-of-domain reply?
      - switching to chat-oriented dialogue?
  ]

  15. Name and explain two methods for using ASR hypotheses for the NLU inputs. Explain why one is more robust than the other. Explain the ways for NLU prediction using ASR hypotheses.

  16. Give an example of a word confusion network for ASR and explain its benefit.

  17. Explain how NLU can be formulated as a sequence-to-sequence learning task.

  18. What is MLM (Masked Language Modeling)?

  19. Name two challenges for modular dialog system architecture and explain the hybrid approach as its solution.

  20. What is delexicalization, and why is it useful?

  21. What are some challenges associated with dialog state tracking? Name at least four.

  22. Explain the two main approaches to dialog state tracking.

  23. What are the automatic and human metrics that can be used for NLG? (Name three for each and explain.)

  24. What is the interpretation of perplexity as an NLG metric?

  25. What is the main difference between BERTScore and other metrics, such as ROUGE and METEOR, in NLG evaluation?

  26. Explain three things one must consider when evaluating a dialog system with volunteers.

  27. Name and explain three evaluation factors to be included in the questionnaire of human evaluators for task-oriented and chat-oriented systems.

  28. What are the advantages and disadvantages of crowd-sourcing? Name two for each.

  29. How does a data-driven automatic dialog measure work, and what are its problems?

  30. What are the benefits and drawbacks of using prompting for dialog evaluation?

  31. What are the two main features of an ideal evaluation metric?

  32. What is the antibiotic effect in the context of dialog evaluation metrics?

  33. Name and explain the factors that make an NLG system good.

  34. What is the pros and cons of a template-based natural language generator?

  35. Name and explain the components of the trainable generator pipeline (by Walker).

  36. How does class-based language modeling work for NLG?

  37. How does an RNN network improve NLG over its predecessors? In other words, what are its main features?

  38. How does LSTM prevent the vanishing gradient problem?

  39. Why can a semantically conditioned LSTM be better than a non-conditional LSTM?

  40. What distinguishes GPT-3 from earlier GPT models?

  41. What is a major drawback of GPT, as well as semantically conditioned GPT?

  42. What are the three key elements in each dialog turn in dialog management?

  43. What are the three main challenges in modeling dialog, and how does defining it as a control problem provide a solution?

  44. How is dialog management framed in a Markov Decision Process (MDP)?

  45. What is the main difference between generative and discriminative models in belief tracking?

  46. Why is exact belief tracking intractable in partially observable MDP-based dialog systems?

  47. Name and explain three requirements for belief tracking.

  48. What is the Hidden Information State (HIS) model in dialog systems, and how does it address the challenges of belief tracking in partially observable environments?

  49. What is the Bayesian Update of Dialogue State (BUDS) model, and how does it improve upon previous approaches like the Hidden Information State (HIS) model in belief tracking?

  50. Why is grounding important in open-domain dialog systems?

  51. What is Retrieval-Augmented Generation (RAG), and how does it work? Name and explain its two main components.

  52. What is the key advantage of separating the retriever from the generator in RAG systems?

  53. Name two advantages of RAG systems over traditional end-to-end language models.

  54. What are the four pipeline stages in a RAG system?

  55. What are three limitations of RAG systems?

  56. How can retriever quality be improved in RAG systems?

  57. What are two techniques to improve alignment between the generator and retrieved knowledge?

  58. What are the three key evaluation metrics for grounded dialog?

  59. What is the potential risk of RAG systems in open-domain dialog?

  60. Name and explain three reasons why open-domain dialog is more challenging than task-oriented dialog.

  61. Why are generic responses like ‘I don’t know’ problematic in chatbot conversations, and how can they be mitigated?

  62. What are three ways to mitigate hallucination in dialog systems?

  63. What is a major risk when a chatbot loses context in multi-turn conversations, and what are two ways to mitigate it?

  64. What types of errors fall under pragmatic errors in chatbot responses, and what are three ways to mitigate such errors?

  65. How can chatbots mitigate toxic or biased responses?

  66. Why is it difficult for chatbots to handle multi-intent utterances like ‘Book a flight to Tokyo and what’s the weather there?’

  67. What distinguishes a retrieval-based language model from a standard language model?

  68. Give five reasons why we need retrieval-based language models.

  69. What are the three main design questions for retrieval-based language models?

  70. What is the main idea behind kNN-LM?

  71. Give an advantage and a disadvantage of fine-tuning in adapting an LM to downstream tasks.

  72. Give an advantage and a disadvantage of reinforcement learning in adapting an LM to downstream tasks.

  73. Give an advantage and a disadvantage of retrieval-based prompting.

  74. Name and explain three methods for adapting a retrieval-based LM for downstream tasks.

  75. Name and explain four key effectiveness points in downstream tasks for retrieval-based LMs.

  76. Name and explain five scenarios when retrieval-based LMs should be used.

  77. What is an agent?

  78. Name and explain the two competing views on agents.

  79. What is the fundamental difference between current and classic agents?

  80. Name three types of AI agents and compare them in terms of expressiveness, reasoning and adaptivity.

  81. Name and explain three methods that can be used to teach LLMs how to properly use tools.

  82. What is the ReAct agent, and what are its benefits?

  83. What are the four components of the unified framework for LLM agents?

  84. What is multi-agent orchestration, and why do we need it?

  85. Give two examples of a multi-agent system and explain how they work.

  86. What are two potential risks of multi-agent systems, and why are they difficult to deal with?

  87. What is LLM alignment, and why is it important?

  88. How does Proximal Policy Optimization (PPO) work, and what are its two benefits?

  89. What are three drawbacks of PPO?

  90. How does Direction Preference Optimization (DPO) improve upon PPO?

  91. What is Reinforcement Learning from Human Feedback (RLHF)?

  92. What are the challenges of the _human feedback_ in RLHF?

  93. What are the challenges of the _reward model_ in RLHF?

  94. What are the challenges of the _policy_ in RLHF?

  95. Name and explain the three key concepts for language agents.

  96. Why are reasoning and acting helpful for agents?

  97. How do LLM agents have short-term and long-term memories, and what are they most useful for?

  98. Name and explain three planning paradigms for language agents. Give an advantage and a drawback for each.

  99. What are the advantages of code agents?

  100. What is the purpose of the Model Context Protocol (MCP)?
]
