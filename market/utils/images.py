# market/utils/images.py
from django.core.exceptions import ValidationError

ALLOWED_CONTENT_TYPES = (
    "image/jpeg",
    "image/png",
    "image/webp",
)

MAX_FILE_SIZE_MB = 10


def validate_image(uploaded_file):
    """
    Aceita tanto arquivos vindos do formulário (InMemoryUploadedFile)
    quanto instâncias de ImageFieldFile (quando o Django valida o model).
    """

    if not uploaded_file:
        return

    # Tenta descobrir o content_type em diferentes cenários
    content_type = getattr(uploaded_file, "content_type", None)

    # Quando é ImageFieldFile, às vezes o content_type fica no arquivo interno
    if content_type is None and hasattr(uploaded_file, "file"):
        content_type = getattr(uploaded_file.file, "content_type", None)

    file_size = getattr(uploaded_file, "size", None)

    # Só valida o tipo se conseguimos descobrir o content_type
    if content_type is not None and content_type not in ALLOWED_CONTENT_TYPES:
        raise ValidationError("Envie imagens JPEG, PNG ou WebP.")

    if file_size is not None and file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"Cada imagem pode ter no máximo {MAX_FILE_SIZE_MB} MB."
        )
