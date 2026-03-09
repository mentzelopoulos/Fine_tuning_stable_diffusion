## Fine-tuning Stable Diffusion with LoRA

This repository contains scripts and notebooks to fine-tune **Stable Diffusion v1.5** and **Stable Diffusion XL (SDXL)** using **LoRA** on your own images, then run inference with the trained weights.

### Regular (SD 1.5) vs XL

| Model | Training script | Inference notebook |
|-------|-----------------|--------------------|
| **Stable Diffusion v1.5** (512×512) | `train_text_to_image_lora.py` | `lora_inference.ipynb` |
| **Stable Diffusion XL** (1024×1024) | `train_text_to_image_lora_sdxl.py` | `lora_inference_sdxl.ipynb` |

Use the same pair: train with one script, then run the matching notebook to generate images with your LoRA.

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
- Logs metrics to TensorBoard and resumes from the latest checkpoint if present.

### Fine-tuning SDXL

For **Stable Diffusion XL**, use the SDXL script and 1024 resolution:

```bash
accelerate launch train_text_to_image_lora_sdxl.py \
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
  --train_data_dir="/path/to/Fine_tuning_stable_diffusion/training_images" \
  --output_dir="/path/to/Fine_tuning_stable_diffusion/lora-output-sdxl" \
  --resolution=1024 \
  --train_batch_size=2 \
  --gradient_accumulation_steps=4 \
  --num_train_epochs=100 \
  --learning_rate=1e-4 \
  --lr_scheduler="cosine" \
  --mixed_precision="fp16" \
  --report_to="tensorboard" \
  --rank=16 \
  --checkpointing_steps=500
```

Adjust paths and batch size to match your setup.

### Inference with the notebooks

After training, load your LoRA and generate images using the **notebook that matches the model you trained**:

- **If you trained with `train_text_to_image_lora.py` (SD 1.5)**  
  Open **`lora_inference.ipynb`**. Set `base_model` to `"runwayml/stable-diffusion-v1-5"` and `lora_dir` to your SD 1.5 output folder (e.g. `lora-output/` or `lora-output/checkpoint-5000`). Run all cells to load the pipeline, apply LoRA, and generate images.

- **If you trained with `train_text_to_image_lora_sdxl.py` (SDXL)**  
  Open **`lora_inference_sdxl.ipynb`**. Set `base_model` to `"stabilityai/stable-diffusion-xl-base-1.0"` and `lora_dir` to your SDXL output folder (e.g. `lora-output-sdxl/` or `lora-output-sdxl/checkpoint-13500`). Run all cells to load the SDXL pipeline, apply LoRA, and generate images.

In each notebook, `lora_dir` can point to the root `output_dir` from training or to a specific checkpoint subfolder (e.g. `checkpoint-5000`). The notebooks load the LoRA weights and run the pipeline so you can test your fine-tuned model.

