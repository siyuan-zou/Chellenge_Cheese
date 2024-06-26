from .base import DatasetGenerator
import json
import re
# from unidecode import unidecode

def find_keys_containing(target, data, num_images_per_label=200):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if target in key:
                results.append(
                    {
                        "prompt": value,
                        "num_images": num_images_per_label,
                    })
            # Recurse into nested dictionaries
            if isinstance(value, (dict, list)):
                results.extend(find_keys_containing(target, value))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_keys_containing(target, item))
    return results

def clean_label(label):
        if '-' in label:
            # remove spaces around hyphen
            return re.sub(r"\s*-\s*", "-", label)
        elif label == "SCARMOZA":
            return "SCAMORZA"
        elif label == "TÊTE DE MOINES":
            return "TÊTE DE MOINE"
        else:
            return label

class SimplePromptsDatasetGenerator(DatasetGenerator):
    def __init__(
        self,
        generator,
        batch_size=1,
        output_dir="dataset/train",
        num_images_per_label=200,
    ):
        super().__init__(generator, batch_size, output_dir)
        self.num_images_per_label = num_images_per_label
        self.type = "simple_prompts"

    def create_prompts(self, labels_names):
        prompts = {}
        for label in labels_names:
            prompts[label] = []
            prompts[label].append(
                {
                    "prompt": f"An image of a {label} cheese",
                    "num_images": self.num_images_per_label,
                }
            )
        return prompts

class SellingPromptsGenerator(DatasetGenerator):
    def __init__(
        self,
        generator,
        batch_size=1,
        output_dir="dataset/train",
        num_images_per_label=200,
    ):
        super().__init__(generator, batch_size, output_dir)
        self.num_images_per_label = num_images_per_label
        self.type = "selling_prompts"
    def create_prompts(self, labels_names):
        with open("/users/eleves-b/2022/siyuan.zou/DL_SiyuanZou/Chellenge_Cheese/prompts/selling.json", "r") as f:
            designed_prompts = json.load(f)

        prompts = {}
        for label in labels_names:
            label_c = clean_label(label)
            prompts[label] = []
            # remove accents of the label
            prompts[label].append(
                {
                    "prompt": designed_prompts[label_c].replace(f"{label_c.lower()}", f"{label_c.lower()}" + " cheese"),
                    "num_images": self.num_images_per_label,
                }
            )
        return prompts
    
class ProductionPromptsGenerator(DatasetGenerator):
    def __init__(
        self,
        generator,
        batch_size=1,
        output_dir="dataset/train",
        num_images_per_label=200,
    ):
        super().__init__(generator, batch_size, output_dir)
        self.num_images_per_label = num_images_per_label
        self.type = "production_prompts"
    def create_prompts(self, labels_names):
        with open("/users/eleves-b/2022/siyuan.zou/DL_SiyuanZou/Chellenge_Cheese/prompts/production.json", "r") as f:
            designed_prompts = json.load(f)

        prompts = {}
        for label in labels_names:
            label_c = clean_label(label)
            prompts[label] = []
            # remove accents of the label
            prompts[label].append(
                {
                    "prompt": designed_prompts[label_c].replace(f"{label_c.lower()}", f"{label_c.lower()}" + " cheese"),
                    "num_images": self.num_images_per_label,
                }
            )
        return prompts
    
class ProductionLPromptsGenerator(DatasetGenerator):
    def __init__(
        self,
        generator,
        batch_size=1,
        output_dir="dataset/train",
        num_images_per_label=200,
    ):
        super().__init__(generator, batch_size, output_dir)
        self.num_images_per_label = num_images_per_label
        self.type = "production_long"
    def create_prompts(self, labels_names):
        with open("/users/eleves-b/2022/siyuan.zou/DL_SiyuanZou/Chellenge_Cheese/prompts/production_l.json", "r") as f:
            designed_prompts = json.load(f)

        prompts = {}
        for label in labels_names:
            label_c = clean_label(label)
            prompts[label] = []
            # remove accents of the label
            prompts[label].append(
                {
                    "prompt": designed_prompts[label_c].replace(f"{label_c.lower()}", f"{label_c.lower()}" + " cheese"),
                    "num_images": self.num_images_per_label,
                }
            )

        return prompts

class FoodsPromptsGenerator(DatasetGenerator):
    def __init__(
        self,
        generator,
        batch_size=1,
        output_dir="dataset/train",
        num_images_per_label=200,
    ):
        super().__init__(generator, batch_size, output_dir)
        self.num_images_per_label = num_images_per_label
        self.type = "foods_prompts"

    def create_prompts(self, labels_names):
        with open("/users/eleves-b/2022/siyuan.zou/DL_SiyuanZou/Chellenge_Cheese/prompts/foods.json", "r") as f:
            designed_prompts = json.load(f)

        prompts = {}
        for label in labels_names:
            label_c = clean_label(label)
            prompts[label] = []
            for food_type in designed_prompts[label_c]:
                prompts[label].append(
                    {
                        "prompt": label_c.lower() + " cheese " + food_type,
                        "num_images": self.num_images_per_label,
                    }
                )
        return prompts
    
class CaptionningGenerator(DatasetGenerator):
    def __init__(
        self,
        generator,
        batch_size=1,
        output_dir="dataset/train",
        num_images_per_label=200,
    ):
        super().__init__(generator, batch_size, output_dir)
        self.num_images_per_label = num_images_per_label
        self.type = "captionning"

    def create_prompts(self, labels_names):
        with open("/users/eleves-b/2022/siyuan.zou/DL_SiyuanZou/Chellenge_Cheese/prompts/semantic_captionning_validation.json", "r") as f:
            designed_prompts = json.load(f)

        prompts = {}
        for label in labels_names:
            prompts = find_keys_containing(label, designed_prompts, num_images_per_label=self.num_images_per_label)
        return prompts