# CS 690 Assignment 1 Report: Replicating a Controlled Evaluation

## Part 1. Verification evidence

Command:

```text
python -m harness.verify
```

Paste the five `OK` lines here. Keep `results/verification.json` in your repository.

> OK: loaded 20 frozen tasks
> OK: dataset sha256 5d84176547cb679f4145676d1f4dfd5061bf3b9600904911da8e5700e82eee3b
> OK: generated Python executed in Docker sandbox
> OK: candidate network probe was blocked
> OK: model/configuration metadata written to results/verification.json

## Part 2. Tests and code questions

Paste the final summary line of `pytest -q` here.

> .................... [100%]
> 20 passed in 0.97s

Answer each question in your own words, in about 75 to 150 words. Base every answer on the code in this repository, and name the files and functions you describe.

### Q1. The path of one attempt
> Q1. The path of one attempt. Start from one task in tasks/cs690_eval20.json and describe each step until its result becomes one row in results/experiment/raw_results.jsonl. Name the file and function responsible for each step. Explain why the generated code runs inside the Docker sandbox rather than directly on your computer.
Selected task: A1-001
1. The `run` function in `harness/runner.py` is called to start the evaluation.
2. the `load_tasks` function in `harness/task.py` loads the frozen tasks from `cs690_eval20.json` and instantiates a `Task` object for each task. 
3. The task is then passed into the prompt template in `harness/runner.py` to create a prompt string.
4. for each of the runs, the prompt is sent to the model to generate a candidate completion.
5. `grade_candidate` is called to execute the generated candidate code in a sandbox and evaluate it against the test cases for the task.
6. The output is saved to the results JSON

The code is run in a container because its not trusted, and to ensure the environment is consistent. This means that if it works on my computer, it should also work on any other computer with docker set up.

### Q2. What is sent and what comes back
> Q2. What is sent and what comes back. List the settings every request sends, using conditions.json and harness/provider.py, and say in one sentence what each one controls, using the Week 3 definitions. Then list what the harness keeps from each reply. Explain why the requested model name alone would not identify what answered you.

**below is using the doc string from `harness/provider.py` as a starting point. Hope that is okay.**
What is sent, for every request:
* **model**-- the exact model name from conditions.json. For A its gpt-5.6-luna and for B its gpt-5.6-terra
* **the_prompt** -- the task description, wrapped in the fixed template
* **temperature**-- how much randomness is allowed when picking tokens. Bother are set to 1.0 for this assignment
* **top_p**  -- left unset in this assignment. 
* **reasoning effort**   "none", so the model answers without a hidden reasoning step
* **max output tokens**  the longest answer we are willing to pay for. 800 for this assignment

What is kept from the reply (the Generation class below):
* **text**--the answer itself, the part a chat website shows you
* **returned_model**-- the version string the provider says actually answered
* **token counts**   the usage you are billed for
* **stop_reason**-- why the answer ended: finished, or cut off at the limit

What is not kept from the reply:
* **provider** -- the name of the provider, which is not needed to identify the model version
* **requested_model**-- the name of the model we asked for, which is not needed to identify the model version

The requested model name alone would not identify what answered you because the provider may have changed the model version since you requested it, and the provider may have used a different model than the one you requested.

### Q3. Same prompt, different answers
> Q3. Same prompt, different answers. Both conditions use temperature 1.0 and ask for three attempts per problem. Explain why the three attempts on one problem can differ, and why that is intended in this experiment. Then name the files and fields the harness records so that someone else could rerun your experiment and check your work.

Models are probabilistic, meaning that they can produce different outputs for the same input prompt. This can be changed by setting the temperature parameter in the model configuration - as discussed in class. This is intended in this experiment to see how the model performs regardless of the randomness in its output. If it was only run once, we would not know if the model is consistently good or just lucky the one time it ran.

Files and fields recorded by the harness include:
* `results/experiment/raw_results.jsonl` - contains the prompt, the returned model version, the text of the answer, and the token counts for each attempt.
* `results/experiment/summary_A.json` and `results/experiment/summary_B.json` - contain the pass@1 and pass@2 values, model, and token counts for each condition.
* `conditions.json` - contains the requested model, temperature, number of attempts, and other settings for each condition.
* `cs690-a1-controlled-eval/prompts/a1-controlled-eval-fall2026` has all the generated prompts for each task, so that someone else could rerun the experiment and check the work.
* `cs690-a1-controlled-eval/results/experiment/candidates` has all the generated candidates for each task, so that someone else could rerun the experiment and check the work.
* `cs690-a1-controlled-eval/Dockerfile` has the docker configuration for the experiment, so that someone else could rerun the experiment and check the work in the same controlled environment.

