"""
Selectores CSS y XPath centralizados
Evita hardcodear selectores en el código
"""

# FORMULARIO
FORM_SELECTORS = {
    'first_name': '#firstName',
    'last_name': '#lastName',
    'email': '#userEmail',
    'gender_male': 'label[for="gender-radio-1"]',
    'gender_female': 'label[for="gender-radio-2"]',
    'gender_other': 'label[for="gender-radio-3"]',
    'mobile': '#userNumber',
    'date_of_birth': '#dateOfBirthInput',
    'subjects': '#subjectsInput',
    'hobbies_sports': 'label[for="hobbies-checkbox-1"]',
    'hobbies_reading': 'label[for="hobbies-checkbox-2"]',
    'hobbies_music': 'label[for="hobbies-checkbox-3"]',
    'picture': '#uploadPicture',
    'current_address': '#currentAddress',
    'state': '#state',
    'state_option': '#react-select-3-option-0',  # NCR
    'city': '#city',
    'city_option': '#react-select-4-option-0',  # Delhi
    'submit': '#submit',
    'modal_title': '#example-modal-sizes-title-lg',
    'modal_content': '.modal-body',
    'close_modal': '#closeLargeModal'
}

# WEBTABLES
WEBTABLE_SELECTORS = {
    'table': '.rt-table',
    'rows': '.rt-tbody .rt-tr-group',
    'first_name': 'div.rt-td:nth-child(1)',
    'last_name': 'div.rt-td:nth-child(2)',
    'age': 'div.rt-td:nth-child(3)',
    'email': 'div.rt-td:nth-child(4)',
    'salary': 'div.rt-td:nth-child(5)',
    'department': 'div.rt-td:nth-child(6)'
}

# BUTTONS
BUTTON_SELECTORS = {
    'double_click': '#doubleClickBtn',
    'right_click': '#rightClickBtn',
    'dynamic_click': '//button[text()="Click Me"]',  # XPath
    'double_click_message': '#doubleClickMessage',
    'right_click_message': '#rightClickMessage',
    'dynamic_click_message': '#dynamicClickMessage'
}

# DROPPABLE
DROPPABLE_SELECTORS = {
    'draggable': '#draggable',
    'droppable': '#droppable',
    'droppable_text': '#droppable p'
}