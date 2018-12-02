# -*- mode: Python ; coding: utf-8 -*-

"""
Anki2.1 add-on: customize sidebar of the browser.
"""

from aqt.browser import Browser
from aqt.qt import QIcon
from anki.hooks import wrap

# see aqt/browser.py
#   def buildTree(self):
#        self.sidebarTree.clear()
#        root = self.sidebarTree
#        self._stdTree(root)
#        self._favTree(root)
#        self._decksTree(root)
#        self._modelTree(root)
#        self._userTagTree(root)
#        self.sidebarTree.setIndentation(15)

#  def _systemTagTree(self, root):
#        tags = (
#            (_("Whole Collection"), "ankibw", ""),
#            (_("Current Deck"), "deck16", "deck:current"),
#            (_("Added Today"), "view-pim-calendar.png", "added:1"),
#            (_("Studied Today"), "view-pim-calendar.png", "rated:1"),
#            (_("Again Today"), "view-pim-calendar.png", "rated:1:1"),
#            (_("New"), "plus16.png", "is:new"),
#            (_("Learning"), "stock_new_template_red.png", "is:learn"),
#            (_("Review"), "clock16.png", "is:review"),
#            (_("Due"), "clock16.png", "is:due"),
#            (_("Marked"), "star16.png", "tag:marked"),
#            (_("Suspended"), "media-playback-pause.png", "is:suspended"),
#            (_("Leech"), "emblem-important.png", "tag:leech"))
#        for name, icon, cmd in tags:
#            item = self.CallbackItem(
#                root, name, lambda c=cmd: self.setFilter(c))
#            item.setIcon(0, QIcon(":/icons/" + icon))
#        return root
#
#    def _favTree(self, root):

#    def _stdTree(self, root):
#        for name, filt, icon in [[_("Whole Collection"), "", "collection"],
#                           [_("Current Deck"), "deck:current", "deck"]]:
#            item = self.CallbackItem(
#                root, name, self._filterFunc(filt))
#            item.setIcon(0, QIcon(":/icons/{}.svg".format(icon)))


def _stdTree(self, root, _old):
    tags = (
        (_("Marked"), "tag.svg", "tag:marked"),
        (_("Suspended"), "heart.svg", "is:suspended"))
    for name, icon, filter_cmd in tags:
        item = self.CallbackItem(
            root, name, self._filterFunc(filter_cmd))
        item.setIcon(0, QIcon(":/icons/" + icon))

Browser._stdTree = wrap(Browser._stdTree, _stdTree, 'around')
