from sources.lieutenant2k_blog import Lieutenant2kBlogChecker
from sources.packtpub import PacktpubChecker
from post_change_controller import Observer


observer = Observer()
observer.add_source(Lieutenant2kBlogChecker())
observer.add_source(PacktpubChecker())
observer.check_for_changes()
