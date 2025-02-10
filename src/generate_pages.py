from src.markdown_extract import extract_title, markdown_to_html_node
import os
from pathlib import Path


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_text = markdown_file.read()

    markdown_list = markdown_to_html_node(markdown=markdown_text)
    markdown_html_list = []

    for markdown_item in markdown_list.children:
        markdown_html_list.append(markdown_item.to_html())

    page_title = extract_title(markdown_text)

    with open(template_path, "r") as template_file:
        template_text = template_file.read()

    html_from_template = template_text.replace("{{ Title }}", page_title)
    html_to_input = "\n".join(markdown_html_list)
    html_from_template = html_from_template.replace("{{ Content }}", html_to_input)

    with open(dest_path, "w") as html_file:
        html_file.write(html_from_template)


def generate_pages_recursive(source_directory: Path, target_directory: Path):
    file_list = os.listdir(source_directory)

    for file in file_list:
        current_path = f"{source_directory}/{file}"
        target_path = f"{target_directory}/{file}"
        is_file = os.path.isfile(current_path)

        if not is_file:
            generate_pages_recursive(
                source_directory=current_path,
                target_directory=f"{target_directory}/{file}",
            )

        if is_file:
            generate_page(
                from_path=current_path,
                template_path="template.html",
                dest_path=target_path.replace(".md", ".html"),
            )
