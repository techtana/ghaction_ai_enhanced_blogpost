import os
import frontmatter
import openai

# Get environment variables
github_token = os.environ.get("GITHUB_TOKEN")
openai_api_key = os.environ.get("OPENAI_API_KEY")
repo_path = os.environ.get("GITHUB_WORKSPACE", ".") # Default to current directory for local testing

if not openai_api_key:
    print("OPENAI_API_KEY is not set.")
    exit(1)

openai.api_key = openai_api_key

posts_dir = os.path.join(repo_path, "_posts_commit")

if not os.path.isdir(posts_dir):
    print(f"Directory not found: {posts_dir}")
    exit(1)

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"Processing {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Check if the post has already been enhanced
        if "{% comment %}" in post.content:
            print(f"Skipping {filename} as it has already been enhanced.")
            continue

        if "enhance_policy" in post:
            enhance_policy = post["enhance_policy"]
            content = post.content

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": enhance_policy},
                        {"role": "user", "content": content}
                    ]
                )

                new_content = response.choices[0].message.content

                # The user mentioned "minus the beginning and ending boilerplate"
                # This is hard to define without seeing an example.
                # A more robust solution might need some regex or string manipulation.

                post.content = new_content + "\n\n{% comment %}\n" + content + "\n{% endcomment %}"

                with open(filepath, "w", encoding="utf-8") as f:
                    frontmatter.dump(post, f)

                print(f"Enhanced {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
