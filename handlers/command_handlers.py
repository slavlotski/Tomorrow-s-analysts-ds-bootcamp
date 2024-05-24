import json
import git
import os
import shutil
import chardet
from telegram import Update
from telegram.ext import ContextTypes
from config.openai_client import client
from io import BytesIO
import requests
import openai

GITHUB_REPO_PATH = 'temp'

async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = (
        "Welcome to DS Bro!\n\n"
        "I am your daily assistant for data science tasks. Here are my main features:\n"
        "- /motivate: Send a motivational video link.\n"
        "- /sdvg: Send a relaxing video link.\n"
        "- /get_docs <GitHub Repo URL>: Generate documentation for the provided GitHub repository.\n"
        "- /meme: Get a funny and motivational data science meme.\n"
        "- /help: Show this help message.\n"
        "Additionally, in regular conversation mode, I can do the following things:\n"
        "You can simply chat with me on any topic related to Data Science, and more.\n"
        "Ask me to 'загрузи новости', and I will summarize the main news in Data Science.\n"
        "Enter any link, and I will summarize its content.\n"
        "I can generate code based on the task.\n"
        "I am also ready to perform code refactoring.\n"
    )
    await update.message.reply_text(description)

async def motivate_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = "Here's a motivational video for you: [Watch on YouTube](https://www.youtube.com/shorts/GszRpJTPThs)"
    await update.message.reply_text(reply, parse_mode="Markdown")
    print("assistant:", reply)

async def sdvg_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = "Here's a relax video for you: [Watch on YouTube](https://www.youtube.com/watch?v=g_hwy3y3hqQ)"
    await update.message.reply_text(reply, parse_mode="Markdown")
    print("assistant:", reply)

async def help_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - Show the update object.\n"
        "/motivate - Send a motivational video link.\n"
        "/sdvg - Send a relaxing video link.\n"
        "/get_docs <GitHub Repo URL> - Generate documentation for the provided GitHub repository.\n"
        "/meme - Get a funny and motivational data science meme."
    )
    await update.message.reply_text(help_text)

async def meme_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Create a funny and motivational meme for data scientists."
    await update.message.reply_text("Generating meme... I need some time... Please, wait a little...")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        meme_url = response.data[0].url
        meme_image = requests.get(meme_url).content

        await update.message.reply_photo(photo=BytesIO(meme_image))
        print("assistant: Sent a meme")
    except Exception as e:
        error_message = f"Error generating meme: {e}"
        await update.message.reply_text(error_message)
        print(error_message)


def clone_repo(repo_url, clone_path):
    try:
        git.Repo.clone_from(repo_url, clone_path)
        return True
    except Exception as e:
        print(f"Error cloning repo: {e}")
        return False

def read_files_from_repo(path):
    files_content = {}
    for root, _, files in os.walk(path):
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding'] if result['encoding'] else 'utf-8'
                    content = raw_data.decode(encoding, errors='ignore')
                    files_content[file_path] = content
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                files_content[file_path] = "Error reading file content"
    return files_content

def create_project_structure(path):
    project_structure = []
    for root, dirs, files in os.walk(path):
        if '.git' in root:
            continue
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        project_structure.append(f"{indent}├── {os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            project_structure.append(f"{subindent}├── {f}")
    return "\n".join(project_structure)

def create_chatgpt_request(files_content):
    project_structure = []
    file_descriptions = []

    total_length = 0
    max_length = 4000

    for file_path, content in files_content.items():
        if total_length + len(content) > max_length:
            break
        project_structure.append(file_path)
        file_descriptions.append(f"File: {file_path}\nContent:\n{content}\n")
        total_length += len(content)

    request_text = (
        "You are a documentation generator. Please provide detailed documentation for the following project.\n\n"
        "The documentation should include:\n"
        "1. A high-level description of each directory.\n"
        "2. A detailed description of each file within the directories.\n"
        "3. Recommendations on how to run the code.\n\n"
        "Project Structure:\n" + "\n".join(project_structure) + "\n\n"
        "File Descriptions:\n" + "\n".join(file_descriptions) + "\n\n"
        "Additionally, provide a brief recommendation on how to run the code."
    )

    return request_text

async def get_docs_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.split()
    if len(user_input) != 2:
        await update.message.reply_text("Please provide a valid GitHub repository URL.")
        return

    repo_url = user_input[1]
    repo_name = os.path.basename(repo_url).replace('.git', '')
    clone_path = os.path.join(GITHUB_REPO_PATH, repo_name)

    await update.message.reply_text("Cloning repository...")

    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

    if not clone_repo(repo_url, clone_path):
        await update.message.reply_text("Failed to clone repository.")
        return

    await update.message.reply_text("Repository cloned. Reading files...")

    files_content = read_files_from_repo(clone_path)

    if not files_content:
        await update.message.reply_text("No files found in the repository.")
        return

    await update.message.reply_text("Files read. Generating documentation...")

    chatgpt_request = create_chatgpt_request(files_content)
    project_structure = create_project_structure(clone_path)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": chatgpt_request}],
            max_tokens=2048,
            temperature=0.5,
        )
        documentation = response.choices[0].message.content.strip()

        reply = f"## Project Structure\n```\n{project_structure}\n```\n\n## Documentation\n{documentation}"
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error generating documentation: {e}")
    finally:
        shutil.rmtree(clone_path)