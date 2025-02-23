def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # Dosya uzantısını al
    valid_extensions = ['.pdf', '.doc']
    print("Uploaded file extension:", ext)  # Debug için
    if not ext.lower() in valid_extensions:
        print("Invalid file extension!")  # Debug için
        raise ValidationError('Unsupported file extension.')
