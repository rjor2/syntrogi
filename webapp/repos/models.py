import uuid
import git
from django.db import models
import shutil
import subprocess
import logging

logger = logging.getLogger('default')

# Git Repo Model
class Repo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=200)
    branch = models.CharField(max_length=200, blank=True)
    revision = models.CharField(max_length=200, blank=True)
    downloaded = models.BooleanField(default=False, blank=True)
    # STATS
    files = models.IntegerField (blank=True, null=True)
    lines = models.IntegerField (blank=True, null=True)
    deletions = models.IntegerField (blank=True, null=True)
    insertions = models.IntegerField (blank=True, null=True)

    def download(self):
        """
        Download the repo and store in the repos volume
        :return:
        """
        logger.info("Downloading: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))
        # TODO push off to celery
        # Using Git Python
        # http://gitpython.readthedocs.org/
        try:
            if self.branch:
                r = git.Repo.clone_from(self.url, '/repos/%s' % (self.id), branch=self.branch)
            else:
                # don't want to assume that there is a default branch called master....
                r = git.Repo.clone_from(self.url, '/repos/%s' % (self.id))
        except git.GitCommandError as e:
            if ("repository" in str(e.stderr) and "not found" in str(e.stderr)) or \
               "Authentication failed" in str(e.stderr) or  \
               "could not read Username" in str(e.stderr):
                logger.debug("%s Git Repo does not exist or is password protected." %self.id)
                raise Exception('Git Repo does not exist or is password protected.')
            elif "not found in upstream origin" in str(e.stderr):
                logger.debug("%s Git Repo has no branch %s" %(self.id, self.branch))
                raise Exception('Branch does not exist.')
            else:
                raise e

        if self.revision:
            try:
                r.head.reset(self.revision)
            except git.GitCommandError as e:
                if "unknown revision" in str(e.stderr):
                    logger.debug("%s Git Repo has no revision %s" %(self.id, self.revision))
                    self.remove()
                    raise Exception('Revision does not exist.')
                else:
                    raise e

        self.branch = r.active_branch.name
        self.revision = r.active_branch.object.hexsha
        self.downloaded = True
        logger.info("Downloaded: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))
        self.update_stats()
        self.save()

    def update(self):
        r = git.Repo('/repos/%s' %(self.id))
        logger.info("Updating: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))
        try:
            if self.branch:
                r.git.checkout(self.branch)
        except:
            logger.debug("%s Git Repo has no branch %s" %(self.id, self.branch))
            raise Exception('Branch does not exist.')
        try:
            if self.revision:
                r.head.reset(self.revision)
        except:
            logger.debug("%s Git Repo has no revision %s" %(self.id, self.revision))
            raise Exception('Revision does not exist.')

        logger.info("Updated: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))

        self.branch = r.active_branch.name
        self.revision = r.active_branch.object.hexsha
        self.update_stats()
        self.save()

    def remove(self):
        """
        Remove the source code of the repo
        :return:
        """
        logger.info("Removing: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))
        # TODO see if we can use git.Repo to remove this. or run an re over the file name.
        # r = git.Repo(self.url, '/repos/%s' % self.id)
        try:
            shutil.rmtree("/repos/%s" %self.id)
        except FileNotFoundError:
            logger.debug("Repo: %s not there" %self.id)
        # except OSError:
            # GitPython keeps some files open so remove will fail when testing :( (known bug)
            # Need to wait for process to finish before can delete file
            #logger.warn("Couldn't remove repo directory")

        logger.info("Removed: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))

    def update_stats(self):
        r = git.Repo('/repos/%s' %(self.id))
        #
        self.files = r.head.commit.stats.total['files']
        self.lines = r.head.commit.stats.total['lines']
        self.deletions = r.head.commit.stats.total['deletions']
        self.insertions = r.head.commit.stats.total['insertions']

    # Not needes as using gitpython but keeping in for demo purposes
    # def change_branch(self, branch):
    #     git_dir = "/repos/%s/.git" %self.id
    #     work_tree = "/repos/%s" %self.id
    #     try:
    #         subprocess.check_call(["git", '--work-tree',work_tree, '--git-dir',git_dir, 'checkout', branch])
    #     except:
    #         logger.debug("No branch %s" %branch)
    #         return
    #     self.branch = branch
    #
    # def change_revision(self, revision):
    #     git_dir = "/repos/%s/.git" %self.id
    #     work_tree = "/repos/%s" %self.id
    #     try:
    #         subprocess.check_call(["git", '--work-tree',work_tree, '--git-dir',git_dir, 'reset', revision, '--hard'])
    #     except:
    #         logger.debug("No revision %s" %revision)
    #         return
    #     self.revision = revision
