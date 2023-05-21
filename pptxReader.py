import re
from pptx import Presentation

class PowerPointReader:
    def __init__(self, file_path):
        self.presentation = Presentation(file_path)


    def clean_text(self, text):
        # Remove leading/trailing whitespace and unnecessary characters
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        return cleaned_text

    def prepare_prompts(self):
        prompts = []
        for slide in self.presentation.slides:
            slide_data = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            cleaned_text = self.clean_text(run.text)
                            if cleaned_text:
                                slide_data.append(cleaned_text)
            prompt = ' '.join(slide_data)
            prompts.append(prompt)
        return prompts
