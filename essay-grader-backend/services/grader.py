from models.schemas import RubricType
from config import client, supabase, BASE_DIR
from models.schemas import EssayGradingReport
from google.genai import types
from google import genai


def load_instructions(filename="grading_style.md"):
    file_path = BASE_DIR / "prompts" / filename
    return file_path.read_text(encoding="utf-8")


def construct_system_instructions(example_prompt, example_essay_set):
    """
    example_essay_set: The dict from Supabase containing "Sample A", "Sample B", etc.
    """
    base_instructions = load_instructions("grading_style.md")

    calibration_header = (
        "\n\nCALIBRATION EXAMPLES:\nStudy how these scores map to essay quality.\n"
    )

    example_blocks = []

    for row in example_essay_set:
        prompt_text = row.get("prompt_text", example_prompt)
        samples = row.get("samples", {})
        
        for sample_key, data in samples.items():
            essay_text = data.get("essay", "")
            scoring_data = data.get("scoring", {})

            label_map = {"Sample A": "High", "Sample B": "Medium", "Sample C": "Low", "Sample 0": "Example"}
            score_label = label_map.get(sample_key, "Unknown")

            block = f"""
<Example score="{score_label}">
    <EssayPrompt>{prompt_text}</EssayPrompt>
    <Essay>
        {essay_text}
    </Essay>
    <Grade>
        {scoring_to_markdown(scoring_data)}
    </Grade>
</Example>"""
            example_blocks.append(block)

    return base_instructions + calibration_header + "\n".join(example_blocks)


def construct_prompt_contents(prompt, essay, rubric):
    return f"""
Essay prompt:
{prompt}

Essay:
{essay}

RUBRIC:
{rubric}

For each rubric criterion, follow this order:
1. Strengths (with evidence)
2. Weaknesses (with evidence)
3. Weigh strengths vs weaknesses
4. Assign score with justification
5. State what would earn a higher score

"""


def get_essay_report(ai_prompt: str, rubric_type: str):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=[ai_prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EssayGradingReport,
            system_instruction=construct_system_instructions(
                ai_prompt, get_relevant_examples(ai_prompt, rubric_type)
            ),
            temperature=0.3,
        ),
    )
    return response.parsed


def get_relevant_examples(prompt: str, rubric_type: str, num: int = 3) -> list[dict]:
    result = client.models.embed_content(model="gemini-embedding-2-preview", contents=prompt)

    embedding = result.embeddings[0].values

    rubric_filter = None
    if (rubric_type in RubricType):
        rubric_filter = rubric_type

    result = supabase.rpc(
        "match_reference_material",
        {
            "query_embedding": embedding,
            "match_count": num,
            "rubric_type_filter": rubric_filter
        },
    ).execute()

    return result.data

def rubric_to_markdown(rubric_list, title="Essay Rubric"):
    md_output = [f"# {title}\n"]

    for category in rubric_list:
        md_output.append(f"## {category.name}")
        md_output.append(f"* **Possible Points:** {category.possible_points}")
        md_output.append(f"* **Description:** {category.description.strip()}")
        md_output.append("\n---\n")

    return "\n".join(md_output)

def scoring_to_markdown(scoring: dict) -> str:
    criteria = scoring['criteria']
    lines = []

    # Header scores
    for letter, criterion in criteria.items():
        lines.append(f"{criterion['name']} Score: {criterion['points_earned']}")

    lines.append(f"Total Score: {scoring['total_score']}")
    lines.append("")

    # Criteria blocks
    for letter, criterion in criteria.items():
        feedback = criterion['feedback'].replace('\n', ' ').strip()
        lines.append(
            f"{letter}. {criterion['name']} (0\u2013{criterion['points_possible']} points): "
            f"{criterion['points_earned']} {feedback}"
        )
        lines.append("")

    return "\n".join(lines)