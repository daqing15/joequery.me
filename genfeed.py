# Generate an RSS feed. This should be done after creating a blog post.
import os
from joequery import before_first_request
from joequery.settings import app
from joequery.blog.helpers import (
    get_posts, BLOG_SYS_PATH, gen_rss_feed, _alter_rss, get_excerpt
)
from flask import render_template, current_app,g 
import copy
import time

currentDir = os.sep.join(os.path.realpath(__file__).split('/')[:-1])
    
# Write an rss feed to the appropriate file
def write_rss_feed(rss):
  feedPath = os.path.join(BLOG_SYS_PATH, "templates", "rssfeed.static")
  f = open(feedPath, 'w')
  f.write(rss)
  f.close()
  print("Generated static rss feed")

def write_index_pages(postsPerPage):
  i=1
  posts = get_posts(app, postsPerPage)
  while posts:
    for post in posts:
      post['category'] = post['url'].split('/')[1]
      post['pubDate'] = time.strftime("%B %d, %Y", post['pubDate'])

    pagePath = os.path.join(BLOG_SYS_PATH, "pages", category, "page%d.static" % i)
    with app.test_request_context():
      before_first_request()
      newposts = get_posts(app, postsPerPage, postsPerPage * i - 1)

      # Determine if we should display prev/next buttons
      prevPage = False
      nextPage = False
      if i>1:
        prevPage = i-1
      if len(newposts) > 0:
        nextPage = i+1

      # Determine the appropriate title tag to use.
      if i == 1:
      	title = "Programming blog"
      else:
      	title = "Programming blog | Page %d" % i
      html = render_template("templates/blog_index.html", 
          posts=posts, prevPage=prevPage, nextPage=nextPage, title=title)

      f = open(pagePath, 'w')
      f.write(html)
      f.close()
      i += 1
      posts = newposts
  print("Generated static blog pages")

# Write an xml sitemap
def write_xml_sitemap():
  with open('blog/rss.txt', 'r') as f:
    posts = [x.strip() for x in f.readlines()]

  with app.test_request_context():
    html = render_template("sitemap.html", posts=posts)
    sitemapPath = os.path.join(currentDir, "templates", "sitemap.static")
    f = open(sitemapPath, 'w')
    f.write(html)
    f.close()
  print("Generated xml sitemap")

#posts = get_posts(app, 10)
#rss = gen_rss_feed(app, posts)
#write_rss_feed(rss)
#write_from_the_blog(posts)
write_index_pages(10)
#write_xml_sitemap()
