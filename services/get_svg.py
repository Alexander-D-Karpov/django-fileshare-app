from django.conf import settings

conv = {
    "text/plain": "r3/paper.svg",
    "text/x-c++": "r6/c++.svg",
    "application/x-dosexec": "r6/exe.svg",
    "application/vnd.efi.iso": "r6/iso.svg",
    "image/jpeg": "r6/jpg.svg",
    "video/x-msvideo": "r5/avi.svg",
    "application/pdf": "r5/pdf.svg",
}


def get_svg(content_type: str) -> str:
    if content_type in conv:
        return settings.STATIC_URL + "SVG/" + conv[content_type]
    return settings.STATIC_URL + "SVG/" + "r1/documents.svg"