### Q4. pass@k by hand
> Q4. pass@k by hand. One task had n = 3 attempts, and c = 1 of them was correct. Using the formula on the slide "pass@k, worked through," compute pass@1 and pass@2 by hand and show your work. Confirm both values with pass_at_k. Then compute the shortcut 1 - (1 - c/n) ** k for k = 2, and use the slide "The version people get wrong" to explain why the two answers differ.
Show your work for pass@1 and pass@2 with n = 3 and c = 1, the values `pass_at_k` returned, and the shortcut `1 - (1 - c/n) ** k` for k = 2.

I had to look up how to get combinations for this - hope thats ok.
Pass@1:
comb(2,1) = 2
comb(3,1) = 3
pass@1 = 1- 2/3 = 1/3

Pass@2:
comb(2,2) = 1
comb(3,2) = 3
pass@2 = 1 - 1/3 = 2/3

k=2 shortcut:
1 - (1 - 1/3) ^ 2 = 1 - (2/3) ^ 2 = 1 - 4/9 = 5/9


### Q5. Why whole problems are redrawn
> Q5. Why whole problems are redrawn. Explain, step by step, what bootstrap_task_ci does. Explain why it draws whole problems instead of individual attempts. Name the test in tests/test_metrics.py that enforces this rule, and explain what that test checks and why it works.

`bootstrap_task_ci` builds a confidence interval for the pass@k score by bootstrapping at the task level.
Steps: 
1. gets the pass@k score for each task
2. gets the pass@k score for randomly drawn tasks to create a fake benchmark
3. uses the fake benchmark to create a confidence interval for the pass@k score


The test that enforces this rule is: `test_task_bootstrap_resamples_tasks_not_candidate_rows`
The test checks that the bootstrap samples entire tasks, not individual candidate attempts. It works because resampling individual attempts would mix the six candidate rows together instead. That would produce scores clustered more closely around the overall 50% success rate, giving a narrower interval.

## Part 3. Replication

Part 3 has no written section. Its evidence is the committed `results/experiment/` and `prompts/` folders, and the dollars you spent, which go in the Part 4 table.

## Part 4. Results

Take every number from `results/experiment/summary_A.json` and `results/experiment/summary_B.json`, not from the console. Dollars spent come from the Usage page of your OpenAI account. If your account does not show them, write `not available`. If it shows only one total for the whole run, write the total in row A and `included in A` in row B.

<!-- | Condition | Requested model | Returned model version | Attempts per task | Total attempts | pass@1 | 95 percent CI for pass@1 | pass@2 | Input tokens | Output tokens | Dollars spent |
| --------- | --------------- | ---------------------- | ----------------: | -------------: | -----: | ------------------------ | -----: | -----------: | ------------: | ------------- |
| A         |                 |                        |                 3 |             60 |        |                          |        |              |               |               |
| B         |                 |                        |                 3 |             60 |        |                          |        |              |               |               | -->
| Condition | Requested model | Returned model version | Attempts per task | Total attempts | pass@1 | 95 percent CI for pass@1 | pass@2             | Input tokens | Output tokens | Dollars spent |
| --------- | --------------- | ---------------------- | ----------------: | -------------: | -----: | ------------------------ | -----------------: | -----------: | ------------: | ------------- |
| A         | gpt-5.6-luna    | gpt-5.6-luna           | 3                 | 60             | 0.95   | 0.8666666666666666       | 0.9833333333333334 | 7146         | 3829          | 0.006024      |
| B         | gpt-5.6-terra   | gpt-5.6-terra          | 3                 | 60             | 1.0    | 1.0                      | 1.0                | 7146         | 4081          | 0.063264      |
### Memo, no more than 500 words, not counting the table

Address all five items:

1. State the observed ranking by pass@1 point estimate.
2. State whether the uncertainty evidence supports ranking the two conditions.
3. If it does not, include the exact sentence: `The evidence does not support a ranking.`
4. State one external-validity limitation specific to `CS690-Eval20`.
5. State one likely source of variance specific to this experiment, and explain why a rerun, or a classmate's run, gives somewhat different numbers.

Overlapping intervals are not a formal significance test, and you are not asked to run one.

## Part 5. Reading a published score, 300 to 400 words

Benchmark chosen (HumanEval, MBPP, LiveCodeBench, or SWE-bench):

Use the benchmark's primary paper or its official documentation for the task definition. Cite evidence for any contamination, saturation, or current-status claim, and date any current-status source.

### 1. What does it measure?

### 2. What does it not measure that a software project may depend on?

### 3. How can a reported score rise without the underlying model becoming better?

### 4. Could the model have seen the answers already?

End with at least one sentence explaining why the published score is not interchangeable with your `CS690-Eval20` result.

## References
