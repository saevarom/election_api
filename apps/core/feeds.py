# from datetime import datetime, date, time
# from django.contrib.syndication.views import Feed

# from core.models import BlogPage


# # Main blog feed

# class BlogFeed(Feed):
#     title = "The election_api Blog"
#     link = "/blog/"
#     description = ""

#     def item_title(self, item):
#         return item.title

#     def item_description(self, item):
#         return item.intro if item.intro else item.body

#     def item_link(self, item):
#         return item.full_url

#     def item_author_name(self, item):
#         pass

#     def item_pubdate(self, item):
#         return datetime.combine(item.date, time())
