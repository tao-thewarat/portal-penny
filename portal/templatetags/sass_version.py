from django import template
from sass_processor.processor import SassProcessor

register = template.Library()


@register.simple_tag
def sass_src_v(path):
    """
    Same as {% sass_src %}, plus ?v=<compiled mtime>.

    runserver sends CSS without Cache-Control, so browsers keep an old
    main.css after SCSS changes. A new query string forces a refetch.
    """
    processor = SassProcessor(path)
    css_filename = processor(path)
    url = SassProcessor.handle_simple(css_filename)

    try:
        modified = processor.source_storage.get_modified_time(css_filename)
    except (FileNotFoundError, NotImplementedError):
        return url

    return f"{url}?v={int(modified.timestamp())}"
