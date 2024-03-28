def extract_courses(input_file, output_file):

    # Flag to determine whether in the correct section
    sectionOne_flag = False
    # Open the input file for reading
    with open(input_file, 'r') as file:
        # Open the output file for writing
        with open(output_file, 'w') as outfile:
            # Iterate through each line in the input file
            for line in file:
                # Check if reached Section 1
                if line.strip() == "Section 1: Curriculum":
                    sectionOne_flag = True
                # Check reached Section 2, then end
                elif line.strip().startswith("Section 2:"):
                    sectionOne_flag = False
                # If in Section 1, look for lines starting with the index (1.x)
                elif sectionOne_flag and line.strip().startswith("1."):
                    # Extract and write the index and course name
                    course_info = line.strip().split(' ', 1)
                    if len(course_info) > 1:
                        outfile.write(f"{course_info[0]} {course_info[1]}\n")

# Path
input_file_path = 'CDA_Output.txt'
output_file_path = 'Extracted_curriculum.txt'

extract_courses(input_file_path, output_file_path)

print("Extraction complete. Check extracted_curriculum.txt for the results.")
