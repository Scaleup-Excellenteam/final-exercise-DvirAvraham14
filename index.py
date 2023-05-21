import pptxReader as ppR

pptx_file_path = "/Users/dviravraham/Downloads/09-Spring-Listeners-Filters.pptx"
powerpoint_reader = ppR.PowerPointReader(pptx_file_path)

for slide_data in powerpoint_reader.prepare_prompts():
    # Do something with the slide data
    print(slide_data, "\n\n")
