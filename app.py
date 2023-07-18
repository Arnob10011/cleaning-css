import cssutils
from bs4 import BeautifulSoup
html_path = './index.html'
css_path = './style.css'


def html_parser(path):
    html_class, html_id, html_updated_class = [], [], []

    with open(path, 'r') as html_file:
        html = html_file.read()
 
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup.find_all():
        if 'class' in element.attrs:
            classes = element['class']
            html_class.extend(classes)

        if 'id' in element.attrs:
            ids = f"#{element['id']}"
            html_id.append(ids)

    for i in html_class:
        value = f'.{i}'
        html_updated_class.append(value)


    return [*html_updated_class, *html_id]



def css_parser(path):

    with open(path, 'r') as css_file:
        css = css_file.read()
        class_and_id = []

    css_soup = cssutils.parseString(css)
    for rule in css_soup:
        class_and_id.append(rule.selectorText)

    return class_and_id




def compare_between_html_css():
    html = html_parser(html_path)
    css = css_parser(css_path)

    shall_delete = [i for i in css if i not in html]
    return shall_delete
    
    


def delete_classes_and_ids(css_file_path, css_new_path , classes_and_id=None):
    classes_to_delete, ids_to_delete = [], []
    for i in classes_and_id:
        if i.startswith('.'):
            value = i[1 :]
            classes_to_delete.append(value)
        if i.startswith('#'):
            value = i[1:]
            ids_to_delete.append(value)


    # Read the CSS file
    with open(css_file_path, 'rb') as css_file:
        css_content_byte = css_file.read()

    # Parse the CSS using cssutils
    css_content = css_content_byte.decode('utf-8')
    css_rules = cssutils.parseString(css_content)

    # Delete classes and IDs from the CSS content using cssutils
    for rule in css_rules:
        if rule.type == cssutils.css.CSSRule.STYLE_RULE:
            if classes_to_delete and any(cls in rule.selectorText for cls in classes_to_delete):
                rule.deleted = True
            elif ids_to_delete and any(id_ in rule.selectorText for id_ in ids_to_delete):
                rule.deleted = True



    # Serialize the modified CSS content
    new_css_content = css_rules.cssText

    # Write the modified CSS content back to the file
    with open(css_new_path, 'wb') as css_file:
        css_file.write(new_css_content)
        print('works')
    

# Example usage
compare = compare_between_html_css()
css_new_path = './new_style.css'
delete_classes_and_ids(css_path,css_new_path , compare)
