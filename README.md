# How to use
## Update config.yaml 
Add your OPENAI_ENDPOINT and OPENAI_API_KEY

The reasoning models will take considerably more time and tokens. I've adjusted the MAX_TOKENS to 16k for these models. Otherwise the regular chat models should do just fine on 1k or 2k tokens.

## Update problem.py
Put your problem statement and method_header in this file.

The infra relies on running tests on different generated solutions until the tests pass. Hence it will munch on tokens. I'd adjust the max_solutions accordingly - I suggest max_solutions=5 for reasoning models and max_solutions=15 for chat (normal) models

## Run clientChat.py
clientChat.py contains the main client built for normal OpenAI API endpoints. client.py uses TabbyAPI's completion endpoint. The message formats are slightly different and are seen in promptsChat.py and prompts.py respectively.

The client will first generate a python test script. You must manually validate the test script before proceeding. Do not assume the test script is written correctly.

Next the client will generate (default: 15) max_solutions with a timeout of 10 minutes to generate an answer.

Then it will run the test.py script against each solution with a timeout of 10 seconds.

If a solution is found, the client will break out of the code. Otherwise it will send a debug message and regenerate an answer.

# Problems & TODOs
## Test Script Output Ordering
Imagine a problem where the output doesn't need to be in-order
The test script either needs to convert both outputs into sets and/or sort the array outputs and compare.

Furthermore I'm unsure how graph problems will go.

## Reasoning
I've seen great results with the o3-mini and deepseek-reasoner models. I can copy the o3-mini reasoning block and add it to my query to further improve results with normal chat models.

I want to figure out a way to incorporate "reasoning" into my models without directly using o3-mini and deepseek-reasoner and keeping everything local. The current plan is to use Deepseek-R1-Distill-Llama-70B to generate "reasoning" about a question. This model has a problem with terminating and is very verbose. An intermediate step could include taking the verbose output and summarizing with an intermediate step (to produce something like o3-mini reasoning block.)

## Code Examples
Too many examples in the context might confuse the model. I can setup a RAG database and pull in relevant LC problems and solutions that are similar to the problem.

