import uuid
import git
from django.db import models
import shutil

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
            r.git.checkout(self.branch)
        except:
            logger.debug("%s Git Repo has no branch %s" %(self.id, self.branch))
            raise Exception('Branch does not exist.')
        try:
            r.head.reset(self.revision)
        except:
            logger.debug("%s Git Repo has no revision %s" %(self.id, self.revision))
            raise Exception('Revision does not exist.')
        logger.info("Updated: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))
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
        except:
            logger.warn("Couldn't remove Repo: %s from file system" %self.id)
        logger.info("Removed: id:%s url:%s branch:%s revision:%s" %(self.id, self.url, self.branch, self.revision))

    def update_stats(self):
        r = git.Repo('/repos/%s' %(self.id))
        self.files = r.commit().stats.total['files']
        self.lines = r.commit().stats.total['lines']
        self.deletions = r.commit().stats.total['deletions']
        self.insertions = r.commit().stats.total['insertions']
