import json
import re

def parse_panic_file(file_text):
    # Витягуємо другий JSON-об'єкт (основний)
    json_blocks = re.findall(r'\{[\s\S]*?\}', file_text)
    main_json = json.loads(json_blocks[1])

    model = main_json.get('product', 'Невідомо')
    ios = main_json.get('build', 'Невідомо')
    date = main_json.get('date', 'Невідомо')
    panic_string = main_json.get('panicString', '')

    errors = []
    if "i2c3::_checkInterrupts error" in panic_string:
        errors.append("i2c3_interrupt_error")
    # Додавайте свої патерни тут!

    return {
        'model': model,
        'ios': ios,
        'date': date,
        'errors': errors,
        'panic_string': panic_string[:700]
    }
