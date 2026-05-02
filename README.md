# ACG AI Picture Character LoRA Project

This project organizes a local experiment workflow for training character LoRA models from ACG character references and generating new compositions.

Default scope: all project outputs are for local experiments only and will not be published or shared externally.

## Project Stages

1. Data collection and curation
   - Input: work title, character name, optional reference URLs, and user-provided images/screenshots.
   - Output: a reviewed character dataset with clean images and captions.

2. Tool selection
   - Prefer high-star, active open-source tools from GitHub.
   - Use separate tools for dataset curation, captioning, LoRA training, generation, and pose/control workflows.

3. Training preparation
   - Recommended target: SDXL anime base model + one LoRA per character.
   - Recommended training tool: kohya_ss GUI or kohya-ss/sd-scripts.

4. Generation workflow
   - Recommended UI: ComfyUI.
   - Use LoRA for identity, prompts for scene/expression, ControlNet/OpenPose for composition, and inpaint for fixes.

5. Evaluation
   - Test fixed prompts across checkpoints.
   - Compare identity, flexibility, pose control, artifacts, and overfitting.

## Files

- `AGENTS.md`: root instructions for any agent that continues the work.
- `docs/01_data_collection_pipeline.md`: agent-assisted data collection and cleaning workflow.
- `docs/02_open_source_tool_survey.md`: GitHub project survey with current star counts.
- `docs/03_tool_setup_plan.md`: tools to install and where to get them.
- `docs/04_generation_test_plan.md`: 10 composition tests and evaluation checklist.
- `docs/05_agent_handoff.md`: short handoff guide for Codex or Claude.
- `configs/project.yaml`: project defaults for dataset, training, and generation.
- `templates/character_intake.csv`: character/project intake template.
- `templates/dataset_review_sheet.csv`: image review template.
- `templates/composition_tests.csv`: 10 prompt tests in spreadsheet form.
- `templates/evaluation_sheet.csv`: checkpoint evaluation table.
- `templates/agent_task_brief.md`: prompt skeleton for starting a new task.
- `workflows/`: place ComfyUI workflow JSON files here.

## Directory Layout

```txt
data/raw/        candidate images
data/selected/   reviewed usable images
data/rejected/   rejected images for audit
data/train/      final image + caption pairs
outputs/lora/    trained LoRA files
outputs/samples/ generated test images
configs/         project and training defaults
workflows/       ComfyUI workflow JSON files
logs/            notes, training logs, comparisons
```

## Recommended First Run

Fill `templates/character_intake.csv` with one character first. Start with 30-80 candidate images, narrow to 25-50 clean images, train a first SDXL LoRA, then evaluate 4-6 checkpoints before collecting more data.

## Next Input Needed

Provide a work title, a character name, or both. The next project step is to create that character's source plan and candidate image review sheet.
