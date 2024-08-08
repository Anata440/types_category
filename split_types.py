import xml.etree.ElementTree as ET
from collections import defaultdict
import os

def split_xml_by_category(input_file):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Словарь для хранения элементов по категориям
        categories = defaultdict(list)
        errors = []

        # Проходим по всем элементам <type>
        for type_element in root.findall('type'):
            # Находим категорию внутри <type>
            category = type_element.find('category')
            if category is not None:
                category_name = category.get('name')
                if category_name:
                    categories[category_name].append(type_element)
                else:
                    errors.append(type_element)
            else:
                errors.append(type_element)
        
        # Создаем отдельные файлы для каждой категории
        for category, elements in categories.items():
            category_tree = ET.ElementTree(ET.Element('types'))
            category_root = category_tree.getroot()
            
            for element in elements:
                category_root.append(element)
            
            output_file = f"{category}.xml"
            category_tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"File '{output_file}' created with {len(elements)} items.")
        
        # Создаем файл для элементов без категории
        if errors:
            errors_tree = ET.ElementTree(ET.Element('types'))
            errors_root = errors_tree.getroot()
            
            for element in errors:
                errors_root.append(element)
            
            errors_file = "errors.xml"
            errors_tree.write(errors_file, encoding='utf-8', xml_declaration=True)
            print(f"File '{errors_file}' created with {len(errors)} items.")
        
        print("Processing completed successfully.")
    except ET.ParseError:
        print("Error: Failed to parse the XML file. Please check the input file for correctness.")
    except FileNotFoundError:
        print("Error: Input file not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_file = input("Please enter the path to the input XML file (e.g., types.xml): ").strip()
    
    # Check if the input file exists
    if os.path.isfile(input_file):
        split_xml_by_category(input_file)
    else:
        print("Error: The specified file does not exist. Please check the file path and try again.")
