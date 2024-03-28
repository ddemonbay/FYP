#This function is used to insert Researcher Agent Materials in to the Curriculum Designer txt file

original_file_path = 'CurriculumDesignerAgent.txt'
replacement_file_path = 'RA_Output.txt'

# Read the replacement text from its file
with open(replacement_file_path, 'r', encoding='utf-8') as file:
    replacement_text = file.read()

# Read the original file
with open(original_file_path, 'r', encoding='utf-8') as file:
    file_contents = file.read()

# Replace the $$ReplacementIndicationSymbol$$ with the text from the replacement file
updated_contents = file_contents.replace('$$ReplacementIndicationSymbol$$', replacement_text)

# Write the updated contents back to the original file
with open(original_file_path, 'w', encoding='utf-8') as file:
    file.write(updated_contents)

print("The original file has been updated with the text from the replacement file.")