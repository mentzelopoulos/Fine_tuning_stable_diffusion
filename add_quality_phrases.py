#!/usr/bin/env python3
"""Add quality phrases to every prompt in metadata.jsonl if not already present."""

import json
from pathlib import Path

METADATA_PATH = Path("training_images/metadata.jsonl")

QUALITY_PHRASES = [
    "ultra-realistic underwater photography with natural light and detailed textures",
    "professional DSLR underwater shot with vivid colors and sharp focus",
    "macro underwater photography with fine details, realistic water caustics, and natural textures",
    "high-resolution underwater image, cinematic lighting, realistic ocean environment",
    "scientific-style underwater photo, perfectly clear water, detailed coral and marine life",
    "realistic wide-angle underwater photography, dynamic lighting, high texture detail",
    "macro shot of marine life underwater, ultra-sharp details, photorealistic",
    "professional underwater portrait, realistic skin, cinematic lighting, high-resolution capture",
    "4K photorealistic underwater scene, natural sunlight, realistic color grading",
    "DSLR-quality underwater image, realistic light refraction and water texture",
    "vivid underwater photography with sun rays and detailed textures",
    "underwater wildlife photography, realistic fish scales and coral detail",
    "close-up underwater macro shot, high resolution and photorealistic",
    "cinematic underwater photography, realistic shadows and highlights",
    "professional underwater photography with lens flare and natural color",
    "crystal-clear underwater scene, natural lighting, photorealistic marine life",
    "macro underwater portrait of marine animal, sharp details and textures",
    "realistic underwater photography, 4K quality, vibrant colors",
    "scientific underwater imaging, ultra-detailed textures, natural lighting",
    "underwater landscape photography, realistic water surface and sand details",
    "DSLR-style underwater photo, realistic depth of field and lighting",
    "photorealistic underwater coral reef, natural light and high detail",
    "close-up underwater shot with realistic water particles and textures",
    "professional underwater photography, cinematic depth and realistic colors",
    "high-resolution underwater macro of fish, vivid detail and sharp focus",
    "natural underwater photography with volumetric lighting and realistic textures",
    "DSLR underwater portrait of marine life, photorealistic and highly detailed",
    "macro shot of coral reef, natural light, ultra-realistic textures",
    "underwater photography in 4K, realistic reflections, and high detail",
    "realistic underwater scene with diverse marine life and detailed textures",
]


def prompt_has_any_phrase(text: str) -> bool:
    return any(p.lower() in text.lower() for p in QUALITY_PHRASES)


def main():
    lines = METADATA_PATH.read_text(encoding="utf-8").strip().split("\n")
    out_lines = []
    idx = 0
    added = 0
    for line in lines:
        if not line.strip():
            out_lines.append(line)
            continue
        obj = json.loads(line)
        text = obj.get("text", "")
        if not text:
            out_lines.append(line)
            continue
        if prompt_has_any_phrase(text):
            out_lines.append(line)
            continue
        phrase = QUALITY_PHRASES[idx % len(QUALITY_PHRASES)]
        idx += 1
        added += 1
        # Append phrase before the final period
        if text.endswith("."):
            new_text = text[:-1].rstrip() + ", " + phrase + "."
        else:
            new_text = text.rstrip() + ", " + phrase + "."
        obj["text"] = new_text
        out_lines.append(json.dumps(obj, ensure_ascii=False))
    METADATA_PATH.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Added quality phrase to {added} prompts. Total lines: {len(lines)}.")


if __name__ == "__main__":
    main()
