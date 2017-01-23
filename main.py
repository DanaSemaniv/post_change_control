from sources.lieutenant2k_blog import Lieutenant2kBlogChecker
from post_change_controller import Observer


observer = Observer()
observer.add_source(Lieutenant2kBlogChecker())
observer.check_for_changes()
