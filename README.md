## Fine-tuning Stable Diffusion with LoRA

This repository contains scripts and notebooks to fine-tune **Stable Diffusion v1.5** using **LoRA** on custom (in the example underwater wildlife) datasets.

### Data layout

- Training images are stored under:
  - `training_images/`
    - `Category_1`
    - `Category_2`
    - ...

- Captions are provided via a single `metadata.jsonl` file in `training_images/`, in the standard `imagefolder` format used by 🤗 Datasets:
  - Each line is a JSON object with:
    - `file_name`: relative path to the image (e.g. `"Category_1/image_XXX.jpg"`)
    - `text`: the corresponding caption/prompt.

### Environment

You should have at least:

- Python 3.10+
- A CUDA-capable GPU
- The following Python packages installed:
  - `diffusers[torch]`
  - `transformers`
  - `accelerate`
  - `datasets`
  - `peft`
  - `safetensors`

Example installation:

```bash
pip install "diffusers[torch]" transformers accelerate datasets peft safetensors
```

Configure `accelerate` once:

```bash
accelerate config
```

### Fine-tuning command

From the repository root (`.../Fine_tuning_stable_diffusion`), run:

```bash
accelerate launch train_text_to_image_lora.py \
  --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
  --train_data_dir="/home/ament/Fine_tuning_stable_diffusion/training_images" \
  --output_dir="/home/ament/Fine_tuning_stable_diffusion/lora-output" \
  --resolution=512 \
  --train_batch_size=16 \
  --gradient_accumulation_steps=1 \
  --num_train_epochs=100 \
  --learning_rate=2e-4 \
  --lr_scheduler="cosine" \
  --mixed_precision="fp16" \
  --report_to="tensorboard" \
  --rank=16 \
  --lr_warmup_steps=50 \
  --resume_from_checkpoint="latest"
```

This command:

- Fine-tunes `runwayml/stable-diffusion-v1-5` using LoRA rank 16 on all images in `training_images/`.
- Trains at 512×512 resolution with batch size 16.
- Uses a cosine learning rate schedule with warmup and mixed-precision FP16.
- Logs metrics to TensorBoard and resumes from the latest checkpoint in `lora-output-Jan-23-26` if present.

