from contextlib import nullcontext
from readline import replace_history_item
from keyring import delete_password
import scrapy
import traceback
from github import Github
import time
from githubAlPR.items import GithubalprItem

class githubPRSpider(scrapy.Spider):
    name = 'githubPR'
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        # you need to specify the project name to crawl
        self.PROJECT_NAME = 'facebook/fresco'
        BASE_URL = 'https://github.com/' + self.PROJECT_NAME + '/pull/'

        # crate github client instance
        # you should use your own github access token
        g = Github("access_token")
        self.repo = g.get_repo(self.PROJECT_NAME)
        self.pulls = self.repo.get_pulls(state='closed',sort='closed', direction='desc', base='main')
        self.start_urls = []
        # Map url to index of pr
        self.url_to_idx = {}
        for idx, pr in enumerate(self.pulls):
            url = BASE_URL + str(pr.number)
            self.start_urls.append(url)
            self.url_to_idx[url] = idx
    
    def parse(self, response):
        try:
            # extract linked issues
            linked_issues = self.extract_linked_issues(response)
            if not linked_issues:
                return
            # extract author association
            author_association = self.extract_author_association(response)
            # get PR info from Github API
            idx = self.url_to_idx[response.url]
            pr = self.pulls[idx]
            item = GithubalprItem(_id = self.PROJECT_NAME+'/'+str(pr.number),
                                  project_name = self.PROJECT_NAME,
                                  linked_issues = linked_issues,
                                  author_association = author_association,
                                  status = 'merged' if pr.merged else 'closed',
                                  changed_files = pr.changed_files,
                                  additions = pr.additions,
                                  deletions = pr.deletions,
                                  commits = pr.commits,
                                  comments = pr.comments,  # number of comments
                                  review_comments = pr.review_comments,
                                  time_span = time.mktime(pr.closed_at.timetuple()) - time.mktime(pr.created_at.timetuple())
                                  )
            yield item
        except Exception as e:
             self.logger.error(str(e))
             self.logger.error(traceback.format_exc())

    @staticmethod
    def extract_linked_issues(response):
        issue_forms = response.xpath('//form[@class="js-issue-sidebar-form"]')
        form_ind = len(issue_forms.getall()) - 1
        if issue_forms[form_ind].xpath('@aria-label').extract()[0] == 'Link issues':
            return issue_forms[form_ind].css('a::attr(href)').extract()
        return None
    
    @staticmethod
    def extract_author_association(response):
        author_box = response.xpath('//span[@class="Label tooltipped tooltipped-multiline tooltipped-s ml-2"]/text()')
        if len(author_box.getall()) <= 1:
            return None
        if bool(author_box.re("Owner")):
            return "Owner"
        if bool(author_box.re("Contributor")):
            return "Contributor"
        if bool(author_box.re("Member")):
            return "Member"
        if bool(author_box.re("Collaborator")):
            return "Collaborator"
        return None