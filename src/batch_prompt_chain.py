import sys
sys.path.append(r"C:\Users\silvh\OneDrive\lighthouse\Ginkgo coding\content-summarization\src")
from summary_chain import *
from response_processing import *
from article_processing import create_text_dict_from_folder
from file_functions import *
import time
import traceback

# Create text dictionary
folder_path = '../text/2023-06-20 discussion' # ** UPDATE REQUIRED**

encoding='ISO-8859-1'
subset=None

text_dict = create_text_dict_from_folder(folder_path, encoding=encoding, subset=subset)

# Set parameters
iteration_id = 1
n_choices = 2
pause_per_request=0
# summary_iteration_id = iteration_id
chatbot_id = iteration_id
model = 'gpt-3.5-turbo-16k-0613'

# Create prompt lists

system_role = "You are a helpful assistant."
summarize_task = [
    # "Tell your friend about the research in a text message.",
    "In the summary, cover the following information: \
    \n- Identify the key points and statistics from this text that would make interesting or helpful health content. \
    \n- If available, include the effect sizes found in the research. \
    Otherwise, skip this step. \
    \n- If applicable, get a brief description of the research participants, \
    such as age, sex, and health conditions. Otherwise, you can skip this step.\
    \n- Think about why the general population should care about the research.",
]

prep_step = [
    "Summarize the text for a LinkedIn post.",
    # "1. Tell your friend about the research in a text message.",
    # "Take the key points and numerical descriptors to",
    # "summarize the research in a text message to someone you know",
    # "summarize for a LinkedIn post.",
    # "Describe the interesting points to your coworker at the water cooler",
    # "Create an Instagram post without hashtags.",
]
edit_task = [
    """
    \nOnce you have written your text message: \
    \nEvaluate your text message to see if it may be confusing or redundant. \
    \nIf so, re-write it so it is clear and concise. Otherwise, keep it the same. \
    \n2. Create an intriguing subject line for the text.\
    \n3. Return your final response in a JSON format with the following format: \
    \n{"headline": <subject line from step 2>, \
    \n"body": <text from step 1>} \
    """,
]

user_simplify_task = [
    """If needed, rewrite the text using terms appropriate for the audience. If not keep it the same.\
    Follow these steps to accomplish this: \
    \n1. Check if the content and language are appropriate for the audience. \
    \n2. If it is suitable for the audience, keep it the same. If not, rewrite using terms appropriate for the audience. \ 
    \n3. Return the final version of the summary to be shown to the audience. \
    \n\nYour audience is""",
]

simplify_audience = [
    # "a lay audience",
    "people without a science background",
]

user_relevance_task = [
    """Rewrite this summary to include a statement of how it is relevant for the audience. \
        Follow these steps to accomplish this: \
        \n1. Think about why this might be relevant for the audience in the grand scheme of things.\
        \n2. If it is not evident why the text is relevant for the audience in the grand scheme of things, \
        add a sentence to inform the audience. Otherwise, keep it the same. \
        \n3. Modify the summary if needed to reduce redundancy. \
        \n4. Check if the content and language are appropriate for the audience. \
        If it is suitable for the audience, keep it the same. If not, rewrite using terms appropriate for the audience. \ 
        \n5. Return the final version of the summary to be shown to the audience. \
        \n6. Remove the backticks.
        \n\nYour audience consists of""",
]

relevance_audience = [
    "seniors",
    # "people who enjoy sports",
    "people new to resistance training"
]

qna_dict = dict()
chatbot_dict = dict()
simple_summaries_dict = dict()
relevance_dict = dict()
chain_results_dict = dict()
save = True
# save_outputs = False
save_outputs = True
empty_columns = True

# Create initial summaries
chaining_dict = batch_summarize_chain(
    text_dict, folder_path, prep_step, summarize_task, edit_task, chatbot_dict,
    system_role=system_role, model=model, max_tokens=1000,
    n_choices=n_choices, pause_per_request=pause_per_request,
    iteration_id=iteration_id, save_outputs=save_outputs
    )
qna_dict = spreadsheet_columns(
    qna_dict, chatbot_dict, iteration_id, chatbot_id=chatbot_id, save=save, path=folder_path
    )

time.sleep(pause_per_request)

# # Create simple summaries
# simple_summaries = prompt_chaining_dict(user_simplify_task, simplify_audience, simple_summaries_dict, 
#     chatbot_dict[chatbot_id], iteration_id,
#     n_choices=1, pause_per_request=pause_per_request, chatbot_id=chatbot_id
#     )

# # Add relevance
# relevance = prompt_chaining_dict(user_relevance_task, relevance_audience, relevance_dict, 
#     chatbot_dict[chatbot_id], iteration_id, prompt_column='relevance', 
#     n_choices=1, pause_per_request=pause_per_request, chatbot_id=chatbot_id
#     )

# # Merge the results
# try:
#     qna_dict = merge_all_chaining_results(
#         chatbot_dict, qna_dict, iteration_id=iteration_id, relevance_audiences=2, pivot=True,
#         empty_columns=empty_columns, chatbot_id=chatbot_id,
#         save_df=save, save_chatbot=save, 
#             csv_path=folder_path,
#     )
#     print(f'\nCompleted merge_all_chaining_results!:)')
# except Exception as error:
#     exc_type, exc_obj, tb = sys.exc_info()
#     f = tb.tb_frame
#     lineno = tb.tb_lineno
#     file = f.f_code.co_filename
#     print(f'An error occurred on line {lineno} in {file}: {error}')
#     print('Unable to merge results')
#     if save:
#         save_instance_to_dict(chatbot_dict[chatbot_id], ext=None, json_path=folder_path)
#         print(f'\nCould not merge; saved Chaining instances as JSON.')