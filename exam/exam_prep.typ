#set page("a4", columns: 1, numbering: "1")
#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true, first-line-indent: 1em)
#set heading(numbering: "1.")

#import "@preview/abbr:0.2.3"

#abbr.load("abbreviations.csv")

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

#let answer-box(width: 1fr, height: auto, color: blue, body) = {
  box(
    width: width,
    height: height,
    inset: 5pt,
    fill: color.lighten(95%),
    stroke: (paint: color, thickness: 1pt, dash: "dashed"),
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

      - #abbr.a[POL]: #writing-area[D]
      - #abbr.a[NLU]: #writing-area[C]
      - #abbr.a[DST]: #writing-area[A]
      - #abbr.a[NLG]: #writing-area[B]
      - #abbr.a[DM]: #writing-area[E]


    + Write the initials (e.g., #abbr.s[DM] for #abbr.lo[DM]) of the dialog component next to the statement that best matches it:

      - Keeps track of the users goals: #writing-area()[#abbr.s[DST]]
      - Historically involved sentence planning and surface realization: #writing-area()[#abbr.s[NLG]]
      - Proposes an assignment of values to slots from an ontology: #writing-area()[#abbr.s[NLU]]
      - Typically learned through reinforcement learning and decides what action to take next: #writing-area()[#abbr.s[POL]]

  ]

  2. Name and provide examples of five types of dialog system applications.
  #answer-box[
    + *Phone-Based Systems*:
      - Example: Banking hotlines (e.g., balance inquiries), public transport info services (e.g., "Let's Go" bus schedule system).
    + *Assistant Apps*:
      - Example: Language learning apps (e.g., Duolingo), navigation tools (e.g., "Spacebook").
    + *Smart Speakers*:
      - Example: Amazon Alexa or Google Home controlling lights, playing music, or answering questions.
    + *Voice-Operated Appliances*:
      - Example: Voice-controlled TVs (e.g., Samsung QLED TVs with Bixby) or smart refrigerators.
    + *Car Systems*:
      - Example: Android Auto or Apple CarPlay for navigation, music control, and phone calls.
  ]

  3. What is turn‑taking in dialog and why is it difficult for a dialog system to handle it? Name and explain at least two reasons.
  #answer-box[
    - *Turn-taking* is the process of alternating speaking turns between speakers in a conversation.
    - Difficulties for dialog systems:
      + *Complex human cues*: Systems may struggle to predict when to respond, leading to interruptions or delays.
      + *Overlaps*: Natural conversations often have overlapping speech, which can confuse systems that expect clear turn boundaries.
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
  \  #answer-box[
    - *Broken maxims*: Quantity, Relation
    - *Implicature*: Person B states too much information and does not answer the question directly, suggesting they did not study enough for the exam.
  ]

  7. Describe *grounding* in dialog systems and name at least two grounding signals, each briefly explained in a sentence.
  #answer-box[
    + *Grounding* ensures mutual understanding.
    + *Grounding signals*:
      - *Implicit*: confirm without state it
      - *Explicit*: confirm message
  ]
  8. What are anaphora and cataphora, and why are they problematic for dialog systems?
  #answer-box[
    - *Anaphora*: refers to entities mentioned earlier in the conversation.
    - *Cataphora*: refers to entities mentioned later in the conversation.
    - *Problematic*: Dialog systems may struggle to resolve these references without sufficient context, leading to misunderstandings or incorrect responses.
  ]
  9. What is adaptation/entrainment in dialog, and in what forms does it take place?
  #answer-box[
    - *Adaptation/Entrainment* refers to the phenomenon where speakers adjust their language, style, or behavior to align with their conversational partner. It can take place in various forms, including:
      - *Lexical entrainment*: using similar words or phrases.
      - *Syntactic entrainment*: adopting similar sentence structures.
      - *Prosodic entrainment*: matching speech rate, tone, and rhythm.
  ]
  10. You have developed a function to measure lexical entrainment over the turns in a conversation. You apply this to a dataset of human–machine conversations with your system and find that over time, the entrainment increases. What does this tell you about your system?
  #answer-box[
    An increase in lexical entrainment over time in human-machine conversations suggests that your system is successfully adapting its word choices to align with those of the human user.
    This indicates that the system is becoming:
    - *More efficient and natural* in the dialogue flow.
    - Likely *enhancing mutual understanding* between the user and the system.
    - Potentially leading to *improved user experience* and preference, as entrainment is a sign of successful interaction and can make the system's responses feel more human-like and cooperative.
  ]
  11. What is the difference between a chatbot and a dialog system?
  #answer-box[
    - A *chatbot* is a system that only response to the inputs relied on static knowledge.
    - A *dialog system* is an interface to an external knowledge source with the main goal is to retrieve information from the knowledge source.
  ]
  12. What is an ontology, and how are the ontology slots distinguished from one another?
  #answer-box[
    - An *ontology* is a structured description of the external knowledge that defines the Domain, Slot, and Value.
    - *Ontology slots* are distinguished by 3 types based on their values:
      - Categorical: one of the possible values
      - Binary: True/False values
      - Non-Categorical: number of values is not limited
  ]
  13. Explain and give examples for the two semantic concepts in dialog acts.
  #answer-box[
    + *intent or dialogue act type*:
      - encodes the system or the user intention in a (part of) dialogue turn
    + *semantic slots and values*:
      - further describe entities from the ontology that a dialogue turn refers to

    #figure(
      image("images/intent_semantic_example.png", width: 80%),
      caption: [
        Examples for the two semantic concepts.
      ],
    )
  ]
  14. Name and explain three challenges in #abbr.a[NLU].
  #answer-box[
    + Spontaneous speech contains mistakes!
      - non-grammatical
      - disfluencies: hesitations, incomplete utterances, self-correction
      - higher #abbr.a[ASR] errors compared to read speech
    + Possibly unlimited ways to express the same meaning
    + User may behave unexpectedly
      - out-of-domain reply?
      - switching to chat-oriented dialogue?
  ]
  15. Name and explain two methods for using #abbr.a[ASR] hypotheses for the #abbr.a[NLU] inputs. Explain why one is more robust than the other. Explain the ways for #abbr.a[NLU] prediction using #abbr.a[ASR] hypotheses.
  #answer-box[
    + *Top #abbr.a[ASR] hypothesis*: Features are extracted directly from single best hypothesis and the classification is performed into relevant semantic classes.
    + *N-best list of #abbr.a[ASR] hypothesis*: Uses multiple #abbr.a[ASR] hypotheses to provide a more comprehensive input for #abbr.a[NLU].

    - N-best list of #abbr.a[ASR] hypothesis is *more robust* because it incorporates uncertainty in #abbr.a[ASR] output, reducing the chance of #abbr.a[NLU] errors.

    - *#abbr.a[NLU] prediction using #abbr.a[ASR] hypotheses*: the goal is to obtain $p(d|a)$, which is the probability of a dialogue act $d$ given the audio signal $a$. It is achieved by the following ways:
      + Sum it up
        $
          p(d|a) = sum_(i=1)^N p(d|t_i)p(t_i|a)
        $
        where $t_i$ is the N-best list
      + Train #abbr.a[ASR] and #abbr.a[NLU] jointly
      + Use separate encoders and combine the embeddings for final prediction
  ]
  16. Give an example of a word confusion network for #abbr.a[ASR] and explain its benefit.
  #figure(
    image("images/word_confusion.png", width: 80%),
    caption: [
      A word confusion network example.
    ],
  )
  #answer-box[
    - *Benefit*: It allows #abbr.a[NLU] systems to consider multiple interpretations of the input, improving robustness against #abbr.a[ASR] errors.
  ]
  17. Explain how #abbr.a[NLU] can be formulated as a sequence-to-sequence learning task.
  #answer-box[
    - #abbr.a[NLU] can be formulated as a sequence-to-sequence learning task by treating the input utterance as a sequence of tokens and the output as a sequence of semantic representations, such as dialog acts or slot-value pairs.
  ]
  18. What is #abbr.a[MLM]?
  #answer-box[
    - *Masked Language Modeling* is a self-supervised learning technique where certain tokens in a sentence are masked, and the model learns to predict them based on the surrounding context.
  ]
  19. Name two challenges for modular dialog system architecture and explain the hybrid approach as its solution.
  #answer-box[
    + *Challenges*:
      - Modular approaches suffer from information loss between the components.
      - Labeled data not always available to train individual modules.
    + *Hybrid approach*:
      - Combines modular and end-to-end approaches to leverage the strengths of both.
      - Allows for flexibility in component design while ensuring overall system coherence.
  ]
  20. What is delexicalization, and why is it useful?
  #answer-box[
    - *Delexicalization* is the process of replacing specific values in a dialog system with placeholders, allowing the system to generalize across different instances of the same dialog act.
    - *Usefulness*: It helps solve data sparsity.
  ]
  21. What are some challenges associated with dialog state tracking? Name at least four.
  #answer-box[
    *Challenges*:
    - Process long context.
    - Remember past information.
    - Infer/Extract implicit information.
    - Solve coreference.
  ]
  22. Explain the two main approaches to dialog state tracking.
  #answer-box[
    + *Picklist-based*: Given full ontology, perform prediction over slot-value pairs. Good performance on small datasets, but difficult to scale.
    + *Span-based*: Directly extract slot values from dialogue context. No need for candidate pairs, but struggles with more subtle cases such as implicit choice.
  ]
  23. What are the automatic and human metrics that can be used for #abbr.a[NLG]? (Name three for each and explain.)
  #answer-box[
    - *Automatic metrics*:
      - *#abbr.a[BLEU]*: is a precision-based metric that compares n-gram overlap between generated text and reference text.
      - *#abbr.a[ROUGE]*: is a recall-based metric that compares n-gram overlap between generated text and reference text.
      - *BERTScore*: Measures contextual embedding similarity.
    - *Human metrics*:
      - *Naturalness*: Evaluates how natural and grammatically correct the generated text is.
      - *Informativeness*: Compare the relevance between the generated text and the input or context.
      - *Coherence*: Measures how logically consistent and well-structured the generated text is.
  ]
  24. What is the interpretation of perplexity as an #abbr.a[NLG] metric?
  #answer-box[
    - *Perplexity* is a measure of how well a language model predicts a sample. The lower the perplexity, the less confused the model is in making its predictions
  ]
  25. What is the main difference between BERTScore and other metrics, such as #abbr.a[ROUGE] and #abbr.a[METEOR], in #abbr.a[NLG] evaluation?
  #answer-box[
    - *BERTScore* measures the semantic similarity between generated text and reference text by comparing their contextual embeddings
    - *#abbr.a[ROUGE]* and *#abbr.a[METEOR]* focus on n-gram overlap.
  ]
  26. Explain three things one must consider when evaluating a dialog system with volunteers.
  #answer-box[
    + *Volunteer Recruitment*: recruit volunteers from a variety of demographics.
    + *Dialogue Task Design*: must be carefully designed.
    + *Researcher Interference*: Researcher should not interfere with the interaction.
  ]
  27. Name and explain three evaluation factors to be included in the questionnaire of human evaluators for task-oriented and chat-oriented systems.
  #answer-box[
    - *Task-oriented systems*:
      + *Repetition*: How repetitive was the system?
      + *Making sense:*: How often did the system say something which did NOT make sense?
      + *Fluency*: How grammatical was the language?
    - *Chat-oriented systems*:
      + *Interestingness*: How interesting or boring did you find this conversation?
      + *Inquisitiveness*: How much did the user try to get to know you?
      + *Engagement*: How much did you enjoy talking to this user?
  ]
  28. What are the advantages and disadvantages of crowd-sourcing? Name two for each.
  #answer-box[
    - *Advantages*:
      - Scaling up and speeding up evaluation.
      - Reduced cost.
    - *Disadvantages*:
      - Reduced quality of interactions.
      - Difficultly controlling who enters the experiment.
  ]
  29. How does a data-driven automatic dialog measure work, and what are its problems?
  #answer-box[
    - *Data-driven automatic dialog measure* can be trained from a human-labeled dataset with scores. The model then predict the evaluation score for an unseen dialogue.
    - *Problems*: domain-dependence, lack of interpretability, single output, susceptibility to adversarial attacks
  ]
  30. What are the benefits and drawbacks of using prompting for dialog evaluation?
  #answer-box[
    - *Benefits*:
      - Intuitive, can express more nuanced criteria.
      - Time and cost effective.
      - More and more powerful models now available.
    - *Drawbacks*:
      - Result may be model and prompt dependent.
      - #abbr.pla[LLM] have biases, optimizing for #abbr.a[LLM] evaluation may create a feedback loop that exacerbates these biases.
      - Data contamination.
  ]
  31. What are the two main features of an ideal evaluation metric?
  #answer-box[
    + Automatic and thus repeatable.
    + Correlates highly with human judgement.
  ]
  32. What is the antibiotic effect in the context of dialog evaluation metrics?
  #answer-box[
    - The *antibiotic effect* is the phenomenon where optimization on one fixed automatic metric can lead to models that exploit weaknesses in the metric rather than truly improving performance.
  ]
  33. Name and explain the factors that make an #abbr.a[NLG] system good.
  #answer-box[
    + *Adequacy*: correct meaning.
    + *Fluency*: linguistic fluency.
    + *Readability*: fluency in dialogue context.
    + *Variation*: multiple realisations for the same concept.
  ]
  34. What is the pros and cons of a template-based natural language generator?
  #answer-box[
    - *Pros*: simple, usually error free, controllable
    - *Cons*: time consuming, rigid, not scalable
  ]
  35. Name and explain the components of the trainable generator pipeline (by Walker).
  #answer-box[
    + *Sentence plan generator*:
      - Produces multiple sentence plans for a given dialogue act (or set of dialogue acts) and governs which information should be given in which order.
    + *Sentence plan reranker*:
      - Ranks possible candidates.
    + *Surface realiser*:
      - Turns the top candidate into an utterance.
  ]
  36. How does class-based language modeling work for #abbr.a[NLG]?
  #answer-box[
    - *Classes*:
      #[
        - _inform_area_
        - _inform_address_
        - _inform_phone_
        - _request_area_
        - ...
      ]

    - *Generation process*:
      + Generate utterances by sampling words from a particular class language model in which the dialogue act belongs to.
      + Re-rank utterances according to scores.
  ]

  37. How does an #abbr.a[RNN] improve #abbr.a[NLG] over its predecessors? In other words, what are its main features?
  #answer-box[
    - An #abbr.a[RNN] as a language generator improves over its predecessors due to its natural ability to model sequences.

    - Main features:
      - *Handling Long-Term Dependencies*
      - *Flexibility to Condition on Auxiliary Inputs*
  ]
  38. How does #abbr.a[LSTM] prevent the vanishing gradient problem?
  #answer-box(color: red)[
    #align(center)[#text(red)[[ Needs some rework ]]]

    - Consider memory cell, where recurrence actually happens:
      $
        C_t = i_t ⊙ Ĉ_t + f_t ⊙ C_(t - 1)
      $
    - We can back-propagate the gradient by chain rule:
      $
        (∂ E_t) / (∂ C_(t - 1))
        =
        (∂ E_t) / (∂ C_t)
        (∂ C_t) / (∂ C_(t - 1))
        =
        ((∂ E_t) / (∂ C_t)) f_t
      $
  ]

  39. Why can a semantically conditioned #abbr.a[LSTM] be better than a non-conditional #abbr.a[LSTM]?
  #answer-box[
    - A semantically conditioned #abbr.a[LSTM] can be better than a non-conditional #abbr.a[LSTM] because it incorporates additional semantic information into the generation process, allowing it to produce more contextually relevant and coherent responses.
    - This conditioning helps the model to focus on specific aspects of the dialog state, leading to improved performance in generating appropriate utterances.
  ]

  40. What distinguishes #abbr.s[GPT]-3 from earlier #abbr.a[GPT] models?
  #answer-box[
    - Effectively the same model structure with substantially more parameters and training data:

    #table(
      columns: 4,
      inset: .75em,
      align: center + horizon,

      [], [#abbr.a[GPT]], [#abbr.a[GPT]-2], [#abbr.a[GPT]-3],
      [Parameters], [117M], [1.5B], [175B],
      [Data], [12GB], [40GB], [570GB],
    )
  ]

  41. What is a major drawback of #abbr.a[GPT], as well as semantically conditioned #abbr.a[GPT]?
  #answer-box[
    - *Cons*: produces hallucinations
  ]

  42. What are the three key elements in each dialog turn in dialog management?
  #answer-box[
    + *Actions*: What the system says.
    + *States*: What the user wants.
    + *Observations*: What the system hears.
  ]

  43. What are the three main challenges in modeling dialog, and how does defining it as a control problem provide a solution?
  #answer-box[
    + How to define the state space?
    + How to tractably maintain the dialogue state?
    + Which actions to take?

    - *Solution*: Define dialogue as a control problem where the behaviour can be automatically learned.
  ]

  44. How is dialog management framed in a #abbr.a[MDP]?
  #answer-box(color: red)[
    #align(center)[#text(red)[[ Needs some rework ]]]

    + *Data*:
      - Dialogue states
      - Reward: a measure of dialogue quality
    + *Model*:
      - Markov decision process
    + *Predictions*:
      - Optimal system actions

    #line(length: 100%, stroke: (paint: blue, thickness: 1pt, dash: "dashed"))

    - *$s_t$*:  dialogue states
    - *$a_t$*:  system actions
    - *$r_t$*:  rewards
    - *$p(s_(t+1) | s_t, a_t)$*: transition probability
  ]

  45. What is the main difference between generative and discriminative models in belief tracking?
  #answer-box[
    - *Discriminative models*: focus on the relationship between observations and states without modeling how the observations were generated.
    - *Generative models*: model both the states and the observations, considering how states generate observations. The probability of the state depends on how likely it is that this state generated the given observation, combined with our prior belief about the state itself.
  ]

  46. Why is exact belief tracking intractable in partially observable #abbr.a[MDP]-based dialog systems?
  #answer-box[
    Requires summation over all possible states at every dialogue turn - *intractable*!
  ]

  47. Name and explain three requirements for belief tracking.
  #answer-box[
    + *Dialogue history*: The system needs to keep track of what happened so far in the dialogue. This is normally done via the *Markov property*.
    + *Task-orientated dialogue*: The system needs to know what the user wants. This is modelled via the *user goal*.
    + *Robustness to errors*: The system needs to know what the user says. This is modelled via the *user act*.
  ]

  48. What is the #abbr.a[HIS] model in dialog systems, and how does it address the challenges of belief tracking in partially observable environments?
  #answer-box[
    - The #abbr.a[HIS] model is a practical framework for #abbr.a[POMDP]-based spoken dialogue management.

    - It addresses the challenges of belief tracking in partially observable environments by structuring the belief state around several components:
      + *Observation*: N-best list of user acts
      + *User Goal*: Partitions of the goal space built according to ontology
      + *Dialogue history*: Grounding states
      + *Hypotheses*: Every combination of user act, partition and history

    - *Belief state*: Distribution over most likely hypotheses
  ]

  49. What is the #abbr.a[BUDS] model, and how does it improve upon previous approaches like the #abbr.a[HIS] model in belief tracking?
  #answer-box[
    - The #abbr.a[BUDS] model is an advancement in #abbr.a[POMDP] frameworks for spoken dialogue systems.

    - Improve upon previous approaches by:
      - Further decomposes the dialogue state
      - Produces tractable belief state update
      - Transition and observation probability distributions can be parametrized and their shape learned
  ]

  50. Why is grounding important in open-domain dialog systems?
  #answer-box[
    - Prevent hallucinations and improve factual accuracy
    - Improve trustworthiness and transparency
    - Respond accurately on dynamic or rare topics
  ]

  51. What is #abbr.a[RAG], and how does it work? Name and explain its two main components.
  #answer-box[
    - (#abbr.a[RAG]) is a framework that enhances generation models with real-time document retrieval.

    - Main components:
      + *Retriever*: Finds relevant documents based on input query
      + *Generator*: Produces the final response using retrieved docs
  ]
  52. What is the key advantage of separating the retriever from the generator in #abbr.a[RAG] systems?
  #answer-box[
    - Up-to-date knowledge without retraining
  ]

  53. Name two advantages of #abbr.a[RAG] systems over traditional end-to-end language models.
  #answer-box[
    + Fewer hallucinations with citation-worthy sources
    + Modular: swap retriever/generator independently
  ]

  54. What are the four pipeline stages in a #abbr.a[RAG] system?
  #answer-box[
    + Encode user input to query embedding
    + Retrieve top-k documents (using #abbr.a[DPR], BM25, etc.)
    + Concatenate each document with query
    + Generate response using encoder-decoder model (BART, T5)
  ]

  55. What are three limitations of #abbr.a[RAG] systems?
  #answer-box[
    + Slow response due to retrieval latency
    + Noisy or irrelevant documents degrade output
    + Generator might ignore retrieved text
  ]

  56. How can retriever quality be improved in #abbr.a[RAG] systems?
  #answer-box[
    - Use dense retrievers (e.g., #abbr.a[DPR], ColBERT) over sparse (e.g. BM25)
    - Fine-tune retriever on dialog queries
    - Rerank candidates with cross-encoder models
  ]

  57. What are two techniques to improve alignment between the generator and retrieved knowledge?
  #answer-box[
    + Train with gold-grounded responses
    + Use contrastive learning between relevant and irrelevant docs
    + Penalize hallucinations with #abbr.a[RLHF] or fact-checking signals
  ]

  58. What are the three key evaluation metrics for grounded dialog?
  #answer-box[
    + *Faithfulness*: Is it factually accurate?
    + *Relevance*: Is it context-appropriate?
    + *Attribution*: Does it cite or reflect the retrieved source?
  ]

  59. What is the potential risk of #abbr.a[RAG] systems in open-domain dialog?
  #answer-box[
    - *Leakage of private data*, if the external datastore used by the #abbr.a[RAG] system contains sensitive or private information, there is a risk that this data could be retrieved and inadvertently exposed in the system's responses.
    - Could still produce *hallucinations or misleading information* if the retrieved data itself is incorrect, biased, or misinterpreted by the language model.
  ]

  60. Name and explain three reasons why open-domain dialog is more challenging than task-oriented dialog.
  #answer-box[
    + *Unlimited topics*: Users can ask about anything
    + *Ambiguity*: Same phrase can have many meanings
    + *Context management*: Conversations span multiple turns
    + *Lack of grounding*: Risk of hallucinating information
  ]

  61. Why are generic responses like "I don't know" problematic in chatbot conversations, and how can they be mitigated?
  #answer-box[
    - *Problem*: Safe defaults like "I don't know" or "That's interesting."
      - Reduce user engagement
      - Perceived as evasive or boring

    - *Mitigation*:
      - Penalize frequent responses in decoding (frequency penalties)
      - Use top-k/top-p sampling to promote lexical diversity
      - Train with contrastive or adversarial losses for engaging answers
  ]

  62. What are three ways to mitigate hallucination in dialog systems?
  #answer-box[
    + Incorporate retrieval-based grounding (#abbr.a[RAG])
    + Post-generation fact checking modules
    + Human feedback training to penalize factual errors
  ]

  63. What is a major risk when a chatbot loses context in multi-turn conversations, and what are two ways to mitigate it?
  #answer-box[
    - *Problem*: Bots lose track of user preferences or dialog history
      - Responses feel disconnected
      - Violates consistency, especially for multi-turn dialog

    - *Mitigation*:
      - Use long-context transformers (e.g. Longformer, #abbr.a[GPT] with memory)
      - Add dialog memory modules
      - Use dialog history explicitly as input
  ]

  64. What types of errors fall under pragmatic errors in chatbot responses, and what are three ways to mitigate such errors?
  #answer-box[
    - *Problem*: Bot says things that are socially or contextually inappropriate
      - Fails to detect sarcasm, humor, formality
      - Lacks understanding of politeness or indirectness

    - *Mitigation*:
      - Train on datasets annotated for tone, register
      - Use style-conditioned generation
      - Explicit modeling of Grice’s Maxims
  ]

  65. How can chatbots mitigate toxic or biased responses?
  #answer-box[
    - Filter training data using toxicity classifiers
    - Post-process outputs with safety layers
    - #abbr.a[RLHF]
  ]

  66. Why is it difficult for chatbots to handle multi-intent utterances like ‘Book a flight to Tokyo and what’s the weather there?’
  #answer-box[
    - *Problem*: Users combine multiple intents in one utterance
    - *Example*: “Book me a flight to Tokyo and what’s the weather there?”
      - Requires multi-task understanding
      - Potentially separate dialog states

    - *Mitigation*:
      - Semantic parsing into sub-tasks
      - Intent detection + follow-up prompts
  ]

  67. What distinguishes a retrieval-based language model from a standard language model?
  #answer-box[
    - It retrieves from an external datastore (at least during inference time)
  ]

  68. Give five reasons why we need retrieval-based language models.
  #answer-box[
    + #abbr.pla[LLM] can't memorize all (long-tail) knowledge in their parameters
    + #abbr.pla[LLM]' knowledge is easily outdated and hard to update
    + #abbr.pla[LLM]' output is challenging to interpret and verify
    + #abbr.pla[LLM] are shown to easily leak private training data
    + #abbr.pla[LLM] are *large* and expensive to train and run
  ]

  69. What are the three main design questions for retrieval-based language models?
  #answer-box[

    #grid(
      columns: 3,
      inset: .75em,
      align: horizon,

      [*1. What to retrieve?*], [*2. How to use retrieval?*], [*3. When to retrieve?*],
      [
        - Chunks
        - Tokens
        - Others
      ],
      [
        - Input layer
        - Intermediate layers
        - Output layer
      ],
      [
        - Once
        - Every n tokens (n>1)
        - Every token
      ],
    )

  ]

  70. What is the main idea behind k#abbr.s[NN]-#abbr.s[LM]?
  #answer-box[
    - A different way of using retrieval, where the #abbr.s[LM] outputs a nonparametric distribution over every token in the data.
    - Can be seen as an incorporation in the “output” layer
  ]

  71. Give an advantage and a disadvantage of fine-tuning in adapting an #abbr.a[LM] to downstream tasks.
  #answer-box[
    - *Advantages*:
      - Customizable
      - Competitive w/ more data
    - *Disadvantages*:
      - Requiring training
  ]

  72. Give an advantage and a disadvantage of reinforcement learning in adapting an #abbr.a[LM] to downstream tasks.
  #answer-box[
    - *Advantages*:
      - Better alignment with user preferences
    - *Disadvantages*:
      - Requiring additional data collection (preference)
  ]

  73. Give an advantage and a disadvantage of retrieval-based prompting.
  #answer-box[
    - *Advantages*:
      - No training & strong performance
    - *Disadvantages*:
      - Hard to control, underperforming full #abbr.a[FT] model
  ]

  74. Name and explain three methods for adapting a retrieval-based #abbr.a[LM] for downstream tasks.
  #answer-box[
    + *Fine-tuning*:
      - Involves *training the #abbr.a[LM] and/or the retriever on task-specific data and a datastore*. Fine-tuning can be done on both the retriever and the #abbr.a[LM], or just the query-side of the retriever while fixing the index.
    + *Reinforcement learning*:
      - Uses *human feedback to optimize the language model's policy*. Instead of relying solely on supervised fine-tuning, #abbr.a[RL] allows the model to learn to present information and align with human preferences for aspects like helpfulness, honesty, and harmlessness.
    + *Prompting*:
      - Involves *providing retrieved knowledge as part of the input context to a frozen (pre-trained) #abbr.a[LM]*. It does not require additional training of the #abbr.a[LM] on downstream tasks.
  ]

  75. Name and explain four key effectiveness points in downstream tasks for retrieval-based LMs.
  #answer-box[
    + *Long-tail*:
      - #abbr.pla[LLM] often struggle in *long-tail/less frequent entities*. Scaling #abbr.pla[LLM] only helps for *popular knowledge*; for long tail, scaling gives marginal performance improvements Retrieval gives large performance gain in such *long-tail*. Largely reduce hallucinations in *long-form generations*.
    + *Knowledge update*:
      - Standard #abbr.pla[LLM] need to be *trained again* to adapt to evolving world knowledge. Swapping the knowledge corpus to *accommodate temporal changes* without additional training.
    + *Verifiability*:
      - *Much smaller LMs with retrieval* can outperform much larger LMs in fact completions.
    + *Parameter-efficiency*:
      - Human and model can reliably assess the *factuality of the generations* using the retrieved evidence.
  ]

  76. Name and explain five scenarios when retrieval-based LMs should be used.
  #answer-box[
    + When the task requires frequent updates.
    + When access to long-tail or less popular knowledge is crucial.
    + When high verifiability is required.
    + When the parameter efficiency is a priority.
    + When the privacy of data is a concern.
  ]
  77. What is an agent?
  #answer-box[
    An *agent* is artificial entity that enhance #abbr.pla[LLM] with essential capabilities enabling them to sense their environment, make decisions, and take actions.
  ]
  78. Name and explain the two competing views on agents.
  #answer-box[
    + *#abbr.a[LLM]-first view*: We make an #abbr.a[LLM] into an agents!
      - Implications: scaffold on top of #abbr.a[LLM], prompting-focused, heavy on engineering
    + *Agent-first view*: We integrate #abbr.a[LLM] into #abbr.a[AI] agents so they can use language for reasoning and communication!
      - Implications: All the same challenges faced by previous #abbr.a[AI] agents (e.g., perception, reasoning, world models, planning) still remain, but we need to *re-examine them through the new lens of #abbr.a[LLM]* and tackle new ones (e.g., synthetic data, self-reﬂection, internalized search)
  ]
  79. What is the fundamental difference between current and classic agents?
  #answer-box[
    Contemporary #abbr.a[AI] agents, with integrated #abbr.a[LLM]\(s), can use language as a vehicle for reasoning and communication
  ]
  80. Name three types of #abbr.a[AI] agents and compare them in terms of expressiveness, reasoning and adaptivity.
  #answer-box[
    #table(
      columns: 4,
      inset: .75em,
      align: center + horizon,

      [], [Logical Agent], [Neural Agent], [Language Agent],
      [Expressiveness], [Low], [Medium], [High],
      [Reasoning], [Logical inferences], [Parametric inferences], [Language-based inferences],
      [Adaptivity], [Low], [Medium], [High],
    )
  ]
  81. Name and explain three methods that can be used to teach #abbr.a[LLM] how to properly use tools.
  #answer-box[
    + *Tutorial Learning*:
      - Have model tuned for tool use read tool manuals (tutorials), so that it understands the functions of the tool and how to invoke them
      - Works well with powerful #abbr.a[LLM]
    + *Reinforcement Learning*:
      - Autonomous exploration and correction of errors based on environmental feedback through reinforcement learning
      - Action space defined by tools
      - Agent learns to select appropriate tool
      - Correct action maximize reward signal
    + *Self-supervised Tool Learning*:
      - Pre-defined tool APIs
      - Encourage models to call and execute tool APIs
      - Design self-supervised loss to evaluate tool execution helpfulness
  ]
  82. What is the ReAct agent, and what are its benefits?
  #answer-box[
    - The *ReAct agent* is a new paradigm of agents that reason and act to achieve tasks.
    - *Benefits*:
      - Synergy of Reasoning and Acting.
      - Simple and intuitive to use.
      - General across domains.
  ]
  83. What are the four components of the unified framework for #abbr.a[LLM] agents?
  #answer-box[
    + *Profile*
    + *Memory*
    + *Planning*
    + *Action*
  ]
  84. What is multi-agent orchestration, and why do we need it?
  #answer-box[
    - *Multi-agent orchestration* is the process of managing multiple agents to work together effectively.
    - We need it to:
      + Enable collaboration between agents.
      + Improving scalability and robustness when dealing with complex tasks.
      + Optimize resource allocation and task distribution.
  ]
  85. Give two examples of a multi-agent system and explain how they work.
  #answer-box[
    + *Multi-Agent Coding*:
      - Commander receives user questions and executes code
      - Writer writes code
      - Safeguard ensures no information leakage or malicious code
    + *Decision Making*:
      - Two agents: One suggests next step, Executor does action and provides feedback
      - Three agents: additional agent that provides commonsense facts about the domain when needed
  ]
  86. What are two potential risks of multi-agent systems, and why are they difficult to deal with?
  #answer-box[
    + Leaking private data
    + Causing financial loss.

    - They difficult to deal with because Identifying these risks is labor-intensive as testing becomes difficult with increased agent complexity.
  ]
  87. What is #abbr.a[LLM] alignment, and why is it important?
  #answer-box[
    - *#abbr.a[LLM] alignment* is a learning phase where they learn how to present information to users and align to human preferences.
    - It is important because it helps prevent harmful or unintended consequences, ensuring that LLMs act in ways that are beneficial and safe for users.
  ]
  88. How does #abbr.a[PPO] work, and what are its two benefits?
  #answer-box[
    - *#abbr.a[PPO]* is a reinforcement learning algorithm that optimizes the policy of an agent by balancing exploration and exploitation.
    - *Benefits*:
      + Prevents mode collapse to single high reward answers.
      + Prevents the model from deviating too far from the distribution where the reward model is accurate.
  ]
  89. What are three drawbacks of #abbr.a[PPO]?
  #answer-box[
    + Need to train multiple models
      - Reward model
      - Policy model
    + Needs sampling from Language model during fine-tuning.
    + Complicated reinforcement learning training process.
  ]
  90. How does #abbr.a[DPO] improve upon #abbr.a[PPO]?
  #answer-box[
    *#abbr.a[DPO]* improves upon #abbr.a[PPO] by directly optimizing the policy based on preference data, rather than relying on a reward model.
  ]
  91. What is #abbr.l[RLHF]?
  #answer-box[
    *#abbr.a[RLHF]* is a method that combines reinforcement learning with human feedback to train language models, allowing them to align with human preferences and improve their performance in generating responses.
  ]
  92. What are the challenges of the _human feedback_ in #abbr.a[RLHF]?
  #answer-box[
    - *Biases of human evaluators*:
      - Studies found that ChatGPT became politically biased after #abbr.a[RLHF]
    - *Good oversight is difficult*:
      - Evaluators are paid per example and may make mistakes given time constraints
      - Poor feedback when evaluating difficult tasks
    - *Data Quality*:
      - Cost/Quality tradeoff
    - *Tradeoff between richness and efficiency of feedback types*:
      - Comparison-based feedback, scalar feedback, correction feedback, language feedback, …
  ]
  93. What are the challenges of the _reward model_ in #abbr.a[RLHF]?
  #answer-box[
    - A single reward model cannot represent a diverse society of humans.
    - Reward misgeneralization: reward model may fit with human preference data due to unexpected features.
    - Evaluation of reward model is difficult and expensive.
  ]
  94. What are the challenges of the _policy_ in #abbr.a[RLHF]?
  #answer-box[
    - Robust reinforcement learning is difficult
      - Balance between exploring new actions and exploiting known rewards
      - Challenge increases in high-dimensional or sparse reward settings
    - Policy misgeneralization: training and deployment environments are different
  ]
  95. Name and explain the three key concepts for language agents.
  #answer-box[
    + *Reasoning*: The ability to update short-term memory.
    + *Memory*: The capacity to store and retrieve information.
    + *Planning*: The algorithm to choose an action from the action space.
  ]
  96. Why are reasoning and acting helpful for agents?
  #answer-box[
    - *Reasoning* helps agents to make informed decisions based on the current context and available information.
    - *Acting* allows agents to take actions that can change the environment or achieve specific goals, enabling them to interact effectively with users and systems.
  ]
  97. How do #abbr.a[LLM] agents have short-term and long-term memories, and what are they most useful for?
  #answer-box[
    - *Short-term memory*: This is primarily the context window of the #abbr.a[LLM].
      - Most useful for reasoning.
    - *Long-term memory*: retains knowledge and experiences over time, enabling the agent to learn from past interactions and improve future performance.
      - Most usefull for retrieving and learning.
  ]
  98. Name and explain three planning paradigms for language agents. Give an advantage and a drawback for each.
  #answer-box[
    + *Reactive*: Combines reasoning and acting in a single framework.
      - *Advantage*: fast, easy to implement.
      - *Drawback*: greedy, short-sighted.
    + *Tree Search with Real Interactions*: Breaks down complex tasks into smaller, manageable steps.
      - *Advantage*: systematic exploration.
      - *Drawback*:  irreversible actions, unsafe, slow.
    + *Model-Based Planning*: Organizes actions into a hierarchy of goals and sub-goals.
      - *Advantage*: faster, safer, systematic exploration.
      - *Drawback*: relies on the accuracy and generalizability of the world model.
  ]
  99. What are the advantages of code agents?
  #answer-box[
    + Can perform complex tasks that require programming skills.
    + Can automate repetitive tasks, saving time and effort.
    + Can handle large datasets and perform data analysis efficiently.
    + Can integrate with various APIs and services to extend functionality.
  ]
  100. What is the purpose of the #abbr.a[MCP]?
  #answer-box[
    The purpose of the #abbr.a[MCP] is to dramatically reduce integration complexity and maintenance burden when building #abbr.a[AI] applications that interact with various tools and data sources. It achieves this by:
    - Defining a standard protocol where each #abbr.a[AI] application implements the client side of #abbr.a[MCP] only once.
    - Requiring each tool or data source to implement the server side of #abbr.a[MCP] only once.
  ]
]

#abbr.list()
